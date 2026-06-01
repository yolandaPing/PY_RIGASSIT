import os

from ngSkinTools2.api.pyside import QtCore, QtGui, QtWidgets, get_main_window
from ngSkinTools2.api.python_compatibility import Object


def wrap_layout_into_widget(layout):
    w = QtWidgets.QWidget()
    w.setLayout(layout)
    return w


def signals_blocked(widget):
    return SignalBlockContext(widget)


class SignalBlockContext(Object):
    def __init__(self, widget):
        self.widget = widget

    def __enter__(self):
        self.prevState = self.widget.blockSignals(True)

    def __exit__(self, *args):
        self.widget.blockSignals(self.prevState)


class updateGuard(Object):
    def __init__(self):
        self.updating = False

    def __enter__(self):
        self.updating = True

    def __exit__(self, *args):
        self.updating = False


def on(*signals):
    """
    decorator for function: list signals that should fire for this function.

    instead of:

        def something():
            ...
        btn.clicked.connect(something)

    do:

        @qt.on(btn.clicked)
        def something():
            ...
    """

    def decorator(fn):
        for i in signals:
            i.connect(fn)
        return fn

    return decorator


class SingleWindowPolicy(Object):
    def __init__(self):
        self.lastWindow = None

    def setCurrent(self, window):
        if self.lastWindow:
            self.lastWindow.close()
        self.lastWindow = window

        on(window.finished)(self.cleanup)

    def cleanup(self):
        self.lastWindow = None


def alternative_palette_light():
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(243, 244, 246))
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(33, 37, 41))
    return palette


def bind_action_to_button(action, button):
    """

    :type button: PySide2.QtWidgets.QPushButton
    :type action: PySide2.QtWidgets.QAction
    """

    @on(action.changed)
    def update_state():
        button.setText(action.text())
        button.setEnabled(action.isEnabled())
        button.setToolTip(action.toolTip())
        button.setStatusTip(action.statusTip())
        button.setVisible(action.isVisible())
        if action.isCheckable():
            button.setChecked(action.isChecked())

    button.setCheckable(action.isCheckable())

    on(button.clicked)(action.trigger)
    update_state()

    return button


images_path = os.path.join(os.path.dirname(__file__), "images")


def icon_path(path):
    if path.startswith(':'):
        return path
    return os.path.join(images_path, path)


def scaled_icon(path, w, h):
    from ngSkinTools2.ui.layout import scale_multiplier

    return QtGui.QIcon(
        QtGui.QPixmap(icon_path(path)).scaled(w * scale_multiplier, h * scale_multiplier, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
    )


def image_icon(file_name):
    return QtGui.QIcon(icon_path(file_name))


def select_data(combo, data):
    """
    set combo box index to data index
    """
    combo.setCurrentIndex(combo.findData(data))


mainWindow = get_main_window()
