# -*- coding: utf-8 -*-

# .FileName:mirror_sdk_dlg.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/23 19:42
# .Finish time:
from functools import partial

from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
from py_rigAssit.dialogs import Help, mayaPrint
from Utils import sdk_info
from Utils.undo import undo

import maya.cmds as cmds

PY_WIDGEAT = Widgets()


class AxisRow(QtWidgets.QWidget):
    def __init__(self, label):
        super(AxisRow, self).__init__()
        self.layout = QtWidgets.QHBoxLayout(self)

        self.layout.addWidget(QtWidgets.QLabel(label))

        self.axes = {}
        for axis in ["X", "Y", "Z"]:
            cb = QtWidgets.QCheckBox(axis)
            combo = QtWidgets.QComboBox()
            combo.addItems(["same", "reverse"])
            combo.setEnabled(False)

            cb.toggled.connect(combo.setEnabled)

            self.layout.addWidget(cb)
            self.layout.addWidget(combo)

            self.axes[axis] = (cb, combo)

    def get_values(self):
        data = {}
        for axis, (cb, combo) in self.axes.items():
            if cb.isChecked():
                data[axis] = combo.currentText()
        return data


class PYMirrorSDKMainUI(PyouPersistentWindow):
    MAP = {1: [("Search Prefix:", "L_"), ("Replace Prefix:", "R_")],
         2: [("Search Middle:", "_L_"), ("Replace Middle:", "_R_")],
         3: [("Search Suffix:", "_L"), ("Replace Suffix:", "_R")]
         }

    def __init__(self, parent=PY_WIDGEAT.maya_main_window()):
        super(PYMirrorSDKMainUI, self).__init__("MirrorSDKMainApp", "MirrorSDKMainUI",parent=parent)
        self.window_name = "SDK Manager"
        self.setWindowTitle(self.window_name)
        self.setMinimumWidth(280)
        self.init_ui(True)
        self.loadWindowSettings()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocus()

    def init_ui(self, copyright=False):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(8, 0, 8, 8)
        main_layout.setSpacing(0)
        main_layout.addWidget(PY_WIDGEAT.create_title(self.window_name, 16, None))

        frame_button_op = PY_WIDGEAT.create_collapsible_frame(u"Export/Import Node", True)
        group_node = QtWidgets.QGroupBox(u"Export/Import Node:")
        _layout = QtWidgets.QVBoxLayout(group_node)
        btn_layout = QtWidgets.QHBoxLayout(group_node)
        frame_button_op.addWidget(group_node)

        self.time_ignore_chx = QtWidgets.QCheckBox(u' 忽略时间关键帧')
        self.time_ignore_chx.setChecked(True)

        self.export_node_btn = QtWidgets.QPushButton('Export Node')
        self.import_node_btn = QtWidgets.QPushButton('Import/Create Node')
        self.node_help_btn = QtWidgets.QPushButton()
        self.node_help_btn.setIcon(QtGui.QIcon(":\help.png"))
        self.export_node_btn.setProperty("main", True)
        self.import_node_btn.setProperty("main", True)
        self.node_help_btn.setProperty("help", True)
        self.export_node_btn.setToolTip(u"选择sdk节点导出数据")
        self.import_node_btn.setToolTip(u"导入sdk数据")
        btn_layout.addWidget(self.export_node_btn, 5)
        btn_layout.addWidget(self.import_node_btn, 5)
        btn_layout.addWidget(self.node_help_btn)

        _layout.addWidget(PY_WIDGEAT.create_text(u'文件路径 "C:/Users/Administrator/Documents/maya/Data_py/create_sdk_info_py.json"'))
        _layout.addWidget(self.time_ignore_chx)
        _layout.addLayout(btn_layout)

        self.export_node_btn.clicked.connect(self.export_node_data)
        self.import_node_btn.clicked.connect(sdk_info.create_sdk_node)

        group = QtWidgets.QGroupBox(u"Search Name:")
        layout = QtWidgets.QVBoxLayout(group)
        search_layout = QtWidgets.QHBoxLayout()

        self.search_type_group = PY_WIDGEAT.create_radiogroup(
            "Type:",
            [
                ("prefix", 1, None),
                ("middle", 2, None),
                ("suffix", 3, None),
            ],
            default_id=1
        )
        search_layout.addWidget(self.search_type_group)

        layout.addLayout(search_layout)
        self.search_type_group.idClicked.connect(self._optional_type_Toggled)

        prefix_layout = QtWidgets.QHBoxLayout()
        self.search_label = QtWidgets.QLabel("Search prefix:")
        self.search_le = QtWidgets.QLineEdit("L_")
        prefix_layout.addWidget(self.search_label)
        prefix_layout.addWidget(self.search_le)
        self.replace_label = QtWidgets.QLabel("Replace prefix:")
        self.replace_le = QtWidgets.QLineEdit("R_")
        prefix_layout.addWidget(self.replace_label)
        prefix_layout.addWidget(self.replace_le)

        main_layout.addWidget(frame_button_op)
        layout.addLayout(prefix_layout)
        layout.addWidget(PY_WIDGEAT.create_text("* 请确保驱动者和被驱动者查询的字符串一致"))
        main_layout.addWidget(PY_WIDGEAT.create_text("Mirror SDK Tool"))
        main_layout.addWidget(group, 1)
        PY_WIDGEAT.separator(main_layout, True)

        main_layout.addWidget(PY_WIDGEAT.create_text(">> same 是相同的值; reverse 是相反的值"))

        self.translate_row = AxisRow("translate:")
        self.rotate_row = AxisRow("     rotate:")
        self.scale_row = AxisRow("      scale:")
        main_layout.addWidget(self.translate_row, alignment=QtCore.Qt.AlignRight)
        main_layout.addWidget(self.rotate_row, alignment=QtCore.Qt.AlignRight)
        main_layout.addWidget(self.scale_row, alignment=QtCore.Qt.AlignRight)

        main_layout.addStretch()
        main_layout.addWidget(PY_WIDGEAT.create_text("1. 先选择好需要镜像的属性  2. 选择拷贝源对象"))

        button_layout = QtWidgets.QHBoxLayout()
        self.apply_btn = QtWidgets.QPushButton("Apply")
        help_btn = QtWidgets.QPushButton()
        help_btn.setIcon(QtGui.QIcon(":/help.png"))
        self.apply_btn.setProperty("main", True)
        help_btn.setProperty("help", True)
        button_layout.addWidget(self.apply_btn, 9)
        button_layout.addWidget(help_btn)
        help_btn.clicked.connect(partial(Help.HelpImage, "", "mirror_sdk_tool_use"))
        self.apply_btn.clicked.connect(self.apply_mirror_sdk)
        main_layout.addLayout(button_layout)
        if copyright:
            PY_WIDGEAT.create_copyrightText(main_layout, "2024-2026")

        return main_layout

    def _optional_type_Toggled(self, btn_id):
        self.search_label.setText(self.MAP[btn_id][0][0])
        self.search_le.setText(self.MAP[btn_id][0][1])
        self.replace_label.setText(self.MAP[btn_id][1][0])
        self.replace_le.setText(self.MAP[btn_id][1][1])


    def get_flat_values(self):
        result = {}
        mapping = {
            "translate": "t",
            "rotate": "r",
            "scale": "s"
        }

        for name, row in [
            ("translate", self.translate_row),
            ("rotate", self.rotate_row),
            ("scale", self.scale_row)
        ]:
            for axis, val in row.get_values().items():
                # result[mapping[name] + axis.lower()] = 1 if val == "same" else -1
                result[mapping[name] + axis.lower()] = "+" if val == "same" else "-"

        return result

    def export_node_data(self):
        ignore = self.time_ignore_chx.isChecked()
        sdk_info.save_create_sdk_node(ignore)

    @undo
    def apply_mirror_sdk(self):
        data = self.get_flat_values()
        checked_type = self.search_type_group.checkedId()
        search_field = self.search_le.text()
        replace_field = self.replace_le.text()

        sels = cmds.ls(sl=1)

        if sels:
            from Utils.attr_name import PyAttrUtils
            _attr_name = PyAttrUtils()

            for i in sels:
                name = i.split(".")[0]
                map = {search_field: replace_field}
                mirror_obj = _attr_name.mirror_specify_name(name, map, replace_type=checked_type)

                if mirror_obj == None or mirror_obj == "":
                    mayaPrint.warning("{} Check if the searched characters are correct, skip.".format(search_field))
                    continue

                elif not cmds.objExists(mirror_obj):
                    mayaPrint.warning("{} > The object does not exist, skip.".format(mirror_obj))
                    continue

                for attr, value in data.items():
                    object_attr = "{}.{}".format(name, attr)
                    mirror_obj_attr = "{}.{}".format(mirror_obj, attr)
                    sdk_info.mirror_sdk(object_attr, mirror_obj_attr, value, search=search_field,replace=replace_field, replace_type=checked_type)
                    mayaPrint.log("mirror: {} {}".format(object_attr, mirror_obj_attr))

            Help.end_popDialog()
        else:
            mayaPrint.warning("no object seleted!")

    def on_apply(self):
        data = self.get_flat_values()
        print(data)

def main():
    global pyMirrorSDK_ui

    try:
        pyMirrorSDK_ui.close()  # pylint: disable=E0601
        pyMirrorSDK_ui.deleteLater()
    except:
        pass

    pyMirrorSDK_ui = PYMirrorSDKMainUI()
    pyMirrorSDK_ui.show()


if __name__ == '__main__':

    main()
