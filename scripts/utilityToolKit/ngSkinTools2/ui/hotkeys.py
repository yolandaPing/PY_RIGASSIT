"""
Global list of hotkey-able functions within the plugin.


These functions will be embedded in end-user's hotkey setup by absolute path (package.function_name)
so the names should not fluctuate.
"""

from ngSkinTools2.api import NamedPaintTarget, PaintTool, WeightsDisplayMode, plugin
from ngSkinTools2.api.paint import MaskDisplayMode
from ngSkinTools2.api.session import session, withSession
from ngSkinTools2.operations.paint import FloodAction, PaintAction
from ngSkinTools2.ui.action import do_action_hotkey


def paint_tool_start():
    do_action_hotkey(PaintAction)


def paint_tool_toggle_help():
    plugin.ngst2_hotkey(paintContextToggleHelp=True)


def paint_tool_flood():
    do_action_hotkey(FloodAction)


def paint_tool_focus_current_influence():
    plugin.ngst2_hotkey(paintContextViewFit=True)


def paint_tool_brush_size():
    plugin.ngst2_hotkey(paintContextBrushSize=True)


def paint_tool_brush_size_release():
    plugin.ngst2_hotkey(paintContextBrushSize=False)


def paint_tool_sample_influence():
    plugin.ngst2_hotkey(paintContextSampleInfluence=True)


def paint_tool_sample_influence_release():
    plugin.ngst2_hotkey(paintContextSampleInfluence=False)


@withSession
def select_paint_brush_intensity():
    from ngSkinTools2.ui.brush_settings_popup import brush_settings_popup

    brush_settings_popup(session.paint_tool)


@withSession
def paint_tool_toggle_original_mesh():
    paint = session.paint_tool
    paint.display_settings.display_node_visible = not paint.display_settings.display_node_visible
    session.events.toolChanged.emit()


@withSession
def paint_tool_cycle_weights_display_mode():
    """
    cycle current display mode "all influences" -> "current influence" -> "current influence colored"
    :return:
    """
    paint = session.paint_tool

    targets = session.state.currentInfluence.targets
    is_mask_mode = targets is not None and len(targets) == 1 and targets[0] == NamedPaintTarget.MASK

    settings = paint.display_settings
    if is_mask_mode:
        settings.mask_display_mode = {
            MaskDisplayMode.default_: MaskDisplayMode.color_ramp,
            MaskDisplayMode.color_ramp: MaskDisplayMode.default_,
        }.get(settings.mask_display_mode, MaskDisplayMode.default_)
    else:
        settings.weights_display_mode = {
            WeightsDisplayMode.allInfluences: WeightsDisplayMode.currentInfluence,
            WeightsDisplayMode.currentInfluence: WeightsDisplayMode.currentInfluenceColored,
            WeightsDisplayMode.currentInfluenceColored: WeightsDisplayMode.allInfluences,
        }.get(settings.weights_display_mode, WeightsDisplayMode.allInfluences)

    session.events.toolChanged.emit()
