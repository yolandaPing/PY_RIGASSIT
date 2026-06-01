from ngSkinTools2 import signal
from ngSkinTools2.api.pyside import QAction, QtCore, QtWidgets
from ngSkinTools2.api.session import Session
from ngSkinTools2.operations import import_v1_actions
from ngSkinTools2.ui import influencesview, layersview, qt
from ngSkinTools2.ui.influencesview import InfluenceNameFilter
from ngSkinTools2.ui.layout import scale_multiplier


def build_layers_ui(parent, actions, session):
    """

    :type session: Session
    :type actions: ngSkinTools2.ui.actions.Actions
    :type parent: QWidget
    """

    influencesFilter = InfluenceNameFilter()

    def build_infl_filter():
        img = qt.image_icon("clear-input-white.png")

        result = QtWidgets.QHBoxLayout()
        result.setSpacing(5)
        filter = QtWidgets.QComboBox()
        filter.setMinimumHeight(22 * scale_multiplier)
        filter.setEditable(True)
        filter.lineEdit().setPlaceholderText("Search...")
        result.addWidget(filter)
        clear = QAction(result)
        clear.setIcon(img)
        filter.lineEdit().addAction(clear, QtWidgets.QLineEdit.TrailingPosition)

        @qt.on(filter.editTextChanged)
        def filter_edited():
            influencesFilter.set_filter_string(filter.currentText())

            clear.setVisible(len(filter.currentText()) != 0)

        @qt.on(clear.triggered)
        def clear_clicked():
            filter.clearEditText()

        filter_edited()

        return result

    split = QtWidgets.QSplitter(orientation=QtCore.Qt.Horizontal, parent=parent)

    layout = QtWidgets.QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(3)
    clear = QtWidgets.QPushButton()
    clear.setFixedSize(20, 20)
    # layout.addWidget(clear)

    layers = layersview.build_view(parent, actions)
    layout.addWidget(layers)
    split.addWidget(qt.wrap_layout_into_widget(layout))

    layout = QtWidgets.QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(3)
    influences = influencesview.build_view(parent, actions, session, filter=influencesFilter)
    layout.addWidget(influences)
    layout.addLayout(build_infl_filter())
    split.addWidget(qt.wrap_layout_into_widget(layout))

    return split


def build_no_layers_ui(parent, actions, session):
    """
    :param parent: ui parent
    :type actions: ngSkinTools2.ui.actions.Actions
    :type session: Session
    """

    def build_evaluation_banner():
        title = QtWidgets.QLabel("Evaluation/Non-Commercial License")
        title.setWordWrap(True)
        title.setStyleSheet("font-weight: bold; border: none;")
        title.setAlignment(QtCore.Qt.AlignCenter)

        # detail = QtWidgets.QLabel(
        #     "Current license permits plugin usage for evaluation purposes and non-commercial projects. "
        #     'Some features may be restricted to commercial licenses only. <a href="http://www.ngskintools.com">more</a>')
        detail = QtWidgets.QLabel("Current license permits plugin usage for evaluation purposes and non-commercial projects.")
        detail.setOpenExternalLinks(True)
        detail.setWordWrap(True)
        detail.setAlignment(QtCore.Qt.AlignCenter)
        detail.setStyleSheet("border: none;")

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(title)
        layout.addWidget(detail)

        result = QtWidgets.QGroupBox()
        result.setLayout(layout)

        result.setStyleSheet("border: 1px solid #938976; background-color: #fcf8e3; " "color: #8a6d3b;")

        @signal.on(session.licenseClient.statusChanged, qtParent=parent)
        def update_banner_visibility():
            result.setVisible(session.licenseClient.should_show_evaluation_banner())

        update_banner_visibility()

        return result

    layout = QtWidgets.QVBoxLayout()
    layout.setContentsMargins(30, 30, 30, 30)

    selection_display = QtWidgets.QLabel("pPlane1")
    selection_display.setStyleSheet("font-weight: bold")

    selection_note = QtWidgets.QLabel("Skinning Layers cannot be attached to this object")
    selection_note.setWordWrap(True)

    layout.addStretch(1)
    layout.addWidget(selection_display)
    layout.addWidget(selection_note)
    layout.addWidget(qt.bind_action_to_button(actions.import_v1, QtWidgets.QPushButton()))
    layout.addWidget(qt.bind_action_to_button(actions.initialize, QtWidgets.QPushButton()))
    layout.addWidget(build_evaluation_banner())
    layout.addStretch(3)

    layout_widget = qt.wrap_layout_into_widget(layout)

    @signal.on(session.events.targetChanged, qtParent=parent)
    def handle_target_changed():
        if session.state.layersAvailable:
            return  # no need to update

        is_skinned = session.state.selectedSkinCluster is not None
        selection_display.setText(session.state.selectedSkinCluster)
        selection_display.setVisible(is_skinned)

        note = "Select a mesh with a skin cluster attached."
        if is_skinned:
            note = "Skinning layers are not yet initialized for this mesh."
            if import_v1_actions.can_import(session):
                note = "Skinning layers from previous ngSkinTools version are initialized on this mesh."

        selection_note.setText(note)

    if session.active():
        handle_target_changed()

    return layout_widget


def build_target_ui(parent, actions, session):
    """

    :type session: Session
    """
    result = QtWidgets.QStackedWidget()
    result.addWidget(build_no_layers_ui(parent, actions, session))
    result.addWidget(build_layers_ui(parent, actions, session))
    result.setMinimumHeight(300 * scale_multiplier)

    @signal.on(session.events.targetChanged, qtParent=parent)
    def handle_target_changed():
        if not session.state.layersAvailable:
            result.setCurrentIndex(0)
        else:
            result.setCurrentIndex(1)

    if session.active():
        handle_target_changed()

    return result
