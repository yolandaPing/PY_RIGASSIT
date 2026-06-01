# -*- coding: utf-8 -*-

# .FileName:general_mod.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/15 21:59
# .Finish time:
from functools import partial
from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets
from py_rigAssit.dialogs import base_dir, Help, decorator, mayaPrint
from ui_framework.widgets.button import GridButtons
from ControllerTool.Addattr import AddattrFunc
from GeneralTools import split_blendshape_target as split_blendshape_target
from py_rigAssit.common.command_dispatcher import CommandDispatcher
# import py_rigAssit.common.commands,img_commands
import maya.cmds as cmds, maya.mel as mel

py_widgets = Widgets()
AddAttr = AddattrFunc()


class PYQDoubleSpinBox(QtWidgets.QDoubleSpinBox):
    def __init__(self, value_=0.0, min_=-999999, max_=999999, decimals=2):
        super(PYQDoubleSpinBox, self).__init__()
        self.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.setRange(min_, max_)
        self.setDecimals(decimals)
        self.setValue(value_)


class PYBoxLimitInformation(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(PYBoxLimitInformation, self).__init__(parent)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(2, 2, 2, 2)
        self.main_layout.setSpacing(2)

        self.ctrl_map = {}

        self._build()

    def _build(self):
        self._build_group("Translate", "t", -1, 1)
        self._build_group("Rotate", "r", -45, 45)
        self._build_group("Scale", "s", -1, 1)

    def _build_group(self, title, prefix, dmin, dmax):
        grp = QtWidgets.QGroupBox(title)
        self.main_layout.addWidget(grp)

        vbox = QtWidgets.QVBoxLayout(grp)
        vbox.setContentsMargins(2, 2, 2, 2)

        form = QtWidgets.QFormLayout()
        vbox.addLayout(form)

        for axis in "xyz":
            self._create_row(form, axis, prefix + axis, dmin, dmax)

    def _create_row(self, form, label, attr, dmin, dmax):

        min_spin = PYQDoubleSpinBox(dmin)
        max_spin = PYQDoubleSpinBox(dmax)

        min_chk = QtWidgets.QCheckBox()
        max_chk = QtWidgets.QCheckBox()

        min_spin.setEnabled(False)
        max_spin.setEnabled(False)

        min_chk.stateChanged.connect(min_spin.setEnabled)
        max_chk.stateChanged.connect(max_spin.setEnabled)

        btn = QtWidgets.QPushButton("apply")
        btn.clicked.connect(partial(self.apply, attr))

        row = QtWidgets.QHBoxLayout()
        row.addWidget(min_chk, 6)
        row.addWidget(min_spin, 30)
        row.addWidget(max_spin, 30)
        row.addWidget(max_chk, 6)
        row.addWidget(QtWidgets.QLabel(""), 4)
        row.addWidget(btn, 20)

        form.addRow(label, row)

        self.ctrl_map[attr] = {
            "min": min_spin,
            "max": max_spin,
            "min_chk": min_chk,
            "max_chk": max_chk
        }

    def limitInformation(self, objects, attr, data, enable_flags):
        if not objects:
            return

        for obj in objects:
            try:
                cmds.transformLimits(
                    obj,
                    **{
                        attr: data,
                        "e{}".format(attr): enable_flags
                    }
                )
            except Exception as e:
                mayaPrint.warning("{} failed: {}".format(obj, e))

    def apply(self, attr):
        if attr not in self.ctrl_map:
            return

        ui = self.ctrl_map[attr]

        data = [ui["min"].value(), ui["max"].value()]
        enable = [ui["min_chk"].isChecked(), ui["max_chk"].isChecked()]

        self.limitInformation(cmds.ls(sl=True), attr, data, enable)


class PYGeneralLayout(QtWidgets.QDialog):


    def __init__(self, parent=None):
        super(PYGeneralLayout, self).__init__(parent)

        self.setWindowTitle("General_mod")
        self.resize(420, 720)
        self.dispatcher = CommandDispatcher()
        self.init_ui()


    def init_ui(self):

        main = QtWidgets.QVBoxLayout(self)
        main.setContentsMargins(2, 2, 2, 2)

        main.addWidget(py_widgets.create_title("General Dialog", 15, 30))

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)

        container = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(container)

        scroll.setWidget(container)
        main.addWidget(scroll)

        text_widget = py_widgets.create_text(u"You can see how to use it on the button\n你可以放置在按钮上看如何使用它")
        text_widget.setContentsMargins(0, 0, 0, 0)
        scroll_layout.addWidget(text_widget)
        scroll_layout.addWidget(self.build_tabs())

        scroll_layout.addStretch()
        self.create_connection()

        return main


    def build_tabs(self):
        frame = QtWidgets.QFrame()
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        self.tab_block = py_widgets.create_radiogroup(
            "",
            [
                (" Attribute / Data ", 1, None),
                (" Mesh Module", 2, None),
                (" All Module", 3, None),
            ],
            default_id=1
        )

        layout.addWidget(self.tab_block)
        layout.addWidget(self.build_attribute_tab())
        layout.addWidget(self.build_mesh_tab())

        self.tab_block.idClicked.connect(self._on_general_tab_block_toggled)

        return frame

    def build_attribute_tab(self):

        self.attribute_page = QtWidgets.QWidget()
        lay = QtWidgets.QVBoxLayout(self.attribute_page)
        lay.setSpacing(2)
        lay.setContentsMargins(0, 0, 0, 0)
        sec0 = py_widgets.create_section("Quick")
        node_grid = GridButtons("node_edit", 3)
        global_grid = GridButtons("global_vis", 3)
        node_grid.clicked.connect(self.run_action)
        global_grid.clicked.connect(self.run_action)

        sec1 = py_widgets.create_section("Add Attribute")
        sec2 = py_widgets.create_section("Attribute Edit")
        grid0 = GridButtons("attribute_edit", 3)
        grid0.clicked.connect(self.run_action)

        sec3 = py_widgets.create_section("Data Import/Export")
        data_grid = GridButtons("data_edit", 3)
        data_grid.clicked.connect(self.run_action)

        set_frame = py_widgets.create_collapsible_frame(u"Attribute Display/RotateOrder")

        layout = QtWidgets.QHBoxLayout()
        sec_vlock = py_widgets.create_section("Display and Lock:")
        sec_lh_vis = py_widgets.create_section(" ")
        vlovk_layout = QtWidgets.QVBoxLayout()
        vlovk_layout.setSpacing(8)
        t_layout, self.trans_vis_cb, self.trans_lock_cb = self.create_checkbox_group("T: ", True, False)
        r_layout, self.rotate_vis_cb, self.rotate_lock_cb = self.create_checkbox_group("R: ", True, False)
        s_layout, self.scale_vis_cb, self.scale_lock_cb = self.create_checkbox_group("S: ", True, False)
        v_layout, self.vis_vis_cb, self.vis_lock_cb = self.create_checkbox_group("V: ", True, False)

        btn_layout, self.vlock_apply_btn, vlock_help_btn = py_widgets.create_Qbuttons("Apply")
        vlock_help_btn.clicked.connect(self.show_vlock_help)
        vlovk_layout.addLayout(t_layout)
        vlovk_layout.addLayout(r_layout)
        vlovk_layout.addLayout(s_layout)
        vlovk_layout.addLayout(v_layout)
        vlovk_layout.addLayout(btn_layout)
        sec_vlock.addLayout(vlovk_layout)

        layout_r = QtWidgets.QHBoxLayout(self)
        ord_layout = QtWidgets.QHBoxLayout(self)
        lh_vis_layout, self.lh_vis_apply_btn, lh_vis_help_btn = py_widgets.create_Qbuttons("Lock/Hide Vis")
        self.lh_vis_apply_btn.setToolTip(u"锁定并隐藏场景里所有曲线的visibility")
        self.lh_vis_apply_btn.clicked.connect(lambda: self.dispatcher.execute("Lock/Hide Ctrls Vis"))
        lh_vis_help_btn.clicked.connect(self.show_vis_help)
        self.combo = QtWidgets.QComboBox()
        self.rotate_orders_list = ["xyz", "yzx", "zxy", "xzy", "yxz", "zyx"]
        self.combo.addItems(self.rotate_orders_list)
        self.combo.setMinimumWidth(50)
        self.combo.currentIndexChanged.connect(self.set_rotate_order)

        add_attribute_frame = self.add_attribute_lay()
        edit_attribute_frame = self.edit_attribute_lay()

        ord_layout.addWidget(QtWidgets.QLabel("RotateOrder:"))
        ord_layout.addWidget(self.combo)
        layout_r.addLayout(lh_vis_layout)
        layout_r.addLayout(ord_layout)
        # sec_lh_vis.addLayout(layout_r)
        layout.addWidget(sec_vlock )
        set_frame.addLayout(layout)
        sec0.addWidget(global_grid)
        sec0.addWidget(node_grid)
        sec3.addWidget(data_grid)
        # sec3.addWidget(sec_lh_vis)
        sec1.addWidget(add_attribute_frame)
        sec2.addWidget(grid0)
        sec2.addLayout(layout_r)
        sec2.addWidget(set_frame)
        sec2.addWidget(edit_attribute_frame)
        lay.addWidget(sec0)
        lay.addWidget(sec3)
        lay.addWidget(sec2)
        lay.addWidget(sec1)
        lay.addStretch()
        return self.attribute_page

    def edit_attribute_lay(self):
        frame = py_widgets.create_collapsible_frame(u"LimitInformation 属性限制")
        main_layout = QtWidgets.QVBoxLayout()
        self.limit_ui = PYBoxLimitInformation()

        main_layout.addWidget(self.limit_ui)
        frame.addLayout(main_layout)
        return frame

    def add_attribute_lay(self):
        frame = py_widgets.create_collapsible_frame(u"Add Attribute 添加属性")
        main_layout = QtWidgets.QVBoxLayout()
        cbx_layout = QtWidgets.QVBoxLayout()
        self._attr_value_page = QtWidgets.QWidget()
        value_layout = QtWidgets.QHBoxLayout(self._attr_value_page)
        separator_layout, self.add_separator_name, self.add_separator_btn = py_widgets.create_QLineEdit_row(" ________________: ")
        self.add_separator_btn.setText("  Add  ")
        self.attr_type_block = py_widgets.create_radiogroup(
            title="Type:",
            items=[
                ("Enum", 1, None),
                ("Float ", 2, None),
                ("Int", 3, None),
                ("Bool", 4, None),
                ("String", 5, None)
            ],
            default_id=1
        )

        self.value_cbx = py_widgets.add_checkbox('Min/Max/Default value:')
        self.min_value_field = QtWidgets.QSpinBox()
        self.max_value_field = QtWidgets.QSpinBox()
        self.default_value_field = QtWidgets.QSpinBox()
        self.proxy_cbx = py_widgets.add_checkbox('Is Proxy ?(代理属性不可单独使用)')
        self.add_attr_hit = py_widgets.create_text(u"Enum first is the attribute name, then the internal object name\nEnum: 第一个名称是属性名，然后开个后全部是内部对象名")
        name_layout, self.add_attr_name_field = py_widgets.create_QLineEdit_grp("Attribute Name:")
        btn_layout, self.add_attr_apply_btn, add_attr_help_btn = py_widgets.create_Qbuttons(" Apply ")

        self.attr_type_block.idClicked.connect(self._attr_block_toggled)
        add_attr_help_btn.clicked.connect(lambda: self.dispatcher.execute("Show Help", 15))

        value_layout.addWidget(self.value_cbx)
        value_layout.addWidget(self.min_value_field)
        value_layout.addWidget(self.max_value_field)
        value_layout.addWidget(self.default_value_field)
        cbx_layout.addWidget(self._attr_value_page)
        cbx_layout.addWidget(self.proxy_cbx)
        main_layout.addWidget(py_widgets.create_text("Add separator"))
        main_layout.addLayout(separator_layout)
        py_widgets.separator(main_layout)
        main_layout.addWidget(py_widgets.create_text(u"Write multiple attributes, separated by spaces\n编写多个属性，用空格分隔"))
        main_layout.addWidget(self.attr_type_block)
        main_layout.addLayout(cbx_layout)
        main_layout.addWidget(self.add_attr_hit)
        py_widgets.separator(main_layout, True)
        main_layout.addLayout(name_layout)
        main_layout.addLayout(btn_layout)
        self._attr_value_page.setEnabled(False),self.min_value_field.setEnabled(False),self.max_value_field.setEnabled(False),self.default_value_field.setEnabled(False)
        self.value_cbx.stateChanged.connect(self._on_value_fields)
        frame.addLayout(main_layout)
        return frame

    def build_mesh_tab(self):

        self.page_widget = QtWidgets.QWidget()
        lay = QtWidgets.QVBoxLayout(self.page_widget)
        lay.setSpacing(6)
        lay.setContentsMargins(0, 0, 0, 0)

        sec0 = py_widgets.create_section("Mesh Edit")
        grid0 = GridButtons("mesh_edit", 3)
        grid0.clicked.connect(self.run_action)
        sec0.addWidget(grid0)

        sec1 = py_widgets.create_section("Mesh Data transfer")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(py_widgets.create_text(u" 模型数据导出导入 "))
        btn_layout = QtWidgets.QHBoxLayout()
        uv_cbx = py_widgets.add_checkbox('Export UV?')
        export_mesh_btn = QtWidgets.QPushButton(u'导出选中的模型')
        import_mesh_data_btn = QtWidgets.QPushButton(u'导入数据生成模型')
        mesh_help_btn = QtWidgets.QPushButton()
        mesh_help_btn.setIcon(QtGui.QIcon(":\help.png"))
        export_mesh_btn.setProperty("main", True)
        import_mesh_data_btn.setProperty("main", True)
        mesh_help_btn.setProperty("help", True)

        btn_layout.addWidget(export_mesh_btn, 5)
        btn_layout.addWidget(import_mesh_data_btn, 5)
        btn_layout.addWidget(mesh_help_btn)
        layout.addWidget(uv_cbx)
        layout.addLayout(btn_layout)
        sec1.addLayout(layout)

        lay.addWidget(sec0)
        lay.addWidget(sec1)
        lay.addWidget(self.split_target_lay())
        lay.addStretch()
        export_mesh_btn.clicked.connect(lambda: self.dispatcher.execute("Export Mesh Data", uv_cbx.isChecked()))
        import_mesh_data_btn.clicked.connect(lambda: self.dispatcher.execute("Import Mesh Data"))
        self.page_widget.setVisible(False)
        return self.page_widget


    def split_target_lay(self):
        sec0 = py_widgets.create_section("Split blendShape Target")
        main_layout = QtWidgets.QVBoxLayout()
        sec0.addLayout(main_layout)
        main_layout.addWidget(py_widgets.create_text(u" 拆分blendShape目标体 "))
        base_layout, self.base_shape_field, self.assign_base_btn = py_widgets.create_QLineEdit_row("Shape:")
        blend_layout, self.dest_blsp_field, self.assign_dest_btn = py_widgets.create_QLineEdit_row("BlendShape:")
        self.assign_base_btn.clicked.connect(self.assign_base_shape)
        self.assign_dest_btn.clicked.connect(self.assign_dest_blendshape)
        main_layout.addLayout(base_layout)
        main_layout.addLayout(blend_layout)

        layout3, self.split_name_field = py_widgets.create_QLineEdit_grp("Split Name:")
        form_layout = QtWidgets.QFormLayout()
        self.divisions_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.divisions_slider.setMinimum(2)
        self.divisions_slider.setMaximum(20)
        self.divisions_slider.setValue(2)
        self.divisions_slider.valueChanged.connect(self.update_division_label)
        self.division_label = QtWidgets.QLabel("2")
        div_layout = QtWidgets.QHBoxLayout()
        div_layout.addWidget(self.divisions_slider)
        div_layout.addWidget(self.division_label)
        form_layout.addRow("Number Divisions:", div_layout)
        main_layout.addLayout(layout3)
        main_layout.addLayout(form_layout)
        py_widgets.separator(main_layout)

        group = QtWidgets.QGroupBox(u"Add Ctrl:")
        layout = QtWidgets.QVBoxLayout(group)
        ctrl_layout = QtWidgets.QHBoxLayout()
        self.create_ctrl_cb = QtWidgets.QCheckBox("Add Controller ?")
        self.create_ctrl_cb.toggled.connect(self.on_create_ctrl_toggled)
        ctrl_layout.addWidget(self.create_ctrl_cb)

        self.controller_type_group = QtWidgets.QButtonGroup(self)
        self.radio_slider = QtWidgets.QRadioButton("Sliders")
        self.radio_circle = QtWidgets.QRadioButton("Circles")
        self.radio_slider.setChecked(True)
        self.radio_slider.setEnabled(False)
        self.radio_circle.setEnabled(False)
        self.controller_type_group.addButton(self.radio_slider)
        self.controller_type_group.addButton(self.radio_circle)
        ctrl_layout.addWidget(self.radio_slider)
        ctrl_layout.addWidget(self.radio_circle)
        layout.addLayout(ctrl_layout)

        self.pos_dir_cb = QtWidgets.QCheckBox("Positive Direction")
        self.pos_dir_cb.setChecked(True)
        self.pos_dir_cb.setEnabled(False)
        layout.addWidget(self.pos_dir_cb)
        main_layout.addWidget(group)

        # 按钮行
        btn_layout = QtWidgets.QHBoxLayout()
        create_plane_btn = QtWidgets.QPushButton("Create Plane")
        create_plane_btn.clicked.connect(self.create_plane_btn_cmd)
        make_blsp_btn = QtWidgets.QPushButton("Make blendshapes")
        make_blsp_btn.clicked.connect(self.make_blsp_btn_cmd)
        help_btn = QtWidgets.QPushButton()
        help_btn.setIcon(QtGui.QIcon(":\help.png"))
        create_plane_btn.setProperty("main", True)
        make_blsp_btn.setProperty("main", True)
        help_btn.setProperty("help", True)
        help_btn.clicked.connect(self.show_split_help)
        btn_layout.addWidget(create_plane_btn, 1)
        btn_layout.addWidget(make_blsp_btn, 1)
        btn_layout.addWidget(help_btn)
        main_layout.addLayout(btn_layout)
        return sec0

    def create_checkbox_group(self, label_text, vis_checked=True, lock_checked=False):
        label = QtWidgets.QLabel(label_text)
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)  # 右对齐垂直居中
        label.setFixedWidth(80)

        vis_cb = QtWidgets.QCheckBox("vis")
        lock_cb = QtWidgets.QCheckBox("lock")
        vis_cb.setChecked(vis_checked)
        lock_cb.setChecked(lock_checked)

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(label)
        h_layout.addWidget(vis_cb)
        h_layout.addWidget(lock_cb)
        h_layout.addStretch()  # 使复选框靠右
        return h_layout, vis_cb, lock_cb


    def create_connection(self):
        self.add_separator_btn.clicked.connect(self.create_separator)
        self.add_attr_apply_btn.clicked.connect(self.create_attr)
        self.vlock_apply_btn.clicked.connect(self.apply_attr_vis_lock)


    def _on_general_tab_block_toggled(self, btn_id):

        if btn_id == 1:
            self.attribute_page.show()
            self.page_widget.hide()

        elif btn_id == 2:
            self.attribute_page.hide()
            self.page_widget.show()
        else:
            self.attribute_page.show()
            self.page_widget.show()


    def _on_value_fields(self, enabled):
        self.min_value_field.setEnabled(enabled), self.max_value_field.setEnabled(
            enabled), self.default_value_field.setEnabled(enabled)


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
            
    
    def update_division_label(self, value):
        self.division_label.setText(str(value))

    def on_create_ctrl_toggled(self, checked):
        self.radio_slider.setEnabled(checked)
        self.radio_circle.setEnabled(checked)
        self.pos_dir_cb.setEnabled(checked)

    def assign_base_shape(self):
        sel = cmds.ls(sl=True)
        if sel:
            try:
                shape = cmds.listRelatives(sel[0], s=True)[0]
                self.base_shape_field.setText(shape)
            except:
                mayaPrint.warning("Please select a mesh or nurbs surface.")
        else:
            mayaPrint.warning("Nothing selected.")

    def assign_dest_blendshape(self):
        sel = cmds.ls(sl=True)
        if sel and cmds.objectType(sel[0], i="blendShape"):
            self.dest_blsp_field.setText(sel[0])
        else:
            mayaPrint.error("Please select a blendShape node.")


    def show_vlock_help(self):
        QtWidgets.QMessageBox.information(self, "帮助", "Diaplay\n\n"
                                                      "Translate, Rotate, Scale, Visibility属性显示和隐藏\n")

    def show_vis_help(self):
        QtWidgets.QMessageBox.information(self, "帮助", "Lock/Hide Vis\n\n"
                                                      "锁定并隐藏创建里所有控制器的visibility\n")

    def show_split_help(self):
        QtWidgets.QMessageBox.information(self, "帮助", "拆分BlendShape目标工具\n\n"
                                                      "1. 选择模型载入Shape\n"
                                                      "2. 选择blendShape载入, 且将拆分的目标weight设置1\n"
                                                      "3. 写入拆分后对象名称\n"
                                                      "4. 设置拆分的数量\n"
                                                      "5. 点击“Create Plane”生成分割平面(自行调整plane位置)\n"
                                                      "6. 点击“Make blendShape”创建分割目标和控制器\n")



    def run_action(self, text):
        print("Run:", text)
        if hasattr(self, "dispatcher"):
            self.dispatcher.execute(text)


    def create_separator(self):
        name = self.add_separator_name.text()
        self.dispatcher.execute("create separator", name)


    def create_attr(self):
        attr_id = self.attr_type_block.checkedId()
        names_str = self.add_attr_name_field.text()
        if self.value_cbx.isChecked():
            min_value = self.min_value_field.value()
            max_value = self.max_value_field.value()
            def_value = self.default_value_field.value()
        else:
            min_value,max_value,def_value = 0,0,0

        proxy = self.proxy_cbx.isChecked()

        datas = {
            "attr_id": attr_id,
            "names_str": names_str,
            "min_value": min_value,
            "max_value": max_value,
            "def_value": def_value,
            "proxy": proxy,
        }
        self.dispatcher.execute("create attrs", datas)


    def apply_attr_vis_lock(self):
        t_key = self.trans_vis_cb.isChecked()
        t_lock = self.trans_lock_cb.isChecked()
        r_key = self.rotate_vis_cb.isChecked()
        r_lock = self.rotate_lock_cb.isChecked()
        s_key = self.scale_vis_cb.isChecked()
        s_lock = self.scale_lock_cb.isChecked()
        v_key = self.vis_vis_cb.isChecked()
        v_lock = self.vis_lock_cb.isChecked()

        datas = {
            "t_info": [t_key, t_lock],
            "r_info": [r_key, r_lock],
            "s_info": [s_key, s_lock],
            "v_info": [v_key, v_lock],
        }
        self.dispatcher.execute("apply attr vis lock", datas)


    def set_rotate_order(self, index):
        sel = cmds.ls(sl=True)
        if not sel:
            mayaPrint.error("Select object first")
            return

        cmds.undoInfo(openChunk=True)
        try:
            for obj in sel:
                if cmds.attributeQuery("rotateOrder", node=obj, exists=True):
                    cmds.setAttr("{}.rotateOrder".format(obj), index)
        finally:
            cmds.undoInfo(closeChunk=True)
        
    def get_ui_values(self):
        return (
            self.divisions_slider.value(),
            self.create_ctrl_cb.isChecked(),
            "Slider" if self.radio_slider.isChecked() else "Circle",
            self.name_base_field.text(),
            True,
            self.base_shape_field.text(),
            self.dest_blsp_field.text(),
            self.pos_dir_cb.isChecked()
        )

    def print_info(self):
        divisions, create_ctrl, ctrl_type, name_base, specify_base, base_shape, dest_blsp, pos_dir = self.get_ui_values()
        print("="*60)
        print("Number of Division is:", divisions)
        print("Should create controller:", create_ctrl)
        print("Controller type:", ctrl_type)
        print("Name base:", name_base)
        print("Should Specify BaseShape:", specify_base)
        print("BaseShape:", base_shape)
        print("Destination blendShape:", dest_blsp)
        print("Positive Direction:", pos_dir)


    def create_plane_btn_cmd(self):
        divisions, create_ctrl, ctrl_type, name_base, specify_base, base_shape_text, dest_blsp, pos_dir = self.get_ui_values()
        split_blendshape_target.create_plane_btn_cmd(divisions, specify_base, base_shape_text)


    def make_blsp_btn_cmd(self):
        divisions, create_ctrl, ctrl_type, name_base, specify_base, base_shape_text, dest_blsp, pos_dir = self.get_ui_values()
        split_blendshape_target.make_blsp_btn_cmd(divisions, create_ctrl, ctrl_type, name_base, specify_base, base_shape_text, dest_blsp, pos_dir)


