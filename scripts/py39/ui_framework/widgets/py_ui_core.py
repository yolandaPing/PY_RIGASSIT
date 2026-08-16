# -*- coding: utf-8 -*-

# .FileName:py_ui_core.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/26 22:51
# .Finish time:
import os
try:
    from ui_framework.core.qtCompat import *
except:
    from CommonUse.qtCompat import *


class ArrowDir:
    VERTICAL = 0
    HORIZONTAL = 1


class CardWidget(QtWidgets.QFrame):
    def __init__(self, title="", parent=None):
        super(CardWidget, self).__init__(parent)

        self.setProperty("card", True)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 8, 10, 10)
        self.main_layout.setSpacing(6)

        # ===== 标题 =====
        self.title_label = QtWidgets.QLabel(title)
        self.title_label.setProperty("cardTitle", True)
        self.main_layout.addWidget(self.title_label)

        # ===== 分割线 =====
        line = QtWidgets.QFrame()
        line.setProperty("cardLine", True)
        line.setFixedHeight(1)
        self.main_layout.addWidget(line)

        # ===== 内容区 =====
        self.content_layout = QtWidgets.QVBoxLayout()
        self.content_layout.setSpacing(4)
        self.main_layout.addLayout(self.content_layout)

    def addWidget(self, w):
        self.content_layout.addWidget(w)

    def addLayout(self, l):
        self.content_layout.addLayout(l)


class CollapsibleArrow(QtWidgets.QFrame):
    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent=parent)

        self.isCollapsed = False
        self.setMaximumSize(20, 20)

        self.arrowPointsFhorizontal = (QtCore.QPointF(4.0, 8.0), QtCore.QPointF(14.0, 8.0), QtCore.QPointF(9.0, 14.0))
        self.arrowPointsFvertical = (QtCore.QPointF(8.0, 4.0), QtCore.QPointF(14.0, 9.0), QtCore.QPointF(8.0, 14.0))
        self.arrowPointsF = self.arrowPointsFhorizontal

    def setArrow(self, arrowDir):
        self.arrowPointsF = self.arrowPointsFhorizontal if arrowDir else self.arrowPointsFvertical

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setBrush(QtGui.QColor(238, 238, 238))
        qp.drawPolygon(self.arrowPointsF)
        qp.end()


class TitleLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        QtWidgets.QLabel.__init__(self, parent=parent)


