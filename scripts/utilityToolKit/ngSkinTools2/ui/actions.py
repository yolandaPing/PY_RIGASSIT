from ngSkinTools2 import signal
from ngSkinTools2.api import PasteOperation
from ngSkinTools2.api.pyside import QAction, QtGui, QtWidgets
from ngSkinTools2.api.python_compatibility import Object
from ngSkinTools2.api.session import Session
from ngSkinTools2.operations import import_export_actions, import_v1_actions
from ngSkinTools2.operations.layers import (
    ToggleEnabledAction,
    build_action_initialize_layers,
)
from ngSkinTools2.operations.paint import FloodAction, PaintAction
from ngSkinTools2.operations.website_links import WebsiteLinksActions
from ngSkinTools2.ui import action
from ngSkinTools2.ui.updatewindow import build_action_check_for_updates


def define_action(parent, label, callback=None, icon=None, shortcut=None, tooltip=None):
    result = QAction(label, parent)
    if icon is not None:
        result.setIcon(QtGui.QIcon(icon))
    if callback is not None:
        result.triggered.connect(callback)
    if shortcut is not None:
        if not isinstance(shortcut, QtGui.QKeySequence):
            shortcut = QtGui.QKeySequence(shortcut)
        result.setShortcut(shortcut)
    if tooltip is not None:
        result.setToolTip(tooltip)
        result.setStatusTip(tooltip)
    return result


def build_action_delete_custom_nodes_for_selection(parent, session):
    from ngSkinTools2.operations import removeLayerData

    result = define_action(
        parent,
        "Delete Custom Nodes For Selection",
        callback=lambda: removeLayerData.remove_custom_nodes_from_selection(interactive=True, session=session),
    )

    @signal.on(session.events.nodeSelectionChanged)
    def update():
        result.setEnabled(bool(session.state.selection))

    update()
    return result


class Actions(Object):
    def separator(self, parent, label=""):
        separator = QAction(parent)
        separator.setText(label)
        separator.setSeparator(True)
        return separator

    def __init__(self, parent, session):
        """
        :type session: Session
        """
        qt_action = lambda a: action.qt_action(a, session, parent)
        from ngSkinTools2.operations import layers, removeLayerData, tools
        from ngSkinTools2.ui.transferDialog import build_transfer_action

        self.initialize = build_action_initialize_layers(session, parent)
        self.exportFile = import_export_actions.buildAction_export(session, parent)
        self.importFile = import_export_actions.buildAction_import(session, parent)
        self.import_v1 = import_v1_actions.build_action_import_v1(session, parent)

        self.addLayer = layers.buildAction_createLayer(session, parent)
        self.deleteLayer = layers.buildAction_deleteLayer(session, parent)
        self.toggle_layer_enabled = qt_action(ToggleEnabledAction)

        # self.moveLayerUp = defineCallbackAction(u"Move Layer Up", None, icon=":/moveLayerUp.png")
        # self.moveLayerDown = defineCallbackAction(u"Move Layer Down", None, icon=":/moveLayerDown.png")
        self.paint = qt_action(PaintAction)
        self.flood = qt_action(FloodAction)

        self.toolsAssignFromClosestJoint, self.toolsAssignFromClosestJointOptions = tools.create_action__from_closest_joint(parent, session)
        (
            self.toolsAssignFromClosestJointSelectedInfluences,
            self.toolsAssignFromClosestJointOptionsSelectedInfluences,
        ) = tools.create_action__from_closest_joint(parent, session)
        self.toolsAssignFromClosestJointOptionsSelectedInfluences.all_influences.set(False)
        self.toolsAssignFromClosestJointOptionsSelectedInfluences.create_new_layer.set(False)
        self.toolsUnifyWeights, self.toolsUnifyWeightsOptions = tools.create_action__unify_weights(parent, session)

        self.toolsDeleteCustomNodes = define_action(
            parent, "Delete All Custom Nodes", callback=lambda: removeLayerData.remove_custom_nodes(interactive=True, session=session)
        )

        self.toolsDeleteCustomNodesOnSelection = build_action_delete_custom_nodes_for_selection(parent, session)

        self.transfer = build_transfer_action(session=session, parent=parent)

        # self.setLayerMirrored = defineAction(u"Mirrored", icon=":/polyMirrorGeometry.png")
        # self.setLayerMirrored.setCheckable(True)

        self.documentation = WebsiteLinksActions(parent=parent)

        self.check_for_updates = build_action_check_for_updates(parent=parent)

        from ngSkinTools2.operations import copy_paste_actions

        self.cut_influences = copy_paste_actions.action_copy_cut(session, parent, True)
        self.copy_influences = copy_paste_actions.action_copy_cut(session, parent, False)
        self.paste_weights = copy_paste_actions.action_paste(session, parent, PasteOperation.replace)
        self.paste_weights_add = copy_paste_actions.action_paste(session, parent, PasteOperation.add)
        self.paste_weights_sub = copy_paste_actions.action_paste(session, parent, PasteOperation.subtract)

        self.copy_components = tools.create_action__copy_component_weights(parent=parent, session=session)
        self.paste_component_average = tools.create_action__paste_average_component_weight(parent=parent, session=session)

        self.merge_layer = tools.create_action__merge_layers(parent=parent, session=session)
        self.duplicate_layer = tools.create_action__duplicate_layer(parent=parent, session=session)
        self.fill_layer_transparency = tools.create_action__fill_transparency(parent=parent, session=session)

        self.add_influences = tools.create_action__add_influences(parent=parent, session=session)
        from ngSkinTools2.ui import influencesview

        self.showUsedInfluencesOnly = influencesview.build_used_influences_action(parent)
        self.randomizeInfluencesColors = layers.build_action_randomize_influences_colors(parent=parent, session=session)

        self.select_affected_vertices = tools.create_action__select_affected_vertices(parent=parent, session=session)

    def addLayersActions(self, context):
        context.addAction(self.addLayer)
        context.addAction(self.deleteLayer)
        context.addAction(self.separator(context))
        context.addAction(self.merge_layer)
        context.addAction(self.duplicate_layer)
        context.addAction(self.fill_layer_transparency)
        context.addAction(self.separator(context))
        context.addAction(self.toggle_layer_enabled)

    def addInfluencesActions(self, context):
        context.addAction(self.separator(context, "Actions"))
        context.addAction(self.toolsAssignFromClosestJointSelectedInfluences)
        context.addAction(self.select_affected_vertices)
        context.addAction(self.separator(context, "Clipboard"))
        context.addAction(self.cut_influences)
        context.addAction(self.copy_influences)
        context.addAction(self.paste_weights)
        context.addAction(self.paste_weights_add)
        context.addAction(self.paste_weights_sub)
