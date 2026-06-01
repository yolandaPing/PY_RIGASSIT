# -*- coding: utf-8 -*-

# .FileName:combine_sdk_ui.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2025/11/15 12:03
# .Finish time:
from py_rigAssit import QtWidgets, QtCore, QtGui, QAction, Widgets, PyouPersistentWindow
from ConstrainEdit.setDefaultsAttr import SetDirveKeyTool
from AttrNameUtils import PyAttrUtils
import HelpImageUI as Help

import maya.cmds as mc, maya.OpenMaya as om

_SDK = SetDirveKeyTool()
_ATTR = PyAttrUtils()
PY_WIDGEAT = Widgets()


class PYCombine_SDK_UI(PyouPersistentWindow):
    web = "https://www.bilibili.com/video/BV1qHmqBSEbk/?share_source=copy_web&vd_source=7b50d73ef3e3d9c8d5f26b106034eb71"


    def __init__(self, parent=PY_WIDGEAT.maya_main_window()):
        super(PYCombine_SDK_UI, self).__init__("PYCombine_SDK_UI", "PYCombine_SDK_UI", parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.WINDOW_NAME = 'combine SDK Tool'
        self.windowT = 'Combine_SDK_ToolWindow'
        self.timeStamp = ' 22024-2025'

        self.driverTextfilePath = ''
        self.drn_layout_bth = 0

        # Store dynamic widgets
        self.driver_widgets = []
        self.driven_widgets = []

        self.setup_ui(True)

    def setup_ui(self, copyright=False):
        self.setWindowTitle(self.WINDOW_NAME)
        self.setMinimumSize(500, 400)

        # self.loadWindowSettings()
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        self.create_menu_bar(main_layout)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        content_layout.setContentsMargins(2, 2, 2, 2)
        content_layout.setSpacing(8)

        content_layout.addWidget(PY_WIDGEAT.create_title(self.WINDOW_NAME, 15, self.web))

        self.create_driven_section(content_layout)
        self.create_driver_section(content_layout)
        self.create_control_buttons(content_layout)

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        if copyright:
            PY_WIDGEAT.create_copyrightText(main_layout, self.timeStamp)

        return main_layout

    def create_menu_bar(self, parent_layout):
        menu_bar = QtWidgets.QMenuBar()
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("bilibili: 我有一只猛犬", self)
        e_mail = QAction("pyrigassit@gmail.com", self)
        # about_action.triggered.connect(lambda: self.helpWebs('gui'))
        help_menu.addAction(about_action)
        help_menu.addAction(e_mail)
        parent_layout.setMenuBar(menu_bar)

    def create_driven_section(self, parent_layout):
        driven_group = QtWidgets.QGroupBox("> Driven 被驱动对象:")
        driven_group.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        driven_layout = QtWidgets.QVBoxLayout(driven_group)
        driven_layout.setContentsMargins(4, 12, 8, 8)
        driven_layout.setSpacing(8)

        self.add_driven_widget(driven_layout)

        type_layout = QtWidgets.QHBoxLayout()
        type_layout.addWidget(QtWidgets.QLabel("Driven Type:"))

        self.driven_type_group = QtWidgets.QButtonGroup()
        self.average_radio = QtWidgets.QRadioButton("  Average  ")
        self.must_both_radio = QtWidgets.QRadioButton("  Must both  ")
        self.clamp_both_radio = QtWidgets.QRadioButton("  Clamp value  ")
        self.must_both_radio.setChecked(True)

        self.driven_type_group.addButton(self.average_radio)
        self.driven_type_group.addButton(self.must_both_radio)
        self.driven_type_group.addButton(self.clamp_both_radio)

        type_layout.addWidget(self.average_radio)
        type_layout.addWidget(self.must_both_radio)
        type_layout.addWidget(self.clamp_both_radio)
        type_layout.addStretch()

        driven_layout.addLayout(type_layout)
        parent_layout.addWidget(driven_group)

    def create_driver_section(self, parent_layout):
        driver_group = QtWidgets.QGroupBox("> Driver 驱动对象:")
        driver_group.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        driver_layout = QtWidgets.QVBoxLayout(driver_group)
        driver_layout.setContentsMargins(8, 12, 8, 8)
        driver_layout.setSpacing(8)

        self.driver_widgets_container = QtWidgets.QVBoxLayout()
        driver_layout.addLayout(self.driver_widgets_container)

        self.add_driver_widget()
        self.add_driver_widget()

        parent_layout.addWidget(driver_group)

    def create_control_buttons(self, parent_layout):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(10)

        self.add_driver_btn = QtWidgets.QPushButton("+")
        self.add_driver_btn.setToolTip("add Driver 添加驱动对象")

        self.add_driver_btn.setFixedWidth(30)
        self.add_driver_btn.clicked.connect(self.add_driver_widget)

        self.remove_driver_btn = QtWidgets.QPushButton("-")
        self.remove_driver_btn.setToolTip("remove Driver 减少驱动对象")

        self.remove_driver_btn.setFixedWidth(30)
        self.remove_driver_btn.clicked.connect(self.remove_driver_widget)

        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.apply_btn.setProperty("main", True)
        self.apply_btn.clicked.connect(self.apply_combine_sdk)

        self.help_btn = QtWidgets.QPushButton()
        self.help_btn.setIcon(QtGui.QIcon(":/help.png"))

        self.help_btn.clicked.connect(lambda: Help.HelpImage("", "combine_sdk"))

        button_layout.addWidget(self.add_driver_btn)
        button_layout.addWidget(self.remove_driver_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.apply_btn, 10)
        button_layout.addWidget(self.help_btn)

        parent_layout.addLayout(button_layout)

    def add_driven_widget(self, parent_layout):
        widget_layout = QtWidgets.QHBoxLayout()
        widget_layout.setSpacing(5)

        attr_field = QtWidgets.QLineEdit()
        attr_field.setPlaceholderText("Attribute path")

        start_value_field = QtWidgets.QLineEdit("0.00")
        start_value_field.setFixedWidth(100)

        end_value_field = QtWidgets.QLineEdit("0.00")
        end_value_field.setFixedWidth(100)

        load_btn = QtWidgets.QPushButton("<<<")
        load_btn.setToolTip("Load Attr 载入属性")
        load_btn.setProperty("main", True)
        load_btn.clicked.connect(
            lambda: self.load_selectedAttr_to_TextField(attr_field, start_value_field, end_value_field))

        widget_layout.addWidget(attr_field)
        widget_layout.addWidget(start_value_field)
        widget_layout.addWidget(end_value_field)
        widget_layout.addWidget(load_btn)

        driven_widget = {
            'attr_field': attr_field,
            'start_value_field': start_value_field,
            'end_value_field': end_value_field
        }
        self.driven_widgets.append(driven_widget)

        parent_layout.addLayout(widget_layout)

    def add_driver_widget(self):
        widget_layout = QtWidgets.QHBoxLayout()
        widget_layout.setSpacing(5)

        attr_field = QtWidgets.QLineEdit()
        attr_field.setPlaceholderText("Attribute path")

        start_value_field = QtWidgets.QLineEdit("0.00")
        start_value_field.setFixedWidth(80)

        end_value_field = QtWidgets.QLineEdit("0.00")
        end_value_field.setFixedWidth(80)

        load_btn = QtWidgets.QPushButton("<<<")
        load_btn.setToolTip("Load Attr 载入属性")
        load_btn.setProperty("main", True)
        load_btn.clicked.connect(
            lambda: self.load_selectedAttr_to_TextField(attr_field, start_value_field, end_value_field))

        widget_layout.addWidget(attr_field)
        widget_layout.addWidget(start_value_field)
        widget_layout.addWidget(end_value_field)
        widget_layout.addWidget(load_btn)

        driver_widget = {
            'attr_field': attr_field,
            'start_value_field': start_value_field,
            'end_value_field': end_value_field,
            'layout': widget_layout
        }
        self.driver_widgets.append(driver_widget)
        self.driver_widgets_container.addLayout(widget_layout)
        self.adjust_window_height(30)

    def remove_driver_widget(self):
        if len(self.driver_widgets) > 1:

            widget = self.driver_widgets.pop()

            layout = widget['layout']
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            self.driver_widgets_container.removeItem(layout)
            self.adjust_window_height(-30)

    def adjust_window_height(self, delta):
        # 调整窗口高度以适应内容
        current_height = self.height()
        self.resize(self.width(), current_height + delta)

    def load_selectedAttr_to_TextField(self, attr_field, start_value_field, end_value_field):
        selectedAttr = _ATTR.getSelectedAttr()
        if selectedAttr != []:
            selectedAttr = selectedAttr[0]
            value = mc.getAttr(selectedAttr)

            attr_field.setText(str(selectedAttr))
            end_value_field.setText(str('%.3f' % value))
            return True
        else:
            om.MGlobal.displayError("Please select the object attribute to load first.")
            return False

    def apply_combine_sdk(self):
        # type_value = 1 if self.average_radio.isChecked() else 2
        type_value = 2
        if self.average_radio.isChecked():
            type_value = 1
        elif self.must_both_radio.isChecked():
            type_value = 2
        else:
            type_value = 3

        driven_data = []
        if self.driven_widgets:
            driven_widget = self.driven_widgets[0]  # 假设只有一个被驱动对象
            driven_attr = driven_widget['attr_field'].text()
            driven_value_st = driven_widget['start_value_field'].text()
            driven_value_ed = driven_widget['end_value_field'].text()

            driven_values = (float(driven_value_st), float(driven_value_ed))
            driven_data = (driven_attr, driven_values)

        driver_data_list = []
        for driver_widget in self.driver_widgets:
            driver_attr = driver_widget['attr_field'].text()
            driver_value_st = driver_widget['start_value_field'].text()
            driver_value_ed = driver_widget['end_value_field'].text()

            values = (float(driver_value_st), float(driver_value_ed))
            obj_info = (driver_attr, values)
            driver_data_list.append(obj_info)

        driver_data_tuple = tuple(driver_data_list)
        data_dict = {driver_data_tuple: driven_data}
        print(driver_data_tuple)
        if type_value == 1:
            _SDK.createCombineDirve(data_dict, True)
        elif type_value == 2:
            _SDK.createCombineDirve(data_dict, False)
        else:
            _SDK.combine_driven_clamp(data_dict)

        om.MGlobal.displayInfo("succeed!")


def main():
    global pyCcombine_sdk_ui

    try:
        pyCcombine_sdk_ui.close()  # pylint: disable=E0601
        pyCcombine_sdk_ui.deleteLater()
    except:
        pass

    pyCcombine_sdk_ui = PYCombine_SDK_UI()
    pyCcombine_sdk_ui.show()


if __name__ == '__main__':
    main()