class TitleFrame(QtWidgets.QFrame):
    clicked = QtCore.Signal(object)

    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent=parent)

        self.titleLabel = None
        self.arrow = None
        self.initTitleFrame()

    def initArrow(self):
        self.arrow = CollapsibleArrow(self)

    def initTitleLabel(self):
        self.titleLabel = TitleLabel(self)
        self.titleLabel.setMinimumHeight(24)
        self.titleLabel.move(QtCore.QPoint(24, 0))

    def mousePressEvent(self, event):
        self.clicked.emit(1)
        return super(TitleFrame, self).mousePressEvent(event)

    def initTitleFrame(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumHeight(26)
        self.setMaximumHeight(26)
        self.setStyleSheet("QFrame {\
        background-color: rgba(93, 93, 93, 255);\
        margin: 0px, 0px, 0px, 0px;\
        padding: 0px, 0px, 0px, 0px;\
        }")

        self.initArrow()
        self.initTitleLabel()


class CollapsibleWidget(QtWidgets.QWidget):

    def __init__(self, title="", expanded=False, parent=None):
        super(CollapsibleWidget, self).__init__(parent)

        self._expanded = expanded
        self._alive = True

        # ===== Header =====
        self.header_btn = QtWidgets.QToolButton(self)
        self.header_btn.setText(title)
        self.header_btn.setCheckable(True)
        self.header_btn.setChecked(expanded)
        self.header_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.header_btn.setArrowType(
            QtCore.Qt.DownArrow if expanded else QtCore.Qt.RightArrow
        )
        self.header_btn.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )

        self.header_btn.clicked.connect(self._on_toggle)

        # ===== Content =====
        self.content = QtWidgets.QWidget(self)
        self.content.setVisible(expanded)

        self.content_layout = QtWidgets.QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(6, 6, 6, 6)
        self.content_layout.setSpacing(4)

        self.content.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Preferred
        )

        # ===== Root =====
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(2)

        root.addWidget(self.header_btn)
        root.addWidget(self.content)

    # ===============================

    def addWidget(self, w):
        if not w:
            return

        if w.parent() is not None and w.parent() != self.content:
            w.setParent(None)

        self.content_layout.addWidget(w)

    def addLayout(self, lay):
        if not lay:
            return

        if lay.parent() is not None:
            # 已经被使用，直接报错或跳过
            print("layout already has parent, skip:", lay)
            return

        wrapper = QtWidgets.QWidget(self.content)
        wrapper.setLayout(lay)
        self.content_layout.addWidget(wrapper)

    def set_content_layout(self, layout):
        self.setContentLayout(layout)

    def setContentLayout(self, lay):
        if not lay:
            return

        if lay.parent() is not None:
            raise RuntimeError("Layout already has parent. Cannot reuse.")

        container = QtWidgets.QWidget(self.content)
        container.setLayout(lay)

        self.content_layout.addWidget(container)


    def _on_toggle(self, checked=False):
        if not self._alive:
            return
        self.toggle()

    def toggle(self):
        self.setExpanded(not self._expanded)

    def setExpanded(self, state):
        self._expanded = state

        self.header_btn.setChecked(state)
        self.header_btn.setArrowType(
            QtCore.Qt.DownArrow if state else QtCore.Qt.RightArrow
        )

        self.content.setVisible(state)

        self.content.updateGeometry()
        self.updateGeometry()

        p = self.parentWidget()
        if p:
            p.updateGeometry()

    def isExpanded(self):
        return self._expanded


    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)

            w = item.widget()
            if w:
                w.setParent(None)
                w.deleteLater()

            l = item.layout()
            if l:
                self._clear_layout(l)

    def clear(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)

            w = item.widget()
            if w:
                w.setParent(None)
                w.deleteLater()

            l = item.layout()
            if l:
                self._clear_layout(l)


    def deleteLater(self):
        self._alive = False

        try:
            self.header_btn.clicked.disconnect()
        except:
            pass

        super(CollapsibleWidget, self).deleteLater()


class FloatFieldGroup(QtWidgets.QWidget):

    def __init__(self, label, values, decimals=5, parent=None):
        super(FloatFieldGroup, self).__init__(parent)

        layout = QtWidgets.QHBoxLayout(self)

        layout.addWidget(QtWidgets.QLabel(label))

        self.fields = []
        for v in values:
            f = QtWidgets.QDoubleSpinBox()
            f.setDecimals(decimals)
            f.setValue(v)
            self.fields.append(f)
            layout.addWidget(f)


class FloatSliderGroup(QtWidgets.QWidget):
    valueChange = QtCore.Signal(float)

    def __init__(self, label="", parent=None):
        super(FloatSliderGroup, self).__init__(parent)

        self.layout = QtWidgets.QHBoxLayout(self)
        if label:
            self.layout.addWidget(QtWidgets.QLabel(label))
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.spin = QtWidgets.QDoubleSpinBox()
        self.layout.addWidget(self.spin)
        self.layout.addWidget(self.slider)
        self.setRange(0, 1)
        self.spin.valueChanged.connect(self.convert_slider)
        self.slider.valueChanged.connect(self.convert_spin)
        self.spin.setSingleStep(0.01)
        self.spin.setDecimals(3)

    def convert_spin(self, value):
        self.spin.setValue(value / 1000.0)
        self.valueChange.emit(self.spin.value())
        self.spin.setMinimumWidth(65)

    def convert_slider(self, value):
        self.slider.setValue(int(round(1000 * value)))

    def setRange(self, min_value, max_value):
        self.spin.setRange(min_value, max_value)
        self.slider.setRange(min_value * 1000, max_value * 1000)

    def value(self):
        return self.spin.value()

    def setValue(self, value):
        self.spin.setValue(value)


