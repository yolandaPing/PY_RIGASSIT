# -*- coding: utf-8 -*-

# .FileName:split_skin_dlg.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/23 19:42
# .Finish time:
from functools import partial
from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
from py_rigAssit.dialogs import Help, decorator, mayaPrint
from selectOrRemove import SelectOrremoveObj
from py_rigAssit.common.loader import SelectionLoader
from py_rigAssit.common.command_dispatcher import CommandDispatcher
import py_rigAssit.common.img_commands
from DefromConvertWeight.soft_core_controller import SoftCoreController

import maya.cmds as cmds

PY_WIDGEST = Widgets()
dispatcher = CommandDispatcher()

MAYA_VISON = int(cmds.about(version=True))
_obj = SelectOrremoveObj()

labels = [u"sec  ", u"vertical", u"tangent", u"IK ", u"FK chain  ", u"chains root", u"chains path"]
types = ["soft", "vertical", "tangent", "points", "lines", "chains_root", "chains"]


class PYSoftWeight_Manager(QtWidgets.QWidget):
    txts = ('选择点，调节好soft的范围，解锁对应关节', "解锁关节竖直拆分权重", "解锁关节沿这轴向的切面", "解锁所有需要拆分的IK（single/ point）关节",
            "解锁所有需要拆分的FK（joint chain）关节", "解锁关节链里的父级拆分", "解锁的所有链条按path拆分")

    def __init__(self, parent=None):
        super(PYSoftWeight_Manager, self).__init__( parent)
        self.SOFT_HEADS = "SoftWeightHEADS"
        self.vector = 0
        self.controller = SoftCoreController()

    def setup_ui(self):
        container_main = QtWidgets.QWidget()
        container_main.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        main_layout = QtWidgets.QVBoxLayout(container_main)
        main_layout.setContentsMargins(5, 2, 5, 2)
        main_layout.setSpacing(2)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(4)
        option_form = QtWidgets.QFormLayout()
        selected_field_layout = QtWidgets.QHBoxLayout()

        self.bezier = PY_WIDGEST.create_Bezier()
        gird_layout = QtWidgets.QHBoxLayout()
        self.show_grid_mode = QtWidgets.QCheckBox('show gird')
        gird_key = QtWidgets.QLabel(u"shift: 镜像, x:吸附栅格, shift+x:镜像吸附")
        gird_key.setStyleSheet("color: #888;")
        gird_layout.addWidget(self.show_grid_mode)
        gird_layout.addWidget(gird_key, 1)
        self.interpolation_menu = QtWidgets.QComboBox()
        self.interpolation_menu.addItems(['Default', 'Linear', 'Smooth', 'Spline'])
        self.interpolation_menu.currentTextChanged.connect(self.on_interpolation_changed)
        interpolation_menu_layout = QtWidgets.QFormLayout()
        interpolation_menu_layout.addRow('Interpolation:', self.interpolation_menu)

        decimals = 2
        selected_value_field = QtWidgets.QDoubleSpinBox()
        selected_opsition_field = QtWidgets.QDoubleSpinBox()

        selected_value_field.setDecimals(decimals)
        selected_opsition_field.setDecimals(decimals)
        selected_value_field.setRange(0.0, 1.0)
        selected_opsition_field.setRange(0.0, 1.0)

        selected_field_layout.addLayout(interpolation_menu_layout)
        selected_field_layout.addStretch()
        selected_field_layout.addWidget(QtWidgets.QLabel("value:"))
        selected_field_layout.addWidget(selected_value_field, 1)
        selected_field_layout.addWidget(QtWidgets.QLabel("pos:"))
        selected_field_layout.addWidget(selected_opsition_field, 1)

        selected_value_field.setEnabled(False)
        selected_opsition_field.setEnabled(False)

        self.type = PY_WIDGEST.create_radioSelector(labels, columns=4)
        vector = PY_WIDGEST.create_radioSelector(["X", "Y", "Z"], columns=3)
        vector.valueChanged.connect(self.on_vector_map_changed)
        self.hit_txt = PY_WIDGEST.create_text('{}'.format(self.txts[0]))
        self.falloff_radius = PY_WIDGEST.create_floatSlider("Falloff radius")
        self.falloff_radius.setRange(.001, 50)
        self.falloff_radius.setValue(1)

        radius_layout = QtWidgets.QHBoxLayout()
        self.falloff_reset_btn = QtWidgets.QPushButton("reset 1.0")
        radius_layout.addWidget(self.falloff_radius, 2)
        radius_layout.addWidget(self.falloff_reset_btn)

        self.real_mode = QtWidgets.QCheckBox("运行后，可使用实时")

        option_form.addRow(self.type)
        option_form.addRow(self.hit_txt)
        option_form.addRow("Vector:",vector)
        option_form.addRow(radius_layout)
        option_form.addRow("Real:", self.real_mode)

        sec = PY_WIDGEST.create_section("Option")
        sec.addLayout(option_form)
        layout.addWidget(PY_WIDGEST.create_text('Weight Falloff Curve'))
        layout.addWidget(self.bezier, 1)
        layout.addLayout(gird_layout)
        layout.addLayout(selected_field_layout)
        layout.addWidget(sec)

        btn_layout, self.btn_apply, self.soft_help_btn = PY_WIDGEST.create_Qbuttons(" Apply ")

        main_layout.addLayout(layout, 1)
        main_layout.addLayout(btn_layout)

        self._connect_signals()
        self.controller.set_vector(self.vector)
        return container_main

    def _connect_signals(self):
        self.bezier.valueChanged.connect(self.real_paint_weight)
        self.show_grid_mode.stateChanged.connect( lambda state: self.bezier.setGridVisible(state == QtCore.Qt.Checked))
        self.falloff_radius.valueChange.connect(self.real_paint_weight)
        self.falloff_reset_btn.clicked.connect(self.reset_radius_to_default)
        self.type.valueChanged.connect(self.on_type_changed)
        self.real_mode.stateChanged.connect(self.real_mode_changed)
        self.btn_apply.clicked.connect(self.paint_weight)
        self.soft_help_btn.clicked.connect(self.show_split_help)
        self.on_real = False

    def get_menu_item(self, item):
        return item

    def show_heads(self):
        if cmds.headsUpDisplay(self.SOFT_HEADS, ex=1):
            cmds.headsUpDisplay(self.SOFT_HEADS, rem=1)

        if self.on_real:
            cmds.headsUpDisplay(
                self.SOFT_HEADS,
                s=2,
                b=0,
                bs="medium",
                l="Soft Weight Real-time",
                lfs="large"
            )
            Help.inView_Message("red", "Entered Soft Weight Real-time")
        else:
            Help.inView_Message("yellow", "Exited Soft Weight Real-time")

    def on_interpolation_changed(self, item):
        presets = {
            'Default': [[0.0, 1.0], [0.33, 1.0], [0.67, 0.0], [1.0, 0.0]],
            'Linear': [[0.0, 1.0], [0.0, 1.0], [1.0, 0.0], [1.0, 0.0]],
            'Smooth': [[0.0, 1.0], [0.5, 1.0], [0.5, 0.0], [1.0, 0.0]],
            'Spline': [[0.0, 1.0], [0.25, 1.0], [0.75, 0.0], [1.0, 0.0]]
        }

        points = presets.get(item, presets['Default'])
        self.bezier.points = points
        self.bezier.update()

        if self.real_mode.isChecked() and self.on_real:
            self.real_paint_weight()

    def on_radius_slider_changed(self):
        self.real_paint_weight()

    def reset_radius_to_default(self):
        self.falloff_radius.setValue(1.0)

    def on_type_changed(self, xid):
        self.hit_txt.setText(self.txts[xid])
        typ = types[xid]
        self.controller.set_type(typ)
        if self.real_mode.isChecked():
            self.real_paint_weight()

    def on_vector_map_changed(self, xid):
        self.vector = xid
        self.controller.set_vector(xid)
        self.controller.set_type(types[self.type.checkedId()])
        if self.real_mode.isChecked():
            self.real_paint_weight()

    def type_changed(self):
        self.real_mode.setChecked(QtCore.Qt.Unchecked)

    def real_mode_changed(self, state):
        enabled = (state == QtCore.Qt.Checked)

        self.controller.set_real_mode(enabled)
        self.on_real = enabled

        if enabled:
            self.real_paint_weight()

        self.show_heads()

    def get_ui_kwargs(self):
        typ = types[self.type.checkedId()]
        r = self.falloff_radius.value()
        xs = [x for x, y in self.bezier.points]
        ys = [1 - y for x, y in self.bezier.points]
        return typ, xs, ys, r

    def paint_weight(self):
        typ, xs, ys, r = self.get_ui_kwargs()
        self.controller.paint(typ, xs, ys, r)

    def real_paint_weight(self):
        if self.real_mode.isChecked():
            typ, xs, ys, r = self.get_ui_kwargs()
            self.controller.solve(typ, xs, ys, r)

    def show_split_help(self):
        QtWidgets.QMessageBox.information(self, "帮助", "拆分权重工具\n\n"
                                                      "前往b站观看使用视频 \n")



