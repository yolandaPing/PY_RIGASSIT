import json

from maya import cmds

from ngSkinTools2 import signal
from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.python_compatibility import Object, is_string
from ngSkinTools2.observableValue import ObservableValue

log = getLogger("plugin")


class Value(Object):
    def __init__(self, value=None):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

    def getInt(self):
        try:
            return int(self.get())
        except:
            return 0


class PersistentValue(Value):
    """
    persistent value can store itself into Maya's "option vars" array
    """

    def __init__(self, name, default_value=None, prefix=None):
        Value.__init__(self)

        if prefix is None:
            prefix = VAR_OPTION_PREFIX
        self.name = prefix + name
        self.default_value = default_value
        self.value = load_option(self.name, self.default_value)

    def set(self, value):
        Value.set(self, value)
        save_option(self.name, self.value)


class PersistentDict(Object):
    def __init__(self, name, default_values=None):
        if default_values is None:
            default_values = {}
        self.persistence = PersistentValue(name=name, default_value=json.dumps(default_values))

    def __get_values(self):
        # type: () -> dict
        return json.loads(self.persistence.get())

    def __getitem__(self, item):
        return self.__get_values().get(item, None)

    def __setitem__(self, key, value):
        v = self.__get_values()
        v[key] = value
        self.persistence.set(json.dumps(v))


def load_option(var_name, default_value):
    """
    loads value from optionVar
    """

    from ngSkinTools2 import BATCH_MODE

    if BATCH_MODE:
        return default_value

    if cmds.optionVar(exists=var_name):
        return cmds.optionVar(q=var_name)

    return default_value


def save_option(varName, value):
    """
    saves option via optionVar
    """
    from ngSkinTools2 import BATCH_MODE

    if BATCH_MODE:
        return

    # variable does not exist, attempt to save it
    key = None
    if isinstance(value, float):
        key = 'fv'
    elif isinstance(value, int):
        key = 'iv'
    elif is_string(value):
        key = 'sv'
    else:
        raise ValueError("could not save option %s: invalid value %r" % (varName, value))

    kvargs = {key: (varName, value)}
    log.info("saving optionvar: %r", kvargs)
    cmds.optionVar(**kvargs)


VAR_OPTION_PREFIX = 'ngSkinTools2_'


def delete_custom_options():
    for varName in cmds.optionVar(list=True):
        if varName.startswith(VAR_OPTION_PREFIX):
            cmds.optionVar(remove=varName)

    cmds.windowPref('MirrorWeightsWindow', ra=True)


def build_config_property(name, default_value, doc=''):
    return property(lambda self: self.__get_value__(name, default_value), lambda self, val: self.__set_value__(name, val), doc=doc)


class Config(Object):
    """
    Maya-wide settings for ngSkinTools2
    """

    mirrorInfluencesDefaults = build_config_property('mirrorInfluencesDefaults', "{}")  # type: string

    def __init__(self):
        from ngSkinTools2.api.mirror import MirrorOptions

        self.__storage__ = PersistentValue("config", "{}")
        self.__state__ = self.load()

        self.unique_client_id = PersistentValue('updateCheckUniqueClientId')

        self.checkForUpdatesAtStartup = self.build_observable_value('checkForUpdatesAtStartup', True)
        self.influences_show_used_influences_only = self.build_observable_value("influencesViewShowUsedInfluencesOnly", False)

        default_mirror_options = MirrorOptions()
        self.mirror_direction = self.build_observable_value("mirrorDirection", default_mirror_options.direction)
        self.mirror_dq = self.build_observable_value("mirrorDq", default_mirror_options.mirrorDq)
        self.mirror_mask = self.build_observable_value("mirrorMask", default_mirror_options.mirrorMask)
        self.mirror_weights = self.build_observable_value("mirrorWeights", default_mirror_options.mirrorWeights)

    def __get_value__(self, name, default_value):
        result = self.__state__.get(name, default_value)
        log.info("config: return %s=%r", name, result)
        return result

    def __set_value__(self, name, value):
        log.info("config: save %s=%r", name, value)
        self.__state__[name] = value
        self.save()

    def build_observable_value(self, name, default_value):
        """
        builds ObservableValue that is loaded and persisted into config when changed
        :type name: str
        :rtype: ngSkinTools2.observableValue.ObservableValue
        """
        result = ObservableValue(self.__get_value__(name=name, default_value=default_value))

        @signal.on(result.changed)
        def save():
            self.__set_value__(name, result())

        return result

    def load(self):
        # noinspection PyBroadException
        try:
            return json.loads(self.__storage__.get())
        except:
            return {}

    def save(self):
        self.__storage__.set(json.dumps(self.__state__))


config = Config()


def bind_checkbox(cb, option):
    from ngSkinTools2.ui import qt

    cb.setChecked(option())

    @qt.on(cb.toggled)
    def update():
        option.set(cb.isChecked())

    return cb
