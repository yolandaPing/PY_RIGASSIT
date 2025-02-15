from ngSkinTools2 import cleanup, licenseClient, signal
from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.pyside import Qt, QtGui, QtWidgets
from ngSkinTools2.api.python_compatibility import Object
from ngSkinTools2.api.session import session, withSession
from ngSkinTools2.licenseClient import LicenseData
from ngSkinTools2.observableValue import ObservableValue
from ngSkinTools2.ui import dialogs, qt
from ngSkinTools2.ui.layout import scale_multiplier

log = getLogger("license window")


class Message(Object):
    type_error = 'error'
    type_info = 'info'

    def __init__(self, text, msg_type=None):
        self.type = msg_type if msg_type is not None else self.type_info
        self.text = text

    def __repr__(self):
        return "Message(type:{self.type}, text: {self.text!r})".format(self=self)


class LicenseWindowModel(Object):
    mode_license_key = "License key"
    mode_activation_code = "Activation code"
    mode_license_server = "License server"

    def __init__(self, license_info):
        self.license_status = ObservableValue()
        self.message = ObservableValue()
        self.operation_in_progress = ObservableValue()
        self.activation_code_link = ObservableValue()

        self.__license_info = license_info
        self.license_key_activation_method = 'online'

        self.license_key = ''
        self.activation_method_selected = 'License key'

        self.activation_code = ''

        self.server_address = ''

        @signal.on(session.licenseClient.statusChanged)
        def on_license_client_status_change():
            self.update_status()

        self.update_status()

    def update_status(self):
        status = self.__license_info.current_status()  # type:LicenseData
        self.license_status.set(status)
        log.info("status updated to %s", status)
        descr = status.status_description
        if descr is None:
            self.message.set(None)
        else:
            self.message.set(Message(descr, msg_type=Message.type_info if not status.errors else Message.type_error))
            log.info("setting message to %s", self.message())

    def activate(self):
        def do_license_key_online():
            self.operation_in_progress.set(True)
            task = self.__license_info.activate_with_license_key(self.license_key)

            def done(context):
                self.operation_in_progress.set(False)
                self.update_status()

            task.add_done_handler(done)
            task.start()

        def do_license_key_offline():
            try:
                self.activation_code_link.set(self.__license_info.generate_acivation_code_link(self.license_key))
                self.message.set(Message("Activation code generated", Message.type_info))
            except Exception as err:
                self.message.set(Message(str(err), msg_type=Message.type_error))

        def do_activation_code():
            try:
                self.__license_info.accept_activation_code(self.activation_code)
                self.update_status()
            except Exception as err:
                self.message.set(Message(str(err), msg_type=Message.type_error))

        def do_license_server():
            self.__license_info.accept_license_server_url(self.server_address)
            self.update_status()

        if self.activation_method_selected == self.mode_license_key:
            if self.license_key_activation_method == 'online':
                do_license_key_online()
            if self.license_key_activation_method == 'offline':
                do_license_key_offline()

        if self.activation_method_selected == self.mode_activation_code:
            do_activation_code()

        if self.activation_method_selected == self.mode_license_server:
            do_license_server()

    def clear_license_configuration(self):
        self.__license_info.clear_configuration()
        self.update_status()

    def license_is_active(self):
        status = self.license_status(None)
        return status is not None and status.active

    def is_readonly(self):
        return not self.__license_info.current_configuration().is_editable

    def describe_license_status(self):
        if not self.license_is_active():
            return "Evaluation/non-commercial use"

        text = "License active"
        status = self.license_status()  # type: LicenseData

        if status.licensed_to:
            text += "; licensed to " + status.licensed_to

        return text

    def describe_configuration(self):
        text = []

        c = self.current_configuration()
        if not c.is_editable:
            text.append("License setup provided via environment configuration and is not editable.")
            text.append("")
        if c.active_license_file:
            if 'source_file' in c.active_license_file:
                text.append("License file: " + c.active_license_file['source_file'])
            if 'licensekey' in c.active_license_file:
                text.append("License key: " + c.active_license_file['licensekey'])
        if c.license_server_url:
            text.append("License server url: " + c.license_server_url)

        return "\n".join(text)

    def current_configuration(self):
        """
        :rtype: licenseClient.Configuration
        """
        return self.__license_info.current_configuration()

    def config_empty(self):
        c = self.current_configuration()
        log.info("checking if config is empty: %r", c.active_license_file)
        return not c.active_license_file and not c.license_server_url


class UI:
    def __init__(self):
        self.status_label = None


