import webbrowser

from ngSkinTools2.api import versioncheck
from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.pyside import Qt, QtWidgets
from ngSkinTools2.ui.options import bind_checkbox, config

from .. import cleanup, signal, version
from . import qt
from .layout import scale_multiplier

log = getLogger("plugin")


def show(parent, silent_mode):
    """
    :type parent: QWidget
    """

    error_signal = signal.Signal("error")
    success_signal = signal.Signal("success")

    # noinspection PyShadowingNames
    def body():
        result = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        result.setLayout(layout)
        layout.setContentsMargins(20, 30, 20, 20)

        header = QtWidgets.QLabel("<strong>Checking for update...</strong>")
        result1 = QtWidgets.QLabel("Current version: <strong>2.0.0</strong>")
        result2 = QtWidgets.QLabel("Update available: 2.0.1")
        download = QtWidgets.QPushButton("Download ngSkinTools v2.0.1")
        # layout.addWidget(QtWidgets.QLabel("Checking for updates..."))
        layout.addWidget(header)
        layout.addWidget(result1)
        layout.addWidget(result2)
        layout.addWidget(download)

        result1.setVisible(False)
        result2.setVisible(False)
        download.setVisible(False)

        @signal.on(error_signal)
        def error_handler(error):
            header.setText("<strong>Error: {0}</strong>".format(error))

        @signal.on(success_signal)
        def success_handler(info):
            """

            :type info: ngSkinTools2.api.versioncheck.
            """

            header.setText("<strong>{0}</strong>".format('Update available!' if info.update_available else 'ngSkinTools is up to date.'))
            result1.setVisible(True)
            result1.setText("Current version: <strong>{0}</strong>".format(version.pluginVersion()))
            if info.update_available:
                result2.setVisible(True)
                result2.setText(
                    "Update available: <strong>{0}</strong>, released on {1}".format(info.latest_version, info.update_date.strftime("%d %B, %Y"))
                )
                download.setVisible(True)
                download.setText("Download ngSkinTools v" + info.latest_version)

                @qt.on(download.clicked)
                def open_link():
                    webbrowser.open_new(info.download_url)

        return result

    # noinspection PyShadowingNames
    def buttonsRow(window):
        btn_close = QtWidgets.QPushButton("Close")
        btn_close.setMinimumWidth(100 * scale_multiplier)

        check_do_on_startup = bind_checkbox(QtWidgets.QCheckBox("Check for updates at startup"), config.checkForUpdatesAtStartup)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(check_do_on_startup)
        layout.addStretch()
        layout.addWidget(btn_close)
        layout.setContentsMargins(20 * scale_multiplier, 15 * scale_multiplier, 20 * scale_multiplier, 15 * scale_multiplier)

        btn_close.clicked.connect(lambda: window.close())
        return layout

    window = QtWidgets.QWidget(parent, Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
    window.resize(400 * scale_multiplier, 200 * scale_multiplier)
    window.setAttribute(Qt.WA_DeleteOnClose)
    window.setWindowTitle("ngSkinTools2 version update")
    layout = QtWidgets.QVBoxLayout()
    window.setLayout(layout)
    layout.setContentsMargins(0, 0, 0, 0)

    layout.addWidget(body())
    layout.addStretch(2)
    layout.addLayout(buttonsRow(window))

    if not silent_mode:
        window.show()

    @signal.on(success_signal)
    def on_success(info):
        if silent_mode:
            if info.update_available:
                window.show()
            else:
                log.info("not showing the window")
                window.close()

    cleanup.registerCleanupHandler(window.close)

    @qt.on(window.destroyed)
    def closed():
        log.info("deleting update window")

    versioncheck.download_update_info(success_callback=success_signal.emit, failure_callback=error_signal.emit)


def silent_check_and_show_if_available(parent):
    show(parent, silent_mode=True)


def show_and_start_update(parent):
    show(parent, silent_mode=False)


def build_action_check_for_updates(parent):
    from ngSkinTools2.ui import actions

    return actions.define_action(parent, "Check for Updates...", callback=lambda: show_and_start_update(parent))
