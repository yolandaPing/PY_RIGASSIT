# -*- coding: utf-8 -*-

# .FileName:joint_mod_layout.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/8 19:52
# .Finish time:
# -*- coding: utf-8 -*-
# Joint Mod Dialog - Professional Refactor UI
# Maya 2018 - 2026
# PySide2 / PySide6 compatible
from functools import partial
import json
from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
from py_rigAssit.dialogs import base_dir, Help, mayaPrint
try:
    from ui_framework.widgets.button import GridButtons
except:
    from CommonUse.button import GridButtons
from JointEdit.JointEditFun import EditJnt
from py_rigAssit.dialogs.skin_inverseMatrix_dialog import SkinInvertMatrixDialog
from py_rigAssit.dialogs.ikfk_system_layout import IKFKWidget
from py_rigAssit.common.loader import SelectionLoader
from JointEdit import mirror_skinWeight
from py_rigAssit.common.command_dispatcher import CommandDispatcher
import py_rigAssit.common.commands
import JointEdit.exp_inp_skinClusterIO as exp_inp_skinClusterIO
import maya.cmds as cmds, maya.mel as mel

_widgest = Widgets()

skinInverse_lay = SkinInvertMatrixDialog()
EditJnt = EditJnt()


class PYJointEditLayout(PyouPersistentWindow):
    OPTIMIZE_HINT = {1: u'自动计算飘带（条状物）模型权重，参与权重的关节必须是有序选择参与蒙皮',
                     2: u'自动拆分关节权重，有序选择需要拆分权重的关节+mesh(且将需要拆的权重刷给第一个)',
                     3: u'变形器转权重，先添权重模型加DeltaMush/Tension变形器,设置好内部值',
                     4: u'选择拷贝源+需要拷贝的对象,此功能会直接将拷贝源提高细分来优化权重'}


    def __init__(self, parent=None):
        super(PYJointEditLayout, self).__init__("PYJointEditLayout", "PYJointEditDialog", parent)

        self.setWindowTitle("Joint Mod Dialog")
        self.resize(360, 720)

        self.init_ui(True)


    def init_ui(self, copyright=False):
        self.dispatcher = CommandDispatcher()
        main = QtWidgets.QVBoxLayout(self)
        main.setContentsMargins(2, 2, 2, 2)
        main.setSpacing(4)
        main.addWidget(_widgest.create_title("Rigging Dialog", 15, None))
        # main.addWidget(_widgest.create_text(u"You can see how to use it on the button\n你可以放置在按钮上看如何使用它"))
        # main.addWidget(self.build_tabs(), 1)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setContentsMargins(0, 0, 0, 0)

        cld_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(cld_widget)
        scroll_layout.setContentsMargins(2, 2, 2, 2)
        scroll_layout.setSpacing(4)

        scroll.setWidget(cld_widget)
        main.addWidget(scroll)
        text_widget =_widgest.create_text(u"You can see how to use it on the button\n你可以放置在按钮上看如何使用它")
        text_widget.setContentsMargins(0, 0, 0, 0)
        scroll_layout.addWidget(text_widget)
        scroll_layout.addWidget(self.build_tabs())

        scroll_layout.addStretch()

        if copyright:
            _widgest.create_copyrightText(main, "2026")

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocus()
        self.create_connection()
        return main


    # def build_tabs(self):
    #
    #     self.tabs = QtWidgets.QTabWidget()
    #     self.tabs.setTabPosition(QtWidgets.QTabWidget.West)
    #     # self.tabs.setTabPosition(QtWidgets.QTabWidget.North)
    #     self.tabs.setMovable(False)
    #     self.tabs.setUsesScrollButtons(False)
    #
    #     self.tabs.addTab(self.build_joint_tab(), "Quick")
    #     self.tabs.addTab(self.build_skin_tab(), "Skin")
    #     self.tabs.addTab(self.build_rig_tab(), "Rigging")
    #
    #     return self.tabs


    def build_tabs(self):
        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setSpacing(6)
        layout.setContentsMargins(0, 0, 0, 0)
        self.rigging_tab_block = _widgest.create_radiogroup(
            "Module:",
            [
                (" Quick ", 1, None),
                (" Skin ", 2, None),
                (" Rigging ", 3, None),
                (" All ", 4, None),
            ],
            default_id=1
        )
        layout.addWidget(self.rigging_tab_block)
        layout.addWidget(self.build_joint_tab())
        layout.addWidget(self.build_skin_tab())
        layout.addWidget(self.build_rig_tab())
        self.rigging_tab_block.idClicked.connect(self._on_rigging_tab_block_toggled)
        return frame


    def build_joint_tab(self):

        self.py_joint_page = QtWidgets.QWidget()
        lay = QtWidgets.QVBoxLayout(self.py_joint_page)
        lay.setSpacing(6)
        lay.setContentsMargins(0, 0, 0, 0)

        # Quick
        joint_size_layout = QtWidgets.QHBoxLayout(self)
        self.joint_size = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.joint_size.setRange(1, 1000)  # 映射 0.1~10.0 => 1~100
        self.joint_spinbox = QtWidgets.QDoubleSpinBox()
        self.joint_spinbox.setRange(0.01, 10.0)
        self.joint_spinbox.setSingleStep(0.01)
        self.joint_spinbox.setDecimals(2)
        self.joint_reset_btn = QtWidgets.QPushButton("reset 1.0")
        joint_size_layout.addWidget(_widgest.create_text("Joint Size:"), 1)
        joint_size_layout.addWidget(self.joint_spinbox, 1)
        joint_size_layout.addWidget(self.joint_size, 2)
        joint_size_layout.addWidget(self.joint_reset_btn)

        sec1 = _widgest.create_section("Quick Actions")

        grid = GridButtons("joint_quick", 3)
        gridb = GridButtons("joint_edit", 2)
        gridc = GridButtons("joint_skin", 3)
        grid.clicked.connect(self.run_action)
        gridb.clicked.connect(self.run_action)
        gridc.clicked.connect(self.run_action)
        sec1.addWidget(grid)
        sec1.addWidget(gridb)
        sec1.addWidget(gridc)
        # Create
        sec2 = _widgest.create_section("Create / Edit")

        grid1 = GridButtons("center_create", 3)
        grid2 = GridButtons("joint_create", 3)
        grid2b = GridButtons("joint_Make", 3)
        grid1.clicked.connect(self.run_action)
        grid2.clicked.connect(self.run_action)
        grid2b.clicked.connect(self.run_action)
        sec2.addWidget(grid1)
        sec2.addWidget(grid2)
        sec2.addWidget(grid2b)

        # Mirror
        sec3 = _widgest.create_section("Mirror Joint")
        sec3.addLayout(self.mirror_joint_lay())
        _widgest.separator(lay, True)
        lay.addLayout(joint_size_layout)
        lay.addWidget(sec1)
        lay.addWidget(sec2)
        lay.addWidget(sec3)
        lay.addStretch()

        return self.py_joint_page

    def build_skin_tab(self):

        self.py_skin_page = QtWidgets.QWidget()
        lay = QtWidgets.QVBoxLayout(self.py_skin_page)
        lay.setSpacing(2)
        lay.setContentsMargins(0, 0, 0, 0)

        sec1 = _widgest.create_section("Skin Option")
        frame5 = self.ex_im_skin_wigets_lay()
        frame2 = self.mirror_skin_lay()
        frame1 = self.copy_skin_lay()
        frame3 = self.optimize_skin_lay()
        frame4 = self.skin_inverse_lay()
        sec1.addWidget(frame1)
        sec1.addWidget(frame2)
        sec1.addWidget(frame3)
        sec1.addWidget(frame5)
        sec1.addWidget(frame4)

        sec1.main_layout.setAlignment(frame1, QtCore.Qt.AlignTop)
        sec1.main_layout.setAlignment(frame2, QtCore.Qt.AlignTop)
        sec1.main_layout.setAlignment(frame3, QtCore.Qt.AlignTop)
        sec1.main_layout.setAlignment(frame4, QtCore.Qt.AlignTop)
        sec1.main_layout.setAlignment(frame5, QtCore.Qt.AlignTop)
        lay.addWidget(sec1)
        lay.addStretch()
        self.py_skin_page.setVisible(False)
        return self.py_skin_page

    def build_rig_tab(self):

        self.py_rigging_page = QtWidgets.QWidget()
        lay = QtWidgets.QVBoxLayout(self.py_rigging_page)
        lay.setSpacing(2)
        lay.setContentsMargins(0, 0, 0, 0)

        ikfk = IKFKWidget(parent=self)
        lay.addWidget(ikfk.init_ui(False))

        lay.addStretch()
        self.py_rigging_page.setVisible(False)
        return self.py_rigging_page

    def mirror_joint_lay(self):

        main_layout = QtWidgets.QVBoxLayout()
        search_replace_layout = QtWidgets.QHBoxLayout()
        self.across_block = _widgest.create_radiogroup(
            "Mirror across:",
            [
                (" XY ", 1, None),
                (" YZ ", 2, None),
                (" XZ ", 3, None),
            ],
            default_id=2
        )

        self.function_block = _widgest.create_radiogroup(
            "Mirror function:",
            [
                ("Behavior      ", 1, None),
                ("Orientation", 2, None),
            ],
            default_id=1
        )

        search_layout, self.mir_jnt_search_filed = self._QLineEdit_row("Search:", "L_")
        replace_layout, self.mir_jnt_replace_filed = self._QLineEdit_row("Replace:", "R_")

        self.mir_jnt_apple_btn = QtWidgets.QPushButton(" Apply ")
        self.mir_jnt_apple_btn.setProperty("main", True)
        main_layout.addWidget(self.across_block)
        main_layout.addWidget(self.function_block)
        search_replace_layout.addLayout(search_layout)
        search_replace_layout.addLayout(replace_layout)
        main_layout.addLayout(search_replace_layout)
        main_layout.addWidget(self.mir_jnt_apple_btn)
        main_layout.addStretch()

        return main_layout

    def mirror_skin_lay(self):
        frame = _widgest.create_collapsible_frame(" Mirror Skin")
        main_layout = QtWidgets.QVBoxLayout()

        left_layout, self.skin_left_filed = self._QLineEdit_row("Left side:", "L_/_L/l_")
        right_layout, self.skin_right_filed = self._QLineEdit_row("Right side:", "R_/_R/r_")
        middle_layout, self.skin_middle_filed = self._QLineEdit_row("Mid side:", "M_/_M/m_")

        other_layout = QtWidgets.QHBoxLayout()
        self.skin_label_hint = _widgest.create_text(u"     如有报错提示,可选择报错提示的关节 >>> ")
        self.skin_other_select_btn = QtWidgets.QPushButton(" select ")
        self.skin_other_select_btn.setProperty("danger", True)

        other_layout.addWidget(self.skin_label_hint, 4)
        other_layout.addWidget(self.skin_other_select_btn)
        self.skin_other_select_btn.setEnabled(False)

        other_middle_layout, self.skin_other_middle_filed, self.skin_other_middle_btn = _widgest.create_QLineEdit_row("  Other Mid:" )
        self.skin_other_middle_filed.setEnabled(False)
        self.skin_other_middle_btn.setEnabled(False)
        self.skin_other_middle_filed.setPlaceholderText("Unavailable")

        self.skin_direction_block = _widgest.create_radiogroup(
            "Mirror direction:",
            [
                ("-x to x    ", 1, None),
                ("x to -x    ", 2, None),
            ],
            default_id=2
        )
        btn_layout, self.sk_mirror_btn, mir_help_btn = _widgest.create_Qbuttons(" Mirror ")
        mir_help_btn.clicked.connect(lambda: Help.HelpImage("", "special_mirror_tool"))
        main_layout.addWidget(_widgest.create_text(u"检查关节的前后缀"))
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(other_layout)
        main_layout.addLayout(other_middle_layout)
        main_layout.addWidget(self.skin_direction_block)
        _widgest.separator(main_layout, True)

        main_layout.addLayout(btn_layout)
        frame.addLayout(main_layout)
        return frame

    def copy_skin_lay(self):
        frame = _widgest.create_collapsible_frame(" Copy Skin Weight Options")
        main_layout = QtWidgets.QVBoxLayout()

        layout, self.sk_source_filed, self.sk_source_btn = _widgest.create_QLineEdit_row("Source:" )

        self.sk_copy_block = _widgest.create_radiogroup(
            "Type:",
            [
                ("Closest joint", 1, None),
                ("One by one", 2, None),
                ("Label", 3, None)
            ],
            default_id=2
        )

        btn_layout, self.sk_copy_btn, sk_copy_help_btn = _widgest.create_Qbuttons(" Copy ")
        sk_copy_help_btn.clicked.connect(lambda: Help.HelpImage("", "special_copy_tool"))
        main_layout.addWidget(_widgest.create_text(u"载入拷贝源Source, 选择copy方式, 选择需要拷贝的对象或点\n>>>如需要大量组需要拷贝，前往Copy模块里的copy skinWeight"))

        main_layout.addLayout(layout)
        main_layout.addWidget(self.sk_copy_block)
        _widgest.separator(main_layout, True)

        main_layout.addLayout(btn_layout)
        frame.addLayout(main_layout)
        return frame

    def optimize_skin_lay(self):
        frame = _widgest.create_collapsible_frame(" Optimize Skin Weight Options")
        main_layout = QtWidgets.QVBoxLayout()
        group = QtWidgets.QGroupBox(u"自动优化/拆分权重类型:")
        layout = QtWidgets.QVBoxLayout(group)
        btn_layout = QtWidgets.QHBoxLayout()

        self.sk_optimize_block = _widgest.create_radiogroup(
            title="",
            items=[
                ("Auto ik", 1, u"自动计算权重（ik类型）"),
                ("Split ", 2, u"拆分关节权重"),
                ("DeltaMush", 3, u"DeltaMush/Tension变形器优化权重"),
                ("Divisions", 4, u"自动细分优化拷贝权重")
            ],
            default_id=1
        )
        self.sk_optimize_block.idClicked.connect(self._on_copy_type_toggled)

        self.sk_optimize_hint = _widgest.create_text(self.OPTIMIZE_HINT[1])
        btn_layout, self.sk_optimize_btn, sk_optimize_help_btn = _widgest.create_Qbuttons(" Apply ")
        sk_optimize_help_btn.clicked.connect(lambda: Help.HelpImage("", "optimize_skin_tool"))
        group2= QtWidgets.QGroupBox(u"Curve计算权重(Maya 2022 and above):")
        layout2 = QtWidgets.QVBoxLayout(group2)
        btn_layout2 = QtWidgets.QHBoxLayout()
        self.sk_mesh_block = _widgest.create_radiogroup(
            title="Mesh type:",
            items=[
                ("Linear(条状)", 1, u"条状"),
                ("Circular(环形) ", 2, u"环形，闭合"),
            ],
            default_id=1
        )
        self.sk_curve_type_block = _widgest.create_radiogroup(
            title="Degree:",
            items=[
                ("1", 1, u"条状"),
                ("2", 2, u"环形，闭合"),
                ("3", 3, u"环形，闭合"),
            ],
            default_id=3
        )

        btn_layout2, self.sk_curve_convert_btn, sk_convert_help_btn = _widgest.create_Qbuttons(" Apply ")
        sk_convert_help_btn.clicked.connect(lambda: Help.HelpImage("", "optimize_skin_tool"))

        layout.addWidget(self.sk_optimize_block)
        layout.addWidget(self.sk_optimize_hint)
        _widgest.separator(layout, True)

        layout.addLayout(btn_layout)
        main_layout.addWidget(group)
        layout2.addWidget(_widgest.create_text(u"参与权重的关节必须是有序选择参与蒙皮"))
        layout2.addWidget(self.sk_mesh_block)
        layout2.addWidget(self.sk_curve_type_block)
        _widgest.separator(layout2, True)
        layout2.addLayout(btn_layout2)
        main_layout.addWidget(group2)

        frame.addLayout(main_layout)
        return frame

    def skin_inverse_lay(self):
        frame = _widgest.create_collapsible_frame(" Skin Inverse")
        group = QtWidgets.QGroupBox(u"Skin Inverse:")
        main_layout = QtWidgets.QVBoxLayout(group)
        main_layout.addWidget(skinInverse_lay.init_ui())
        frame.addWidget(group)
        return frame

    def ex_im_skin_wigets_lay(self):
        try:
            import numpy
            _num = True
        except:
            _num = False

        frame = _widgest.create_collapsible_frame(" Api Export/Import skinWeight")
        main_layout = QtWidgets.QVBoxLayout()
        group1 = QtWidgets.QGroupBox(u"mesh/surface/curve/ffd:")
        layout1 = QtWidgets.QVBoxLayout(group1)

        group2 = QtWidgets.QGroupBox(u"mesh (numpy版):")
        layout2= QtWidgets.QVBoxLayout(group2)

        api_btn_layout1 = QtWidgets.QHBoxLayout()
        api_btn_layout2 = QtWidgets.QHBoxLayout()

        self.exp_btn = QtWidgets.QPushButton('Export')
        self.imp_btn = QtWidgets.QPushButton('Import')
        self.batch_exp_btn = QtWidgets.QPushButton('Batch Export')
        self.batch_imp_btn = QtWidgets.QPushButton('Batch Import')
        self.exp_btn.setProperty("main", True)
        self.imp_btn.setProperty("main", True)
        self.batch_exp_btn.setProperty("green", True)
        self.batch_imp_btn.setProperty("green", True)

        self.numpy_widget = QtWidgets.QWidget()
        numpy_layout = QtWidgets.QVBoxLayout(self.numpy_widget)
        numpy_btn_layout1 = QtWidgets.QHBoxLayout()
        numpy_btn_layout2 = QtWidgets.QHBoxLayout()

        self.numpy_exp_btn = QtWidgets.QPushButton('npy Export')
        self.numpy_imp_btn = QtWidgets.QPushButton('npy Import')
        self.numpy_batch_exp_btn = QtWidgets.QPushButton('npy Batch Export')
        self.numpy_batch_imp_btn = QtWidgets.QPushButton('npy Batch Import')
        self.numpy_exp_btn.setProperty("main", True)
        self.numpy_imp_btn.setProperty("main", True)
        self.numpy_batch_exp_btn.setProperty("green", True)
        self.numpy_batch_imp_btn.setProperty("green", True)

        api_btn_layout1.addWidget(self.exp_btn)
        api_btn_layout1.addWidget(self.imp_btn)
        api_btn_layout2.addWidget(self.batch_exp_btn)
        api_btn_layout2.addWidget(self.batch_imp_btn)
        layout1.addLayout(api_btn_layout1)
        layout1.addLayout(api_btn_layout2)

        numpy_btn_layout1.addWidget(self.numpy_exp_btn)
        numpy_btn_layout1.addWidget(self.numpy_imp_btn)
        numpy_btn_layout2.addWidget(self.numpy_batch_exp_btn)
        numpy_btn_layout2.addWidget(self.numpy_batch_imp_btn)
        numpy_layout.addLayout(numpy_btn_layout1)
        numpy_layout.addLayout(numpy_btn_layout2)
        layout2.addWidget(self.numpy_widget)
        main_layout.addWidget(group1)
        main_layout.addWidget(group2)
        frame.addLayout(main_layout)

        self.numpy_widget.setVisible(_num)

        return frame

    def _QLineEdit_row(self, label_text, default_text="", label_width=60):
        layout = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel(label_text)
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedWidth(label_width)
        line_edit = QtWidgets.QLineEdit(default_text)
        line_edit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout.addWidget(label)
        layout.addWidget(line_edit)
        layout.addStretch()
        return layout, line_edit

    def create_connection(self):
        self.joint_size.valueChanged.connect(self.on_joint_slider_changed)
        self.joint_reset_btn.clicked.connect(self.reset_joint_to_default)
        self.joint_spinbox.valueChanged.connect(self.on_spinbox_joint_changed)
        self.mir_jnt_apple_btn.clicked.connect(self.mirror_build)
        self.sk_mirror_btn.clicked.connect(self.mirror_skin_build)
        self.exp_btn.clicked.connect(exp_inp_skinClusterIO.devSave_json)
        self.imp_btn.clicked.connect(exp_inp_skinClusterIO.devLoad_json)
        self.batch_exp_btn.clicked.connect(exp_inp_skinClusterIO.batch_save_json)
        self.batch_imp_btn.clicked.connect(exp_inp_skinClusterIO.batch_load_json)
        self.numpy_exp_btn.clicked.connect(exp_inp_skinClusterIO.devSave)
        self.numpy_imp_btn.clicked.connect(exp_inp_skinClusterIO.devLoad)
        self.numpy_batch_exp_btn.clicked.connect(exp_inp_skinClusterIO.batch_save)
        self.numpy_batch_imp_btn.clicked.connect(exp_inp_skinClusterIO.batch_load)
        self.sk_optimize_btn.clicked.connect(self.execute_optimize_weight)
        self.sk_curve_convert_btn.clicked.connect(self.execute_optimize_weight)
        self.sk_copy_btn.clicked.connect(self.run_batch_copy_skin)
        self.sk_source_btn.clicked.connect(
            partial(SelectionLoader.load_lineedit, self, self.sk_source_filed, "mesh")
        )
        self.skin_other_middle_btn.clicked.connect(
            partial(SelectionLoader.load_lineedit, self, self.skin_other_middle_filed, "joint")
        )


    def _on_rigging_tab_block_toggled(self, btn_id):

        if btn_id == 1:
            self.py_joint_page.show()
            self.py_skin_page.hide()
            self.py_rigging_page.hide()

        elif btn_id == 2:
            self.py_joint_page.hide()
            self.py_skin_page.show()
            self.py_rigging_page.hide()
        elif btn_id == 3:
            self.py_joint_page.hide()
            self.py_skin_page.hide()
            self.py_rigging_page.show()
        else:
            self.py_joint_page.show()
            self.py_skin_page.show()
            self.py_rigging_page.show()


    def load_current_scale(self):
        try:
            current = cmds.jointDisplayScale(q=True)
        except:
            current = 1.0
        self.joint_spinbox.blockSignals(True)
        self.joint_size.blockSignals(True)
        self.joint_spinbox.setValue(current)
        self.joint_size.setValue(int(current * 100))
        self.joint_spinbox.blockSignals(False)
        self.joint_size.blockSignals(False)

    def apply_joint_scale(self, value):
        try:
            cmds.jointDisplayScale(value)
        except Exception as e:
            cmds.warning(u"设置关节显示比例失败: {}".format(str(e)))

    def on_joint_slider_changed(self, slider_val):
        real_val = slider_val / 100.0
        self.joint_spinbox.blockSignals(True)
        self.joint_spinbox.setValue(real_val)
        self.joint_spinbox.blockSignals(False)
        self.apply_joint_scale(real_val)

    def on_spinbox_joint_changed(self, real_val):
        slider_val = int(round(real_val * 100))
        slider_val = max(1, min(1000, slider_val))
        self.joint_size.blockSignals(True)
        self.joint_size.setValue(slider_val)
        self.joint_size.blockSignals(False)
        self.apply_joint_scale(real_val)

    def reset_joint_to_default(self):
        self.joint_spinbox.setValue(1.0)

    def _on_copy_type_toggled(self, btn_id):
        self.sk_optimize_hint.setText(self.OPTIMIZE_HINT[btn_id])

    def load_field(self, field, list=False):
        objs = cmds.ls(sl=1)
        if objs is None:
            QtWidgets.QMessageBox.warning(self, u"警告", u"请先选择一个对象")
            return
        if list:
            field.setText(objs)
        else:
            field.setText(objs[0])

    
    def mirror_build(self):
        EditJnt.mirror_joints_build(self.mir_jnt_search_filed.text(), self.mir_jnt_replace_filed.text(), self.across_block.checkedId(), self.function_block.checkedId())

    
    def mirror_skin_build(self):
        cmds.undoInfo(openChunk=True)
        mel.eval(("source \"" + (base_dir.replace("\\", "/") + "scripts/mel/" + "pyFindOtherSide.mel") + "\" ;"))
        mel.eval(("source \"" + (base_dir.replace("\\", "/") + "scripts/mel/" + "pyPoseMirrorSkin.mel") + "\" ;"))

        left_prex = self.skin_left_filed.text()
        right_prex = self.skin_right_filed.text()
        mid_prex = self.skin_middle_filed.text()
        no_mirror = self.skin_other_middle_filed.text()
        left_to_right = self.skin_direction_block.checkedId()
        try:
            objes = cmds.ls(sl=1)

            if objes:
                mel_cmd = 'pyPoseMirrorSkin({}, {}, {}, {}, {});'.format(json.dumps(left_prex), json.dumps(right_prex), json.dumps(mid_prex), json.dumps(no_mirror), left_to_right)
                for i in objes:
                    cmds.select(i, r=1)
                    result = mel.eval(mel_cmd)

                    if result == "PoseMirrorSkin completed successfully.":
                        mayaPrint.log(result)

                    elif result == "Error retrieving string, please check!!!":
                        mayaPrint.error(result)

                    elif result == "No skinCluster found on selected object.":
                        mayaPrint.error(result)

                    else:
                        result_list = result.split('/')
                        self.no_stand_joint = result_list
                        self.skin_other_select_btn.setEnabled(True)
                        self.skin_other_middle_filed.setEnabled(True)
                        self.skin_other_middle_btn.setEnabled(False)

                        print("# Error: --------------------------------------------------------------------------")
                        mayaPrint.warning(result_list)
                        print("# Error: --------------------------------------------------------------------------")

                        if cmds.objExists("PoseMirrorSkin_Temp_grp"):
                            cmds.delete("PoseMirrorSkin_Temp_grp")

                        mayaPrint.error(
                            "There are joints with non-standard names, check if they participate in mirroring. {}".format(
                                result_list))

                        return

        finally:
            cmds.undoInfo(closeChunk=True)

        return
    
    def execute_optimize_weight(self):
        map={1:"IK Weight", 2:"Split Weight", 3:"DeltaMush Weight", 4:"Divisions Weight"}
        if hasattr(self, "dispatcher"):
            self.dispatcher.execute(map[self.sk_optimize_block.checkedId()])

    
    def curve_split_weight(self):
        if hasattr(self, "dispatcher"):
            self.dispatcher.execute("Curve Split", [self.sk_mesh_block.checkedId(), self.sk_curve_type_block.checkedId()])

    
    def run_action(self, text):
        print("Run:", text)
        if hasattr(self, "status"):
            self.status.setText("Run: {}".format(text))
        if hasattr(self, "dispatcher"):
            self.dispatcher.execute(text)

    
    def run_batch_copy_skin(self):
        source_field = self.sk_source_filed.text()
        type = self.sk_copy_block.checkedId()
        new_sc = False
        if source_field:
            if not cmds.objExists(source_field):
                mayaPrint.error(u"请载入源权重对象不存在!")
            source = True
        else:
            source_field = ""
            source = False

        if type == 1:
            EditJnt.create_copySkinWeight(new_sc, True, False, False, source, source_field)
        elif type == 2:
            EditJnt.create_copySkinWeight(new_sc, False, True, False, source, source_field)
        elif type == 3:
            EditJnt.create_copySkinWeight(new_sc, False, False, True, source, source_field)
        else:
            EditJnt.create_copySkinWeight(new_sc, False, False, True, source, source_field)


def main():

    global py_joint_mod_dialog
    try:
        py_joint_mod_dialog.close()  # pylint: disable=E0601
        py_joint_mod_dialog.deleteLater()
    except:
        pass

    py_joint_mod_dialog = PYJointEditLayout()
    py_joint_mod_dialog.show()

if __name__ == '__main__':

    main()
