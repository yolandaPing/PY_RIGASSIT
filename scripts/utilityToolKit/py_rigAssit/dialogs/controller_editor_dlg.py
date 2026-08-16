# -*- coding: utf-8 -*-

# .FileName:controller_editor_dialog.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/6 22:40
# .Finish time:
import os, json
from functools import partial
from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
from ui_framework.widgets.button import GridButtons
from py_rigAssit.dialogs import decorator, mayaPrint
from ControllerTool.CurveEdit import CurvesEdit
import saveRootPath as Root
import ControllerTool.ControllerFiles as curve_shape

import maya.cmds as cmds, maya.mel as mel

PY_WIDGEAT = Widgets()
curve_edit = CurvesEdit()


class PYColorGrid(QtWidgets.QWidget):
    colorClicked = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(PYColorGrid, self).__init__(parent)

        layout = QtWidgets.QGridLayout(self)
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)

        self.colors = [
            (.467, .467, .467), (.000, .000, .000), (.247, .247, .247), (.498, .498, .498),
            (0.608, 0, 0.157), (0, 0.016, 0.373), (0, 0, 1), (0, 0.275, 0.094),
            (0.145, 0, 0.263), (0.78, 0, 0.78), (0.537, 0.278, 0.2), (0.243, 0.133, 0.122),
            (0.6, 0.145, 0), (1, 0, 0), (0, 1, 0), (0, 0.255, 0.6),
            (1, 1, 1), (1, 1, 0), (0.388, 0.863, 1), (0.263, 1, 0.635),
            (1, 0.686, 0.686), (0.89, 0.675, 0.475), (1, 1, 0.384), (0, 0.6, 0.325),
            (0.627, 0.412, 0.188), (0.62, 0.627, 0.188), (0.408, 0.627, 0.188), (0.188, 0.627, 0.365),
            (0.188, 0.627, 0.627), (0.188, 0.404, 0.627), (0.435, 0.188, 0.627), (0.463, 0.162, 0.299)
        ]

        self.buttons = []
        for i, c in enumerate(self.colors):
            btn = QtWidgets.QPushButton()
            btn.setFixedSize(40, 25)
            btn.setStyleSheet(
                "background-color: rgb(%d,%d,%d);" % (
                    int(c[0] * 255), int(c[1] * 255), int(c[2] * 255)
                )
            )
            btn.clicked.connect(partial(self._emit_color, i))
            layout.addWidget(btn, i // 8, i % 8)
            self.buttons.append(btn)

    def _emit_color(self, idx):
        self.colorClicked.emit(idx)


class PYCustomColorButton(QtWidgets.QLabel):
    colorChanged = QtCore.Signal(QtGui.QColor)

    def __init__(self, color=QtCore.Qt.white, parent=None):
        super(PYCustomColorButton, self).__init__(parent)

        self._color = QtGui.QColor()
        self.set_size(60, 18)
        self.set_color(color)

    def set_size(self, width, height):
        self.setFixedSize(width, height)

    def set_color(self, color):
        color = QtGui.QColor(color)
        self._color = color
        pixmap = QtGui.QPixmap(self.size())
        pixmap.fill(self._color)
        self.setPixmap(pixmap)

    def get_color(self):
        return self._color

    def select_color(self):
        color = QtWidgets.QColorDialog.getColor(
            self.get_color(),
            self,
            options=QtWidgets.QColorDialog.DontUseNativeDialog
        )
        if color.isValid():
            self.set_color(color)
            self.colorChanged.emit(color)

    def mouseReleaseEvent(self, event):
        self.select_color()


class PYControllerEditorLayout(QtWidgets.QWidget):

    shape_icon_path = Root.CurveDataPath.replace("\\", '/') + "/"
    icon_path = Root.IconsPath.replace("\\", '/') + "/"

    def __init__(self, parent=PY_WIDGEAT.maya_main_window()):
        super(PYControllerEditorLayout, self).__init__(parent)


    def init_ui(self, copyright=False):
        container_main = QtWidgets.QWidget()
        container_main.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        main_layout = QtWidgets.QVBoxLayout(container_main)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(2)
        main_layout.addWidget(PY_WIDGEAT.create_title("Controller Editor", 15, 30))

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setContentsMargins(2, 2, 2, 2)

        container = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(container)
        self.scroll_layout.setContentsMargins(6, 0, 6, 0)
        self.scroll_layout.setSpacing(6)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)
        self.scroll_layout.addWidget(self.build_curve_edit())
        self.scroll_layout.addWidget(self.build_resize_block())
        self.scroll_layout.addWidget(self.build_curve_shape())
        self.scroll_layout.addStretch()

        self.create_connections()

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocus()

        return container_main

    # ---------------------- CURVE EDIT ----------------------
    def build_curve_edit(self):
        layout =PY_WIDGEAT.create_section("Color")
        layout.setContentsMargins(0, 0, 8, 0)
        self.color_grid = PYColorGrid()
        layout.addWidget(self.color_grid)
        self.custom_color_button = PYCustomColorButton(QtCore.Qt.white)

        type_layout = QtWidgets.QHBoxLayout()
        type_layout.setContentsMargins(0, 0, 8, 0)
        self.type_group = PY_WIDGEAT.create_radiogroup(
            "",
            [
                ("Default ", 1, "对象shape overrideColor"),
                ("Outliner ", 2, "大纲对象显示颜色")
            ],
            default_id=2
        )

        type_layout.addWidget(PY_WIDGEAT.create_text("Custom Type:"), 1)
        type_layout.addWidget(self.type_group, 1)
        type_layout.addWidget(PY_WIDGEAT.create_text(" Color:"),1)
        type_layout.addWidget(self.custom_color_button,2)
        layout.addLayout(type_layout)

        return layout

    # ---------------------- RESIZE / ROTATE ----------------------
    def build_resize_block(self):
        layout = PY_WIDGEAT.create_section("Curve Editor")
        layout.setContentsMargins(0, 0, 12, 0)

        scale_layout = QtWidgets.QHBoxLayout()
        size_layout = QtWidgets.QHBoxLayout()
        rotate_layout = QtWidgets.QVBoxLayout()
        aixs_layout = QtWidgets.QHBoxLayout()
        rot_type_layout = QtWidgets.QHBoxLayout()
        scale_layout.setContentsMargins(0, 0, 0, 0)
        scale_layout.setContentsMargins(10, 0, 35, 0)
        aixs_layout.setContentsMargins(10, 0, 35, 0)
        curve_edit_grid = GridButtons("curve_edit", 4)
        curve_edit_grid.clicked.connect(self.run_action)

        self.rot_type_block = PY_WIDGEAT.create_radiogroup(
            "",
            [
                ("Center ", 1, "中心"),
                ("Piovt ", 2, "轴心")
            ],
            default_id=1
        )
        rot_type_layout.addWidget(PY_WIDGEAT.create_text("调整方式:  "))
        rot_type_layout.addWidget(self.rot_type_block, 1)
        self.scale_slider = PY_WIDGEAT.create_floatSlider()
        self.scale_slider.setRange(0.01, 5.0)
        self.scale_slider.setValue(0.25)
        size = QtCore.QSize(20, 20)
        self.add_btn = QtWidgets.QPushButton()
        self.add_btn.setIcon(QtGui.QIcon(self.icon_path + "/AddSets.png"))
        self.add_btn.setProperty("help", True)
        self.add_btn.setIconSize(size)
        self.subtract_btn = QtWidgets.QPushButton()
        self.subtract_btn.setIcon(QtGui.QIcon(self.icon_path + "/SubtractSets.png"))
        self.subtract_btn.setProperty("help", True)
        self.subtract_btn.setIconSize(size)

        self.add_btn.setFixedSize(35, 25)
        self.subtract_btn.setFixedSize(35, 25)

        size_layout.addWidget(self.subtract_btn)
        size_layout.addWidget(self.scale_slider)
        size_layout.addWidget(self.add_btn)
        scale_layout.addLayout(size_layout)
        self.rotate_spin = QtWidgets.QDoubleSpinBox()
        self.rotate_spin.setValue(90)
        self.btn_x = QtWidgets.QPushButton()
        self.btn_y = QtWidgets.QPushButton()
        self.btn_z = QtWidgets.QPushButton()
        size = QtCore.QSize(30, 30)
        for bn, ic in zip((self.btn_x, self.btn_y, self.btn_z), ("/AxisX.png", "/AxisY.png", "/AxisZ.png")):
            bn.setIcon(QtGui.QIcon(self.icon_path + ic))
            bn.setProperty("class", "iconBtn")
            bn.setIconSize(size)
        aixs_layout.addWidget(QtWidgets.QLabel("Rotate:"), 1)
        aixs_layout.addWidget(self.rotate_spin, 1)
        aixs_layout.addWidget(self.btn_x)
        aixs_layout.addWidget(self.btn_y)
        aixs_layout.addWidget(self.btn_z)
        rotate_layout.addLayout(aixs_layout)
        layout.addWidget(curve_edit_grid)
        PY_WIDGEAT.separator(layout, True)
        layout.addLayout(rot_type_layout)
        layout.addLayout(scale_layout)
        layout.addLayout(rotate_layout)

        return layout

    # ---------------------- SHAPE ICONS ----------------------
    def build_curve_shape(self):
        layout = PY_WIDGEAT.create_section("Custom Shape")
        layout.setContentsMargins(0, 0, 4, 0)
        text_layout, self.text_edit, self.create_btn = PY_WIDGEAT.create_QLineEdit_row("Text:")
        self.create_btn.setText("Create")
        text_layout.setContentsMargins(8, 0, 20, 0)

        self.cons_block = PY_WIDGEAT.create_radiogroup(
            u"约束方式:",
            [
                ("none", 1, "只创建控制器，不做任何约束"),
                ("child", 2, "子级"),
                ("parent", 3, u"父子约束"),
                ("point", 4, u"点约束"),
                ("orient", 5, u"旋转约束")
            ],
            default_id=1
        )

        checkbox_layout = QtWidgets.QHBoxLayout()
        self.add_scale_cbx = QtWidgets.QCheckBox(' add scale ?')
        self.add_grp_cbx = QtWidgets.QCheckBox(' add sec/pri group ?')
        checkbox_layout.addWidget(self.add_scale_cbx)
        checkbox_layout.addWidget(self.add_grp_cbx)

        layout.addLayout(text_layout)
        PY_WIDGEAT.separator(layout, True)
        layout.addWidget(self.cons_block)
        layout.addLayout(checkbox_layout)
        PY_WIDGEAT.separator(layout, True)
        layout.addWidget(self.build_icon_grid(self.shape_icon_path))

        return layout

    def build_icon_grid(self, icon_path):
        widget = QtWidgets.QWidget()
        layout = PY_WIDGEAT.flowLayout(widget, spacing=4)
        widget.setLayout(layout)

        files = [f for f in os.listdir(icon_path) if f.endswith('_M.png')]
        self.icon_buttons = []
        size = QtCore.QSize(33, 33)
        for f in files:
            icon_name = f[:f.index('.')]
            shape_name = icon_name.replace('_icon_M', '')
            img_path = os.path.join(icon_path, icon_name + '.png').replace("\\", "/")

            btn = QtWidgets.QToolButton()
            btn.setIcon(QtGui.QIcon(img_path))
            btn.setIconSize(size)
            btn.setFixedSize(40, 40)
            btn.setToolTip(shape_name)
            btn.setProperty("class", "iconBtn")
            btn.clicked.connect(lambda checked=False, s=shape_name: self.on_create_ctrl(s))

            layout.addWidget(btn)
            self.icon_buttons.append(btn)

        return widget

    def create_connections(self):
        self.color_grid.colorClicked.connect(self.on_color_clicked)
        self.custom_color_button.colorChanged.connect(self.on_custom_color_clicked)
        self.subtract_btn.clicked.connect(lambda: self.on_scale_shape(False))
        self.add_btn.clicked.connect(lambda: self.on_scale_shape(True))
        self.create_btn.clicked.connect(self.on_create_text)
        self.btn_x.clicked.connect(lambda: self.rotate_curve(1))
        self.btn_y.clicked.connect(lambda: self.rotate_curve(2))
        self.btn_z.clicked.connect(lambda: self.rotate_curve(3))


    def on_color_clicked(self, index):
        curve_edit.updateColorSlider(index)
        print("Color index:", index)


    def on_custom_color_clicked(self, color):
        if cmds.ls(sl=1):
            if self.type_group.checkedId() == 1:
                curve_edit.set_custom_color((color.redF(), color.greenF(), color.blueF()))
            else:
                curve_edit.set_Outliner_Color((color.redF(), color.greenF(), color.blueF()))


    @decorator.keep_selected
    def on_scale_shape(self, add=False):
        controls = cmds.ls(sl=1)
        if controls:
            curve_edit.scale_curve_shapes(controls, self.scale_slider.value(), self.rot_type_block.checkedId(), add)


    def on_create_text(self):
        txt = self.text_edit.text()
        curve_shape.creat_text_shape(txt)
        print("Create text:", txt)


    def on_create_ctrl(self, shape):
        cons_mod = self.cons_block.checkedId()
        scale = self.add_scale_cbx.isChecked()
        pri = self.add_grp_cbx.isChecked()
        curve_shape.create_shape(shape, cons_mod-1, pri, scale)


    @decorator.keep_selected
    def rotate_curve(self, axis):
        value = self.rotate_spin.value()
        curves = cmds.ls(sl=1)
        curve_edit.shape_rotation(curves, value, axis, self.rot_type_block.checkedId())
        print("Rotate:", axis, value)


    def run_action(self, text):
        print("Run:", text)
        controls = cmds.ls(sl=1)
        if not controls:
            mayaPrint.warning("Please select an object.")
            return
        if text == "Mirror L/R":
            curve_edit.mirror_ctrl()
        elif text == "Mirror self":
            curve_edit.mirrorCrv()
        elif text == "build Curve":
            mel.eval('source ' + json.dumps(Root.ParentPath.replace("\\", '/') + "scripts/mel/CurveFromSelectedObjs.mel"))
        else:
            curve_edit.VisShape()


class PYControllerEditorDialog(PyouPersistentWindow):

    def __init__(self, parent=PY_WIDGEAT.maya_main_window()):
        super(PYControllerEditorDialog, self).__init__("PYControllerEditorDialog", "PYControllerEditorDialog", parent)

        self.setWindowTitle("Controller Editor")
        self.resize(280, 680)
        self.loadWindowSettings()

        self._build_ui()


    def _build_ui(self):
        main = QtWidgets.QVBoxLayout(self)
        main.setContentsMargins(4, 4, 4, 4)
        main.setSpacing(4)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setContentsMargins(0, 0, 0, 0)

        cld_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(cld_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(4)

        scroll.setWidget(cld_widget)
        main.addWidget(scroll)

        self.widget = PYControllerEditorLayout(parent=self)

        scroll_layout.addWidget(self.widget.init_ui())

        PY_WIDGEAT.create_copyrightText(main, "2026")


def main():
    global UI
    try:
        UI.close()
        UI.deleteLater()
    except:
        pass

    UI = PYControllerEditorDialog()
    UI.show()


if __name__ == "__main__":
    main()