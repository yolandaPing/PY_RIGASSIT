"""
Maya internals dissection, comments are ours. similar example available in "command|hotkey code", see "Here's an example
of how to create runtimeCommand with  a certain hotkey context"


```

// add new hotkey ctx
//  t: Specifies the context type. It's used together with the other flags such as "currentClient", "addClient",
//     "removeClient" and so on.
//  ac: Associates a client to the given hotkey context type. This flag needs to be used with the flag "type" which
//      specifies the context type.
hotkeyCtx -t "Tool" -ac "sculptMeshCache";

// create new runtime command, associate with created context
runTimeCommand -default true
    -annotation (uiRes("m_defaultRunTimeCommands.kModifySizePressAnnot"))
    -category   ("Other items.Brush Tools")
    -command    ("if ( `contextInfo -ex sculptMeshCacheContext`) sculptMeshCacheCtx -e -adjustSize 1 sculptMeshCacheContext;")
    -hotkeyCtx ("sculptMeshCache")
    SculptMeshActivateBrushSize;

// create named command for the runtime command
nameCommand
    -annotation "Start adjust size"
    -command ("SculptMeshActivateBrushSize")
    SculptMeshActivateBrushSizeNameCommand;

// assign hotkey for name command
hotkey -keyShortcut "b" -name ("SculptMeshActivateBrushSizeNameCommand") -releaseName ("SculptMeshDeactivateBrushSizeNameCommand");
```

"""

from maya import cmds

from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.python_compatibility import is_string

from . import hotkeys

hotkeySetName = 'ngSkinTools2'
context = 'ngst2PaintContext'
command_prefix = "ngskintools_2_"  # maya breaks command name on capital letters and before numbers, so this will ensure that all command names start with "ngskintools 2 "

log = getLogger("hotkeys setup")


def uninstall_hotkeys():
    if cmds.hotkeySet(hotkeySetName, q=True, exists=True):
        cmds.hotkeySet(hotkeySetName, e=True, delete=True)


def setup_named_commands():
    # "default" mode will force a read-only behavior for runTimCommands
    # only turn this on for production mode
    import ngSkinTools2

    append_only_mode = not ngSkinTools2.DEBUG_MODE

    def add_command(name, annotation, command, context=None):
        if not is_string(command):
            command = function_link(command)

        runtime_command_name = command_prefix + name

        # delete (if exists) and recreate runtime command
        if not append_only_mode and cmds.runTimeCommand(runtime_command_name, q=True, exists=True):
            cmds.runTimeCommand(runtime_command_name, e=True, delete=True)

        if not cmds.runTimeCommand(runtime_command_name, q=True, exists=True):
            additional_args = {}
            if context is not None:
                additional_args['hotkeyCtx'] = context

            cmds.runTimeCommand(
                runtime_command_name,
                category="Other items.ngSkinTools2",
                default=append_only_mode,
                annotation=annotation,
                command=command,
                commandLanguage="python",
                **additional_args
            )

            cmds.nameCommand(
                command_prefix + name + "NameCommand",
                annotation=annotation + "-",
                sourceType="python",
                default=append_only_mode,
                command=runtime_command_name,
            )

    def add_toggle(name, annotation, command_on, command_off, context=None):
        add_command(name + 'On', annotation=annotation, command=command_on, context=context)
        add_command(name + 'Off', annotation=annotation + "(release)", command=command_off, context=context)

    add_toggle(
        'BrushSize',
        annotation='Toggle brush size mode',
        command_on=hotkeys.paint_tool_brush_size,
        command_off=hotkeys.paint_tool_brush_size_release,
        context=context,
    )

    add_command('ToggleHelp', annotation='toggle help', command=hotkeys.paint_tool_toggle_help, context=context)
    add_command('ViewFitInfluence', annotation='fit influence in view', command=hotkeys.paint_tool_focus_current_influence, context=context)
    add_toggle(
        'SampleInfluence',
        annotation='Sample influence',
        command_on=hotkeys.paint_tool_sample_influence,
        command_off=hotkeys.paint_tool_sample_influence_release,
        context=context,
    )

    add_command("SetBrushIntensity", annotation="set brush intensity", command=hotkeys.select_paint_brush_intensity, context=context)
    add_command("PaintFlood", annotation="apply current brush to all vertices", command=hotkeys.paint_tool_flood, context=context)

    add_command("Paint", annotation="start paint tool", command=hotkeys.paint_tool_start)
    add_command(
        "ToggleOriginalMesh",
        annotation="toggle between weights display and original mesh while painting",
        command=hotkeys.paint_tool_toggle_original_mesh,
    )
    add_command(
        "CycleWeightsDisplayMode",
        annotation='Cycle weights display mode "all influences" -> "current influence" -> "current influence colored"',
        command=hotkeys.paint_tool_cycle_weights_display_mode,
    )


def define_hotkeys():
    setup_named_commands()

    def nc(name_command_short_name):
        return command_prefix + name_command_short_name + "NameCommand"

    # cmds.hotkey(k="b", name=nc("BrushSizeOn"), releaseName=nc("BrushSizeOff"))
    cmds.hotkey(keyShortcut="b", name=nc("BrushSizeOn"), releaseName=nc("BrushSizeOff"))
    cmds.hotkey(keyShortcut="i", name=nc("SetBrushIntensity"))
    cmds.hotkey(keyShortcut="f", ctrlModifier=True, name=nc("PaintFlood"))
    cmds.hotkey(keyShortcut="f", name=nc("ViewFitInfluence"))
    cmds.hotkey(keyShortcut="h", name=nc("ToggleHelp"))

    cmds.hotkey(keyShortcut="s", name=nc("SampleInfluenceOn"), releaseName=nc("SampleInfluenceOff"))
    cmds.hotkey(keyShortcut="d", name=nc("CycleWeightsDisplayMode"))
    cmds.hotkey(keyShortcut="t", name=nc("ToggleOriginalMesh"))


def install_hotkeys():
    uninstall_hotkeys()

    __hotkey_set_handler.remember()
    try:
        if cmds.hotkeySet(hotkeySetName, q=True, exists=True):
            cmds.hotkeySet(hotkeySetName, e=True, current=True)
        else:
            cmds.hotkeySet(hotkeySetName, current=True)

        cmds.hotkeyCtx(addClient=context, type='Tool')

        define_hotkeys()
    finally:
        __hotkey_set_handler.restore()


def function_link(fun):
    return "import {module}; {module}.{fn}()".format(module=fun.__module__, fn=fun.__name__)


class HotkeySetHandler:
    def __init__(self):
        log.info("initializing new hotkey set handler")
        self.prev_hotkey_set = None

    def remember(self):
        if self.prev_hotkey_set is not None:
            return

        log.info("remembering current hotkey set")
        self.prev_hotkey_set = cmds.hotkeySet(q=True, current=True)

    def restore(self):
        if self.prev_hotkey_set is None:
            return

        log.info("restoring previous hotkey set")
        cmds.hotkeySet(self.prev_hotkey_set, e=True, current=True)
        self.prev_hotkey_set = None


__hotkey_set_handler = HotkeySetHandler()


def toggle_paint_hotkey_set(enabled):
    if enabled:
        __hotkey_set_handler.remember()
        cmds.hotkeySet(hotkeySetName, e=True, current=True)
    else:
        __hotkey_set_handler.restore()
