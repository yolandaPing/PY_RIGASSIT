from maya import cmds

from ngSkinTools2.api import PaintTool
from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.session import session
from ngSkinTools2.ui.action import Action

log = getLogger("operations/paint")


class FloodAction(Action):
    name = "Flood"
    tooltip = "Apply current brush to whole selection"

    def run(self):
        session.paint_tool.flood(self.session.state.currentLayer.layer, influences=self.session.state.currentLayer.layer.paint_targets)

    def enabled(self):
        return PaintTool.is_painting() and self.session.state.selectedSkinCluster is not None and self.session.state.currentLayer.layer is not None

    def update_on_signals(self):
        return [
            self.session.events.toolChanged,
            self.session.events.currentLayerChanged,
            self.session.events.currentInfluenceChanged,
            self.session.events.targetChanged,
        ]


class PaintAction(Action):
    name = "Paint"
    tooltip = "Toggle paint tool"
    checkable = True

    def run(self):
        if self.checked():
            cmds.setToolTo("moveSuperContext")
        else:
            self.session.paint_tool.start()

    def update_on_signals(self):
        return [self.session.events.toolChanged]

    def checked(self):
        return PaintTool.is_painting()
