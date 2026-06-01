# -*- coding: utf-8 -*-

# .FileName:ikfk_system_layout.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/11 18:13
# .Finish time:
from functools import partial
from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
from py_rigAssit.dialogs import Help, decorator, mayaPrint
from ControllerTool.ikfk_guide_mod import IKFK_GUIDE
from ControllerTool.ikfk_ribbon_mod import IKFKRIGGING
from ControllerTool.Joint_Chain_IKFK_System import Joint_Chain_Ribbon
from ControllerTool.CurveEdit import CurvesEdit
from py_rigAssit.dialogs.functionality_layout import PYFunctionalityLayout
import user_defined as _AllowUsers
import Utils.Util as _util
from py_rigAssit.common.command_dispatcher import CommandDispatcher
import py_rigAssit.common.img_commands
import Utils.json_info as json_info
import maya.cmds as mc

_widgest = Widgets()
_JOINYS_CHAIN = Joint_Chain_Ribbon()
_RIGGING_MOD = IKFKRIGGING()
_IKFK_GUIDE = IKFK_GUIDE()
_CURVE_EDIT = CurvesEdit()


def _version_info(obj="ikfktool"):
    return json_info.version_info(obj)


class IKFKWidget(QtWidgets.QWidget):

    DNYM_HINT = {
        1: u'select the start joint to make dynamic',
        2: u'select start joint and curve to make dynamic',
        3: u'select the curve to make dynamic'
    }

    def __init__(self, parent=None):
        super(IKFKWidget, self).__init__(parent)

        try:
            self.MotionPath = _AllowUsers.MotionPath_Enable
        except:
            self.MotionPath = False

        self.dispatcher = CommandDispatcher()
        self.joint_aixs = None


    def init_ui(self, tbs=True):
        container = QtWidgets.QWidget()
        container.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        main = QtWidgets.QVBoxLayout(container)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(2)

        if tbs:
            main.addWidget(self.build_tabs(), 1)
            _widgest.create_copyrightText(main, "2024-2026")
        else:
            sec1 = _widgest.create_section("IKFK Rigging")
            sec2 = _widgest.create_section("Functionality Rigging")
            base_ikfk = self.base_ikfk_lay()
            chain_ikfk = self.chain_ikfk_lay()
            ribbon_ikfk = self.ribbon_ikfk_lay()
            functionality_lay = PYFunctionalityLayout(parent=self)
            sec1.addWidget(base_ikfk)
            sec1.addWidget(chain_ikfk)
            sec1.addWidget(ribbon_ikfk)
            sec2.addWidget(functionality_lay.init_ui())
            main.addWidget(sec1)
            main.addWidget(sec2)
        main.addStretch()
        self.create_connection()

        return container

    def build_tabs(self):

        self.tabs = QtWidgets.QTabWidget()
        pag1 = QtWidgets.QWidget()
        pag2 = QtWidgets.QWidget()
        lay1 = QtWidgets.QVBoxLayout(pag1)
        lay2 = QtWidgets.QVBoxLayout(pag2)
        base_ikfk = self.base_ikfk_lay()
        chain_ikfk = self.chain_ikfk_lay()
        ribbon_ikfk = self.ribbon_ikfk_lay()
        functionality_lay = PYFunctionalityLayout(parent=self)
        lay1.addWidget(base_ikfk)
        lay1.addWidget(chain_ikfk)
        lay1.addWidget(ribbon_ikfk)
        lay2.addWidget(functionality_lay.init_ui())
        self.tabs.addTab(pag1, "IKFK")
        self.tabs.addTab(pag2, "Functionality")
        lay1.addStretch()
        lay2.addStretch()
        return self.tabs

    def base_ikfk_lay(self):
        frame = _widgest.create_collapsible_frame("Add Base IKFK")
        group = QtWidgets.QGroupBox(u"base:")
        main_layout = QtWidgets.QVBoxLayout(group)
        scale_layout = QtWidgets.QHBoxLayout()

        self.ctrl_scale_slider = _widgest.create_floatSlider()
        self.ctrl_scale_slider.setValue(0.25)
        self.ctrl_scale_slider.setMinimumWidth(120)
        scale_layout.addWidget(QtWidgets.QLabel("Size:"))
        scale_layout.addWidget(self.ctrl_scale_slider)

        self.ctrl_type_block = _widgest.create_radiogroup(
            "Crtl:",
            [
                ("IK ", 1, None),
                ("FK ", 2, None),
                ("FKIK ", 3, None),
            ],
            default_id=1
        )
        self.cons_block = _widgest.create_radiogroup(
            "Constrain:",
            [
                ("None ", 1, None),
                ("Parent ", 2, None),
                ("Constrain ", 3, None),
            ],
            default_id=1
        )

        checkbox_layout = QtWidgets.QHBoxLayout()
        self.add_pri_cbx = QtWidgets.QCheckBox(' add sec/pri grp')
        self.hierachy_cbx = QtWidgets.QCheckBox(' Hierachy')
        checkbox_layout.addWidget(self.add_pri_cbx)
        checkbox_layout.addWidget(self.hierachy_cbx)

        btn_layout, self.base_apply_btn, self.base_help_btn = _widgest.create_Qbuttons(" Apply ")
        main_layout.addWidget(_widgest.create_text(u" Create a controller based on the selected object 基于选定对象创建控制器"))
        main_layout.addLayout(scale_layout)
        main_layout.addWidget(self.ctrl_type_block)
        main_layout.addWidget(self.cons_block)
        main_layout.addLayout(checkbox_layout)

        _widgest.separator(main_layout, True)
        main_layout.addLayout(btn_layout)
        frame.addWidget(group)
        return frame

    def chain_ikfk_lay(self):
        frame = _widgest.create_collapsible_frame("Joints Chain Quick Rigging")
        main_layout = _widgest.create_section("ribbon")

        checkbox_layout, self.chain_pri_ik_cbx, self.chain_over_cbx, self.chain_over_ik_field, = self.add_ik_box()
        self.chain_splineikrig_cbx = _widgest.add_checkbox('add splineik rig?')
        btn_layout = QtWidgets.QHBoxLayout()

        self.chain_builda_btn = QtWidgets.QPushButton('Build A')
        self.chain_buildb_btn = QtWidgets.QPushButton('Build B')
        self.chain_help_btn = QtWidgets.QPushButton()
        self.chain_help_btn.setIcon(QtGui.QIcon(":\help.png"))
        self.chain_builda_btn.setProperty("main", True)
        self.chain_buildb_btn.setProperty("main", True)
        self.chain_help_btn.setProperty("help", True)

        btn_layout.addWidget(self.chain_builda_btn, 5)
        btn_layout.addWidget(self.chain_buildb_btn, 5)
        btn_layout.addWidget(self.chain_help_btn)

        self.chain_constrain_type = _widgest.create_radiogroup(
            "Constrain:",
            [
                ("Parent ", 1, None),
                ("Constraint ", 2, None),
            ],
            default_id=1
        )


        main_layout.addWidget(
            _widgest.create_text(u"关节名称后缀: _jnt/_bind/_joint"))
        main_layout.addWidget(
            _widgest.create_text(u"确定好关节轴向\n选择关节链的第一节Build"))

        _widgest.separator(main_layout, True)
        main_layout.addLayout(checkbox_layout)
        main_layout.addWidget(self.chain_splineikrig_cbx )
        main_layout.addWidget(self.chain_constrain_type)
        main_layout.addWidget(_widgest.create_text(u" >>> 如果关节不是直的，请选择build B"))

        _widgest.separator(main_layout, True)
        main_layout.addLayout(btn_layout)
        frame.addWidget(main_layout)
        return frame

    def ribbon_ikfk_lay(self):
        frame = _widgest.create_collapsible_frame("Ribbon IKFK System")
        group = QtWidgets.QGroupBox(u"guide:")
        main_layout = QtWidgets.QVBoxLayout(group)
        name_layout, self.name_field = _widgest.create_QLineEdit_grp("Name:")

        self.rig_type_block = _widgest.create_radiogroup(
            "Rig Type:",
            [
                ("Default ", 1, None),
                ("Spline ik ", 2, None),
                ("Motion Path ", 3, None),
            ],
            default_id=1,
            enabled_map = { 3: self.MotionPath}
        )
        # Axis 选择
        self.axis_menu = QtWidgets.QComboBox()
        self.axis_menu.addItems(['1,0,0', '0,1,0', '0,0,1', '-1,0,0', '0,-1,0', '0,0,-1'])
        self.axis_menu.setFixedWidth(120)  # 设置宽度为 120
        self.axis_menu.currentTextChanged.connect(self.get_menu_item)
        axis_layout = QtWidgets.QFormLayout()
        axis_layout.addRow('Axis:', self.axis_menu)


        self.constrain_type_block = _widgest.create_radiogroup(
            "Constrain:",
            [
                ("Parent ", 1, None),
                ("Constraint ", 2, None),
            ],
            default_id=1
        )

        btn_layout = QtWidgets.QHBoxLayout()

        self.guide_btn = QtWidgets.QPushButton('Create Guide')
        self.build_btn = QtWidgets.QPushButton('Build')
        self.adv_help_btn = QtWidgets.QPushButton()
        self.adv_help_btn.setIcon(QtGui.QIcon(":\help.png"))
        self.guide_btn.setProperty("main", True)
        self.build_btn.setProperty("main", True)
        self.adv_help_btn.setProperty("help", True)

        btn_layout.addWidget(self.guide_btn, 5)
        btn_layout.addWidget(self.build_btn, 5)
        btn_layout.addWidget(self.adv_help_btn)

        main_layout.addLayout(name_layout)
        _widgest.separator(main_layout)
        self.ikfk_count_lay(main_layout)

        main_layout.addWidget(self.rig_type_block)
        _widgest.separator(main_layout)
        main_layout.addLayout(axis_layout)

        main_layout.addWidget(self.constrain_type_block)

        _widgest.separator(main_layout)
        main_layout.addLayout(btn_layout)

        frame.addWidget(group)
        return frame

    def ikfk_count_lay(self, parent):
        main_layout = QtWidgets.QVBoxLayout()
        ik_field_layout_main = QtWidgets.QHBoxLayout()

        self.ik_field = QtWidgets.QSpinBox()
        self.ik_field.setValue(7)
        self.ik_field.setFixedWidth(80)
        ik_field_layout = QtWidgets.QFormLayout()

        label = _widgest.create_bold_label('IK / Joint : ')
        ik_field_layout.addRow(label, self.ik_field)

        self.ik_count_label = _widgest.create_text(u" > 设置 ik 的数量: 2n+1 ")

        ik_field_layout_main.addLayout(ik_field_layout)
        ik_field_layout_main.addWidget(self.ik_count_label)

        fk_field_layout_main = QtWidgets.QHBoxLayout()

        self.fk_field = QtWidgets.QSpinBox()
        self.fk_field.setValue(1)
        self.fk_field.setFixedWidth(75)

        fk_field_layout = QtWidgets.QFormLayout()
        label = _widgest.create_text('FK Interval: ')
        fk_field_layout.addRow(label, self.fk_field)

        label = _widgest.create_text(u" > 设置间隔多少个ik生成一个fk， 默认间隔一个 ", 12, "left")

        fk_field_layout_main.addLayout(fk_field_layout)
        main_layout.addLayout(ik_field_layout_main)
        main_layout.addWidget(label)
        main_layout.addLayout(fk_field_layout_main)

        checkbox_layout,  self.enable_pri_ik_cbx, self.enable_over_cbx, self.over_ik_field, = self.add_ik_box()

        main_layout.addLayout(checkbox_layout)
        parent.addLayout(main_layout)


    def add_ik_box(self):
        checkbox_layout = QtWidgets.QHBoxLayout()
        pri_ik_cbx = _widgest.add_checkbox('Enable pri IK ?')
        over_cbx = _widgest.add_checkbox('Enable over IK ?')

        over_ik_field = QtWidgets.QSpinBox()
        over_ik_field.setValue(2)
        over_ik_field.setFixedWidth(80)

        ik_count_layout = QtWidgets.QFormLayout()
        label = _widgest.create_text('Over IK : ')
        ik_count_layout.addRow(label, over_ik_field)
        over_ik_field.setEnabled(False)

        checkbox_layout.addWidget(pri_ik_cbx)
        checkbox_layout.addWidget(over_cbx)
        checkbox_layout.addLayout(ik_count_layout)

        return checkbox_layout, pri_ik_cbx, over_cbx, over_ik_field

    def create_connection(self):
        dispatcher = CommandDispatcher()

        self.base_apply_btn.clicked.connect(self.basa_build)
        self.fk_field.valueChanged.connect(self._calculate_number_ik)
        self.enable_over_cbx.stateChanged.connect(self._on_over_ik_Toggled)
        self.chain_over_cbx.stateChanged.connect(self._chain_over_ik_Toggled)
        self.chain_builda_btn.clicked.connect(self.chain_build)
        self.chain_buildb_btn.clicked.connect(partial(self.chain_build, True))
        self.guide_btn.clicked.connect(self.create_guide)
        self.build_btn.clicked.connect(self.build_system)
        self.base_help_btn.clicked.connect(partial(self._show_img, 1))
        self.chain_help_btn.clicked.connect(partial(self._show_img, 2))
        self.adv_help_btn.clicked.connect(partial(self._show_img, 3))

    def _calculate_number_ik(self):
        num = self.fk_field.value()
        # print(num)
        if num == 0:
            self.ik_count_label.setText(u"无需计算")
        else:
            self.ik_count_label.setText(u" > 设置 ik 的数量: {}n+1 ".format(num + 1))

    def _chain_over_ik_Toggled(self, enabled):
        # print(enabled)
        self.chain_over_ik_field.setEnabled(enabled)

    def _on_over_ik_Toggled(self, enabled):
        # print(enabled)
        self.over_ik_field.setEnabled(enabled)

    def get_menu_item(self, item):
        return item

    def _show_img(self, id, *args):
        self.dispatcher.execute("Show Help", id)

    def get_adv_values(self):
        """获取界面上的所有设置值"""
        filed_name = self.name_field.text()
        ik_value = self.ik_field.value()
        fk_value = self.fk_field.value()
        pri_ik_en = self.enable_pri_ik_cbx.isChecked()
        over_ik_en = self.enable_over_cbx.isChecked()
        over_ik_value = self.over_ik_field.value() if over_ik_en else 0
        axis_text = self.axis_menu.currentText()
        axis_map = {
            '1,0,0': (1, 0, 0),
            '0,1,0': (0, 1, 0),
            '0,0,1': (0, 0, 1),
            '-1,0,0': (-1, 0, 0),
            '0,-1,0': (0, -1, 0),
            '0,0,-1': (0, 0, -1)
        }
        axis_value = axis_map[axis_text]
        # 获取 spineik type
        selected = self.rig_type_block.checkedId()
        if selected == 1:
            spinkrig = 0
        elif selected == 2:
            spinkrig = 2
        elif selected == 3:
            spinkrig = 3
        else:
            spinkrig = 0

        return filed_name, ik_value, fk_value, pri_ik_en, over_ik_value, axis_value, spinkrig, self.constrain_type_block.checkedId()


    def basa_build(self):
        objs = mc.ls(sl=True)
        if objs:
            _CURVE_EDIT.create_base_ctrls(objs,self.cons_block.checkedId(),self.ctrl_type_block.checkedId(),self.ctrl_scale_slider.value()+1.0, bool(self.add_pri_cbx.isChecked()), self.hierachy_cbx.isChecked())
        return


    def chain_build(self, crooked=False):
        pri_ik_en = self.chain_pri_ik_cbx.isChecked()
        over_ik_en = self.chain_over_cbx.isChecked()
        over_ik_value = self.chain_over_ik_field.value() if over_ik_en else 0
        add_spineik = self.chain_splineikrig_cbx.isChecked()
        rigType = self.chain_constrain_type.checkedId()

        if crooked:
            _RIGGING_MOD.crooked_joints_chain_rigging_build(pri_ik_en, over_ik_en, add_spineik, over_ik_value, rigType=rigType - 1)
        else:
            _RIGGING_MOD.joints_chain_rigging_build(pri_ik_en, over_ik_en, add_spineik, over_ik_value, rigType=rigType - 1)


    def create_guide(self):
        """创建引导定位器"""
        filed_name, ik_value, fk_value, pri_ik_en, over_ik_value, axis_value, add_spineik, rigType = self.get_adv_values()
        if not filed_name:
            mayaPrint.error("请给予一个名称!!!")
            return
        print("ikfk system guide info:------------------------------")
        print("Name: {}".format(filed_name))
        print("IK Value: {}".format(ik_value))
        print("FK Value: {}".format(fk_value))
        print("Over IK Value: {}".format(over_ik_value))
        print("Aim Axis: {}".format(axis_value))
        print("Joints Rig Type: {}".format(rigType))
        self.joint_aixs = _IKFK_GUIDE.create_guide_system(filed_name, ik_value, fk_value, over_ik_value, axis_value)

    def is_aixsExists(self, filed_name):
        """检查引导轴是否存在"""
        if not self.joint_aixs:
            self.joint_aixs = mc.ls("{}_*_generate_aixs".format(filed_name))
            if not self.joint_aixs:
                mayaPrint.error("not found {}_*_generate_aixs".format(filed_name))
                return False
            return True
        elif self.joint_aixs and not mc.objExists(self.joint_aixs[0]):
            self.joint_aixs = mc.ls("{}_*_generate_aixs".format(filed_name))
            if not self.joint_aixs:
                mayaPrint.error("not found {}_*_generate_aixs".format(filed_name))
                return False
            return True
        elif self.joint_aixs and self.joint_aixs != mc.ls("{}_*_generate_aixs".format(filed_name)):
            self.joint_aixs = mc.ls("{}_*_generate_aixs".format(filed_name))
            if not self.joint_aixs:
                mayaPrint.error("not found {}_*_generate_aixs".format(filed_name))
                return False
            return True
        else:
            return True


    def build_system(self):
        """构建IKFK系统"""
        filed_name, ik_value, fk_value, pri_ik_en, over_ik_value, axis_value, add_spineik, rigType = self.get_adv_values()
        if not filed_name:
            mayaPrint.error(u"请给予一个名称!!!")
            return
        if self.is_aixsExists(filed_name):
            trans_locs = [i.replace("_aixs", "_guide") for i in self.joint_aixs]
            if _util.is_aixsCrooked(objects=trans_locs, aim_vector=axis_value):
                _RIGGING_MOD.crooked_complex_rigging_build(filed_name, self.joint_aixs, fk_value, pri_ik_en,
                                                           over_ik_value, spineik=add_spineik, rigType=rigType - 1)
            else:
                _RIGGING_MOD.complex_rigging_build(filed_name, self.joint_aixs, fk_value, pri_ik_en,
                                                   over_ik_value, spineik=add_spineik, rigType=rigType - 1)


class PYIKFKLayout(PyouPersistentWindow):

    def __init__(self, parent=None):
        super(PYIKFKLayout, self).__init__("PYIKFKLayoutDlg", "PYIKFKLayoutDlg", parent)

        self.setWindowTitle("IFKF Rigging Dialog")
        self.resize(360, 680)

        self._build_ui()


    def _build_ui(self):
        main = QtWidgets.QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
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

        scroll_layout.addWidget(_widgest.create_title("IFKF Rigging", 15, None))

        self.widget = IKFKWidget(parent=self)

        main.addWidget(self.widget)


def main():

    global py_ikfk_system
    try:
        py_ikfk_system.close()  # pylint: disable=E0601
        py_ikfk_system.deleteLater()
    except:
        pass

    py_ikfk_system = PYIKFKLayout()
    py_ikfk_system.show()

if __name__ == '__main__':

    main()
