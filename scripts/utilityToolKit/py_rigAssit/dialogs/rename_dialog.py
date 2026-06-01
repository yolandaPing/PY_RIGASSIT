# -*- coding: utf-8 -*-

# .FileName:rename_dialog.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2025/11/14 23:52
# .Finish time:
from functools import partial

from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
from AttrNameUtils import PyAttrUtils
import GeneralTools.pyRenameFun as pyRename
import user_defined as _user
import HelpImageUI as _help
import maya.cmds as cmds
import pymel.core as pm


__PyAttrUtils__ = PyAttrUtils()
PY_WIDGEAT = Widgets()


class PYRenameBox(PyouPersistentWindow):
    def __init__(self, parent=PY_WIDGEAT.maya_main_window()):
        super(PYRenameBox, self).__init__("PYRenameBox", "PYRenameBox", parent)

        self.timeStamp = '2022-2026'
        self.window_name = 'Rename Box'

        self.setup_ui(True)
        self.loadWindowSettings()


    def setup_ui(self, copyright=False):
        self.setWindowTitle(self.window_name)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(PY_WIDGEAT.create_title(self.window_name, 16, 30))
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        self.create_check_scene_rename_section(main_layout)
        self.create_rename_tool_section(main_layout)
        self.create_search_replace_section(main_layout)
        main_layout.addStretch()
        if copyright:
            PY_WIDGEAT.create_copyrightText(main_layout, self.timeStamp)

        self.create_connections()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocus()
        return main_layout

    def create_check_scene_rename_section(self, parent_layout):
        self.frame_button_op = PY_WIDGEAT.create_collapsible_frame(u"Check Scene Name 检查场景重名")
        # group = QtWidgets.QGroupBox(u"Check Scene Name 检查场景重名:")
        layout = QtWidgets.QVBoxLayout()
        # layout.setContentsMargins(2, 2, 2, 2)
        layout.addWidget(PY_WIDGEAT.create_text(u">>> Check all renamed objects in the scene\n检查场景是否存在重命名的对象"))

        button_layout = QtWidgets.QHBoxLayout()
        self.check_scene_btn = QtWidgets.QPushButton(u"Check Scene Name 检查场景重名")
        self.check_scene_btn.setProperty("main", True)
        self.help_btn = QtWidgets.QPushButton()
        self.help_btn.setIcon(QtGui.QIcon(":/help.png"))
        self.help_btn.setProperty("help", True)

        button_layout.addWidget(self.check_scene_btn, 9)
        button_layout.addWidget(self.help_btn, 1)
        layout.addLayout(button_layout)
        self.frame_button_op.addLayout(layout)
        parent_layout.addWidget(self.frame_button_op)

    def create_rename_tool_section(self, parent_layout):
        group = QtWidgets.QGroupBox(u"Rename Tool 命名:")
        layout = QtWidgets.QVBoxLayout(group)
        layout.addWidget(PY_WIDGEAT.create_text(u"Rename type 重命名的方式"))

        self.type_radio_group = QtWidgets.QButtonGroup()
        self.selected_radio = QtWidgets.QRadioButton(u"Selected 选择的")
        self.hierarchy_radio = QtWidgets.QRadioButton(u"Heirarchy 层级")
        self.selected_radio.setChecked(True)

        self.type_radio_group.addButton(self.selected_radio, 1)
        self.type_radio_group.addButton(self.hierarchy_radio, 2)

        radio_layout = QtWidgets.QHBoxLayout()
        radio_layout.addWidget(QtWidgets.QLabel("Type :"))
        radio_layout.addWidget(self.selected_radio)
        radio_layout.addWidget(self.hierarchy_radio)
        layout.addLayout(radio_layout)

        PY_WIDGEAT.separator(layout, True)
        layout.addWidget(QtWidgets.QLabel("> Quick replacement:"))

        quick_btn_layout1 = QtWidgets.QHBoxLayout()
        quick_btn_layout2 = QtWidgets.QHBoxLayout()
        self.remove_prefix_btn = QtWidgets.QPushButton("Remove prefix ")
        self.remove_suffix_btn = QtWidgets.QPushButton("Remove suffix ")
        self.remove_first_btn = QtWidgets.QPushButton("Remove First Chr ")
        self.remove_last_btn = QtWidgets.QPushButton("Remove Last Chr ")
        self.remove_prefix_btn.setToolTip(u'移除前缀')
        self.remove_suffix_btn.setToolTip(u'移除后缀')
        self.remove_first_btn.setToolTip(u'移除第一个对象')
        self.remove_last_btn.setToolTip(u'移除最后一个对象')

        quick_btn_layout1.addWidget(self.remove_prefix_btn)
        quick_btn_layout1.addWidget(self.remove_suffix_btn)
        quick_btn_layout2.addWidget(self.remove_first_btn)
        quick_btn_layout2.addWidget(self.remove_last_btn)
        layout.addLayout(quick_btn_layout1)
        layout.addLayout(quick_btn_layout2)
        PY_WIDGEAT.separator(layout, True)
        layout.addWidget(PY_WIDGEAT.create_text("Renaming"))

        # Form layout for rename fields
        form_layout = QtWidgets.QGridLayout()
        form_layout.setVerticalSpacing(5)
        form_layout.setHorizontalSpacing(5)

        # Prefix
        form_layout.addWidget(QtWidgets.QLabel("Prefix:"), 0, 0)
        self.prefix_field = QtWidgets.QLineEdit()
        # self.prefix_field.textEdited.connect(self.add_prefix)
        form_layout.addWidget(self.prefix_field, 0, 1)

        self.prefix_btn = QtWidgets.QPushButton("add Prefix")
        form_layout.addWidget(self.prefix_btn, 0, 2)

        # Increment
        form_layout.addWidget(QtWidgets.QLabel("Inc:"), 1, 0)
        self.start_number_field = QtWidgets.QSpinBox()
        self.start_number_field.setMinimum(0)
        self.start_number_field.setMaximum(999)
        self.start_number_field.setValue(1)
        form_layout.addWidget(self.start_number_field, 1, 1)

        self.inc_btn = QtWidgets.QPushButton("add Inc")
        form_layout.addWidget(self.inc_btn, 1, 2)

        # Suffix
        form_layout.addWidget(QtWidgets.QLabel("Suffix:"), 2, 0)
        self.suffix_field = QtWidgets.QLineEdit(_user.suffix)
        form_layout.addWidget(self.suffix_field, 2, 1)

        self.suffix_btn = QtWidgets.QPushButton("add Suffix")
        form_layout.addWidget(self.suffix_btn, 2, 2)

        # Name
        form_layout.addWidget(QtWidgets.QLabel("Name:"), 3, 0)
        self.full_name_field = QtWidgets.QLineEdit()
        form_layout.addWidget(self.full_name_field, 3, 1)

        self.rename_btn = QtWidgets.QPushButton("Rename")
        self.rename_btn.setProperty("main", True)
        form_layout.addWidget(self.rename_btn, 3, 2)

        layout.addLayout(form_layout)
        parent_layout.addWidget(group)

    def create_search_replace_section(self, parent_layout):
        group = QtWidgets.QGroupBox(u"Search Replace Options 搜索替换")
        layout = QtWidgets.QVBoxLayout(group)

        form_layout = QtWidgets.QGridLayout()
        form_layout.setVerticalSpacing(5)
        form_layout.setHorizontalSpacing(5)

        form_layout.addWidget(QtWidgets.QLabel("Search:"), 0, 0)
        self.search_field = QtWidgets.QLineEdit()
        form_layout.addWidget(self.search_field, 0, 1)

        form_layout.addWidget(QtWidgets.QLabel("Replace:"), 1, 0)
        self.replace_field = QtWidgets.QLineEdit()
        form_layout.addWidget(self.replace_field, 1, 1)

        apply_layout = QtWidgets.QHBoxLayout()
        self.hierarchy_option = QtWidgets.QComboBox()
        self.hierarchy_option.addItems(["Selected", "Heirarchy"])
        self.search_replace_btn = QtWidgets.QPushButton("Apply")
        self.search_replace_btn.setProperty("main", True)

        apply_layout.addWidget(QtWidgets.QLabel("Type:"), 1)
        apply_layout.addWidget(self.hierarchy_option, 1)
        apply_layout.addWidget(self.search_replace_btn, 5)

        layout.addLayout(form_layout)
        layout.addLayout(apply_layout)
        parent_layout.addWidget(group)


    def create_connections(self):
        self.check_scene_btn.clicked.connect(partial(pyRename.check_scene_name))
        self.help_btn.clicked.connect(partial(_help.HelpImage, "", "rename_Tool"))

        self.remove_prefix_btn.clicked.connect(partial(self.remove_prefix_or_suffix, True))
        self.remove_suffix_btn.clicked.connect(partial(self.remove_prefix_or_suffix, False))

        self.remove_first_btn.clicked.connect(partial(pyRename.py_remove_FirstChr))
        self.remove_last_btn.clicked.connect(partial(pyRename.py_remove_LastChr))

        self.prefix_field.returnPressed.connect(self._add_prefix)
        self.suffix_field.returnPressed.connect(self._add_suffix)
        # self.full_name_field.textEdited.connect(self._rename)
        self.full_name_field.returnPressed.connect(self._rename)
        self.prefix_btn.clicked.connect(partial(self._run_rename, 1))
        self.inc_btn.clicked.connect(partial(self._run_rename, 2))
        self.suffix_btn.clicked.connect(partial(self._run_rename, 3))
        self.rename_btn.clicked.connect(self._rename_apply)

        self.search_replace_btn.clicked.connect(self.search_fieldReplace)

    def getShortName(self, obj):
        ret = ""
        if obj == "":
            return ret
        else:
            parts = obj.split("|")
            cnt = len(parts)
            if cnt == 0:
                ret == obj
            else:
                ret = parts[cnt - 1]
            return ret

    def _run_rename(self, mode):
        pyRename.rename(
            Mode=mode,
            select_type=self.type_radio_group.checkedId(),
            prefix=self.prefix_field.text(),
            Inc=self.start_number_field.value(),
            suffix=self.suffix_field.text()
        )

    def _rename_apply(self):
        pyRename.rename(
            Mode=4,
            select_type=self.type_radio_group.checkedId(),
            prefix=self.prefix_field.text(),
            Inc=self.start_number_field.value(),
            suffix=self.suffix_field.text(),
            fullName=self.full_name_field.text()
        )

    def _add_prefix(self):
        selection = pm.ls(sl=True)
        prefix = self.prefix_field.text()
        for each in selection:
            new_name = prefix + '_' + each
            pm.rename(each, new_name)

    def _rename(self):
        selection = pm.ls(sl=True)
        prefix = self.prefix_field.text()
        name = self.full_name_field.text()
        increment = self.start_number_field.value()
        suffix = self.suffix_field.text()

        if prefix != '':
            prefix = prefix + '_'

        if suffix != '':
            suffix = '_' + suffix

        for individual_object in selection:
            if increment is not None:
                number = str(increment)
                increment += 1

            new_name = (prefix + name + number + suffix)
            pm.rename(individual_object, new_name)

    def _add_suffix(self):
        selection = pm.ls(sl=True)
        suffix = self.suffix_field.text()

        for individual_object in selection:
            new_name = individual_object + '_' + suffix
            pm.rename(individual_object, new_name)

    def search_fieldReplace(self):
        replace_method = self.hierarchy_option.currentIndex() + 1  # Convert to 1-based index
        search_text = self.search_field.text()
        replace_text = self.replace_field.text()

        if replace_method == 1:
            selection = pm.ls(sl=True)
        else:
            pm.select(hi=True)
            selection = pm.ls(sl=True)

        for individual_object in selection:
            new_name = individual_object.replace(search_text, replace_text)
            pm.rename(individual_object, new_name)

    def remove_prefix_or_suffix(self, is_prefix=True):
        replace_method = 1 if self.selected_radio.isChecked() else 2

        selection = cmds.ls(sl=True)

        cmds.undoInfo(openChunk=True)

        try:
            for individual_object in selection:
                if replace_method == 2:
                    children = cmds.listRelatives(individual_object.strip(), ad=True, type='transform')
                    if children:
                        for child in children:
                            if is_prefix:
                                self.remove_prefix_from_object(child)
                            else:
                                self.remove_suffix_from_object(child)
                if is_prefix:
                    self.remove_prefix_from_object(individual_object)
                else:
                    self.remove_suffix_from_object(individual_object)
        finally:
            cmds.undoInfo(closeChunk=True)

        return

    def remove_prefix_from_object(self, obj="", prefix=""):
        if prefix == "":
            prefix = __PyAttrUtils__.get_prefix_name(obj)
            if prefix != []:
                prefix = prefix[0]
            else:
                prefix == ""
        if prefix == "" or prefix is None or prefix == []:
            return

        if obj.startswith(prefix):
            new_name = obj[len(prefix):]
            cmds.rename(obj.strip(), new_name.strip())

    def remove_suffix_from_object(self, obj="", suffix=""):
        if suffix == "":
            suffix = __PyAttrUtils__.get_suffix_name(obj)
            if suffix != []:
                suffix = suffix[0]
            else:
                suffix == ""

        if suffix == "" or suffix is None or suffix == []:
            return

        if obj.endswith(suffix):
            new_name = obj[:-len(suffix)]
            cmds.rename(obj.strip(), new_name.strip())


def main():
    global pyRenameBox_ui

    try:
        pyRenameBox_ui.close()  # pylint: disable=E0601
        pyRenameBox_ui.deleteLater()
    except:
        pass

    pyRenameBox_ui = PYRenameBox()
    pyRenameBox_ui.show()


if __name__ == '__main__':

    main()