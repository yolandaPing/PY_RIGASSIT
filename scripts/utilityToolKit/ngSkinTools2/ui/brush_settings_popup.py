from ngSkinTools2.api import PaintTool
from ngSkinTools2.api.paint import popups
from ngSkinTools2.api.pyside import QtCore, QtGui, QtWidgets
from ngSkinTools2.ui import qt, widgets
from ngSkinTools2.ui.layout import scale_multiplier


def brush_settings_popup(paint):
    """

    :type paint: PaintTool
    """
    window = QtWidgets.QWidget(qt.mainWindow)
    window.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)
    window.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    spacing = 5

    layout = QtWidgets.QVBoxLayout()
    layout.setSpacing(spacing)

    intensity_slider = widgets.NumberSliderGroup()
    widgets.set_paint_expo(intensity_slider, paint.paint_mode)
    intensity_slider.set_value(paint.intensity)

    @qt.on(intensity_slider.slider.sliderReleased, intensity_slider.spinner.editingFinished)
    def close_with_slider_intensity():
        close_with_intensity(intensity_slider.value())

    def close_with_intensity(value):
        paint.intensity = value
        window.close()

    def create_intensity_button(intensity):
        btn = QtWidgets.QPushButton("{0:.3g}".format(intensity))
        btn.clicked.connect(lambda: close_with_intensity(intensity))
        btn.setMinimumWidth(60 * scale_multiplier)
        btn.setMinimumHeight(30 * scale_multiplier)
        return btn

    layout.addLayout(intensity_slider.layout())

    for values in [(0.0, 1.0), (0.25, 0.5, 0.75), (0.025, 0.05, 0.075, 0.1, 0.125)]:
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(spacing)
        for v in values:
            row.addWidget(create_intensity_button(v))
        layout.addLayout(row)

    group = QtWidgets.QGroupBox("Brush Intensity")
    group.setLayout(layout)

    layout = QtWidgets.QVBoxLayout()
    layout.setContentsMargins(4 * scale_multiplier, 4 * scale_multiplier, 4 * scale_multiplier, 4 * scale_multiplier)
    layout.addWidget(group)

    window.setLayout(layout)

    window.show()
    mp = QtGui.QCursor.pos()
    window.move(mp.x() - window.size().width() / 2, mp.y() - window.size().height() / 2)

    window.activateWindow()

    popups.close_all()
    popups.add(window)
