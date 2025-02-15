from maya import OpenMayaUI as omui
from maya import cmds

from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.pyside import QtCore, QtGui, QtWidgets, QWidget, wrap_instance
from ngSkinTools2.api.session import session
from ngSkinTools2.ui.options import config

from .. import cleanup, signal, version
from ..observableValue import ObservableValue
from . import (
    aboutwindow,
    dialogs,
    hotkeys_setup,
    licensewindow,
    qt,
    tabLayerEffects,
    tabMirror,
    tabPaint,
    tabSetWeights,
    tabTools,
    targetui,
    updatewindow,
)
from .layout import scale_multiplier

log = getLogger("main window")


def get_image_path(file_name):
    import os

    for i in os.getenv("XBMLANGPATH", "").split(os.path.pathsep):
        result = os.path.join(i, file_name)
        if os.path.isfile(result):
            return result

    return file_name


def build_menu(parent, actions):
    menu = QtWidgets.QMenuBar(parent=parent)

    def top_level_menu(label):
        sub_item = menu.addMenu(label)
        sub_item.setSeparatorsCollapsible(False)
        sub_item.setTearOffEnabled(True)
        return sub_item

    sub = top_level_menu("File")
    sub.addSeparator().setText("Import/Export")
    sub.addAction(actions.importFile)
    sub.addAction(actions.exportFile)

    sub = top_level_menu("Layers")
    sub.addSeparator().setText("Layer actions")
    sub.addAction(actions.initialize)
    sub.addAction(actions.import_v1)
    actions.addLayersActions(sub)
    sub.addSeparator().setText("Copy")
    sub.addAction(actions.transfer)

    sub = top_level_menu("Tools")
    sub.addAction(actions.add_influences)
    sub.addAction(actions.toolsAssignFromClosestJoint)
    sub.addSeparator()
    sub.addAction(actions.transfer)
    sub.addSeparator()
    sub.addAction(actions.toolsDeleteCustomNodesOnSelection)
    sub.addAction(actions.toolsDeleteCustomNodes)

    sub = top_level_menu("View")
    sub.addAction(actions.showUsedInfluencesOnly)

    sub = top_level_menu("Help")
    sub.addAction(actions.documentation.user_guide)
    sub.addAction(actions.documentation.api_root)
    sub.addAction(actions.documentation.changelog)
    sub.addAction(actions.documentation.contact)
    sub.addSeparator()
    sub.addAction("Register...").triggered.connect(lambda: licensewindow.show(parent))
    sub.addSeparator()
    sub.addAction(actions.check_for_updates)
    sub.addAction("About...").triggered.connect(lambda: aboutwindow.show(parent))

    return menu


def build_rmb_menu_layers(view, actions):
    view.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
    actions.addLayersActions(view)


class MainWindowOptions:
    current_tab = ObservableValue(0)


def build_ui(parent):
    """
    :type parent: QWidget
    """
    options = MainWindowOptions()
    window = QtWidgets.QWidget(parent)

    session.addQtWidgetReference(window)

    from ngSkinTools2.ui.actions import Actions

    actions = Actions(parent=window, session=session)

    tabs = QtWidgets.QTabWidget(window)

    tabs.addTab(tabPaint.build_ui(tabs, actions), "Paint")
    tabs.addTab(tabSetWeights.build_ui(tabs), "Set Weights")
    tabs.addTab(tabMirror.buildUI(tabs), "Mirror")
    tabs.addTab(tabLayerEffects.build_ui(tabs), "Effects")
    tabs.addTab(tabTools.build_ui(actions, session), "Tools")

    @signal.on(options.current_tab.changed)
    def set_current_tab():
        tabs.setCurrentIndex(options.current_tab())

    layers_toolbar = QtWidgets.QToolBar()
    layers_toolbar.addAction(actions.addLayer)
    layers_toolbar.setOrientation(QtCore.Qt.Vertical)

    spacing_h = 5
    spacing_v = 5

    layers_row = targetui.build_target_ui(window, actions, session)

    split = QtWidgets.QSplitter(orientation=QtCore.Qt.Vertical, parent=window)
    split.addWidget(layers_row)
    split.addWidget(tabs)
    split.setStretchFactor(0, 2)
    split.setStretchFactor(1, 3)
    split.setContentsMargins(spacing_h, spacing_v, spacing_h, spacing_v)

    def build_icon_label():
        w = QWidget()
        w.setStyleSheet("background-color: #dcce87;color: #373737;")
        l = QtWidgets.QHBoxLayout()
        icon = QtWidgets.QLabel()
        icon.setPixmap(QtGui.QIcon(":/error.png").pixmap(16 * scale_multiplier, 16 * scale_multiplier))
        icon.setFixedSize(16 * scale_multiplier, 16 * scale_multiplier)
        text = QtWidgets.QLabel("<placeholder>")
        text.setWordWrap(True)
        text.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        l.addWidget(icon)
        l.addWidget(text)
        w.setContentsMargins(0, 0, 0, 0)
        w.setLayout(l)

        return w, text.setText

    def build_license_error():
        label, set_text = build_icon_label()

        @signal.on(session.licenseClient.statusChanged, qtParent=parent)
        def update_license_error():
            log.info("updating license status")
            status = session.licenseClient.current_status()
            label.setVisible(status.has_errors())
            if label.isVisible():
                set_text("There is a problem with your license: " + status.status_description)

        update_license_error()

        return label

    error_section = QtWidgets.QVBoxLayout()
    error_section.addWidget(build_license_error())
    error_section.setContentsMargins(0, 0, 0, 0)

    layout = QtWidgets.QVBoxLayout(window)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(build_menu(window, actions))
    layout.addLayout(error_section)
    layout.addWidget(split)

    window.setLayout(layout)

    hotkeys_setup.install_hotkeys()

    dialogs.promptsParent = window

    if config.checkForUpdatesAtStartup():
        updatewindow.silent_check_and_show_if_available(qt.mainWindow)

    return window, options


DOCK_NAME = 'ngSkinTools2_mainWindow'


def workspace_control_permanent_script():
    from ngSkinTools2 import workspace_control_main_window

    return "import {f.__module__}; {f.__module__}.{f.__name__}()".format(f=workspace_control_main_window)


# noinspection PyShadowingBuiltins
def open():
    """
    opens main window
    """

    if not cmds.workspaceControl(DOCK_NAME, q=True, exists=True):
        # build UI script in type-safe manner

        cmds.workspaceControl(
            DOCK_NAME,
            retain=False,
            floating=True,
            # ttc=["AttributeEditor",-1],
            uiScript=workspace_control_permanent_script(),
        )

    # bring tab to front
    cmds.evalDeferred(lambda *args: cmds.workspaceControl(DOCK_NAME, e=True, r=True))

    def close():
        from maya import cmds

        # noinspection PyBroadException
        try:
            cmds.deleteUI(DOCK_NAME)
        except:
            pass
        pass

    cleanup.registerCleanupHandler(close)


def resume_in_workspace_control():
    """
    this method is responsible for resuming workspace control when Maya is building/restoring UI as part of it's
    workspace management cycle (open UI for the first time, restart maya, change workspace, etc)
    """

    cmds.workspaceControl(DOCK_NAME, e=True, label="ngSkinTools " + version.pluginVersion())
    widget = wrap_instance(omui.MQtUtil.findControl(DOCK_NAME), QtWidgets.QWidget)

    ui, _ = build_ui(widget)
    widget.layout().addWidget(ui)
