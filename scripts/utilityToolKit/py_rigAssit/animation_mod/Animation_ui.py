# -*- coding: utf-8 -*-

# .FileName: Animation_ui.py
# .@Author : Yolanda Ping (You P)
# .Email : yolandaping1224@gmail.com
# .Date....: 2025/11/8 16:45
# Qt wrapper for Maya 2017–2026
import os
from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
import ConstrainEdit.anim_nodes_data as ani_info
# import Utils.Decorator as Decorator
import maya.cmds as cmds

_widgest = Widgets()
_animation_ui_instance = None


class AnimationUI(PyouPersistentWindow):
    web = "https://www.bilibili.com/video/BV1PY84z6EJw/?share_source=copy_web&vd_source=7b50d73ef3e3d9c8d5f26b106034eb71"


    def __init__(self, parent=_widgest.maya_main_window()):
        super(AnimationUI, self).__init__("AnimationUIApp", "AnimationUI", parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.WINDOW_NAME = u"动画文件数据导出/导入"
        self.timeStamp = "2025-2026"
        self.label_width = 120
        self.setWindowTitle(self.WINDOW_NAME)

        self.export_namespace_field = None
        self.replace_namespace_field = None
        self.search_old_name_field = None
        self.replace_new_name_field = None

        self.init_ui()

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocus()
        self.loadWindowSettings()

    def create_input_row(self, label_text, placeholder="", default_text=""):
        layout = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel(label_text)
        label.setFixedWidth(self.label_width)
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        line_edit = QtWidgets.QLineEdit(default_text)
        if placeholder:
            line_edit.setPlaceholderText(placeholder)
        line_edit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        layout.addWidget(label)
        layout.addWidget(line_edit)
        return layout, line_edit

    def create_file_input_row(self, label_text, button_text, default_text=""):
        layout = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel(label_text)
        label.setFixedWidth(self.label_width)
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        line_edit = QtWidgets.QLineEdit(default_text)
        line_edit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        browse_btn = QtWidgets.QPushButton()
        browse_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        browse_btn.setToolTip(button_text)

        layout.addWidget(label)
        layout.addWidget(line_edit)
        layout.addWidget(browse_btn)
        return layout, line_edit, browse_btn

    def create_namespace_row(self, label_text, default_text=""):
        layout = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel(label_text)
        label.setFixedWidth(self.label_width)
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        line_edit = QtWidgets.QLineEdit(default_text)
        line_edit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        load_btn = QtWidgets.QPushButton(u"Load")
        load_btn.setFixedWidth(50)
        load_btn.setToolTip(u"从当前选择对象获取 Namespace")

        layout.addWidget(label)
        layout.addWidget(line_edit)
        layout.addWidget(load_btn)
        return layout, line_edit, load_btn

    def get_namespace_from_selection(self):
        sel = cmds.ls(sl=True, long=False)
        if not sel:
            return None

        name = sel[0]
        if ":" in name:
            return name.rsplit(":", 1)[0] + ":"
        return ""

    def load_namespace_to_field(self, field):
        ns = self.get_namespace_from_selection()
        if ns is None:
            QtWidgets.QMessageBox.warning(self, u"警告", u"请先选择一个对象")
            return
        field.setText(ns)

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(_widgest.create_title(self.WINDOW_NAME, 15, self.web))
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(8, 8, 8, 8)
        export_grp = QtWidgets.QGroupBox("> 导出模块:")
        export_grp.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        export_layout = QtWidgets.QVBoxLayout(export_grp)

        export_file_layout, self.export_namespace_field, export_load_btn = \
            self.create_namespace_row("export Namespace:")

        # Export path
        export_path_layout, self.export_path_field, export_browse_btn = \
            self.create_file_input_row("Export Path:", "Browse")

        export_btn = QtWidgets.QPushButton(u"Export Data")
        export_btn.setProperty("main", True)

        import_grp = QtWidgets.QGroupBox("> 导入模块:")
        import_grp.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        import_file_layout, self.import_file_field, import_browse_btn = \
            self.create_file_input_row("Import File:", "Select File")

        replace_layout, self.replace_namespace_field, replace_load_btn = \
            self.create_namespace_row("replace Namespace:")

        search_old_layout, self.search_old_name_field = \
            self.create_input_row("search suffix:")

        replace_new_layout, self.replace_new_name_field = \
            self.create_input_row("replace suffix:")

        import_btn = QtWidgets.QPushButton(u"Import Data")
        import_btn.setProperty("main", True)

        export_layout.addWidget(_widgest.create_text(">*选择导出对象自动读取 Namespace"))
        export_layout.addLayout(export_file_layout)
        export_layout.addLayout(export_path_layout)
        export_layout.addWidget(export_btn)
        main_layout.addWidget(export_grp)
        # _widgest.separator(main_layout, True)
        import_layout = QtWidgets.QVBoxLayout(import_grp)
        import_layout.addLayout(import_file_layout)
        import_layout.addWidget(_widgest.create_text(u">*如果导入对象和导出的不是一个，选择导入对象自动读取 Namespace"))
        import_layout.addLayout(replace_layout)
        _widgest.separator(import_layout, True)
        import_layout.addWidget(_widgest.create_text(u">如果导入数据的控制器后缀不一样，写入替换"))
        import_layout.addLayout(search_old_layout)
        import_layout.addLayout(replace_new_layout)
        _widgest.separator(import_layout, True)
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(import_btn)
        import_layout.addLayout(button_layout)
        main_layout.addWidget(import_grp)

        main_layout.addStretch()

        _widgest.create_copyrightText(main_layout, self.timeStamp)

        export_load_btn.clicked.connect(
            lambda: self.load_namespace_to_field(self.export_namespace_field)
        )
        export_browse_btn.clicked.connect(self.browse_export_path)
        export_btn.clicked.connect(self.export_data)
        replace_load_btn.clicked.connect(
            lambda: self.load_namespace_to_field(self.replace_namespace_field)
        )
        import_browse_btn.clicked.connect(self.browse_import_file)
        import_btn.clicked.connect(self.import_data)

    def get_search_prx_from_file(self, filepath):
        filename = os.path.basename(filepath)
        name, _ = os.path.splitext(filename)
        return name.replace("_anim", "") + ":"

    def browse_export_path(self):

        search_prx = self.export_namespace_field.text()
        default_name = "{}_anim.json".format(search_prx.rsplit(":", 1)[0])

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, u"选择导出路径", default_name, "JSON Files (*.json)"
        )
        if file_path:
            self.export_path_field.setText(file_path)

    def browse_import_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, u"选择导入文件", "", "JSON Files (*.json)"
        )
        if file_path:
            self.import_file_field.setText(file_path)

    def export_data(self):
        search_prx = self.export_namespace_field.text()
        export_path = self.export_path_field.text()

        if not search_prx:
            QtWidgets.QMessageBox.warning(self, u"警告", u"请填写导出对象的命名空间")
            return

        if not export_path:
            QtWidgets.QMessageBox.warning(self, u"警告", u"请选择导出路径")
            return

        print("----------------------------", search_prx, export_path)

        try:

            ani_info.store_animKey_data(chr_prx=search_prx, filepath=export_path)
            QtWidgets.QMessageBox.information(self, u"成功", u"数据导出成功！")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, u"错误", u"导出失败：{}".format(str(e)))

   
    def import_data(self):
        import_file = self.import_file_field.text()
        search_prx = self.get_search_prx_from_file(import_file)

        try:
            ani_info.import_animKey_data(
                search_prx=search_prx,
                replace_prx=self.replace_namespace_field.text(),
                old_name=self.search_old_name_field.text(),
                new_name=self.replace_new_name_field.text(),
                filepath=import_file
            )
            QtWidgets.QMessageBox.information(self, u"成功", u"数据导入成功！")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, u"错误", u"导入失败：{}".format(str(e)))

def main():
    global py_Animation_ui

    try:
        py_Animation_ui.close()  # pylint: disable=E0601
        py_Animation_ui.deleteLater()
    except:
        pass

    py_Animation_ui = AnimationUI()
    py_Animation_ui.show()


if __name__ == "__main__":
    main()
