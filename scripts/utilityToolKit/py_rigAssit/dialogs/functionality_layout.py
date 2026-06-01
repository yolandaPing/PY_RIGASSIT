# -*- coding: utf-8 -*-

# .FileName:functionality_layout.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/12 1:32
# .Finish time:
from functools import partial
from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets
from py_rigAssit.dialogs import base_dir, decorator, mayaPrint
from py_rigAssit.common.loader import SelectionLoader
from JointEdit.ForwardReverseFKTool import ForwardReverseFKTool
from JointEdit.DynamicCoexist import DynamicCoexistRig
import JointEdit.variable_FK as variable_FK
from JointEdit.JointEditFun import EditJnt
from py_rigAssit.common.command_dispatcher import CommandDispatcher
import py_rigAssit.common.commands
import py_rigAssit.common.img_commands
import maya.cmds as mc, maya.mel as mel

_widgest = Widgets()
reverse_fk = ForwardReverseFKTool()
Dyn = DynamicCoexistRig()
EditJnt = EditJnt()


class PYFunctionalityLayout(QtWidgets.QDialog):

    DNYM_HINT = {1: u'select the start joint to make dynamic 选择要加动力学绑定的起始关节',
                     2: u'select start joint and curve to make dynamic 选择需要添加动力学绑定的开始关节和曲线',
                     3: u'select the curve to make dynamic 选择需要添加动力学的曲线'}

    IKSPLINE_HINT = {1: u'select the joint that needs to be stretched 选择拉伸的关节',
                     2: u'select the joints to be created 选择关节链的初始关节',
                     3: u'Select all joints that need to be linked 选择所有需要链接的关节'}

    def __init__(self, parent=None):
        super(PYFunctionalityLayout, self).__init__(parent)


    def init_ui(self):
        self.dispatcher = CommandDispatcher()

        container = QtWidgets.QWidget()
        main = QtWidgets.QVBoxLayout(container)
        main.setContentsMargins(2, 2, 2, 2)
        main.setSpacing(2)

        rivet_frame = self.rivet_layout()
        ribbon_frame = self.ribbon_animation_layout()
        ikspline_frame = self.ikspline_rigging_layout()
        bidirectional_frame = self.bidirectional_fk_layout()
        dynamic_frame = self.dynamic_rig_layout()
        zipper_frame = self.zipper_rig_layout()
        variable_frame = self.variable_fk_layout()
        main.addWidget(rivet_frame)
        main.addWidget(ribbon_frame)
        main.addWidget(ikspline_frame)
        main.addWidget(bidirectional_frame)
        main.addWidget(dynamic_frame)
        main.addWidget(zipper_frame)
        main.addWidget(variable_frame)

        self.create_connection()

        return container


    def bidirectional_fk_layout(self):
        frame = _widgest.create_collapsible_frame("Forward Reverse FK ")
        main_layout = _widgest.create_section("Double FK")
        name_layout, self.forward_name_field = _widgest.create_QLineEdit_grp("Name:")
        self.forward_joints_chain_cbx = QtWidgets.QCheckBox(' is joints chain')
        btn_layout, self.forward_apply_btn, self.forward_help_btn = _widgest.create_Qbuttons(" Apply ")

        group = QtWidgets.QGroupBox(u"Rig Type:")
        layout = QtWidgets.QVBoxLayout(group)
        btn_layout2 = QtWidgets.QHBoxLayout()

        self.forward_parent_btn = QtWidgets.QPushButton('Parent')
        self.forward_cons_btn = QtWidgets.QPushButton('Constrain')

        self.forward_parent_btn.setProperty("main", True)
        self.forward_cons_btn.setProperty("main", True)

        btn_layout2.addWidget(self.forward_parent_btn)
        btn_layout2.addWidget(self.forward_cons_btn)

        main_layout.addWidget(_widgest.create_text(u" select the objects to be controlled in sequence\n按顺序选择需要添加双向FK的对象 "))
        main_layout.addLayout(name_layout)
        main_layout.addWidget(self.forward_joints_chain_cbx)
        main_layout.addLayout(btn_layout)
        layout.addLayout(btn_layout2)
        main_layout.addWidget(group)
        frame.addWidget(main_layout)
        return frame

    def dynamic_rig_layout(self):
        frame = _widgest.create_collapsible_frame("Dynamic Coexist Rig ")
        group = QtWidgets.QGroupBox(u"Dynamic:")
        main_layout = QtWidgets.QVBoxLayout(group)
        layout, self.dyn_attr_filed, self.dyn_attr_btn = _widgest.create_QLineEdit_row("Attribute Ctrl:" , label_width=78)
        self.dny_type_block = _widgest.create_radiogroup(
            "Type:",
            [
                ("Joint ", 1, u"选择关节"),
                ("Joint and Curve ", 2, u"选择当前关节和曲线"),
                ("Curve ", 3, u"选择曲线"),
            ],
            default_id=1
        )
        self.dny_hint = _widgest.create_text(self.DNYM_HINT[1])

        btn_layout, self.dyn_apply_btn, self.dyn_help_btn = _widgest.create_Qbuttons(" Apply ")

        main_layout.addWidget(_widgest.create_text(u" first Add dynamic switch attributes 先添加动态开关属性的组或控制器 "))
        main_layout.addLayout(layout)
        main_layout.addWidget(self.dny_type_block)
        main_layout.addWidget(self.dny_hint)
        main_layout.addLayout(btn_layout)
        frame.addWidget(group)
        return frame

    def zipper_rig_layout(self):
        frame = _widgest.create_collapsible_frame("Zipper Rig ")
        main_layout = _widgest.create_section("Zipper Option:")
        layout, self.zip_name_field = _widgest.create_QLineEdit_grp("Name:")

        layout1, self.zip_mid_filed, self.zip_mid_btn = _widgest.create_QLineEdit_row("M Joint:")
        layout2, self.zip_left_filed, self.zip_left_btn = _widgest.create_QLineEdit_row("L Joint:")
        layout3, self.zip_right_filed, self.zip_right_btn = _widgest.create_QLineEdit_row("R Joint:")
        add_ctrl_layout = _widgest.create_section("Ctrl Set:")
        zip_ctrl_layout = QtWidgets.QVBoxLayout()
        zip_count_layout = QtWidgets.QHBoxLayout()
        layout4, self.zip_root_filed, self.zip_root_btn = _widgest.create_QLineEdit_row("Root:")
        block_layout = QtWidgets.QHBoxLayout()
        self.zip_stretch_aixs_block = _widgest.create_radiogroup(
            "Scale Axis:",
            [("X ", 1, None), ("Y ", 2, None),("Z ", 3, None) ],default_id=1)

        self.zip_ctrl_block = _widgest.create_radiogroup(
            "Ctrl:",
            [("IK ", 1, None), ("FK ", 2, None), ("FKIK ", 3, None)], default_id=1)

        block_layout.addWidget(self.zip_stretch_aixs_block)
        block_layout.addWidget(self.zip_ctrl_block)

        self.zip_count = QtWidgets.QSpinBox()
        self.zip_count.setRange(4, 100)
        self.zip_count.setValue(5)
        self.zip_count.setMinimumWidth(60)

        zip_count_layout.addWidget(QtWidgets.QLabel("Ctrl count:"))
        zip_count_layout.addWidget(self.zip_count)
        zip_count_layout.addStretch()

        zip_ctrl_layout.addLayout(layout4)
        zip_ctrl_layout.addLayout(block_layout)
        zip_ctrl_layout.addLayout(zip_count_layout)
        add_ctrl_layout.addLayout(zip_ctrl_layout)
        self.zip_rig_block = _widgest.create_radiogroup(
            "Type:",
            [("Expression ", 1, u"表达式"),
                ("SDK ", 2, u"驱动关键帧")],
            default_id=1
        )
        btn_layout, self.zip_apply_btn, self.zip_help_btn = _widgest.create_Qbuttons(" Apply ")

        main_layout.addLayout(layout)
        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)
        main_layout.addLayout(layout3)
        _widgest.separator(main_layout, True)
        main_layout.addWidget(add_ctrl_layout)
        _widgest.separator(main_layout, True)
        main_layout.addWidget(self.zip_rig_block)
        main_layout.addWidget(_widgest.create_text(u" 绑定完成后,拉链的属性会在你载入的左右关节上! 你可以将属性连接到任何对象上"))
        main_layout.addLayout(btn_layout)
        frame.addWidget(main_layout)
        return frame

    def ikspline_rigging_layout(self):
        frame = _widgest.create_collapsible_frame(" IK Spline Rigging")
        frame.setObjectName("IKSplineCollapsibleFrame")
        main_layout = QtWidgets.QVBoxLayout()
        group = QtWidgets.QGroupBox(u"Ikspline Rigging Set:")
        layout = QtWidgets.QVBoxLayout(group)

        scale_layout, self.ik_global_scale_filed, self.ik_global_scale_btn = _widgest.create_QLineEdit_row(
            "Global scale:")
        attr_layout, self.ik_add_attr_filed, self.ik_add_attr_btn = _widgest.create_QLineEdit_row("Attrbute ctrl:", label_width=75)

        checkbox_layout = QtWidgets.QHBoxLayout()
        self.strech_cbx = QtWidgets.QCheckBox(' Strech')
        self.unified_cbx = QtWidgets.QCheckBox(' Is unified?')
        checkbox_layout.addWidget(self.strech_cbx)
        checkbox_layout.addWidget(self.unified_cbx)
        self.unified_cbx.setChecked(True)

        self.ikspline_block = _widgest.create_radiogroup(
            "Rig Option:",
            [
                ("Add joints stretch  ", 1, u"给已有ikspline关节添加拉伸"),
                ("IKFK Switch", 2, u"IKFK 可切换绑定"),
                ("IKFK", 3, u"IKFK自选绑定")
            ],
            default_id=3
        )

        btn_layout, self.ikspline_rigging_btn, self.ikspline_help_btn = _widgest.create_Qbuttons(" Apply")
        self.ikspline_block.idClicked.connect(self._ikspline_block_toggled)
        self.ikspline_text_hint = _widgest.create_text(self.IKSPLINE_HINT[1])

        group2 = QtWidgets.QGroupBox(u"Rig Option:")
        group2.setObjectName("RigOptionGroupBox")
        layout2 = QtWidgets.QVBoxLayout(group2)

        self.add_strech_widget = QtWidgets.QWidget()
        self.add_strech_widget.setVisible(False)
        add_strech_layout = QtWidgets.QVBoxLayout(self.add_strech_widget)

        spline_curve_layout, self.spline_curve_filed, self.spline_curve_btn = _widgest.create_QLineEdit_row(
            "Spline curve:")
        self.spline_stretch_aixs_block = _widgest.create_radiogroup(
            "Scale Axis:",
            [
                ("X ", 1, None),
                ("Y ", 2, None),
                ("Z ", 3, None)
            ],
            default_id=1
        )

        add_strech_layout.addLayout(spline_curve_layout)
        add_strech_layout.addWidget(self.spline_stretch_aixs_block)

        self.ikfk_switch_widget = QtWidgets.QWidget()
        self.ikfk_switch_widget.setVisible(False)
        ikfk_switch_layout = QtWidgets.QHBoxLayout(self.ikfk_switch_widget)

        self.ikfk_switch_count = QtWidgets.QSpinBox()
        self.ikfk_switch_count.setRange(4, 100)
        self.ikfk_switch_count.setValue(5)
        self.ikfk_switch_count.setMinimumWidth(60)

        ikfk_switch_layout.addWidget(QtWidgets.QLabel("Ctrl count:"))
        ikfk_switch_layout.addWidget(self.ikfk_switch_count)
        ikfk_switch_layout.addStretch()

        self.ikfk_select_widget = QtWidgets.QWidget()
        ikfk_select_main_layout = QtWidgets.QVBoxLayout(self.ikfk_select_widget)

        ikfk_count_layout = QtWidgets.QHBoxLayout()
        self.ikfk_select_count = QtWidgets.QSpinBox()
        self.ikfk_select_count.setRange(4, 100)
        self.ikfk_select_count.setValue(5)
        self.ikfk_select_count.setMinimumWidth(60)
        ikfk_count_layout.addWidget(QtWidgets.QLabel("Ctrl count:"))
        ikfk_count_layout.addWidget(self.ikfk_select_count)
        ikfk_count_layout.addStretch()

        self.ikfk_type_block = _widgest.create_radiogroup(
            "Ctrl:",
            [
                ("IK ", 1, None),
                ("FK ", 2, None),
                ("IKFK ", 3, None)
            ],
            default_id=1
        )
        ikfk_select_main_layout.addLayout(ikfk_count_layout)
        ikfk_select_main_layout.addWidget(self.ikfk_type_block)
        # =====================================================

        layout2.addWidget(self.add_strech_widget)
        layout2.addWidget(self.ikfk_switch_widget)
        layout2.addWidget(self.ikfk_select_widget)

        layout.addLayout(scale_layout)
        layout.addLayout(attr_layout)
        layout.addLayout(checkbox_layout)
        _widgest.separator(layout)
        layout.addWidget(self.ikspline_block)
        layout.addWidget(group2)

        layout.addWidget(self.ikspline_text_hint)
        layout.addLayout(btn_layout)
        main_layout.addWidget(group)

        frame.setContentLayout(main_layout)
        return frame

    def variable_fk_layout(self):
        frame = _widgest.create_collapsible_frame(" Variable FK")
        group = QtWidgets.QGroupBox(u"滑动的fk:")
        main_layout = QtWidgets.QVBoxLayout(group)
        layout, self.variable_name_field = _widgest.create_QLineEdit_grp("Prefix:")
        count_layout = QtWidgets.QHBoxLayout()
        self.variable_count = QtWidgets.QSpinBox()
        self.variable_count.setRange(4, 100)
        self.variable_count.setValue(5)
        self.variable_count.setMinimumWidth(60)
        count_layout.addWidget(QtWidgets.QLabel("Ctrl count:"))
        count_layout.addWidget(self.variable_count)
        count_layout.addStretch()

        btn_layout, self.variable_rigging_btn, self.variable_help_btn = _widgest.create_Qbuttons(" Apply")

        main_layout.addLayout(layout)
        main_layout.addLayout(count_layout)
        main_layout.addWidget(_widgest.create_text("Generate joints based on the number of curve points.根据曲线点数生成关节"))
        main_layout.addWidget(_widgest.create_text("Select curve to Apply 选择曲线运行"))
        main_layout.addLayout(btn_layout)
        frame.addWidget(group)
        return frame

    def rivet_layout(self):
        frame = _widgest.create_collapsible_frame(" Follicle/Rivet")
        group = QtWidgets.QGroupBox(u"Follicle/Rivet:")
        main_layout = QtWidgets.QVBoxLayout(group)

        self.rivet_rig_wtg = _widgest.create_section("Rig Type:")
        self.rivet_rig_block = _widgest.create_radiogroup(
            "",
            [
                ("Parent", 1, None),
                ("Contrain", 2, u"约束"),
            ],
            default_id=1
        )
        self.rivet_constrain_block = _widgest.create_radiogroup(
            "Constrain",
            [
                ("parentConstrain", 1, u"父约束"),
                ("pointCons", 2, u"点约束"),
                ("orientCons", 3, u"方向约束"),
            ],
            default_id=1,
            enabled_map={1: False, 2: False, 3: False}
        )

        self.rivet_cons_block = _widgest.create_radiogroup(
            "Type:",
            [
                ("Follicle", 1, u"毛囊"),
                ("Matrix", 2, u"locator"),
                ("Constrain", 3, u"获取最近的权重关节创建约束"),
            ],
            default_id=1
        )
        self.rivet_hint = _widgest.create_text("select objects and then Surface/Mesh\n选择需要钉的对象+Surface/Mesh")
        btn_layout, self.rivet_apple_btn, self.rivet_help_btn = _widgest.create_Qbuttons(" Apply ")

        main_layout.addWidget(self.rivet_hint)
        self.rivet_rig_wtg.addWidget(self.rivet_rig_block)
        self.rivet_rig_wtg.addWidget(self.rivet_constrain_block)
        main_layout.addWidget(self.rivet_rig_wtg)
        main_layout.addWidget(self.rivet_cons_block)

        main_layout.addLayout(btn_layout)
        self.rivet_rig_block.idClicked.connect(self._rivet_rig_toggled)
        self.rivet_cons_block.idClicked.connect(self._rivet_cons_toggled)
        frame.addWidget(group)
        return frame

    def ribbon_animation_layout(self):
        frame = _widgest.create_collapsible_frame(" Ribbon Animation Rigging")
        group = QtWidgets.QGroupBox(u"Ribbon Animation:")
        main_layout = QtWidgets.QVBoxLayout(group)
        name_count_layout = QtWidgets.QHBoxLayout()
        block_layout = QtWidgets.QHBoxLayout()

        ribbon_name_layout, self.ribbon_name_filed = _widgest.create_QLineEdit_grp("Name:", "")
        self.ribbon_joint_filed = QtWidgets.QSpinBox()
        self.ribbon_joint_filed.setValue(7)
        self.ribbon_joint_filed.setFixedWidth(40)
        ribbon_joint_layout = QtWidgets.QFormLayout()

        label = _widgest.create_bold_label('counts : ')
        ribbon_joint_layout.addRow(label, self.ribbon_joint_filed)

        self.ribbon_rig_block = _widgest.create_radiogroup(
            "Rig Type:",
            [
                ("None", 1, None),
                ("Parent", 2, None),
                ("Constrain", 3, None),
            ],
            default_id=1
        )

        self.ribbon_direction_block = _widgest.create_radiogroup(
            "Direction:",
            [
                ("U", 1, None),
                ("V", 2, None),
            ],
            default_id=1
        )

        self.ribbon_animation_block = _widgest.create_radiogroup(
            "Animation",
            [
                ("none", 1, u""),
                ("Slide", 2, u"滑动"),
                ("Spread", 3, u""),
                ("Slide+Spread", 4, u""),
                ("Tract", 5, u""),
            ],
            default_id=1,
            enabled_map={5: False}
        )

        apply_layout = QtWidgets.QHBoxLayout()
        self.type_menu = QtWidgets.QComboBox()
        self.type_menu.addItem('Rivet', 1)
        self.type_menu.addItem('Follicle', 2)
        self.type_menu.setFixedWidth(80)
        self.type_menu.setFixedHeight(28)
        self.type_menu.setCurrentIndex(1)
        self.type_menu.currentIndexChanged.connect(self._on_type_toggled)
        type_menu_layout = QtWidgets.QFormLayout()
        type_menu_layout.addRow('Type:', self.type_menu)

        self.ribbon_hint = _widgest.create_text("Ribbon Animation Rigging")

        frame_button = _widgest.create_collapsible_frame("Comtroller ?")
        CTRL_layout = QtWidgets.QVBoxLayout()
        CTRL_type_layout = QtWidgets.QHBoxLayout()
        CTRL_layout.addWidget(_widgest.create_text("如需要更高级IKFK绑定前往Joint>Rigging>IKFK System"))

        self.ribbon_ctrl_filed = QtWidgets.QSpinBox()
        self.ribbon_ctrl_filed.setValue(3)
        self.ribbon_ctrl_filed.setFixedWidth(40)
        ribbon_ctrl_layout = QtWidgets.QFormLayout()
        label = _widgest.create_bold_label('counts : ')
        ribbon_ctrl_layout.addRow(label, self.ribbon_ctrl_filed)

        self.ribbon_ctrl_block = _widgest.create_radiogroup(
            "Ctrl Type:",
            [("None", 1, None),
                ("IK", 2, None),
                ("FK", 3, None),
                ("IKFK", 4, None),
            ],
            default_id=1
        )

        CTRL_type_layout.addLayout(ribbon_ctrl_layout, 1)
        CTRL_type_layout.addWidget(self.ribbon_ctrl_block, 2)
        CTRL_layout.addLayout(CTRL_type_layout)
        frame_button.setContentLayout(CTRL_layout)

        btn_layout, self.ribbon_apple_btn, self.ribbon_help_btn = _widgest.create_Qbuttons(" Apply ")

        name_count_layout.addLayout(ribbon_name_layout, 3)
        name_count_layout.addLayout(ribbon_joint_layout, 1)

        main_layout.addWidget(self.ribbon_hint)
        main_layout.addWidget(_widgest.create_text("写入需要创建关节的名字，和数量"))
        main_layout.addLayout(name_count_layout)

        block_layout.addWidget(self.ribbon_rig_block, 2)
        block_layout.addWidget(self.ribbon_direction_block, 1)

        main_layout.addLayout(block_layout)

        main_layout.addWidget(self.ribbon_animation_block)
        main_layout.addWidget(frame_button)
        apply_layout.addLayout(type_menu_layout)
        apply_layout.addLayout(btn_layout)
        main_layout.addLayout(apply_layout)
        frame.addWidget(group)

        return frame

    def _QLineEdit_row(self, label_text, default_text="", label_width=80):
        layout = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel(label_text)
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedWidth(label_width)
        line_edit = QtWidgets.QLineEdit(default_text)
        line_edit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        # line_edit.setMinimumWidth(120)
        layout.addWidget(label)
        layout.addWidget(line_edit)
        # layout.addStretch()
        return layout, line_edit

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

        self.forward_apply_btn.clicked.connect(self.reverse_fk_build)
        self.forward_parent_btn.clicked.connect(partial(reverse_fk.ControlType, False))
        self.forward_cons_btn.clicked.connect(partial(reverse_fk.ControlType, True))
        self.dny_type_block.idClicked.connect(self._on_dny_type_toggled)
        self.zip_apply_btn.clicked.connect(self.zipper_build)
        self.dyn_apply_btn.clicked.connect(self.dynamic_build)
        self.ikspline_rigging_btn.clicked.connect(self.splineik_build)
        self.variable_rigging_btn.clicked.connect(self.variable_fk_build)
        self.rivet_apple_btn.clicked.connect(self.follicle_rivet_constrain)
        self.ribbon_apple_btn.clicked.connect(self.ribbon_rig_build)
        self.ikspline_help_btn.clicked.connect(partial(self._show_img, 5))
        self.forward_help_btn.clicked.connect(partial(self._show_img,  6))
        self.dyn_help_btn.clicked.connect(partial(self._show_img, 7))
        self.zip_help_btn.clicked.connect(partial(self._show_img, 8))
        self.variable_help_btn.clicked.connect(partial(self._show_img, 9))
        self.ribbon_help_btn.clicked.connect(partial(self._show_img, 16))
        self.ik_global_scale_btn.clicked.connect(
            partial(SelectionLoader.load_lineedit, self, self.ik_global_scale_filed, "transform")
        )

        self.ik_add_attr_btn.clicked.connect(
            partial(SelectionLoader.load_lineedit, self, self.ik_add_attr_filed, "transform")
        )

        self.dyn_attr_btn.clicked.connect(
            partial(SelectionLoader.load_lineedit, self, self.dyn_attr_filed, "transform")
        )

        self.zip_mid_btn.clicked.connect(
            partial(SelectionLoader.load_lineedit, self, self.zip_mid_filed, "joint")
        )

        self.zip_left_btn.clicked.connect(
            partial(SelectionLoader.load_lineedit, self, self.zip_left_filed, "joint")
        )

        self.zip_right_btn.clicked.connect(
            partial(SelectionLoader.load_lineedit, self, self.zip_right_filed, "joint")
        )

        self.zip_root_btn.clicked.connect(
            partial(SelectionLoader.load_lineedit, self, self.zip_root_filed, "joint")
        )

    def get_menu_item(self, item):
        return item

    def _show_img(self, id, *args):
        self.dispatcher.execute("Show Help", id)

    def _on_dny_type_toggled(self, btn_id):
        self.dny_hint.setText(self.DNYM_HINT[btn_id])

    def _ikspline_block_toggled(self, btn_id):
        self.ikspline_text_hint.setText(self.IKSPLINE_HINT[btn_id])
        if btn_id == 1:
            self.add_strech_widget.show()
            self.ikfk_switch_widget.hide()
            self.ikfk_select_widget.hide()
        elif btn_id == 2:
            self.add_strech_widget.hide()
            self.ikfk_switch_widget.show()
            self.ikfk_select_widget.hide()
        else:
            self.add_strech_widget.hide()
            self.ikfk_switch_widget.hide()
            self.ikfk_select_widget.show()

        group2 = self.findChild(QtWidgets.QGroupBox, "RigOptionGroupBox")
        if group2:
            group2.updateGeometry()
            if group2.layout():
                group2.layout().activate()

        ikspline_frame = self.findChild(QtWidgets.QFrame, "IKSplineCollapsibleFrame")
        if ikspline_frame:
            ikspline_frame.updateGeometry()
            if ikspline_frame.layout():
                ikspline_frame.layout().activate()

        self.updateGeometry()
        self.adjustSize()

        QtCore.QTimer.singleShot(50, self.adjustSize)

    def _rivet_cons_toggled(self, btn_id):
        if btn_id == 3:
            self.rivet_rig_wtg.setEnabled(False)
        else:
            self.rivet_rig_wtg.setEnabled(True)

    def _rivet_rig_toggled(self, btn_id):
        if btn_id == 2:
            self.rivet_constrain_block.setEnabledByIds([1, 2, 3], True)
        else:
            self.rivet_constrain_block.setEnabledByIds([1, 2, 3], False)

    def _on_type_toggled(self, id):
        custom_id = self.type_menu.currentData()
        # print(id, custom_id)
        if custom_id == 1:
            self.ribbon_animation_block.setEnabledByIds([1, 2, 5], True)
            self.ribbon_animation_block.setEnabledByIds([3, 4], False)
        else:
            self.ribbon_animation_block.setEnabledByIds([1, 2, 3, 4], True)
            self.ribbon_animation_block.setEnabledByIds([5], False)


    def reverse_fk_build(self):
        reverse_fk.Create_ctrls(self.forward_name_field.text(), self.forward_joints_chain_cbx.isChecked())


    def zipper_build(self):
        MainName = self.zip_name_field.text()
        Joint_M = self.zip_mid_filed.text()
        Joint_L = self.zip_left_filed.text()
        Joint_R = self.zip_right_filed.text()

        if not MainName:
            mayaPrint.error("not main name.")
            return

        if not Joint_M:
            mayaPrint.error("not load mid Joint")
            return

        if not Joint_L and not Joint_R:
            mayaPrint.error("not load L/R joint")
            return

        if self.zip_rig_block.checkedId() == 1:
            mode_Exp = "Exp"
        else:
            mode_Exp = "Key"

        datas = {
            "Joint_Middle": Joint_M,
            "Joint_Left": Joint_L,
            "Joint_Right": Joint_R,
            "Name": MainName,
            "zipper": "zipper",
            "mode_Exp": mode_Exp,
            "Root": self.zip_root_filed.text(),
            "axial": self.zip_stretch_aixs_block.checkedId(),
            "ctrlType": self.zip_ctrl_block.checkedId(),
            "ctrlCount": self.zip_count.value(),
        }
        self.dispatcher.execute("zipper Rig", datas)

        mayaPrint.log(" >>> Created successfully.")


    def dynamic_build(self):
        Dyn.dny_build(self.dny_type_block.checkedId(), self.dyn_attr_filed.text())


    def splineik_build(self):
        MasterCtrl = self.ik_global_scale_filed.text()
        Add_attr = self.ik_add_attr_filed.text()
        Strech = self.strech_cbx.isChecked()
        Unified = self.unified_cbx.isChecked()
        app = self.ikspline_block.checkedId()
        if app == 1:
            Joints = mc.ls(sl=1)
            if Joints:
                SpineCurve = self.spline_curve_filed.text()
                aixs = self.spline_stretch_aixs_block.checkedId()
                aixs_map={1:".sx", 2:".sy", 3:".sz"}
                if not SpineCurve:
                    mayaPrint.error("Please load the SpineCurve.")
                    return
                EditJnt.splineik_stretch_build(MasterCtrl, SpineCurve, Joints, aixs_map[aixs], Add_attr, Strech, Unified)
        elif app == 2:
            EditJnt.splineik_build(MasterCtrl, Add_attr, self.ikfk_switch_count.text(), Strech, Unified)
        else:
            EditJnt.splineik_ikfk_build(MasterCtrl, Add_attr, self.ikfk_select_count.value(), Strech, Unified, self.ikfk_type_block.checkedId())


    def variable_fk_build(self):
        sle_obj = mc.ls(sl=1)
        if not sle_obj:
            pass
        else:
            if SelectionLoader.match_type(sle_obj[0], "curve"):
                variable_FK.VarFk(sle_obj[0], self.variable_name_field.text(), self.variable_count.value())


    def follicle_rivet_constrain(self):
        obj = mc.ls(sl=1)
        if len(obj) < 2:
            mayaPrint.error(' Please add NurbsSurface/Mesh. ')
            return

        datas = {
            "cons_block": self.rivet_cons_block.checkedId(),
            "rig_block": self.rivet_rig_block.checkedId(),
            "constrain_block": self.rivet_constrain_block.checkedId()
        }

        self.dispatcher.execute("follicle rivet Rig", datas)


    def ribbon_rig_build(self):

        datas = {
            "cons": self.type_menu.currentData(),
            "name_filed": self.ribbon_name_filed.text(),
            "joint_filed": self.ribbon_joint_filed.value(),
            "rig_block": self.ribbon_rig_block.checkedId(),
            "direction_block": self.ribbon_direction_block.checkedId(),
            "animation_block": self.ribbon_animation_block.checkedId()-1,
            "ctrl_block": self.ribbon_ctrl_block.checkedId(),
            "ctrl_count": self.ribbon_ctrl_filed.value()
        }
        self.dispatcher.execute("ribbon rig build", datas)