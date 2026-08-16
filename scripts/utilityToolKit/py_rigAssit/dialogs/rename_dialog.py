# -*- coding: utf-8 -*-

# .FileName:rename_dialog.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2025/11/14 23:52
# .Finish time:
from functools import partial

import re

from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
from AttrNameUtils import PyAttrUtils
import GeneralTools.pyRenameFun as pyRename
import user_defined as _user
import HelpImageUI as _help

import pymel.core as pm


__PyAttrUtils__ = PyAttrUtils()
PY_WIDGEAT = Widgets()


class PYRenameQWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(PYRenameQWidget, self).__init__(parent)
        self.window_name = 'Rename Box'

    def init_ui(self):
        container = QtWidgets.QWidget()
        container.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        main_layout = QtWidgets.QVBoxLayout(container)
        main_layout.setContentsMargins(8, 0, 8, 4)
        main_layout.setSpacing(0)

        self.create_rename_tool_section(main_layout)
        self.create_search_replace_section(main_layout)
        main_layout.addStretch()

        self.create_connections()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocus()
        return container

    def create_rename_tool_section(self, parent_layout):
        group = QtWidgets.QGroupBox(u"Rename :")
        layout = QtWidgets.QVBoxLayout(group)
        type_layout = QtWidgets.QHBoxLayout()
        type_layout.addWidget(PY_WIDGEAT.create_text("Type: "))
        self.type_radio_group = PY_WIDGEAT.create_radiogroup(
            "",
            [("Selected ", 1, u"选择"),
             ("Heirarchy ", 2, u"层级")],
            default_id=1
        )

        layout.addLayout(type_layout)
        type_layout.addWidget(self.type_radio_group, 1)

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
        hash_rename_layout, self.hash_name_filed, self.hash_rename_btn = PY_WIDGEAT.create_QLineEdit_row("Hash Rename:",
                                                                                                         label_width=78)
        self.hash_name_filed.setPlaceholderText("name_###1_bind")
        self.hash_rename_btn.setText("Apply")
        self.hash_name_filed.setToolTip(u'name_###1_bind > name_001_bind\n(###代表Padding， 1代表Start数值，开始值也可为0）')
        layout.addLayout(hash_rename_layout)

        PY_WIDGEAT.separator(layout, True)
        layout.addWidget(PY_WIDGEAT.create_text("renaming"))
        # Form layout for rename fields
        form_layout = QtWidgets.QGridLayout()
        form_layout.setVerticalSpacing(1)
        form_layout.setHorizontalSpacing(1)

        # Prefix
        form_layout.addWidget(PY_WIDGEAT.create_text("Prefix:"), 0, 0)
        self.prefix_field = QtWidgets.QLineEdit()
        # self.prefix_field.textEdited.connect(self.add_prefix)
        form_layout.addWidget(self.prefix_field, 0, 1)

        self.prefix_btn = QtWidgets.QPushButton("add Prefix")
        form_layout.addWidget(self.prefix_btn, 0, 2)

        # Increment
        form_layout.addWidget(PY_WIDGEAT.create_text("Inc:"), 1, 0)
        self.start_number_field = QtWidgets.QSpinBox()
        self.start_number_field.setMinimum(0)
        self.start_number_field.setMaximum(999)
        self.start_number_field.setValue(1)
        form_layout.addWidget(self.start_number_field, 1, 1)

        self.inc_btn = QtWidgets.QPushButton("add Inc")
        form_layout.addWidget(self.inc_btn, 1, 2)

        # Suffix
        form_layout.addWidget(PY_WIDGEAT.create_text("Suffix:"), 2, 0)
        self.suffix_field = QtWidgets.QLineEdit(_user.suffix)
        form_layout.addWidget(self.suffix_field, 2, 1)

        self.suffix_btn = QtWidgets.QPushButton("add Suffix")
        form_layout.addWidget(self.suffix_btn, 2, 2)

        # Name
        form_layout.addWidget(PY_WIDGEAT.create_text("Name:"), 3, 0)
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
        form_layout.setVerticalSpacing(1)
        form_layout.setHorizontalSpacing(1)

        form_layout.addWidget(PY_WIDGEAT.create_text("Search:"), 0, 0)
        self.search_field = QtWidgets.QLineEdit()
        form_layout.addWidget(self.search_field, 0, 1)

        form_layout.addWidget(PY_WIDGEAT.create_text("Replace:"), 0, 2)
        self.replace_field = QtWidgets.QLineEdit()
        form_layout.addWidget(self.replace_field, 0, 3)

        self.search_replace_btn = QtWidgets.QPushButton("Apply")
        self.search_replace_btn.setProperty("main", True)

        layout.addLayout(form_layout)
        layout.addWidget(self.search_replace_btn)
        parent_layout.addWidget(group)

    def create_connections(self):
        self.remove_prefix_btn.clicked.connect(partial(self.remove_prefix_or_suffix, True))
        self.remove_suffix_btn.clicked.connect(partial(self.remove_prefix_or_suffix, False))
        self.remove_first_btn.clicked.connect(partial(pyRename.py_remove_FirstChr))
        self.remove_last_btn.clicked.connect(partial(pyRename.py_remove_LastChr))
        self.hash_name_filed.returnPressed.connect(self.hash_rename)
        self.hash_rename_btn.clicked.connect(self.hash_rename)
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
        pm.undoInfo(openChunk=True)
        try:
            pyRename.rename(
                Mode=mode,
                select_type=self.type_radio_group.checkedId(),
                prefix=self.prefix_field.text(),
                Inc=self.start_number_field.value(),
                suffix=self.suffix_field.text()
            )
        finally:
            pm.undoInfo(closeChunk=True)

    def _rename_apply(self):
        pm.undoInfo(openChunk=True)
        try:
            pyRename.rename(
                Mode=4,
                select_type=self.type_radio_group.checkedId(),
                prefix=self.prefix_field.text(),
                Inc=self.start_number_field.value(),
                suffix=self.suffix_field.text(),
                fullName=self.full_name_field.text()
            )
        finally:
            pm.undoInfo(closeChunk=True)

    def _add_prefix(self):
        selection = pm.ls(sl=True)
        prefix = self.prefix_field.text()
        pm.undoInfo(openChunk=True)
        try:
            for each in selection:
                new_name = prefix + '_' + each
                pm.rename(each, new_name)
        finally:
            pm.undoInfo(closeChunk=True)

    def _rename(self):
        prefix = self.prefix_field.text()
        name = self.full_name_field.text()
        increment = self.start_number_field.value()
        suffix = self.suffix_field.text()
        if prefix != '':
            prefix = prefix + '_'
        if suffix != '':
            suffix = '_' + suffix

        sel = pm.ls(sl=True)
        pm.undoInfo(openChunk=True)
        try:
            if self.type_radio_group.checkedId() == 1:
                selection = sel
            else:
                selection = self._get_heirarchy(sel)
            for individual_object in selection:
                if increment is not None:
                    number = str(increment)
                    increment += 1
                new_name = (prefix + name + number + suffix)
                pm.rename(individual_object, new_name)
        finally:
            pm.undoInfo(closeChunk=True)

    def hash_rename(self):
        """
        name: e.g. "aaa_test_###1_bind"
        """
        name = self.hash_name_filed.text()
        sel = pm.ls(sl=True, l=True) or []
        if not sel:
            return []
        m = re.search(r"(#+)(\d+)", name)
        if not m:
            raise RuntimeError("Format error: name_###1_bind > name_001_bind")

        token = m.group(1)
        pad = len(token)
        idx = int(m.group(2))
        fmt = "%0{}d".format(pad)
        pattern = name.replace(token + m.group(2), fmt)

        targets = []
        if self.type_radio_group.checkedId() == 1:
            targets = sel
        else:
            targets = self._get_heirarchy(sel)

        pm.undoInfo(openChunk=True)
        try:
            result = []
            for obj in targets:
                if not pm.objExists(obj):
                    continue
                new_name = pattern % idx
                result.append(pm.rename(obj, new_name))
                idx += 1
        finally:
            pm.undoInfo(closeChunk=True)
        return result

    def _add_suffix(self):
        selection = pm.ls(sl=True)
        suffix = self.suffix_field.text()
        pm.undoInfo(openChunk=True)
        try:
            for individual_object in selection:
                new_name = individual_object + '_' + suffix
                pm.rename(individual_object, new_name)
        finally:
            pm.undoInfo(closeChunk=True)

    def search_fieldReplace(self):
        replace_method = self.type_radio_group.checkedId()
        search_text = self.search_field.text()
        replace_text = self.replace_field.text()

        pm.undoInfo(openChunk=True)
        try:
            sel = pm.ls(sl=True)
            if replace_method == 1:
                selection = sel
            else:
                selection = self._get_heirarchy(sel)

            for individual_object in selection:
                new_name = individual_object.replace(search_text, replace_text)
                pm.rename(individual_object, new_name)
        finally:
            pm.undoInfo(closeChunk=True)

    def remove_prefix_or_suffix(self, is_prefix=True):
        replace_method = self.type_radio_group.checkedId()
        selection = pm.ls(sl=True)

        pm.undoInfo(openChunk=True)
        try:
            for individual_object in selection:
                if replace_method == 2:
                    children = pm.listRelatives(individual_object.strip(), ad=True, type='transform')
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
            pm.undoInfo(closeChunk=True)

        return

    def remove_prefix_from_object(self, obj="", prefix=""):
        pm.undoInfo(openChunk=True)

        try:
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
                pm.rename(obj.strip(), new_name.strip())
        finally:
            pm.undoInfo(closeChunk=True)

    def remove_suffix_from_object(self, obj="", suffix=""):
        if suffix == "":
            suffix = __PyAttrUtils__.get_suffix_name(obj)
            if suffix != []:
                suffix = suffix[0]
            else:
                suffix == ""

        if suffix == "" or suffix is None or suffix == []:
            return
        pm.undoInfo(openChunk=True)

        try:
            if obj.endswith(suffix):
                new_name = obj[:-len(suffix)]
                pm.rename(obj.strip(), new_name.strip())
        finally:
            pm.undoInfo(closeChunk=True)

    def _get_heirarchy(self, sel):
        from Utils import Util as _utils
        return _utils.get_hierarchy_outliner(sel)