class SliderWidget(QtWidgets.QWidget):

    def __init__(self, min_value=0.01,max_value=10.0,  parent=None):
        super(SliderWidget, self).__init__(parent)

        self.min_value = min_value
        self.max_value = max_value
        self.scale = 1000.0   # 精度 3 位小数

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)

        # slider 用整数映射 float
        self.slider.setRange(
            int(self.min_value * self.scale),
            int(self.max_value * self.scale)
        )

        self.slider.setValue(int(1.0 * self.scale))   # 默认值 1.0

        self.edit = QtWidgets.QLineEdit("1.0")
        self.edit.setFixedWidth(60)

        self.slider.valueChanged.connect(self.update_edit_from_slider)
        self.edit.editingFinished.connect(self.update_slider_from_edit)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.edit)
        layout.addWidget(self.slider)

    def update_edit_from_slider(self, v):
        value = v / self.scale
        self.edit.setText("{:.3f}".format(value).rstrip("0").rstrip("."))

    def update_slider_from_edit(self):
        try:
            value = float(self.edit.text())

            # 限制范围
            value = max(self.min_value, min(self.max_value, value))

            self.slider.setValue(int(value * self.scale))

        except:
            pass

    def value(self):
        return self.slider.value() / self.scale

    def setValue(self, v):
        v = max(self.min_value, min(self.max_value, v))
        self.slider.setValue(int(v * self.scale))


class RadioGroupBlock(QtWidgets.QWidget):

    idClicked = QtCore.Signal(int)

    def __init__(self,
                 title="",
                 items=None,
                 default_id=None,
                 enabled_map=None,
                 orientation="Horizontal",
                 lay="Vertical",
                 parent=None):

        super(RadioGroupBlock, self).__init__(parent)

        self._alive = True
        self.btns = {}

        self.group = QtWidgets.QButtonGroup()
        self.group.setExclusive(True)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)

        if title:
            label = QtWidgets.QLabel(title)
            label.setProperty("isRadio", True)
            main_layout.addWidget(label)

        radio_layout = QtWidgets.QHBoxLayout() if orientation == "Horizontal" else QtWidgets.QVBoxLayout()
        main_layout.addLayout(radio_layout)

        for item in (items or []):
            text, btn_id = item[:2]
            tooltip = item[2] if len(item) > 2 else ""

            btn = QtWidgets.QRadioButton(text, self)

            if tooltip:
                btn.setToolTip(tooltip)

            self.group.addButton(btn, btn_id)
            self.btns[btn_id] = btn
            radio_layout.addWidget(btn)

            btn.clicked.connect(
                lambda checked=False, i=btn_id: self._safe_emit(i)
            )

        if default_id in self.btns:
            self.btns[default_id].setChecked(True)

        if enabled_map:
            for i, b in self.btns.items():
                b.setEnabled(enabled_map.get(i, True))

    def _safe_emit(self, btn_id):
        if not self._alive:
            return
        self.idClicked.emit(btn_id)

    def checkedId(self):
        return self.group.checkedId()

    def setChecked(self, btn_id):
        if btn_id in self.btns:
            self.btns[btn_id].setChecked(True)
            self._safe_emit(btn_id)

    def deleteLater(self):
        self._alive = False

        try:
            for b in self.btns.values():
                b.clicked.disconnect()
        except:
            pass

        try:
            self.group = None
        except:
            pass

        super(RadioGroupBlock, self).deleteLater()

    def setEnabledByIds(self, ids, state=True):
        for i in ids:
            if i in self.btns:
                self.btns[i].setEnabled(state)

    def button(self, btn_id):
        return self.btns.get(btn_id)

    def text(self, btn_id):
        btn = self.btns.get(btn_id)
        return btn.text() if btn else ""


class FlowLayout(QtWidgets.QLayout):

    def __init__(self, parent=None, margin=0, spacing=2):
        super(FlowLayout, self).__init__(parent)
        self.itemList = []
        self.setSpacing(spacing)
        self.setContentsMargins(margin, margin, margin, margin)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        return None

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self._doLayout(QtCore.QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self._doLayout(rect, False)

    def sizeHint(self):
        return QtCore.QSize(200, 200)

    def _doLayout(self, rect, testOnly):
        x, y = rect.x(), rect.y()
        lineHeight = 0

        for item in self.itemList:
            widget = item.widget()
            spaceX = self.spacing()
            spaceY = self.spacing()

            nextX = x + item.sizeHint().width() + spaceX
            if nextX > rect.right() and lineHeight > 0:
                x = rect.x()
                y += lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(
                    QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint())
                )

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()


