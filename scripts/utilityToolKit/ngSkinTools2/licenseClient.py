import ast
import base64
import json
import os
import platform
import re
from threading import Event, Thread

from maya import cmds
from maya import utils as mu

from ngSkinTools2 import cleanup, signal
from ngSkinTools2.api import plugin
from ngSkinTools2.api.http_client import HTTPError, Request, urlopen
from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.python_compatibility import Object
from ngSkinTools2.ui import options
from ngSkinTools2.ui.parallel import ParallelTask
from ngSkinTools2.version import compare_semver

log = getLogger("license client")


# noinspection PyClassHasNoInit
class Status:
    ok = 0
    unknown = 1
    communicationError = 2
    invalidSignature = 100
    invalidHostId = 101

    @classmethod
    def status_description(cls, status):
        return {
            Status.ok: "",
            Status.unknown: "unknown error",
            Status.communicationError: "communication error",
            Status.invalidSignature: "invalid signature",
            Status.invalidHostId: "license is bound to another workstation",
        }[status]


class MainThreadWrapper:
    def __init__(self, thread_mode):
        self.thread_mode = thread_mode

    def execute(self, fn, *args):
        if self.thread_mode:
            return mu.executeInMainThreadWithResult(fn, *args)

        return fn(*args)

    def execute_deferred(self, fn, *args):
        if self.thread_mode:
            return mu.executeDeferred(fn, *args)

        return fn(*args)


# noinspection PyAttributeOutsideInit,HttpUrlsUsage
class LicenseServerClient(Object):
    """
    this client helps c++ plugin communicate with the license server.
    this only takes care of transport layer, to keep options a bit more open for future like TLS communication,
    without having to embed a proper HTTP client into plugin
    """

    def __init__(self, timeout=30):
        import ngSkinTools2

        self.serverUrl = "http://127.0.0.1:9050"
        self.sleepPeriod = 60 * 2  # amount of seconds
        self.timeout = timeout

        if ngSkinTools2.DEBUG_MODE:
            self.sleepPeriod = 5

        self.lastError = None
        self.current_thread = None  # type: StoppableThread

        self.reservation_cycle_finished_handler = None

    def refresh_reservation(self, thread=None):
        """
        Called periodically to synchronize with license server
        :return:
        """

        log.info("refreshing reservation...")

        def checkout_request():
            return plugin.ngst2License(serverRequest=True, hostName=platform.node())

        # noinspection PyShadowingNames
        def checkin_response(resp):
            return plugin.ngst2License(serverResponse=resp)

        def should_abort():
            return thread is not None and thread.should_stop()

        main_thread = MainThreadWrapper(thread_mode=thread is not None)

        communication_error = None
        try:
            req_contents = main_thread.execute(checkout_request)

            req = Request(self.serverUrl + "/seat-reservations")
            req.data = req_contents.encode()
            req.add_header("content-type", "application/json")

            resp = urlopen(req, timeout=self.timeout)
            # check response version first before validating body
            check_minimum_required_server_version(resp.headers.get("server-version", None))

            resp_body = resp.read()
            if should_abort():
                return

            self.lastError = None
            main_thread.execute(checkin_response, resp_body)
        except HTTPError as err:
            code = err.getcode()

            message = str(err)
            try:
                message = json.load(err)['message']
            except:
                pass
            communication_error = "{0} ({1})".format(message, code)

        except IOError as err:
            communication_error = str(err)

        except Exception as err:
            communication_error = str(err)

        if should_abort():
            return

        if communication_error:
            err = "error communicating with license server: " + communication_error
            log.error(err)
            self.lastError = err

        main_thread.execute_deferred(self.reservation_cycle_finished_handler)

        log.info("reservation refreshed")

    def stop(self):
        log.info("stopping license thread...")
        self.lastError = None

        if self.current_thread is not None:
            self.current_thread.stop()
            self.current_thread = None

    def run_license_reservation_thread(self):
        # stop previous thread
        self.stop()

        def thread_func(t):
            """
            :type t: StoppableThread
            """
            log.info("license thread started")

            while not t.should_stop():
                self.refresh_reservation(thread=t)

                t.wait(self.sleepPeriod)

            log.info("license thread stopped")

        self.current_thread = StoppableThread(target=thread_func)
        self.current_thread.start()

        cleanup.registerCleanupHandler(self.stop)

    def apply_configuration(self, conf):
        """
        :type conf: Configuration
        """
        self.stop()
        if not conf.license_server_url:
            return

        server_address = conf.license_server_url.strip()
        if not server_address.lower().startswith('http://') and not server_address.lower().startswith('https://'):
            server_address = 'http://' + server_address

        self.serverUrl = server_address
        self.run_license_reservation_thread()


