from ngSkinTools2 import signal
from ngSkinTools2.api.pyside import QtWidgets
from ngSkinTools2.ui import qt, widgets


def bind(ui, model):
    if isinstance(ui, QtWidgets.QCheckBox):
        ui.setChecked(model())

        @qt.on(ui.stateChanged)
        def update_model():
            model.set(ui.isChecked())

    elif isinstance(ui, widgets.NumberSliderGroup):
        ui.set_value(model())

        @signal.on(ui.valueChanged)
        def update_model():
            model.set(ui.value())

    else:
        raise Exception("could not bind control to model")
