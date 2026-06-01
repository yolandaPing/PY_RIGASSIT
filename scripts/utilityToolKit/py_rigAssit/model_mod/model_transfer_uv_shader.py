# -*- coding: utf-8 -*-

# .FileName:model_transfer_uv_shader.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2025/7/21 20:00
# .Finish time:
# Qt wrapper for Maya 2017–2025
from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
from selectOrRemove import SelectOrremoveObj
import CopyEdit.copy_FFD_UV as copy_FFD_UV
import maya.cmds as cmds, maya.mel as mel, maya.OpenMaya as om


_widgest = Widgets()
_obj = SelectOrremoveObj()

projects = ("NONE", "")


def get_menu_item(item):
    return item


def reference_file_once(file_path, namespace="scr_m"):
    all_refs = cmds.file(q=True, r=True) or []
    if file_path.replace('\\', '/') not in [ref.replace('\\', '/') for ref in all_refs]:
        cmds.file(file_path, r=1, ignoreVersion=1, gl=1,
                  mergeNamespacesOnClash=False, namespace=namespace)
    else:
        print("// Info: File is already referenced.")


class TransferModelUI(PyouPersistentWindow):
    FILE_FILTERS = "Maya (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"

    selected_filter = "Maya (*ma *.mb)"

    def __init__(self, parent=_widgest.maya_main_window()):
        super(TransferModelUI, self).__init__("CleanModelFileApp", "TransferModelUI", parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.WINDOW_NAME = 'Model trandfer UV Shader '
        self.timeStamp = "2025-2026"
        self.name = "None"
        self._text_font = "font: bold 12px"

        self.setWindowTitle(self.WINDOW_NAME)

        self.init_ui()
        self.create_connections()
        self.loadWindowSettings()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocus()

    def init_ui(self):

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(_widgest.create_title(self.WINDOW_NAME, 15, 30))

        tle_layout = QtWidgets.QHBoxLayout(self)
        tle_layout.addWidget(_widgest.create_text(u" File: ", 15, "left"))

        self.filepath = QtWidgets.QLineEdit()
        self.References_button = QtWidgets.QPushButton()
        self.References_button.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.References_button.setToolTip("Select File")

        tle_layout.addWidget(self.filepath)
        tle_layout.addWidget(self.References_button)


        layout = QtWidgets.QVBoxLayout(self)

        self.file_layout(layout)
        self.model_scroll_layout(layout)

        main_layout.addLayout(tle_layout)
        main_layout.addLayout(layout)


        btn_layout = QtWidgets.QHBoxLayout()

        self.Check_button = QtWidgets.QPushButton("Check", self)
        self.Check_button.setFixedHeight(30)

        self.Apply_button = QtWidgets.QPushButton("Apply", self)
        self.Apply_button.setFixedHeight(30)

        self.Remove_button = QtWidgets.QPushButton("Remove File", self)
        self.Remove_button.setFixedHeight(30)

        btn_layout.addWidget(self.Check_button)
        btn_layout.addWidget(self.Apply_button)
        btn_layout.addWidget(self.Remove_button)
        main_layout.addLayout(btn_layout)

        _widgest.create_copyrightText(main_layout, self.timeStamp)

    def projects(self, parent):
        self.projects = QtWidgets.QComboBox()
        self.projects.addItems(projects)
        self.projects.setFixedWidth(80)
        self.projects.currentTextChanged.connect(get_menu_item)
        axis_layout = QtWidgets.QFormLayout()
        axis_layout.addRow(u'项目: ', self.projects)

        parent.addLayout(axis_layout)

    def file_layout(self, parent):
        layout = QtWidgets.QVBoxLayout()

        label = _widgest.create_text(u" 传递类型：", 12, "left")

        checkbox_layout = QtWidgets.QHBoxLayout()

        self.uv_check = QtWidgets.QCheckBox('UV')
        self.shader_check = QtWidgets.QCheckBox(' Shader')
        # self.uv_check.setStyleSheet("{}; ".format(self._text_font))
        # self.shader_check.setStyleSheet("{}; ".format(self._text_font))
        self.uv_check.setChecked(True)
        self.shader_check.setChecked(True)

        checkbox_layout.addWidget(label)
        checkbox_layout.addWidget(self.uv_check)
        checkbox_layout.addWidget(self.shader_check)

        layout.addLayout(checkbox_layout)
        parent.addLayout(layout)

    def set_layout_visible(self, layout, visible):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.setVisible(visible)

    def model_scroll_layout(self, parent):
        cheek_grp = QtWidgets.QGroupBox("> 检查模型:")
        cheek_grp.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout = QtWidgets.QVBoxLayout(cheek_grp)

        self.extra_list = QtWidgets.QLabel(u"")
        self.extra_list.setHidden(True)

        self.cls_layout = QtWidgets.QHBoxLayout()
        cls_rigging_vis_layout = QtWidgets.QVBoxLayout()

        cls_rigging_vis_layout.addWidget(QtWidgets.QLabel(u"> rigging model grp:"))

        self.rigging_model = QtWidgets.QLineEdit()
        self.rigging_model.setText("")
        self.rigging_model.setEnabled(True)

        cls_rigging_vis_layout.addWidget(self.rigging_model)

        self.rigging_model_scroll_list = QtWidgets.QListWidget(self)
        self.rigging_model_scroll_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        cls_rigging_vis_layout.addWidget(self.rigging_model_scroll_list)

        cls_scr_model_layout = QtWidgets.QVBoxLayout()
        cls_scr_model_layout.addWidget(QtWidgets.QLabel(u"> model grp:"))

        self.scr_model = QtWidgets.QLineEdit()
        self.scr_model.setText("")
        self.scr_model.setEnabled(True)

        cls_scr_model_layout.addWidget(self.scr_model)

        self.model_scroll_list = QtWidgets.QListWidget(self)
        self.model_scroll_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        cls_scr_model_layout.addWidget(self.model_scroll_list)
        self.cls_layout.addLayout(cls_scr_model_layout)
        self.cls_layout.addLayout(cls_rigging_vis_layout)

        # layout.addWidget(label)
        layout.addWidget(self.extra_list)
        layout.addLayout(self.cls_layout)

        self.set_layout_visible(self.cls_layout, False)

        parent.addWidget(cheek_grp)

    def topology_scroll_list(self, parent):
        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(_widgest.create_text(u" 拓扑检查", 12, "left"))
        _widgest.separator(layout, False)
        self.topology_scroll_list = QtWidgets.QListWidget()
        self.topology_scroll_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        layout.addWidget(self.topology_scroll_list)

        parent.addLayout(layout)

    def uv_scroll_list(self, parent):
        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(_widgest.create_text(u" UV检查", 12, "left"))
        _widgest.separator(layout, False)

        self.uv_scroll_list = QtWidgets.QListWidget()
        self.uv_scroll_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        layout.addWidget(self.uv_scroll_list)

        parent.addLayout(layout)

    def create_connections(self):
        self.References_button.clicked.connect(self.show_file_select_dialog)
        # self.check_model.stateChanged.connect(self.on_layout_visible)
        self.Check_button.clicked.connect(self.cheek)
        self.Apply_button.clicked.connect(self.apply)
        self.Remove_button.clicked.connect(self.remove_file)

    def show_file_select_dialog(self):
        file_path, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", "",
                                                                                self.FILE_FILTERS, self.selected_filter)
        if file_path:
            self.filepath.setText(file_path)
            # cmds.file(file_path, reference=True, ignoreVersion=True, namespace='scr_m')
            cmds.file(file_path, i=True, ignoreVersion=True, namespace='scr_m')

        else:
            om.MGlobal.displayWarning(u"请先选择model文件")

    def get_grp_meshs(self, grp):
        cmds.select(grp, hi=1)
        meshs = cmds.ls(type="mesh", sl=1)
        if meshs:
            cmds.select(meshs, r=1)
            cmds.pickWalk(d='up')
            Objs = cmds.ls(sl=1)
            cmds.select(cl=1)

            return Objs
        else:
            return None

    def cheek(self):
        scr_model = self.scr_model.text()
        rigging_model = self.rigging_model.text()

        outputObjs = list(self.get_grp_meshs(self.scr_model.text()))
        inputObjs = list(self.get_grp_meshs(self.rigging_model.text()))

        matched_mod = [item for item in outputObjs if item.split(":")[-1] in inputObjs]
        matched_rig = [item.split(":")[-1] for item in outputObjs if item.split(":")[-1] in inputObjs]

        extra_in_outputObjs = [item for item in outputObjs if item.split(":")[-1] not in inputObjs]

        self.model_scroll_list.clear()
        self.model_scroll_list.addItems(matched_mod)

        self.rigging_model_scroll_list.clear()
        self.rigging_model_scroll_list.addItems(matched_rig)

        if extra_in_outputObjs:
            self.extra_list.setText(str(extra_in_outputObjs))
            self.extra_list.setStyleSheet("font: bold 10px; color: red;")
            self.extra_list.setHidden(False)

            om.MGlobal.displayWarning(u"请检查模型对象: {}".format(extra_in_outputObjs))

        return

    def apply(self):
        # sourcefile = self.filepath.text()
        cmds.undoInfo(openChunk=True)
        try:

            source = list(_obj.get_list_widget_items(self.model_scroll_list))
            target = list(_obj.get_list_widget_items(self.rigging_model_scroll_list))

            copy_FFD_UV.transfer_uv_shader(source, target, self.uv_check.isChecked(), self.shader_check.isChecked(),
                                           name_space=self.scr_model.text().split(":")[0])
            om.MGlobal.displayInfo("列表里的对象已传递成功")

        finally:
            cmds.undoInfo(closeChunk=True)

        return

    def remove_file(self):
        cmds.delete(cmds.ls("{}:*".format(self.scr_model.text().split(":")[0]), type="transform"))
        self.model_scroll_list.clear()
        self.rigging_model_scroll_list.clear()
        self.filepath.setText("")
        self.scr_model.setText("")
        self.rigging_model.setText("")
        self.extra_list.setText("")

        mel.eval('source MLdeleteUnused.mel;MLdeleteUnused;')
        om.MGlobal.displayInfo("Successfully.")

        return


def main():
    if cmds.window("TransferModelUI", exists=True):
        cmds.deleteUI("TransferModelUI", window=True)

    Transfer = TransferModelUI(parent=_widgest.maya_main_window())
    Transfer.setObjectName("TransferModelUI")
    Transfer.show()

    return


if __name__ == "__main__":
    main()