class PYSplitWeightLayout(PyouPersistentWindow):

    WEBS = "https://www.bilibili.com/video/BV1TDCUBRE53/?share_source=copy_web&vd_source=7b50d73ef3e3d9c8d5f26b106034eb71"

    def __init__(self, parent=None):
        super(PYSplitWeightLayout, self).__init__("PYSplitWeightLayout", "PYSplitWeightDialog", parent)
        self.ng2_enable = False
        self.degree_enable = False
        if MAYA_VISON >= 2022:
            self.degree_enable = True
            self.ng2_enable = True

        self.setWindowTitle("Split SkinWeight")
        self.resize(320, 520)
        self.init_ui(True)
        self.loadWindowSettings()


    def init_ui(self, copyright=False):
        main = QtWidgets.QVBoxLayout(self)
        main.setContentsMargins(4, 4, 4, 4)
        main.setSpacing(4)
        main.addWidget(PY_WIDGEST.create_title("Split SkinWeight", 15, self.WEBS))
        main.addWidget(self.build_tabs(), 1)

        if copyright:
            PY_WIDGEST.create_copyrightText(main, "2025-2026")

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocus()
        self.create_connection()
        return main

    def build_tabs(self):

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabPosition(QtWidgets.QTabWidget.West)
        # self.tabs.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabs.setMovable(False)
        self.tabs.setUsesScrollButtons(False)
        self.soft_widget = PYSoftWeight_Manager()
        self.tabs.addTab(self.split_skin_lay(), "de boor")
        self.tabs.addTab(self.soft_widget.setup_ui(), "soft")

        return self.tabs


    def split_skin_lay(self):
        container_main = QtWidgets.QWidget()
        container_main.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        main_layout = QtWidgets.QVBoxLayout(container_main)

        layout1, self.geo_filed, self.geo_btn = PY_WIDGEST.create_QLineEdit_row("Geometry:" )
        layout2, self.mask_filed, self.mask_btn = PY_WIDGEST.create_QLineEdit_row("Joint/Lay:")

        split_type_layout = QtWidgets.QHBoxLayout()
        self.split_mask_block = PY_WIDGEST.create_radiogroup(
            "",
            [
                ("Weight Mask", 1, None),
                ("ng2 Layer", 2, "ng2 层"),
            ],
            default_id=1,
            enabled_map={2: self.ng2_enable}
        )
        self.hit_text = PY_WIDGEST.create_text(u">拆分刷好的骨骼权重")

        split_type_layout.addWidget(self.split_mask_block)
        split_type_layout.addWidget(self.hit_text)

        self.type_block = PY_WIDGEST.create_radiogroup(
            "Type:",
            [
                ("Linear", 1, u"线形"),
                ("Circular", 2, u"环形")
            ],
            default_id=1
        )
        self.degree_container = QtWidgets.QWidget()
        degree_layout = QtWidgets.QHBoxLayout(self.degree_container)
        self.split_degree_block = PY_WIDGEST.create_radiogroup(
            "degree:",
            [
                ("1", 1, None),
                ("2", 2, None),
                ("3", 3, None),
            ],
            default_id=3
        )
        self.degree_container.setEnabled(self.degree_enable)

        btn_layout, self.split_btn, self.split_help_btn = PY_WIDGEST.create_Qbuttons(" Apply ")

        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)
        main_layout.addLayout(split_type_layout)
        PY_WIDGEST.separator(main_layout, True)
        main_layout.addWidget(PY_WIDGEST.create_text(u"Load joints in sequence 按顺序载入关节"))

        main_layout.addLayout(self.listWidget_layout())
        main_layout.addWidget(self.type_block)

        degree_layout.addWidget(self.split_degree_block)
        main_layout.addWidget(self.degree_container)
        PY_WIDGEST.separator(main_layout, True)
        main_layout.addLayout(btn_layout)
        self.split_help_btn.clicked.connect(lambda: dispatcher.execute("Show Help", 19))
        return container_main


    def listWidget_layout(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setSpacing(0)

        list_header = QtWidgets.QWidget()
        list_header_layout = QtWidgets.QHBoxLayout(list_header)
        list_header_layout.setContentsMargins(0, 0, 0, 0)
        list_label = QtWidgets.QLabel("split joints:")
        self.joints_num_label = QtWidgets.QLabel("0")
        list_label.setAlignment(QtCore.Qt.AlignCenter)
        list_header_layout.addWidget(list_label)
        # list_header_layout.addStretch()
        list_header_layout.addWidget(self.joints_num_label)

        horizontal_container = QtWidgets.QWidget()
        horizontal_layout = QtWidgets.QHBoxLayout(horizontal_container)
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout.setSpacing(8)

        self.split_joints_list = QtWidgets.QListWidget()
        self.split_joints_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        horizontal_layout.addWidget(self.split_joints_list, 1)

        right_btn_widget = QtWidgets.QWidget()
        right_btn_layout = QtWidgets.QVBoxLayout(right_btn_widget)
        right_btn_layout.setContentsMargins(0, 0, 0, 0)
        right_btn_layout.setSpacing(0)

        load_btn = QtWidgets.QPushButton("load")
        load_btn.setProperty("green", True)
        load_btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        right_btn_layout.addWidget(load_btn)
        horizontal_layout.addWidget(right_btn_widget)

        list_vertical_layout = QtWidgets.QVBoxLayout()
        list_vertical_layout.addWidget(list_header)
        list_vertical_layout.addWidget(horizontal_container)

        main_layout.addLayout(list_vertical_layout)
        load_btn.clicked.connect(lambda: _obj.load_list_widget_items(self.split_joints_list, True))
        self.split_joints_list.itemSelectionChanged.connect(lambda: _obj.list_widget_seleted_item(self.split_joints_list))
        return main_layout


    def create_connection(self):
        self.geo_btn.clicked.connect(
            lambda: SelectionLoader.load_lineedit(
                self,
                self.geo_filed,
                "mesh"
            )
        )
        self.mask_btn.clicked.connect(
            lambda: SelectionLoader.load_lineedit(
                self,
                self.mask_filed,
                "joint"
            )
        )
        self.split_mask_block.idClicked.connect(self._on_mask_type_toggled)
        self.split_btn.clicked.connect(self.split_weight)


    def _on_mask_type_toggled(self, btn_id):

        maps = {1: u"> 拆分刷好的骨骼权重", 2: u"> 拆分ng2 mask"}
        self.hit_text.setText(maps[btn_id])

        if btn_id == 1:
            self.mask_btn.setEnabled(True)
            self.degree_container.setEnabled(self.degree_enable)
            self.split_help_btn.clicked.connect(lambda: dispatcher.execute("Show Help", 19))
        else:
            self.mask_btn.setEnabled(False)
            self.degree_container.setEnabled(True)
            self.split_help_btn.clicked.connect(lambda: dispatcher.execute("Show Help", 20))


    def _attr_block_toggled(self, btn_id):
        if btn_id == 1:
            self.add_attr_hit.setText(u"Enum first is the attribute name, then the internal object name\nEnum: 第一个名称是属性名，然后开个后全部是内部对象名")
        else:
            self.add_attr_hit.setText(u"\n批量写入多个属性,属性名称用空格分开")
            # self.add_attr_hit.setVisible(False)
        if btn_id == 2 or btn_id == 3:
            self._attr_value_page.setEnabled(True)
        else:
            self._attr_value_page.setEnabled(False)


    def split_weight(self):
        from JointEdit import split_skin_weight
        geo_filed = self.geo_filed.text()
        mask_filed = self.mask_filed.text()
        split_joints_list = _obj.get_list_widget_items(self.split_joints_list)
        v, info = split_skin_weight.split_weight(mesh=geo_filed, mask_joint_layer=mask_filed, mask_type=self.split_mask_block.checkedId(), split_joints=split_joints_list, Type=self.type_block.checkedId(), degree=self.split_degree_block.checkedId())

        if v == True:
            mayaPrint.log(info)
        else:
            mayaPrint.warning(info)
            return
        Help.end_popDialog()

def main():

    global py_splitWeight_dialog
    try:
        py_splitWeight_dialog.close()  # pylint: disable=E0601
        py_splitWeight_dialog.deleteLater()
    except:
        pass

    py_splitWeight_dialog = PYSplitWeightLayout()
    py_splitWeight_dialog.show()

if __name__ == '__main__':

    main()