class PYRenameBox(PyouPersistentWindow):
    def __init__(self, parent=PY_WIDGEAT.maya_main_window()):
        super(PYRenameBox, self).__init__("PYRenameBox", "PYRenameBox", parent)

        self.timeStamp = '2022-2026'
        self.window_name = 'Rename Box'
        self.setWindowTitle(self.window_name)
        self._build_ui()
        self.loadWindowSettings()

    def _build_ui(self):
        main = QtWidgets.QVBoxLayout(self)
        main.setContentsMargins(8, 0, 8, 8)
        main.setSpacing(4)

        main.addWidget(PY_WIDGEAT.create_title(self.window_name, 15, None))
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setContentsMargins(0, 0, 0, 0)

        cld_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(cld_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(4)

        scroll.setWidget(cld_widget)
        main.addWidget(scroll)

        self.widget = PYRenameQWidget(parent=self)

        self.create_check_scene_rename_section(scroll_layout)
        scroll_layout.addWidget(self.widget.init_ui())
        PY_WIDGEAT.create_copyrightText(main, "2023-2026")

    def create_check_scene_rename_section(self, parent_layout):
        self.frame_button_op = PY_WIDGEAT.create_collapsible_frame(u"Check Scene Name 检查场景重名")
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(2, 0, 2, 0)
        layout.addWidget(PY_WIDGEAT.create_text(u">>> Check all renamed objects in the scene\n检查场景是否存在重命名的对象"))

        button_layout = QtWidgets.QHBoxLayout()
        check_scene_btn = QtWidgets.QPushButton(u"Check Scene Name 检查场景重名")
        check_scene_btn.setProperty("main", True)
        help_btn = QtWidgets.QPushButton()
        help_btn.setIcon(QtGui.QIcon(":/help.png"))
        help_btn.setProperty("help", True)

        button_layout.addWidget(check_scene_btn, 9)
        button_layout.addWidget(help_btn, 1)
        layout.addLayout(button_layout)
        self.frame_button_op.addLayout(layout)
        check_scene_btn.clicked.connect(partial(pyRename.check_scene_name))
        help_btn.clicked.connect(partial(_help.HelpImage, "", "rename_Tool"))
        parent_layout.addWidget(self.frame_button_op)


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