def check_minimum_required_server_version(actual_version):
    if actual_version == "v1.0.0-dev":
        # special case for development version of the server
        return

    minimum_required = "v1.0.22"
    if actual_version is None or actual_version.strip() == "":
        raise Exception("License server version unknown: please upgrade to version %s or above" % minimum_required)

    if compare_semver(minimum_required.lstrip("v"), actual_version.lstrip("v")) < 0:
        raise Exception("License server version too low: current version is %s, need version %s or above" % (actual_version, minimum_required))


class StoppableThread(Thread):
    def __init__(self, target):
        super(StoppableThread, self).__init__()
        self.__target = target
        self.finished = Event()

    def should_stop(self):
        return self.finished.is_set()

    def wait(self, timeout):
        """
        wait for specified timeout in this thread, but don't block the "stop" event
        """
        self.finished.wait(timeout=timeout)

    def stop(self):
        self.finished.set()

    def run(self):
        self.__target(self)
        self.finished.set()


def parse_license_contents(contents):
    """

    Example valid contents:

    LICENSE ngstkey ngskintools 1 standalone hostid=123-123
        sig=363c8f7f19679efc324b5ec713ffcf8968b3f4741b3b0d64f62436f8de799ec5

    For historical reasons, this is not a JSON.

    :param str contents:
    """

    values = contents.split()
    if len(values) < 6:
        return None

    result = {}
    for index, v in enumerate(['stamp', 'file-type', 'product', 'product-version', 'license-type']):
        result[v] = values[index]

    # check what we have here
    if result['stamp'] != 'LICENSE':
        return None

    # check if license type is ngstkey
    if result['file-type'] != 'ngstkey':
        return None

    if result['product'] != 'ngskintools2':
        return None

    for value in values[5:]:
        k, v = value.split("=", 2)
        result[k] = v

    # signature is required
    if result.get('sig', None) is None:
        return None

    if result.get('hostid', None) is None:
        return None

    return result


def _is_license_key_valid(license_key):
    """
    checks if given key is in UUID format

    UUID format:  8-4-4-4-12 hexadecimal strings,
    e.g. 12345678-abcd-ef09-1234-56789abcdef0
    """
    key_format = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    return re.match(key_format, license_key)


def _get_host_id():
    result = plugin.ngst2License(q=True, hostid=True)
    return result


def _configuration_for_license_file(license_file):
    parsed_license_contents = parse_license_contents(license_file)
    if parsed_license_contents is None:
        raise Exception

    conf = Configuration()
    conf.license_files = [parsed_license_contents]
    return conf


