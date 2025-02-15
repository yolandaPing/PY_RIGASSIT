from ngSkinTools2.api import PaintMode
from ngSkinTools2.api.pyside import QtCore, QtGui, QtWidgets
from ngSkinTools2.api.python_compatibility import Object
from ngSkinTools2.signal import Signal
from ngSkinTools2.ui import qt
from ngSkinTools2.ui.layout import scale_multiplier


def curve_mapping(x, s, t):
    """
    provides a linear-to smooth curve mapping

    based on a paper https://arxiv.org/abs/2010.09714
    """
    epsilon = 0.000001

    if x < 0:
        return 0
    if x > 1:
        return 1
    if x < t:
        return (t * x) / (x + s * (t - x) + epsilon)

    return ((1 - t) * (x - 1)) / (1 - x - s * (t - x) + epsilon) + 1


class NumberSliderGroup(Object):
    """
    float spinner is the "main control" while the slider acts as complementary way to change value
    """

    slider_resolution = 1000.0
    infinity_max = 65535

    def __init__(self, value_type=float, min_value=0, max_value=1, soft_max=True, tooltip="", expo=None, decimals=3):
        self.value_range = 0
        self.min_value = 0
        self.max_value = 0

        self.float_mode = value_type == float

        self.__layout = layout = QtWidgets.QHBoxLayout()
        self.valueChanged = Signal("sliderGroupValueChanged")

        self.spinner = spinner = QtWidgets.QDoubleSpinBox() if self.float_mode else QtWidgets.QSpinBox()
        spinner.setKeyboardTracking(False)

        self.expo = expo
        self.expo_coefficient = 1.0

        spinner.setFixedWidth(80 * scale_multiplier)
        if self.float_mode:
            spinner.setDecimals(decimals)

        spinner.setToolTip(tooltip)

        self.slider = slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(self.slider_resolution)
        slider.setToolTip(tooltip)

        layout.addWidget(spinner)
        layout.addWidget(slider)

        self.set_range(min_value, max_value, soft_max=soft_max)

        @qt.on(spinner.valueChanged)
        def update_slider():
            with qt.signals_blocked(slider):
                slider.setValue(self.__to_slider_value(spinner.value()))
            self.valueChanged.emit()

        @qt.on(slider.valueChanged)
        def slider_updated():
            spinner.setValue(self.__from_slider_value(slider.value()))

        self.update_slider = update_slider

    def set_range(self, min_value, max_value, soft_max=True):
        with qt.signals_blocked(self.spinner):
            self.spinner.setMaximum(self.infinity_max if soft_max else max_value)
        self.min_value = min_value
        self.max_value = max_value
        self.value_range = max_value - min_value
        single_step = self.value_range / 100.0
        if not self.float_mode and single_step < 1:
            single_step = 1
        self.spinner.setSingleStep(single_step)

    def __to_slider_value(self, v):
        # formulas: https://www.desmos.com/calculator/gjwk5t3wmn

        x = float(v - self.min_value) / self.value_range

        y = x
        if self.expo == 'start':
            y = curve_mapping(x, self.expo_coefficient, 0)
        if self.expo == 'end':
            y = curve_mapping(x, self.expo_coefficient, 1)

        return y * self.slider_resolution

    def __from_slider_value(self, v):
        x = v / self.slider_resolution
        if self.expo == 'start':
            x = curve_mapping(x, self.expo_coefficient, 1)
        if self.expo == 'end':
            x = curve_mapping(x, self.expo_coefficient, 0)

        return self.min_value + self.value_range * x

    def layout(self):
        return self.__layout

    def value(self):
        return self.spinner.value()

    def value_trimmed(self):
        value = self.value()
        if self.min_value is not None and value < self.min_value:
            return self.min_value
        if self.max_value is not None and value > self.max_value:
            return self.max_value
        return value

    def set_value(self, value):
        if self.value != value:
            self.spinner.setValue(value)

    def set_enabled(self, enabled):
        self.spinner.setEnabled(enabled)
        self.slider.setEnabled(enabled)

    # noinspection PyPep8Naming
    def blockSignals(self, block):
        """
        a mimic of qt's blockSignals for both inner widgets
        """
        result = self.spinner.blockSignals(block)
        self.slider.blockSignals(block)
        self.valueChanged.enabled = not block
        return result

    def set_expo(self, expo, coefficient=3):
        self.expo = expo
        self.expo_coefficient = coefficient
        self.update_slider()


def set_paint_expo(number_group, paint_mode):
    """
    Sets number slider group expo according to paint mode.

    :type paint_mode: int
    :type number_group: NumberSliderGroup
    """
    intensity_expo = {
        PaintMode.add: ("start", 3),
        PaintMode.scale: ("end", 8),
        PaintMode.smooth: ("start", 3),
        PaintMode.sharpen: ("start", 3),
    }
    expo, c = intensity_expo.get(paint_mode, (None, 1))
    if number_group.expo == expo and number_group.expo_coefficient == c:
        return

    number_group.set_expo(expo=expo, coefficient=c)


def button_row(button_defs, side_menu=None):
    result = QtWidgets.QHBoxLayout()

    stretch_marker = "Marker"

    for i in (side_menu or []) + [stretch_marker] + button_defs:
        if i == stretch_marker:
            result.addStretch()
            continue
        label, handler = i
        btn = QtWidgets.QPushButton(label, minimumWidth=100)
        qt.on(btn.clicked)(handler)
        result.addWidget(btn)

    return result


class ColorButton(QtWidgets.QPushButton):
    def __init__(self):
        QtWidgets.QPushButton.__init__(self)
        self.color = None
        qt.on(self.clicked)(self.__pick_color)

        self.color_changed = Signal("color changed")

    def set_color(self, color):
        if isinstance(color, (list, tuple)):
            color = QtGui.QColor.fromRgb(color[0] * 255, color[1] * 255, color[2] * 255, 255)
        self.color = color
        self.setStyleSheet("background-color: %s;" % color.name())
        self.color_changed.emit()

    def get_color_3f(self):
        return [i / 255.0 for i in self.color.getRgb()[:3]]

    def __pick_color(self):
        color = QtWidgets.QColorDialog.getColor(initial=self.color, options=QtWidgets.QColorDialog.DontUseNativeDialog)
        if color.isValid():
            self.set_color(color)
