# -*- coding: utf-8 -*-

# .FileName:quick_box_ui.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2025/7/24 21:19
# .Finish time:

import os
from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, \
    PyouPersistentWindow

import saveRootPath as _path
import py_rigAssit.launcherApp as launcher

import maya.cmds as cmds

_widgest = Widgets()


class QuickBoxIconUI(PyouPersistentWindow):


    def __init__(self, icon_folder, parent=_widgest.maya_main_window()):
        super(QuickBoxIconUI, self).__init__("pyQuickBoxIconApp", "pyQuickBoxIconUI", parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.icon_folder = icon_folder
        self.WITH = 520
        self.HIGHT = 600
        self.ICON_WITH = 80

        self.ui_name = "Quick Box"
        self.timeStamp = "2025"
        self.remove_icon = "Rig_gui.png"

        self.icon_folder = icon_folder
        self.setWindowTitle(self.ui_name)
        self.resize(self.WITH, self.HIGHT)
        self.loadWindowSettings()

        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # 创建滚动区域来显示图标按钮
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_content = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_content)

        self.widget_layout(scroll_layout)

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

        _widgest.create_copyrightText(layout, self.timeStamp)

    def widget_layout(self, parent):

        # 创建 Tab 布局
        tab_widget = QtWidgets.QTabWidget()
        # 创建 "tool" 选项 ================================================================
        tool_tab = QtWidgets.QWidget()
        tool_tab_layout = QtWidgets.QVBoxLayout(tool_tab)

        icon_files, icon_names = self.get_icon_files()

        # 移除不需要的icon
        icon_files = [i for i in icon_files if self.remove_icon not in i]
        icon_names = [i for i in icon_names if self.remove_icon not in i]

        row_layout_tool = None
        ii = 0
        for icon_path, icon_name in zip(icon_files, icon_names):
            # print(icon_path, icon_name)
            if ii % 5 == 0:
                row_layout_tool = QtWidgets.QHBoxLayout()
                tool_tab_layout.addLayout(row_layout_tool)

            ii += 1
            button = self.create_icon_button(icon_path, icon_name)
            row_layout_tool.addWidget(button)

        # 创建 "Command" 选项 ================================================================
        command_tab = QtWidgets.QWidget()
        command_layout = QtWidgets.QVBoxLayout(command_tab)

        icon_files_command, icon_name_command = self.get_icon_command_files()

        row_layout_command = None
        ii = 0
        for icon_path, icon_name in zip(icon_files_command, icon_name_command):
            if ii % 5 == 0:
                row_layout_command = QtWidgets.QHBoxLayout()
                command_layout.addLayout(row_layout_command)
            ii += 1
            button = self.create_icon_button(icon_path, icon_name, True)
            row_layout_command.addWidget(button)

        # 创建 "data exp imp" 选项 ================================================================
        data_tab = QtWidgets.QWidget()
        data_layout = QtWidgets.QVBoxLayout(data_tab)

        icon_files_data, icon_name_data = self.get_icon_data_files()

        row_layout_data = None
        ii = 0
        for icon_path, icon_name in zip(icon_files_data, icon_name_data):
            if ii % 3 == 0:
                row_layout_data = QtWidgets.QHBoxLayout()
                data_layout.addLayout(row_layout_data)
            ii += 1
            button = self.create_icon_button(icon_path, icon_name, True)
            row_layout_data.addWidget(button)

        tab_widget.addTab(command_tab, "> command")
        tab_widget.addTab(tool_tab, "> tool_ui")
        tab_widget.addTab(data_tab, "> data_command")

        parent.addWidget(tab_widget)


    def get_icon_files(self):
        icon_files = [f for f in os.listdir(self.icon_folder) if f.endswith(('.png', '.ico', '.jpg', '.svg'))]
        return [os.path.join(self.icon_folder, f) for f in icon_files], icon_files

    def get_icon_command_files(self):
        icon_folder = self.icon_folder + "/command"
        icon_files = [f for f in os.listdir(icon_folder) if
                      f.endswith(('.png', '.ico', '.jpg', '.svg'))]
        return [os.path.join(icon_folder, f) for f in icon_files], icon_files

    def get_icon_data_files(self):
        icon_folder = self.icon_folder + "/exp_imp"
        icon_files = [f for f in os.listdir(icon_folder) if
                      f.endswith(('.png', '.ico', '.jpg', '.svg'))]
        return [os.path.join(icon_folder, f) for f in icon_files], icon_files

    def create_icon_button(self, icon_path, icon_name, command=False):
        # 创建带图标的按钮
        button = QtWidgets.QPushButton()
        button.setIcon(QtGui.QIcon(icon_path))
        button.setIconSize(QtCore.QSize(64, 64))  # 设置图标大小
        button.setFixedSize(self.ICON_WITH, self.ICON_WITH)  # 设置按钮大小

        try:
            button.setToolTip( launcher.toolTip[icon_name])
        except:
            button.setToolTip(u"")

        if command:
            button.clicked.connect(lambda: self.on_button_click_command(icon_name))
        else:
            button.clicked.connect(lambda: self.on_button_click(icon_name))  # 绑定点击事件
        return button

    def create_icon_label(self, icon_name):
        # 创建显示图标文件名的标签
        label = QtWidgets.QLabel(os.path.basename(icon_name))
        label.setAlignment(QtCore.Qt.AlignCenter)  # 居中对齐
        label.setFixedWidth(self.ICON_WITH)  # 与按钮宽度相同
        return label


    def on_button_click(self, icon_name):
        try:
            launcher.tool_info[icon_name]()
        except Exception as e:
            import traceback
            print("❌ Tool Failed:", icon_name)
            print(traceback.format_exc())

    def on_button_click_command(self, icon_name):
        try:
            launcher.command_info[icon_name]()
        except Exception as e:
            import traceback
            print("❌ Command Failed:", icon_name)
            print(traceback.format_exc())

def show_ui(icon_folder=None):
    if icon_folder == None:
        icon_folder = _path.IconsPath.replace("\\", "/") + "/label/quick_box"

    global quickBox_ui
    try:
        quickBox_ui.close()  # pylint: disable=E0601
        quickBox_ui.deleteLater()
    except:
        pass

    quickBox_ui = QuickBoxIconUI(icon_folder)
    quickBox_ui.setObjectName("pyQuickBoxIconUI")
    quickBox_ui.show()


if __name__ == '__main__':

    show_ui(None)