class LicenseFileHandler:
    def __init__(self):
        self.licenseServer = 'https://licensing.ngskintools.com/api/projects/ngskintools2/licenses/'

    # noinspection PyMethodMayBeStatic
    def apply_configuration(self, conf):
        """
        :type conf: Configuration
        """
        if conf.license_files:
            for c in conf.license_files:
                result = plugin.ngst2License(validateLicense=True, hostid=c['hostid'], licenseKey=c['licensekey'], signature=c['sig'])
                if result == 0:
                    conf.active_license_file = c
                    break

    def download_license_file(self, license_key, host_id):
        """
        exchanges licenseKey+hostId for a license file online.
        :type license_key: basestring
        :type host_id: basestring

        """

        host_id = host_id.strip()
        if host_id == "":
            raise Exception("Cannot download license when host ID is empty")

        import json

        try:
            req = Request(
                self.licenseServer + license_key,
                headers={
                    'Accept': 'application/vnd.releasedb.v1.1+json',
                },
            )
            resp = urlopen(req, json.dumps({"hostId": host_id, "licenseFileType": 'ngstKey'}).encode())
            result = json.load(resp)
            return result['licenseFile']
        except HTTPError as err:
            code = err.getcode()

            message = str(err)
            try:
                message = json.load(err)['message']
            except:
                pass

            log.info("received error: %r", message)

            # for client-side errors, just convey the error from the server
            if code == 400:
                raise Exception(message)

            if code == 404:
                raise Exception("invalid license key")

            raise Exception("Failed downloading license information ({0}): {1}".format(err.getcode(), message))
        except Exception as err:
            raise Exception("Failed downloading license information: unknown error ({0})".format(str(err)))

    def create_online_key_download_task(self, license_key):
        """
        :param basestring license_key:
        """
        host_id = _get_host_id()

        def run(context):
            context.error = ""
            context.license_file = None

            try:
                context.license_file = self.download_license_file(license_key, host_id)
            except Exception as err:
                context.error = str(err)

        def done(context):
            context.conf = None
            if context.license_file is not None:
                context.conf = _configuration_for_license_file(context.license_file)

        task = ParallelTask()
        task.add_run_handler(run)
        task.add_done_handler(done)

        return task

    # noinspection PyMethodMayBeStatic
    def generate_activation_code_link(self, license_key):
        # sample key
        if not _is_license_key_valid(license_key):
            raise Exception("Invalid license key format")

        return (
            "https://licensing.ngskintools.com/#/self-service/"
            + base64.b64encode(
                json.dumps({'type': 'activationCode', 'product': 'ngskintools2', 'licenseKey': license_key, 'hostId': _get_host_id()}).encode()
            ).decode()
        )

    # noinspection PyMethodMayBeStatic
    def configuration_for_activation_code(self, activation_code):
        try:
            contents = json.loads(base64.b64decode(activation_code))
        except:
            raise Exception("Invalid activation code: could not parse contents")

        return _configuration_for_license_file(contents['licenseFile'])


class Configuration:
    CONFIGURATION_VAR = options.VAR_OPTION_PREFIX + 'licenseConfig'
    CONFIGURATION_ENV_VAR = 'NGSKINTOOLS2_LICENSE_CONFIG'
    CONFIGURATION_PATH_ENV_VAR = 'NGSKINTOOLS2_LICENSE_PATH'

    type_host_id = "host-id"

    json_mapping = {
        'license_files': 'license-files',
        'license_server_url': 'license-server-url',
    }

    def __init__(self):
        self.license_files = []
        self.license_server_url = ""
        self.active_license_file = None

        self.is_editable = True

    def __discover_license_files__(self, path):
        """
        given a dir or file path, discover ngstkey license files. only files that look like license files are parsed,
        and only those that match ngstkey file format are used.
        """

        if path is None:
            return

        if os.path.isfile(path):
            with open(path) as f:
                try:
                    contents = f.read(7)
                    if contents != 'LICENSE':
                        return
                    contents += f.read()
                except:
                    return

            parsed_contents = parse_license_contents(contents)
            if parsed_contents is None:
                return

            parsed_contents['source_file'] = path
            return [parsed_contents]

        if os.path.isdir(path):
            result = []
            for i in os.listdir(path):
                file_name = os.path.join(path, i)
                if os.path.isfile(file_name):
                    files = self.__discover_license_files__(file_name)
                    if files:
                        result.extend(files)

            return result

        return

    def load(self):
        config_contents = os.getenv(self.CONFIGURATION_ENV_VAR, None)
        if config_contents:
            self.is_editable = False  # can't edit if configuration comes from environment variable
            self.load_from_string(config_contents)
            return

        # discover valid ngskintools2 licenses
        self.license_files = self.__discover_license_files__(cmds.internalVar(userAppDir=True)) or []
        path = os.getenv(self.CONFIGURATION_PATH_ENV_VAR, None)
        if path:
            self.license_files.extend(self.__discover_license_files__(path))
        if self.license_files:
            self.is_editable = False  # can't edit if configuration comes from license files
            return

        self.load_from_string(options.load_option(self.CONFIGURATION_VAR, ""))

    def load_from_string(self, s):
        """
        :param basestring s: either a python dictionary literal or a json containing key:value configuration of this object
        """
        s = s.strip()
        if not s:
            return

        log.info("loading config from: '%s'", s)

        if s.startswith("{"):
            try:
                # try loading as json first
                val = json.loads(s)
            except:
                # revert to ast eval (allows single-quotes)
                val = ast.literal_eval(s)
        else:
            # simple key-value, split with spaces
            items = [i.split("=", 1) for i in s.split(" ")]
            val = {i[0]: i[1] for i in items if len(i) == 2}

        for k, v in self.json_mapping.items():
            if v in val:
                setattr(self, k, val[v])

        literal_license_file = {k: val[k] for k in ['hostid', 'licensekey', 'sig'] if k in val}
        if literal_license_file:
            self.license_files.append(literal_license_file)

    def save_to_string(self):
        """
        :return: json serialization of this object, suitable for load_from_string later
        """
        import json

        return json.dumps({v: getattr(self, k) for k, v in self.json_mapping.items()})

    def save(self):
        if self.is_editable:
            options.save_option(self.CONFIGURATION_VAR, self.save_to_string())


