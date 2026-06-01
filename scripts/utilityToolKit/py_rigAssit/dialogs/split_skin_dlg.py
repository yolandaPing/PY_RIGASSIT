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
import JointEdit.split_skin_weight as split_skin_weight
import py_rigAssit.common.img_commands
import maya.cmds as cmds

PY_WIDGEST = Widgets()
MAYA_VISON = int(cmds.about(version=True))
_obj = SelectOrremoveObj()


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
        self.dispatcher = CommandDispatcher()
        main = QtWidgets.QVBoxLayout(self)
        main.setContentsMargins(4, 4, 4, 4)
        main.setSpacing(4)
        main.addWidget(PY_WIDGEST.create_title("Split SkinWeight", 15, self.WEBS))
        main.addLayout(self.split_skin_lay(), 1)
        if copyright:
            PY_WIDGEST.create_copyrightText(main, "2025-2026")

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocus()
        self.create_connection()
        return main

    def split_skin_lay(self):
        main_layout = QtWidgets.QVBoxLayout()

        layout1, self.geo_filed, self.geo_btn = PY_WIDGEST.create_QLineEdit_row("Geometry:" )
        layout2, self.mask_filed, self.mask_btn = PY_WIDGEST.create_QLineEdit_row("Mask Jnt/Lay:")

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
        self.split_help_btn.clicked.connect(lambda: self.dispatcher.execute("Show Help", 19))
        return main_layout

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
            self.split_help_btn.clicked.connect(lambda: self.dispatcher.execute("Show Help", 19))
        else:
            self.mask_btn.setEnabled(False)
            self.degree_container.setEnabled(True)
            self.split_help_btn.clicked.connect(lambda: self.dispatcher.execute("Show Help", 20))


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