class Section(QtWidgets.QFrame):
    def __init__(self, title="", parent=None):
        super(Section, self).__init__(parent)

        self.setObjectName("Section")

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.main_layout.setSpacing(6)

        self.title = QtWidgets.QLabel(title)
        self.title.setObjectName("SectionTitle")

        self.main_layout.addWidget(self.title)

    def addWidget(self, w):
        self.main_layout.addWidget(w)

    def addLayout(self, lay):
        self.main_layout.addLayout(lay)


class Bezier(QtWidgets.QWidget):
    valueChanged = QtCore.Signal()

    def __init__(self, parent=None):
        super(Bezier, self).__init__(parent)

        self.points = [[0.0, 1.0], [1.0 / 3, 1.0], [2.0 / 3, 0.0], [1.0, 0.0]]
        self.__movePoint = 0
        self.__mirror = False
        self.__adsorb = False
        self.gridVisible = False
        self.setMinimumSize(180, 90)

    def mousePressEvent(self, event):
        self.setFocus()
        QtWidgets.QWidget.mousePressEvent(self, event)
        points = [QtCore.QPointF((self.width() - 1) * p[0], (self.height() - 1) * p[1]) for p in self.points]

        p = QtCore.QPointF(event.pos()) - points[1]
        length = (p.x() ** 2 + p.y() ** 2) ** 0.5
        if length < 10:
            self.__movePoint = 1
            self.update()
            return

        p = QtCore.QPointF(event.pos()) - points[2]
        length = (p.x() ** 2 + p.y() ** 2) ** 0.5
        if length < 10:
            self.__movePoint = 2
            self.update()
            return
        self.__movePoint = 0
        self.update()

    def mouseReleaseEvent(self, event):
        QtWidgets.QWidget.mouseReleaseEvent(self, event)

        self.__movePoint = 0
        self.update()

    def mouseMoveEvent(self, event):
        QtWidgets.QWidget.mouseMoveEvent(self, event)
        if self.__movePoint == 1:
            p = QtCore.QPointF(event.pos())
            x = max(min(float(p.x()) / (self.width() - 1), 1.0), 0.0)
            y = max(min(float(p.y()) / (self.height() - 1), 1.0), 0.0)
            if self.__adsorb:
                x = round(x * 12) / 12.0
                y = round(y * 12) / 12.0
            if self.__mirror:
                mx = (1 - x)
                my = (1 - y)
                self.points[2] = [mx, my]
            self.points[1] = [x, y]
            self.update()
            self.valueChanged.emit()
        if self.__movePoint == 2:
            p = QtCore.QPointF(event.pos())
            x = max(min(float(p.x()) / (self.width() - 1), 1.0), 0.0)
            y = max(min(float(p.y()) / (self.height() - 1), 1.0), 0.0)
            if self.__adsorb:
                x = round(x * 6) / 6.0
                y = round(y * 6) / 6.0
            if self.__mirror:
                mx = (1 - x)
                my = (1 - y)
                self.points[1] = [mx, my]
            self.points[2] = [x, y]
            self.update()
            self.valueChanged.emit()

    def setGridVisible(self, visible):
        self.gridVisible = visible
        self.update()

    def paintEvent(self, event):
        QtWidgets.QWidget.paintEvent(self, event)
        painter = QtGui.QPainter(self)
        # background
        painter.setBrush(QtGui.QBrush(QtGui.QColor(120, 120, 120), QtCore.Qt.SolidPattern))
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 1, QtCore.Qt.SolidLine))
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
        # curve
        painter.setBrush(QtGui.QBrush(QtGui.QColor(100, 100, 100), QtCore.Qt.SolidPattern))
        points = [QtCore.QPointF((self.width() - 1) * p[0], (self.height() - 1) * p[1]) for p in self.points]
        path = QtGui.QPainterPath()
        path.moveTo(0, self.height() - 1)
        path.lineTo(points[0])
        path.cubicTo(*points[1:])
        path.lineTo(self.width() - 1, self.height() - 1)
        painter.drawPath(path)
        # grid
        if self.gridVisible:
            divisions = 12
            painter.setPen(QtGui.QPen(QtGui.QColor(80, 80, 80), 1, QtCore.Qt.DotLine))
            w_step = (self.width() - 1) / float(divisions)
            h_step = (self.height() - 1) / float(divisions)
            for i in range(1, divisions):
                w = w_step * i
                h = h_step * i
                painter.drawLine(w, 0, w, self.height())
                painter.drawLine(0, h, self.width(), h)

        default_handle_color = QtGui.QColor(200, 200, 200)  # 灰色
        highlight_color = QtGui.QColor(0, 150, 225)  # 亮蓝色
        default_line_color = QtGui.QColor(80, 80, 80)  # 深灰色虚线
        highlight_line_color = highlight_color  # 高亮用蓝色

        #起点到控制点1
        line1_color = highlight_line_color if self.__movePoint == 1 else default_line_color
        painter.setPen(QtGui.QPen(line1_color, 1, QtCore.Qt.DashLine))
        painter.drawLine(points[0], points[1])
        #终点到控制点2
        line2_color = highlight_line_color if self.__movePoint == 2 else default_line_color
        painter.setPen(QtGui.QPen(line2_color, 1, QtCore.Qt.DashLine))
        painter.drawLine(points[3], points[2])

        # 控制点1
        handle1_color = highlight_color if self.__movePoint == 1 else default_handle_color
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 1, QtCore.Qt.SolidLine))
        painter.setBrush(QtGui.QBrush(handle1_color, QtCore.Qt.SolidPattern))
        painter.drawEllipse(points[1], 6, 6)
        # 控制点2
        handle2_color = highlight_color if self.__movePoint == 2 else default_handle_color
        painter.setBrush(QtGui.QBrush(handle2_color, QtCore.Qt.SolidPattern))
        painter.drawEllipse(points[2], 6, 6)

        #绘制边框
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 1, QtCore.Qt.SolidLine))
        edge_points = []
        for w, h in zip([0, 0, 1, 1, 0], [0, 1, 1, 0, 0]):
            p = QtCore.QPointF(w * (self.width() - 1), h * (self.height() - 1))
            edge_points.extend([p, p])
        painter.drawLines(edge_points[1:-1])

        painter.end()

    def keyPressEvent(self, event):
        QtWidgets.QWidget.keyPressEvent(self, event)
        if event.key() == QtCore.Qt.Key_X:
            self.__adsorb = True
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            self.__mirror = True

    def keyReleaseEvent(self, event):
        QtWidgets.QWidget.keyReleaseEvent(self, event)
        self.__mirror = False
        self.__adsorb = False


class RadioSelector(QtWidgets.QWidget):

    valueChanged = QtCore.Signal(int, str)

    def __init__(self, labels, columns=4, parent=None):
        super(RadioSelector, self).__init__(parent)

        self.button_group = QtWidgets.QButtonGroup(self)
        self.layout = QtWidgets.QGridLayout(self)

        for i, text in enumerate(labels):
            radio = QtWidgets.QRadioButton(text)
            self.button_group.addButton(radio, i)
            self.layout.addWidget(radio, i // columns, i % columns)

        # 改这里
        self.button_group.buttonClicked.connect(self._on_changed)

        if self.button_group.buttons():
            self.button_group.button(0).setChecked(True)

    def _on_changed(self, btn):
        index = self.button_group.id(btn)
        if btn:
            self.valueChanged.emit(index, btn.text())

    def checkedId(self):
        return self.button_group.checkedId()

    def checkedText(self):
        btn = self.button_group.checkedButton()
        return btn.text() if btn else None

    def setCheckedId(self, index):
        btn = self.button_group.button(index)
        if btn:
            btn.setChecked(True)