class LicenseData:
    def __init__(self):
        self.active = False
        self.status_description = ""
        self.licensed_to = ''
        self.errors = []

    def has_errors(self):
        return bool(self.errors)

    def __repr__(self):
        return "LicenseData(active:{self.active}, status_description: {self.status_description!r}, licensed_to: {self.licensed_to!r}, errors: {self.errors}".format(
            self=self
        )


class LicenseClient:
    def __init__(self):
        self.serverClient = LicenseServerClient()
        self.licenseFileHandler = LicenseFileHandler()
        self.statusChanged = signal.Signal("license status changed")
        self.serverClient.reservation_cycle_finished_handler = self.statusChanged.emit_deferred
        self.conf = Configuration()
        self.errors = []

    def load(self):
        cfg = Configuration()
        cfg.load()
        self.__apply_configuration(cfg)

    def load_deferred(self):
        mu.executeDeferred(self.load)

    def __apply_configuration(self, conf):
        """
        :param Configuration conf:
        """
        self.__reset_errors()

        log.info("applying configuration: %s", json.dumps(conf.__dict__, indent=4))
        self.conf = conf
        try:
            self.licenseFileHandler.apply_configuration(conf)
            self.serverClient.apply_configuration(conf)
        except Exception as err:
            self.errors.append(str(err))
        self.statusChanged.emit()

    def __apply_and_save_configuration(self, conf):
        self.__apply_configuration(conf)
        log.info("saving configuration")
        conf.save()

    def __reset_errors(self):
        self.errors = []

    def current_status(self):
        data = LicenseData()
        status_code = plugin.ngst2License(q=True, licenseStatus=True)
        data.active = status_code == 0
        data.licensed_to = plugin.ngst2License(q=True, licensedTo=True)

        errors = self.errors[:]
        if self.serverClient.lastError is not None:
            errors.append(self.serverClient.lastError)
        data.status_description = None if not errors else "\n".join(errors)
        data.errors = errors
        return data

    def current_configuration(self):
        return self.conf

    def activate_with_license_key(self, license_key):
        task = self.licenseFileHandler.create_online_key_download_task(license_key=license_key)
        self.__reset_errors()

        def done(context):
            if context.error:
                self.errors.append(context.error)
            if context.conf is not None:
                self.__apply_and_save_configuration(context.conf)
            self.statusChanged.emit()

        task.add_done_handler(done)
        return task

    def clear_configuration(self):
        plugin.ngst2License(reset=True)
        self.__apply_and_save_configuration(Configuration())

    def generate_acivation_code_link(self, license_key):
        return self.licenseFileHandler.generate_activation_code_link(license_key)

    def accept_activation_code(self, activation_code):
        self.__apply_and_save_configuration(self.licenseFileHandler.configuration_for_activation_code(activation_code))

    def accept_license_server_url(self, server_address):
        """
        :type server_address: basestring
        """
        conf = Configuration()
        conf.license_server_url = server_address

        self.__apply_and_save_configuration(conf)
        self.serverClient.refresh_reservation()

    def should_show_evaluation_banner(self):
        """
        returns true if we should show evaluation banner in main UI
        """
        status = self.current_status()
        if status.active:
            return False

        if status.errors:
            return True

        # in case there's no errors, and the thread is still running, wait for the current thread to complete
        if self.serverClient.current_thread is not None:
            return False

        return True
