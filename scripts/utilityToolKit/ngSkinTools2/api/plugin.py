import json

from maya import cmds, mel

from ngSkinTools2.api import feedback
from ngSkinTools2.api.log import getLogger

log = getLogger("plugin")


def ngst2Layers(*args, **kwargs):
    log.debug("ngst2layers [%r] [%r]", args, kwargs)
    return cmds.ngst2Layers(*args, **kwargs)


def ngst2LayersMel(cmd):
    cmd = "ngst2Layers " + cmd
    log.debug(cmd)
    return mel.eval(cmd)


def ngst2tools(**kwargs):
    log.debug("ngst2tools [%r]", kwargs)
    result = cmds.ngst2Tools(json.dumps(kwargs))
    if result is not None:
        result = json.loads(result)
    return result


def ngst2License(**kwargs):
    log.debug("ngst2license [%r]", kwargs)
    return cmds.ngst2License(**kwargs)


def ngst2PaintContext():
    log.debug("ngst2PaintContext()")
    return cmds.ngst2PaintContext()


def ngst2PaintSettingsCmd(**kwargs):
    log.debug("ngst2PaintSettingsCmd [%r]", kwargs)
    return cmds.ngst2PaintSettingsCmd(**kwargs)


def ngst2_hotkey(**kwargs):
    log.debug("ngst2Hotkey [%r]", kwargs)
    return cmds.ngst2Hotkey(**kwargs)


pluginBinary = 'ngSkinTools2'


def is_plugin_loaded():
    return cmds.pluginInfo(pluginBinary, q=True, loaded=True)


def load_plugin():
    from maya import cmds

    if not is_plugin_loaded():
        cmds.loadPlugin(pluginBinary, quiet=True)

    if not is_plugin_loaded():
        feedback.display_error("Failed to load the plugin. This is often a case-by-case issue - contact support.")
        return

    from ngSkinTools2 import version

    expected_version = version.pluginVersion()
    actual_version = cmds.pluginInfo(pluginBinary, q=True, version=True)
    if actual_version != expected_version:
        feedback.display_error(
            "Invalid plugin version detected: required '{expectedVersion}', "
            "but was '{actualVersion}'. Clean reinstall recommended.".format(expectedVersion=expected_version, actualVersion=actual_version)
        )
