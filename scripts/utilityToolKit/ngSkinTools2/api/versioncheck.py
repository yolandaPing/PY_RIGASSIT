import datetime

from ngSkinTools2 import version
from ngSkinTools2.api import http_client
from ngSkinTools2.api.python_compatibility import Object


class UpdateInfo(Object):
    def __init__(self):
        self.update_available = False
        self.update_date = ''
        self.latest_version = ''
        self.download_url = ''


def download_update_info(success_callback, failure_callback):
    """
    executes version info download in separate thread,
    then runs provided callbacks in main thread when download completes or fails

    returns thread object that gets started.
    """

    import platform

    from maya import cmds

    os = platform.system()
    maya_version = str(int(cmds.about(api=True)))

    url = http_client.encode_url(
        "https://versiondb.ngskintools.com/releases/ngSkinTools-v2-" + os + "-maya" + maya_version,
        {
            'currentVersion': version.pluginVersion(),
            'uniqueClientId': version.uniqueClientId(),
        },
    )

    def on_success(response):
        try:
            info = UpdateInfo()
            info.update_date = datetime.datetime.strptime(response['dateReleased'], "%Y-%m-%d")
            info.latest_version = response['latestVersion']
            info.download_url = response['downloadUrl']
            info.update_available = version.compare_semver(version.pluginVersion(), info.latest_version) > 0

            success_callback(info)
        except Exception as err:
            failure_callback(str(err))

    return http_client.get_async(url, success_callback=on_success, failure_callback=failure_callback)
