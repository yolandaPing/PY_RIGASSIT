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


# class CollapsibleWidget(QtWidgets.QWidget):
#     def __init__(self, title="", expanded=False, parent=None):
#         super(CollapsibleWidget, self).__init__(parent)
#
#         self._expanded = expanded
#
#         # ===== Header =====
#         self.header_btn = QtWidgets.QToolButton(self)
#         self.header_btn.setText(title)
#         self.header_btn.setCheckable(True)
#         self.header_btn.setChecked(expanded)
#         self.header_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
#         self.header_btn.setArrowType(
#             QtCore.Qt.DownArrow if expanded else QtCore.Qt.RightArrow
#         )
#         self.header_btn.setSizePolicy(
#             QtWidgets.QSizePolicy.Expanding,
#             QtWidgets.QSizePolicy.Fixed
#         )
#         self.header_btn.clicked.connect(self._on_toggle)
#
#         # ===== Content =====
#         self.content = QtWidgets.QWidget(self)
#         self.content.setVisible(expanded)
#
#         self.content_layout = QtWidgets.QVBoxLayout(self.content)
#         self.content_layout.setContentsMargins(6, 6, 6, 6)
#         self.content_layout.setSpacing(4)
#
#         # 关键：用 sizePolicy 控制，而不是 height
#         self.content.setSizePolicy(
#             QtWidgets.QSizePolicy.Expanding,
#             QtWidgets.QSizePolicy.Fixed
#         )
#
#         # ===== Root Layout =====
#         root = QtWidgets.QVBoxLayout(self)
#         root.setContentsMargins(0, 0, 0, 0)
#         root.setSpacing(2)
#
#         root.addWidget(self.header_btn)
#         root.addWidget(self.content)
#
#         # 初始化状态
#         self._apply_state(expanded)
#
#     # ===============================
#     # API
#     # ===============================
#     def addWidget(self, w):
#         self.content_layout.addWidget(w)
#
#     def addLayout(self, lay):
#         self.content_layout.addLayout(lay)
#
#     def set_content_layout(self, layout):
#         # 兼容旧项目
#         self.setContentLayout(layout)
#
#     def setContentLayout(self, lay):
#         # 先清理旧内容（关键）
#         while self.content_layout.count():
#             item = self.content_layout.takeAt(0)
#             w = item.widget()
#             if w:
#                 w.setParent(None)
#                 w.deleteLater()
#
#         lay.setParent(self.content)  # 关键
#         self.content.setLayout(lay)
#
#     # ===============================
#     # 状态控制
#     # ===============================
#     def _on_toggle(self, checked=False):
#         self.toggle()
#
#     def toggle(self):
#         self._expanded = not self._expanded
#         self._apply_state(self._expanded)
#
#     def setExpanded(self, state):
#         self._expanded = state
#         self.header_btn.setChecked(state)
#         self._apply_state(state)
#
#     def isExpanded(self):
#         return self._expanded
#
#     def _apply_state(self, expanded):
#         self.header_btn.setArrowType(
#             QtCore.Qt.DownArrow if expanded else QtCore.Qt.RightArrow
#         )
#
#         # 核心：只控制可见性
#         self.content.setVisible(expanded)
#
#         # 强制刷新布局（避免 ScrollArea 卡死）
#         self.content.updateGeometry()
#         self.updateGeometry()


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


class FloatSlider(QtWidgets.QWidget):
    float_value_changed = QtCore.Signal(float)

    def __init__(self, *args, **kwargs):
        super(FloatSlider, self).__init__(*args, **kwargs)

        self.layout = QtWidgets.QHBoxLayout(self)

        self.line_edit = QtWidgets.QLineEdit("0.000")
        self.line_edit.setFixedWidth(50)
        self.line_edit.setReadOnly(True)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(1000)

        self.slider.valueChanged.connect(self.emit_float_value)
        self.slider.valueChanged.connect(self.update_line_edit)

        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.slider)

    def emit_float_value(self, value):
        self.float_value_changed.emit(value / 1000.0)

    def update_line_edit(self, value):
        self.line_edit.setText("{:.3f}".format(value / 1000.0))

    def setValue(self, value):
        self.slider.setValue(int(value * 1000))

    def value(self):
        return self.slider.value() / 1000.0


# class RadioGroupBlock(QtWidgets.QWidget):
#
#     idClicked = QtCore.Signal(int)
#
#     def __init__(self,
#                  title="",
#                  items=None,
#                  default_id=None,
#                  enabled_map=None,
#                  orientation="Horizontal",
#                  lay="Vertical",
#                  parent=None):
#
#         super(RadioGroupBlock, self).__init__(parent)
#
#         # ======================
#         # 基础结构
#         # ======================
#         self.group = QtWidgets.QButtonGroup(self)
#         self.btns = {}
#
#         main_layout = QtWidgets.QVBoxLayout(self) if lay == "Vertical" else QtWidgets.QHBoxLayout(self)
#         main_layout.setContentsMargins(2, 2, 2, 2)
#         main_layout.setSpacing(4)
#
#         # ======================
#         # Title
#         # ======================
#         if title:
#             label = QtWidgets.QLabel(title, self)
#             label.setProperty("isRadio", True)
#             main_layout.addWidget(label)
#
#         # ======================
#         # Radio Layout
#         # ======================
#         if orientation == "Horizontal":
#             radio_layout = QtWidgets.QHBoxLayout()
#         else:
#             radio_layout = QtWidgets.QVBoxLayout()
#
#         radio_layout.setSpacing(4)
#         main_layout.addLayout(radio_layout)
#
#         items = items or []
#
#         # ======================
#         # 创建按钮
#         # ======================
#         for item in items:
#             text = item[0]
#             btn_id = item[1]
#             tooltip = item[2] if len(item) > 2 else ""
#
#             btn = QtWidgets.QRadioButton(text, self)
#
#             if tooltip:
#                 btn.setToolTip(tooltip)
#
#             self.group.addButton(btn, btn_id)
#             self.btns[btn_id] = btn
#             radio_layout.addWidget(btn)
#
#         # ======================
#         # 默认选中
#         # ======================
#         if default_id in self.btns:
#             self.btns[default_id].setChecked(True)
#
#         # ======================
#         # enabled_map（全量处理）
#         # ======================
#         if enabled_map:
#             for btn_id, btn in self.btns.items():
#                 btn.setEnabled(enabled_map.get(btn_id, True))
#
#         # ======================
#         # 信号（稳定写法）
#         # ======================
#         self.group.idClicked.connect(self._emit_id)
#
#     # ======================
#     # 信号
#     # ======================
#     def _emit_id(self, btn_id):
#         if btn_id == -1:
#             return
#         self.idClicked.emit(btn_id)
#
#     # ======================
#     # API
#     # ======================
#     def checkedId(self):
#         return self.group.checkedId()
#
#     def checkedButton(self):
#         return self.group.checkedButton()
#
#     def setChecked(self, btn_id):
#         if btn_id in self.btns:
#             self.btns[btn_id].setChecked(True)
#             self.idClicked.emit(btn_id)   # 保持行为一致
#
#     def setEnabledByIds(self, ids, state=True):
#         for i in ids:
#             if i in self.btns:
#                 self.btns[i].setEnabled(state)
#
#     def button(self, btn_id):
#         return self.btns.get(btn_id)
#
#     def text(self, btn_id):
#         btn = self.btns.get(btn_id)
#         return btn.text() if btn else ""


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

        # ❗ 不用 QButtonGroup signal（核心）
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

            # ✅ 核心：用 button 自己的 clicked（最稳）
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