@withSession
def show(parent, license_info=None):
    """
    :type license_info: object
    :type parent: QWidget
    """

    ui = UI()

    if license_info is None:
        license_info = session.licenseClient

    model = LicenseWindowModel(license_info)

    log.info("creating ui instance")

    window = QtWidgets.QDialog(parent)
    session.addQtWidgetReference(window)
    window.setModal(False)
    window.resize(600 * scale_multiplier, 500 * scale_multiplier)
    window.setAttribute(Qt.WA_DeleteOnClose)
    window.setWindowTitle("ngSkinTools license activation")
    layout = QtWidgets.QVBoxLayout()
    window.setLayout(layout)
    layout.setContentsMargins(0, 0, 0, 0)

    # noinspection PyShadowingNames
    def license_status():
        result = QtWidgets.QWidget()
        result.setPalette(qt.alternative_palette_light())
        result.setAutoFillBackground(True)

        layout = QtWidgets.QVBoxLayout()
        result.setLayout(layout)

        layout.addWidget(QtWidgets.QLabel("<b>License status:</b>"))
        ui.status_label = status_label = QtWidgets.QLabel("Licensed to debug mode")
        layout.addWidget(status_label)

        @signal.on(model.license_status.changed)
        def update_license_status():
            status_label.setText(model.describe_license_status())

        ui.message_label = message_label = QtWidgets.QLabel()
        layout.addWidget(message_label)
        message_label.setVisible(False)
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        @signal.on(model.message.changed)
        def update_message():
            msg = model.message()
            if msg is None:
                message_label.setVisible(False)
                return

            escaped_msg = msg.text.replace("<", "&lt;").replace(">", "&gt;")

            color = {Message.type_error: '#FF0000', Message.type_info: '#5cb85c'}[msg.type]
            message_label.setText('<b><font color="{color}">{msg}</font></b>'.format(color=color, msg=escaped_msg))
            message_label.setVisible(True)

        update_license_status()
        update_message()

        layout.setContentsMargins(25, 25, 25, 25)
        return result

    def activation_method():
        result = QtWidgets.QVBoxLayout()
        result.setContentsMargins(25, 10, 25, 10)

        radio_row = QtWidgets.QHBoxLayout()
        button_group = QtWidgets.QButtonGroup()
        for index, i in enumerate(
            [LicenseWindowModel.mode_license_key, LicenseWindowModel.mode_activation_code, LicenseWindowModel.mode_license_server]
        ):
            radio = QtWidgets.QRadioButton(i)
            button_group.addButton(radio, index)
            radio_row.addWidget(radio)
        radio_row.addStretch()
        button_group.buttons()[0].setChecked(True)

        result.addWidget(QtWidgets.QLabel("Activate new license with:"))
        result.addLayout(radio_row)

        result.addSpacing(10)

        methods = [qt.wrap_layout_into_widget(i) for i in (license_key_activation_method(), activation_code_method(), license_server_method())]
        for i in methods:
            result.addWidget(i)

        loading_indicator = make_loading_indicator()
        result.addWidget(loading_indicator)

        # noinspection PyShadowingNames
        @qt.on(button_group.buttonClicked)
        @signal.on(model.operation_in_progress.changed)
        def update_controls_state():
            for index, method in enumerate(methods):
                method.setVisible(not model.operation_in_progress(False) and button_group.checkedId() == index)
                method.setEnabled(not model.operation_in_progress(False))

            loading_indicator.setVisible(model.operation_in_progress(False))
            for i in button_group.buttons():
                i.setEnabled(not model.operation_in_progress(False))

            model.activation_method_selected = button_group.checkedButton().text()

        update_controls_state()

        result_widget = qt.wrap_layout_into_widget(result)
        return result_widget

    def make_loading_indicator():
        result = QtWidgets.QLabel("Please wait...")
        return result

    def activation_code_link_info():
        result = QtWidgets.QVBoxLayout()
        result.setContentsMargins(0, 0, 0, 0)
        result.addSpacing(10)
        result.addWidget(QtWidgets.QLabel("Use this link to generate activation code:"))
        link_text = QtWidgets.QTextEdit()
        link_text.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        link_text.setReadOnly(True)
        result.addWidget(link_text)

        result_widget = qt.wrap_layout_into_widget(result)

        @signal.on(model.activation_code_link.changed)
        def update_license_info():
            link = model.activation_code_link("")
            result_widget.setVisible(bool(link))
            link_text.setText(link)

        update_license_info()

        copy_button = QtWidgets.QPushButton("Copy to clipboard")

        @qt.on(copy_button.clicked)
        def copy_clicked():
            QtWidgets.QApplication.clipboard().setText(link_text.toPlainText())

        button_row = QtWidgets.QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(copy_button)
        result.addLayout(button_row)

        return result_widget

    def license_key_activation_method():
        result = QtWidgets.QVBoxLayout()
        result.addWidget(QtWidgets.QLabel("License key:"))
        license_key = QtWidgets.QLineEdit()
        license_key.setPlaceholderText("00000000-0000-0000-0000-000000000000")
        result.addWidget(license_key)

        result.addSpacing(10)

        result.addWidget(QtWidgets.QLabel("Activation method:"))
        radio_row = QtWidgets.QVBoxLayout()
        button_group = QtWidgets.QButtonGroup()
        result.addLayout(radio_row)

        method_online = QtWidgets.QRadioButton("Connect and download license data (requires Internet connectivity)")
        method_offline = QtWidgets.QRadioButton("Offline: generate a link for downloading activation code")
        button_group.addButton(method_online)
        button_group.addButton(method_offline)
        radio_row.addWidget(method_online)
        radio_row.addWidget(method_offline)
        method_online.setChecked(True)

        result.addWidget(activation_code_link_info())

        @qt.on(method_online.toggled, method_offline.toggled)
        def update_activation_method():
            model.license_key_activation_method = 'online' if method_online.isChecked() else "offline"

        @qt.on(license_key.textChanged)
        def update_license_key():
            model.license_key = (license_key.text() or "").strip()

        return result

    def activation_code_method():
        result = QtWidgets.QVBoxLayout()
        result.addWidget(QtWidgets.QLabel("Activation code:"))

        activation_code = QtWidgets.QTextEdit()
        activation_code.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        activation_code.setPlaceholderText("Paste or drop activation code here.")

        @qt.on(activation_code.textChanged)
        def activation_code_updated():
            model.activation_code = activation_code.toPlainText()

        result.addWidget(activation_code)
        return result

    def license_server_method():
        result = QtWidgets.QVBoxLayout()
        result.addWidget(QtWidgets.QLabel("Server address:"))
        server_url = QtWidgets.QLineEdit()
        server_url.setPlaceholderText("your-server:8050 or 10.45.11.85:8050")
        result.addWidget(server_url)

        @qt.on(server_url.textChanged)
        def activation_code_updated():
            model.server_address = server_url.text()

        result.addStretch()
        return result

    # noinspection PyShadowingNames
    def buttons_row():
        btn_activate = QtWidgets.QPushButton("Activate")
        btn_activate.setDefault(True)
        btn_activate.setMinimumWidth(100 * scale_multiplier)

        @qt.on(btn_activate.clicked)
        def activate():
            prev_cursor = window.cursor()
            window.setCursor(Qt.WaitCursor)
            try:
                model.activate()
            finally:
                window.setCursor(prev_cursor)

        btn_close = QtWidgets.QPushButton("Cancel")
        btn_close.setMinimumWidth(100 * scale_multiplier)
        btn_close.clicked.connect(lambda: window.close())

        btn_release = QtWidgets.QPushButton("Clear license configuration")

        @qt.on(btn_release.clicked)
        def handle_release():
            message = (
                "This will reset license configuration so you can choose another activation method.\n"
                "For standalone licenses, this does not release license key binding to this workstation.\n"
                "\n"
                "Do you want to proceed?"
            )

            if dialogs.yesNo(message):
                model.clear_license_configuration()

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(btn_release)
        layout.addStretch()
        layout.setContentsMargins(20 * scale_multiplier, 15 * scale_multiplier, 20 * scale_multiplier, 15 * scale_multiplier)
        layout.addWidget(btn_activate)
        layout.addWidget(btn_close)

        @signal.on(model.license_status.changed, model.operation_in_progress.changed)
        def update_license_status():
            config_available = not model.config_empty()
            btn_activate.setVisible(not model.is_readonly() and not config_available)
            btn_close.setText("Close" if model.is_readonly() or config_available else "Cancel")
            btn_release.setVisible(not model.is_readonly() and config_available)

            btn_activate.setEnabled(not model.operation_in_progress(False))

        update_license_status()

        return layout

    def configuration():
        result = QtWidgets.QVBoxLayout()
        result.setContentsMargins(25, 10, 25, 10)
        ui.configuration_descr = descr = QtWidgets.QLabel()
        descr.setTextInteractionFlags(Qt.TextSelectableByMouse)
        result.addWidget(descr)

        @signal.on(model.license_status.changed)
        def update():
            descr.setText(model.describe_configuration())

        update()
        return qt.wrap_layout_into_widget(result)

    layout.addWidget(license_status())

    method_ui = activation_method()
    configuration_ui = configuration()

    @signal.on(model.license_status.changed)
    def update_controls_state():
        method_ui.setVisible(model.config_empty())
        configuration_ui.setVisible(not model.config_empty())

    layout.addWidget(method_ui)
    layout.addWidget(configuration_ui)
    layout.addStretch(2)
    layout.addLayout(buttons_row())

    update_controls_state()
    window.show()

    cleanup.registerCleanupHandler(window.close)

    return ui
