from ngSkinTools2 import api, cleanup, signal
from ngSkinTools2.api import VertexTransferMode
from ngSkinTools2.api.pyside import QtCore, QtWidgets
from ngSkinTools2.api.session import session
from ngSkinTools2.api.transfer import LayersTransfer
from ngSkinTools2.decorators import undoable
from ngSkinTools2.ui import influenceMappingUI, qt, widgets
from ngSkinTools2.ui.layout import createTitledRow, scale_multiplier


class UiModel:
    def __init__(self):
        self.transfer = LayersTransfer()

    def destination_has_layers(self):
        l = api.Layers(self.transfer.target)
        return l.is_enabled() and len(l.list()) > 0

    @undoable
    def do_apply(self):
        self.transfer.complete_execution()
        from maya import cmds

        cmds.select(self.transfer.target)
        if session.active():
            session.events.targetChanged.emitIfChanged()


single_transfer_dialog_policy = qt.SingleWindowPolicy()


def open(parent, model):
    """

    :type model: UiModel
    """

    def buttonRow(window):
        def apply():
            model.do_apply()
            session.events.layerListChanged.emitIfChanged()
            window.close()

        return widgets.button_row(
            [
                ("Transfer", apply),
                ("Cancel", window.close),
            ]
        )

    def view_influences_settings():
        tabs.setCurrentIndex(1)

    def build_settings():
        result = QtWidgets.QVBoxLayout()

        vertexMappingMode = QtWidgets.QComboBox()
        vertexMappingMode.addItem("Closest point on surface", VertexTransferMode.closestPoint)
        vertexMappingMode.addItem("UV space", VertexTransferMode.uvSpace)
        vertexMappingMode.addItem("By vertex ID (source and destination vert count must match)", VertexTransferMode.vertexId)

        g = QtWidgets.QGroupBox("Selection")
        layout = QtWidgets.QVBoxLayout()
        g.setLayout(layout)

        sourceLabel = QtWidgets.QLabel()
        layout.addLayout(createTitledRow("Source:", sourceLabel))

        destinationLabel = QtWidgets.QLabel()
        layout.addLayout(createTitledRow("Destination:", destinationLabel))
        result.addWidget(g)

        g = QtWidgets.QGroupBox("Vertex mapping")
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(createTitledRow("Mapping mode:", vertexMappingMode))
        g.setLayout(layout)
        result.addWidget(g)

        g = QtWidgets.QGroupBox("Influences mapping")
        layout = QtWidgets.QVBoxLayout()
        g.setLayout(layout)

        edit = QtWidgets.QPushButton("Configure")
        qt.on(edit.clicked)(view_influences_settings)

        button_row = QtWidgets.QHBoxLayout()
        button_row.addWidget(edit)
        button_row.addStretch()
        layout.addLayout(button_row)

        result.addWidget(g)

        g = QtWidgets.QGroupBox("Other options")
        layout = QtWidgets.QVBoxLayout()
        g.setLayout(layout)

        keep_layers = QtWidgets.QCheckBox("Keep existing layers on destination")
        keep_layers_row = qt.wrap_layout_into_widget(createTitledRow("Destination layers:", keep_layers))
        layout.addWidget(keep_layers_row)

        @qt.on(keep_layers.stateChanged)
        def checked():
            model.transfer.keep_existing_layers = keep_layers.isChecked()

        result.addWidget(g)

        result.addStretch()

        def update_settings_to_model():
            keep_layers.setChecked(model.transfer.keep_existing_layers)
            qt.select_data(vertexMappingMode, model.transfer.vertex_transfer_mode)
            source_title = model.transfer.source
            if model.transfer.source_file is not None:
                source_title = 'file ' + model.transfer.source_file
            sourceLabel.setText("<strong>" + source_title + "</strong>")
            destinationLabel.setText("<strong>" + model.transfer.target + "</strong>")
            keep_layers_row.setEnabled(model.destination_has_layers())

        @qt.on(vertexMappingMode.currentIndexChanged)
        def vertex_mapping_mode_changed():
            model.transfer.vertex_transfer_mode = vertexMappingMode.currentData()

        update_settings_to_model()

        return result

    def build_influenes_tab():
        infl_ui, _, recalcMatches = influenceMappingUI.build_ui(parent, model.transfer.influences_mapping)

        padding = QtWidgets.QVBoxLayout()
        padding.setContentsMargins(0, 20 * scale_multiplier, 0, 0)
        padding.addWidget(infl_ui)

        recalcMatches()

        return padding

    tabs = QtWidgets.QTabWidget()

    tabs.addTab(qt.wrap_layout_into_widget(build_settings()), "Settings")
    tabs.addTab(qt.wrap_layout_into_widget(build_influenes_tab()), "Influences mapping")

    window = QtWidgets.QDialog(parent)
    cleanup.registerCleanupHandler(window.close)
    window.setWindowTitle("Transfer")
    window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    window.resize(720 * scale_multiplier, 500 * scale_multiplier)
    window.setLayout(QtWidgets.QVBoxLayout())

    window.layout().addWidget(tabs)
    window.layout().addLayout(buttonRow(window))

    if session.active():
        session.addQtWidgetReference(window)

    single_transfer_dialog_policy.setCurrent(window)
    window.show()


def build_transfer_action(session, parent):
    from maya import cmds

    from .actions import define_action

    targets = []

    def detect_targets():
        targets[:] = []
        selection = cmds.ls(sl=True)
        if len(selection) != 2:
            return False

        if not api.Layers(selection[0]).is_enabled():
            return False

        targets[:] = selection

        return True

    def transfer_dialog(transfer):
        """

        :type transfer: LayersTransfer
        """
        model = UiModel()
        model.transfer = transfer
        open(parent, model)

    def handler():
        if not targets:
            return

        t = LayersTransfer()
        t.source = targets[0]
        t.target = targets[1]
        t.customize_callback = transfer_dialog
        t.execute()

    result = define_action(parent, "Transfer layers...", callback=handler)

    @signal.on(session.events.nodeSelectionChanged)
    def on_selection_changed():
        result.setEnabled(detect_targets())

    on_selection_changed()

    return result
