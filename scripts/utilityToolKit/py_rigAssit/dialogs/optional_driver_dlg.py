# -*- coding: utf-8 -*-
# .FileName:OptionalDriveDialog
# .Date....:2022-12-23 : 10 :16
# .@Author:You P
# .
# .Finish time:2024-06-08
from functools import partial

from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
from py_rigAssit.common.command_dispatcher import CommandDispatcher
import py_rigAssit.common.commands
from selectOrRemove import SelectOrremoveObj
from ConstrainEdit.Multifunctional_Drive import MultifunctionalDrive
from ConstrainEdit.copySDKAttr import CopySDKFun
from py_rigAssit.dialogs import Help, decorator, mayaPrint

import maya.cmds as cmds


PY_WIDGEAT = Widgets()


def _pair_iter(oldMod, newMod):
    if len(oldMod) == 1:
        for tgt in newMod:
            yield oldMod[0], tgt
    elif len(oldMod) == len(newMod):
        for src, tgt in zip(oldMod, newMod):
            yield src, tgt
    else:
        mayaPrint.error("Mismatch source/target count")
        return


class PYOptionalDriveDialog(PyouPersistentWindow):

    _obj = SelectOrremoveObj()
    _mfd = MultifunctionalDrive()
    _cysdk = CopySDKFun()


    def __init__(self, parent=PY_WIDGEAT.maya_main_window()):
        super(PYOptionalDriveDialog, self).__init__("PYOptionalDriveDialog", "PYOptionalDriveDialog", parent)
        self.WINDOW_NAME = "Optional Drive "
        self.timeStamp = '2022-2026'
        self._text_font = "font: bold 11px"
        self.setWindowTitle(self.WINDOW_NAME)
        self.setMinimumWidth(400)
        self.loadWindowSettings()
        self.init_ui(True)


    def init_ui(self, copyright=False):
        self.dispatcher = CommandDispatcher()
        self.SearchReplaceWindow = "pyConstrainSearchReplaceUI"
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(4)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.addWidget(PY_WIDGEAT.create_title(self.WINDOW_NAME, 15, ""))

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)

        scroll_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)

        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

        v_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        v_splitter.setChildrenCollapsible(True)

        # ===== 上 =====
        top_frame = QtWidgets.QFrame()
        top_layout = QtWidgets.QVBoxLayout(top_frame)
        top_layout.setContentsMargins(0, 0, 0, 0)

        self.build_driver_driven_ui(top_layout)
        scroll_layout.addWidget(top_frame)

        # scroll_layout.addStretch(1)
        # ===== 下=====
        bottom_frame = QtWidgets.QFrame()
        bottom_layout = QtWidgets.QVBoxLayout(bottom_frame)
        bottom_layout.setSpacing(1)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        PY_WIDGEAT.separator(bottom_layout)
        bottom_layout.addWidget(self.build_tabs())
        bottom_layout.addStretch()

        bottom_frame.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Maximum
        )
        v_splitter.addWidget(top_frame)
        v_splitter.addWidget(bottom_frame)
        v_splitter.setStretchFactor(0, 1)
        v_splitter.setStretchFactor(1, 0)
        v_splitter.setSizes([1, 1])

        scroll_layout.addWidget(v_splitter)
        if copyright:
            PY_WIDGEAT.create_copyrightText(main_layout, self.timeStamp)
        self.create_connections()
        return main_layout

    def build_tabs(self):
        self.tabs = QtWidgets.QTabWidget()

        self.tabs.addTab(self.build_Optional_tab(), "Optional")
        self.tabs.addTab(self.build_Constraints_tab(), "Constraints")
        self.tabs.addTab(self.build_SDK_tab(), "SDK")
        self.tabs.addTab(self.build_CopyInput_tab(), "Copy Input")
        self.tabs.addTab(self.build_Combine_tab(), "Combine")
        return self.tabs

    # ----------------------------- 各 Tab 构建（返回 QWidget）-----------------------------
    def build_Optional_tab(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.Optional_wigets_layout(layout)
        layout.addStretch()
        return widget

    def build_Constraints_tab(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.Constraint_wigets_layout(layout)
        layout.addStretch()
        return widget

    def build_SDK_tab(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.SetDirveKey_wigets_layout(layout)
        self.copy_SDK_wigrts_layout(layout)
        layout.addStretch()
        return widget

    def build_CopyInput_tab(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.copy_INFOconnect_wigrts_layout(layout)
        layout.addStretch()
        return widget

    def build_Combine_tab(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.combin_Dirve_wigets_layout(layout)
        layout.addStretch()
        return widget

    # ===== Driver / Driven 区 =====
    def add_empty_space_menu(self):

        self.driver_empty_space_menu = QtWidgets.QMenu(self)
        driver_load_menu = PY_WIDGEAT.add_empty_space_menu_item(self, self.driver_empty_space_menu,"Load 载入", None,  enabled=True)
        driver_append_menu = PY_WIDGEAT.add_empty_space_menu_item(self, self.driver_empty_space_menu, "Append 追加", ":QR_add.png",enabled=True)
        driver_remove_menu = PY_WIDGEAT.add_empty_space_menu_item(self, self.driver_empty_space_menu,"Remove 移除", ":QR_delete.png", enabled=True)
        PY_WIDGEAT.add_separator(self, self.driver_empty_space_menu)
        driver_select_all_menu = PY_WIDGEAT.add_empty_space_menu_item(self, self.driver_empty_space_menu, "Select All", None, enabled=True)
        driver_left_to_right_menu = PY_WIDGEAT.add_empty_space_menu_item(self, self.driver_empty_space_menu,"L > R", None, enabled=True)
        driver_right_to_left_menu = PY_WIDGEAT.add_empty_space_menu_item(self, self.driver_empty_space_menu, "R > L", None, enabled=True)
        PY_WIDGEAT.add_separator(self, self.driver_empty_space_menu)
        driver_search_to_replace_menu = PY_WIDGEAT.add_empty_space_menu_item(self, self.driver_empty_space_menu, "Search > Replace", None, enabled=True)


        self.driven_empty_space_menu = QtWidgets.QMenu(self)
        driven_load_menu = PY_WIDGEAT.add_empty_space_menu_item(self, self.driven_empty_space_menu, "Load 载入",
                                                                   None, enabled=True)
        driven_append_menu = PY_WIDGEAT.add_empty_space_menu_item(self, self.driven_empty_space_menu, "Append 追加",
                                                                     ":QR_add.png", enabled=True)
        driven_remove_menu = PY_WIDGEAT.add_empty_space_menu_item(self, self.driven_empty_space_menu, "Remove 移除",
                                                                     ":QR_delete.png", enabled=True)
        PY_WIDGEAT.add_separator(self, self.driven_empty_space_menu)
        driven_select_all_menu = PY_WIDGEAT.add_empty_space_menu_item(self, self.driven_empty_space_menu, "Select All",  None, enabled=True)
        driven_left_to_right_menu = PY_WIDGEAT.add_empty_space_menu_item(self, self.driven_empty_space_menu, "L > R",
                                                                            None, enabled=True)
        driven_right_to_left_menu = PY_WIDGEAT.add_empty_space_menu_item(self, self.driven_empty_space_menu, "R > L",
                                                                            None, enabled=True)
        PY_WIDGEAT.add_separator(self, self.driven_empty_space_menu)
        driven_search_to_replace_menu = PY_WIDGEAT.add_empty_space_menu_item(self, self.driven_empty_space_menu,
                                                                                "Search > Replace", None, enabled=True)

        # # Set context menu policy设置上下文菜单
        self.driver_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.driver_list.customContextMenuRequested.connect(self.show_context_driver_menu)

        self.driven_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.driven_list.customContextMenuRequested.connect(self.show_context_driven_menu)

        # menu mod
        # driver_load_menu.triggered.connect(lambda: self._obj.load_list_widget_items(self.driver_list, True, True))
        # driver_append_menu.triggered.connect(lambda: self._obj.load_list_widget_items(self.driver_list, False, True))
        # driver_remove_menu.triggered.connect(lambda: self._obj.remove_seleted_items(self.driver_list))
        # driver_left_to_right_menu.triggered.connect(lambda: self.mirror_selection(self.driver_list, self.driven_list,True))
        # driver_right_to_left_menu.triggered.connect(lambda: self.mirror_selection(self.driver_list, self.driven_list,False))
        # driver_search_to_replace_menu.triggered.connect( lambda: self.replace_string_ui(self.driver_list, self.driven_list))
        # driver_select_all_menu.triggered.connect(lambda: self.dispatcher.execute("Menu Select All", self.driver_list))
        # driven_load_menu.triggered.connect(lambda: self._obj.load_list_widget_items(self.driven_list, True, True))
        # driven_append_menu.triggered.connect( lambda: self._obj.load_list_widget_items(self.driven_list, False, True))
        # driven_remove_menu.triggered.connect(lambda: self._obj.remove_seleted_items(self.driven_list))
        # driven_left_to_right_menu.triggered.connect(lambda: self.mirror_selection(self.driven_list, self.driver_list, True))
        # driven_right_to_left_menu.triggered.connect(lambda: self.mirror_selection(self.driven_list, self.driver_list, False))
        # driven_search_to_replace_menu.triggered.connect(lambda: self.replace_string_ui(self.driven_list, self.driver_list, obj="Driven"))
        # driven_select_all_menu.triggered.connect(lambda: self.dispatcher.execute("Menu Select All", self.driven_list))

        from functools import partial

        driver_load_menu.triggered.connect(
            partial(self._obj.load_list_widget_items, self.driver_list, True, True)
        )

        driver_append_menu.triggered.connect(
            partial(self._obj.load_list_widget_items, self.driver_list, False, True)
        )

        driver_remove_menu.triggered.connect(
            partial(self._obj.remove_seleted_items, self.driver_list)
        )

        driver_left_to_right_menu.triggered.connect(
            partial(self.mirror_selection, self.driver_list, self.driven_list, True)
        )

        driver_right_to_left_menu.triggered.connect(
            partial(self.mirror_selection, self.driver_list, self.driven_list, False)
        )

        driver_search_to_replace_menu.triggered.connect(
            partial(self.replace_string_ui, self.driver_list, self.driven_list)
        )

        driver_select_all_menu.triggered.connect(
            partial(self.dispatcher.execute, "Menu Select All", self.driver_list)
        )

        driven_load_menu.triggered.connect(
            partial(self._obj.load_list_widget_items, self.driven_list, True, True)
        )

        driven_append_menu.triggered.connect(
            partial(self._obj.load_list_widget_items, self.driven_list, False, True)
        )

        driven_remove_menu.triggered.connect(
            partial(self._obj.remove_seleted_items, self.driven_list)
        )

        driven_left_to_right_menu.triggered.connect(
            partial(self.mirror_selection, self.driven_list, self.driver_list, True)
        )

        driven_right_to_left_menu.triggered.connect(
            partial(self.mirror_selection, self.driven_list, self.driver_list, False)
        )

        driven_search_to_replace_menu.triggered.connect(
            partial(self.replace_string_ui, self.driven_list, self.driver_list, obj="Driven")
        )

        driven_select_all_menu.triggered.connect(
            partial(self.dispatcher.execute, "Menu Select All", self.driven_list)
        )

    def build_driver_driven_ui(self, parent):
        # main_layout = QtWidgets.QVBoxLayout(parent)
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.setHandleWidth(3)
        splitter.setChildrenCollapsible(True)
        # main_layout.addWidget(splitter)

        frame1 = QtWidgets.QFrame()
        frame2 = QtWidgets.QFrame()

        splitter.addWidget(frame1)
        splitter.addWidget(frame2)

        splitter.setSizes([100, 100])

        # ===== 左 =====
        l_layout = QtWidgets.QVBoxLayout(frame1)
        self.driver_list = QtWidgets.QListWidget()
        self.driver_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.load_driver_btn = QtWidgets.QPushButton("Load")
        self.load_driver_btn.setProperty("green", True)

        l_layout.addWidget(QtWidgets.QLabel("Driver"))
        l_layout.addWidget(self.driver_list)

        l_layout.addWidget(self.load_driver_btn)
        # ===== 右 =====
        r_layout = QtWidgets.QVBoxLayout(frame2)

        self.driven_list = QtWidgets.QListWidget()
        self.driven_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.load_driven_btn = QtWidgets.QPushButton("Load")
        self.load_driven_btn.setProperty("green", True)

        r_layout.addWidget(QtWidgets.QLabel("Driven"))
        r_layout.addWidget(self.driven_list)

        r_layout.addWidget(self.load_driven_btn)
        self.add_empty_space_menu()

        parent.addWidget(splitter)

    def Optional_wigets_layout(self, parent_layout):

        self.frame_button_op = PY_WIDGEAT.create_collapsible_frame(' Optional ', True)
        main_layout = QtWidgets.QVBoxLayout()

        label = PY_WIDGEAT.create_text(u'>> First select the type and then run 先选择类型')
        self.parent_closest_cbx = QtWidgets.QCheckBox(' closest pivots parent')

        self.optional_block = PY_WIDGEAT.create_radiogroup(
            items=[
                ("Parent", 1, u'driven -> parent'),
                ("Attributes", 2, u'connect Attribute'),
                ("Double Skin", 3, u'inverseMatrix'),
                ("Add BS", 4, u'add blendshape'),
            ],
            default_id=1
        )

        # buttons
        btn_layout = QtWidgets.QHBoxLayout()
        self.apply_btn_op = QtWidgets.QPushButton('Apply')
        self.help_btn_op = QtWidgets.QPushButton()
        self.help_btn_op.setIcon(QtGui.QIcon(":\help.png"))
        self.apply_btn_op.setProperty("main", True)
        self.help_btn_op.setProperty("help", True)
        btn_layout.addWidget(self.apply_btn_op,9)
        btn_layout.addWidget(self.help_btn_op)

        main_layout.addWidget(label)
        main_layout.addWidget(self.parent_closest_cbx)
        main_layout.addWidget(self.optional_block)
        main_layout.addWidget(QtWidgets.QLabel(""))
        main_layout.addLayout(btn_layout)

        self.frame_button_op.setContentLayout(main_layout)
        parent_layout.addWidget(self.frame_button_op)

    def Constraint_wigets_layout(self, parent_layout):
        # 创建并添加"Buttons"的折叠框
        self.frame_button_con = PY_WIDGEAT.create_collapsible_frame("Constraints / Connect (约束/链接)", True)
        main_layout = QtWidgets.QVBoxLayout()
        # main_layout.setSpacing(4)
        checkbox_layout = QtWidgets.QHBoxLayout()
        self.parent_cbx = QtWidgets.QCheckBox (' Parent')
        self.point_cbx = QtWidgets.QCheckBox(' Point')
        self.orient_cbx = QtWidgets.QCheckBox (' Orient')
        self.scale_cbx = QtWidgets.QCheckBox(' Scale')
        checkbox_layout.addWidget(self.parent_cbx)
        checkbox_layout.addWidget(self.point_cbx)
        checkbox_layout.addWidget(self.orient_cbx)
        checkbox_layout.addWidget(self.scale_cbx)
        button_layout = QtWidgets.QHBoxLayout()
        self.Constraints_btn = QtWidgets.QPushButton('Constraint 约束')
        self.Constraints_btn.setProperty("main", True)
        self.Connect_btn = QtWidgets.QPushButton('Connect 链接')
        self.Connect_btn.setProperty("main", True)
        self.Help_btn_con = QtWidgets.QPushButton()
        self.Help_btn_con.setIcon(QtGui.QIcon(":\help.png"))
        self.Help_btn_con.setProperty("help", True)
        button_layout.addWidget(self.Constraints_btn,5)
        button_layout.addWidget(self.Connect_btn,5)
        button_layout.addWidget(self.Help_btn_con, 0)
        main_layout.addWidget(PY_WIDGEAT.create_text("无需载入属性，直接载入对象，选中需要的类型", 12))
        main_layout.addWidget(QtWidgets.QLabel("Type: "))
        main_layout.addLayout(checkbox_layout)
        # PY_WIDGEAT.separator(main_layout)
        main_layout.addWidget(QtWidgets.QLabel(""))
        main_layout.addLayout(button_layout)
        self.frame_button_con.setContentLayout(main_layout)
        parent_layout.addWidget(self.frame_button_con)

    def SetDirveKey_wigets_layout(self, parent_layout):
        # 创建并添加"Buttons"的折叠框
        frame_button = PY_WIDGEAT.create_collapsible_frame("Set Driven Key (批量驱动关键帧)")
        main_layout = QtWidgets.QVBoxLayout()

        label = PY_WIDGEAT.create_text("> need load objects's Attribute 此功能需要载入对象的属性")

        checkbox_layout = QtWidgets.QHBoxLayout()
        checkbox_label = QtWidgets.QLabel(" > Infinity: ")

        self.pre_Cycle_cbx = QtWidgets.QCheckBox(' Pre Cycle')
        self.post_Cycle_cbx = QtWidgets.QCheckBox(' Post Cycle')

        checkbox_label.setStyleSheet("{}; ".format(self._text_font))

        checkbox_layout.addWidget(checkbox_label)
        checkbox_layout.addWidget(self.pre_Cycle_cbx)
        checkbox_layout.addWidget(self.post_Cycle_cbx)

        decimals = 4
        driver_label = QtWidgets.QLabel("Driver value: ")
        self.driver_field1 = QtWidgets.QDoubleSpinBox()
        self.driver_field2 = QtWidgets.QDoubleSpinBox()
        self.driver_field3 = QtWidgets.QDoubleSpinBox()

        driven_label = QtWidgets.QLabel("Driven value: ")
        self.driven_field1 = QtWidgets.QDoubleSpinBox()
        self.driven_field2 = QtWidgets.QDoubleSpinBox()
        self.driven_field3 = QtWidgets.QDoubleSpinBox()

        # 设置小数点后5位
        self.driver_field1.setDecimals(decimals)
        self.driver_field2.setDecimals(decimals)
        self.driver_field3.setDecimals(decimals)
        self.driven_field1.setDecimals(decimals)
        self.driven_field2.setDecimals(decimals)
        self.driven_field3.setDecimals(decimals)

        #设置范围
        self.driver_field1.setRange(-500.0, 500.0)
        self.driver_field2.setRange(-500.0, 500.0)
        self.driver_field3.setRange(-500.0, 500.0)
        self.driven_field1.setRange(-500.0, 500.0)
        self.driven_field2.setRange(-500.0, 500.0)
        self.driven_field3.setRange(-500.0, 500.0)

        driver_field_layout = QtWidgets.QHBoxLayout()
        driven_field_layout = QtWidgets.QHBoxLayout()

        driver_field_layout.addWidget(driver_label)
        driver_field_layout.addWidget(self.driver_field1)
        driver_field_layout.addWidget(self.driver_field2)
        driver_field_layout.addWidget(self.driver_field3)

        driven_field_layout.addWidget(driven_label)
        driven_field_layout.addWidget(self.driven_field1)
        driven_field_layout.addWidget(self.driven_field2)
        driven_field_layout.addWidget(self.driven_field3)

        button_layout = QtWidgets.QHBoxLayout()
        self.apply_btn_sdk = QtWidgets.QPushButton('Apply')
        self.apply_btn_sdk.setProperty("main", True)
        self.help_btn_sdk = QtWidgets.QPushButton()
        self.help_btn_sdk.setIcon(QtGui.QIcon(":\help.png"))
        self.help_btn_sdk.setProperty("help", True)

        button_layout.addWidget(self.apply_btn_sdk, 80)
        button_layout.addStretch(1)
        button_layout.addWidget(self.help_btn_sdk, 1)

        main_layout.addWidget(label)
        main_layout.addLayout(checkbox_layout)
        main_layout.addLayout(driver_field_layout)
        main_layout.addLayout(driven_field_layout)
        main_layout.addLayout(button_layout)
        frame_button.setContentLayout(main_layout)
        parent_layout.addWidget(frame_button)

    def copy_SDK_wigrts_layout(self, parent_layout):
        self.frame_button_cmsdk = PY_WIDGEAT.create_collapsible_frame(' Copy / Mirror SDK (批量拷贝/镜像SDK)')
        main_layout = QtWidgets.QVBoxLayout()
        self.cmsdk_type_block = PY_WIDGEAT.create_radiogroup(
            title="Type:",
            items=[
                ("Output info", 1, u'拷贝源输出的所有SDK节点信息'),
                ("Input info", 2, u'拷贝源当前输入SDK信息'),
                ("Node", 3, u'载入指定SDK节点')
            ],
            default_id=2
        )
        self.cmsdk_value_block = PY_WIDGEAT.create_radiogroup(
            title="Value:",
            items=[
                (u"same 相同的值", 1, u'相同的值'),
                (u"reverse 相反的值", 2, u'相反的值')
            ],
            default_id=1
        )
        self.search_replace_widget = QtWidgets.QWidget()
        search_all_layout = QtWidgets.QVBoxLayout(self.search_replace_widget)
        label = PY_WIDGEAT.create_text('> need to search and replace prefix/name 搜索和替换前缀/名字"', 12)

        # Search 1
        search_prefixname_layout = QtWidgets.QHBoxLayout()
        search_label = QtWidgets.QLabel("Search: ")
        self.search_text = QtWidgets.QLineEdit("_L_")
        search_prefixname_layout.addWidget(search_label)
        search_prefixname_layout.addWidget(self.search_text)

        # Replace 1
        replace_prefixname_layout = QtWidgets.QHBoxLayout()
        replace_label = QtWidgets.QLabel("Replace: ")
        self.replace_text = QtWidgets.QLineEdit("_R_")
        # self.replace_text.setReadOnly(True)
        replace_prefixname_layout.addWidget(replace_label)
        replace_prefixname_layout.addWidget(self.replace_text)

        main_search_prefixname_layout = QtWidgets.QHBoxLayout()
        main_search_prefixname_layout.addLayout(search_prefixname_layout)
        main_search_prefixname_layout.addLayout(replace_prefixname_layout)

        self.replace_AttrCheckbox_cmsdk = QtWidgets.QCheckBox(' Replace Attr 替换属性?')

        # Search 2
        search_Attrname_layout = QtWidgets.QHBoxLayout()
        self.search_Attr_label = QtWidgets.QLabel("Search Attr: ")
        self.search_Attr_text = QtWidgets.QLineEdit("")
        search_Attrname_layout.addWidget(self.search_Attr_label)
        search_Attrname_layout.addWidget(self.search_Attr_text)

        # Replace 2
        replace_Attrname_layout = QtWidgets.QHBoxLayout()
        self.replace_Attr_label = QtWidgets.QLabel("Replace Attr: ")
        self.replace_Attr_text = QtWidgets.QLineEdit("")
        replace_Attrname_layout.addWidget(self.replace_Attr_label)
        replace_Attrname_layout.addWidget(self.replace_Attr_text)

        self.search_Attr_text.setEnabled(False)
        self.replace_Attr_text.setEnabled(False)
        self.search_Attr_label.setStyleSheet("color: black;")
        self.replace_Attr_label.setStyleSheet("color: black;")
        self.search_Attr_text.setStyleSheet("background-color: dark grey;")
        self.replace_Attr_text.setStyleSheet("background-color: dark grey;")

        main_search_Attr_layout = QtWidgets.QHBoxLayout()
        main_search_Attr_layout.addLayout(search_Attrname_layout)
        main_search_Attr_layout.addLayout(replace_Attrname_layout)

        main_layout.addWidget(self.cmsdk_type_block)
        main_layout.addWidget(self.cmsdk_value_block)
        search_all_layout.addWidget(label)
        search_all_layout.addLayout(main_search_prefixname_layout)
        search_all_layout.addWidget(self.replace_AttrCheckbox_cmsdk)
        search_all_layout.addLayout(main_search_Attr_layout)
        main_layout.addWidget(self.search_replace_widget)
        button_layout = QtWidgets.QHBoxLayout()
        self.apply_btn_cmsdk = QtWidgets.QPushButton('Apply')
        self.apply_btn_cmsdk.setProperty("main", True)
        self.help_btn_cmsdk = QtWidgets.QPushButton()
        self.help_btn_cmsdk.setIcon(QtGui.QIcon(":\help.png"))
        self.help_btn_cmsdk.setProperty("help", True)
        button_layout.addWidget(self.apply_btn_cmsdk, 80)
        button_layout.addStretch(1)
        button_layout.addWidget(self.help_btn_cmsdk, 1)
        self.frame_button_cmsdk.setContentLayout(main_layout)
        main_layout.addLayout(button_layout)
        self.cmsdk_type_block.idClicked.connect(self._cmsdk_block_Toggled)
        parent_layout.addWidget(self.frame_button_cmsdk)

    def copy_INFOconnect_wigrts_layout(self, parent_layout):

        self.frame_button_infocon = PY_WIDGEAT.create_collapsible_frame(u' Copy Input / Output Info  (拷贝/转移信息) ',True)
        main_layout = QtWidgets.QVBoxLayout()

        self.infocon_block = PY_WIDGEAT.create_radiogroup(
            title="Type:",
            items=[
                ("transfer Output info", 1, u'源输出对象转移到新对象'),
                ("copy Input info", 2, u'拷贝源对象的输入信息给新对象')
            ],
            default_id=1
        )

        self.hint_out = PY_WIDGEAT.create_text("Transfer the object information of the source output to the new object output.\n将源输出的对象信息转接到新对象输出")
        self.hint_in = PY_WIDGEAT.create_text("Copy the input information of the source object.\n拷贝源对象的输入信息")
        self.hint_in.setVisible(False)

        button_layout = QtWidgets.QHBoxLayout()
        self.apply_btn_infocon = QtWidgets.QPushButton('Apply')
        self.apply_btn_infocon.setProperty("main", True)
        self.help_btn_infocon = QtWidgets.QPushButton()
        self.help_btn_infocon.setIcon(QtGui.QIcon(":\help.png"))
        self.help_btn_infocon.setProperty("help", True)

        button_layout.addWidget(self.apply_btn_infocon, 9)
        button_layout.addWidget(self.help_btn_infocon)

        main_layout.addWidget(self.infocon_block)
        main_layout.addWidget(self.hint_out)
        main_layout.addWidget(self.hint_in)
        main_layout.addLayout(button_layout)
        self.frame_button_infocon.setContentLayout(main_layout)
        parent_layout.addWidget(self.frame_button_infocon)

    def combin_Dirve_wigets_layout(self, parent_layout):
        # 创建并添加"Buttons"的折叠框
        self.frame_button_combine = PY_WIDGEAT.create_collapsible_frame(' Combine connect Dirve  (多个组合控制) ',True)

        main_layout = QtWidgets.QVBoxLayout()

        label = PY_WIDGEAT.create_text("\n> Two or more drivers are used 载入两个或多个驱动器(1.0*1.0)", 12)

        button_layout = QtWidgets.QHBoxLayout()
        self.apply_btn_combine = QtWidgets.QPushButton('Apply')
        self.apply_btn_combine.setProperty("main", True)
        self.help_btn_combine = QtWidgets.QPushButton()
        self.help_btn_combine.setIcon(QtGui.QIcon(":\help.png"))
        self.help_btn_combine.setProperty("help", True)

        button_layout.addWidget(self.apply_btn_combine, 80)
        button_layout.addStretch(1)
        button_layout.addWidget(self.help_btn_combine, 1)

        main_layout.addWidget(label)
        main_layout.addWidget(QtWidgets.QLabel(""))
        main_layout.addLayout(button_layout)
        self.frame_button_combine.setContentLayout(main_layout)
        parent_layout.addWidget(self.frame_button_combine)

    def create_title(self, title, size=20):
        title_widget = QtWidgets.QLabel(title)
        title_widget.setAlignment(QtCore.Qt.AlignCenter)
        title_widget.setFont(QtGui.QFont('bold', size))
        title_widget.setStyleSheet(
            "color: rgb({}, {}, {});".format(self.title_color[0] * 255, self.title_color[1] * 255,
                                             self.title_color[2] * 255))
        return title_widget
        # self.mainLayout.addWidget(title_widget)

    def create_connections(self):
        self.driver_list.itemSelectionChanged.connect(self._on_seleted_driver)
        self.load_driver_btn.clicked.connect(self._on_load_driver)
        self.driven_list.itemSelectionChanged.connect(self._on_seleted_driven)
        self.load_driven_btn.clicked.connect(self._on_load_driven)
        self.optional_block.idClicked.connect(self._optional_type_Toggled)
        self.parent_closest_cbx.stateChanged.connect(self._closest_cbx_Toggled)
        self.apply_btn_op.clicked.connect(self.optional_apply)
        self.help_btn_op.clicked.connect(self.showHHelpImage)
        self.parent_cbx.stateChanged.connect(self._constrain_parent_Toggled)
        self.Constraints_btn.clicked.connect(partial(self.constraints_apply, False))
        self.Connect_btn.clicked.connect(partial(self.constraints_apply, True))
        self.Help_btn_con.clicked.connect(partial(self._show_img, "drive_con"))
        self.apply_btn_sdk.clicked.connect(self.set_driveKey_apply)
        self.help_btn_sdk.clicked.connect(partial(self._show_img, "drive_setKey"))
        self.replace_AttrCheckbox_cmsdk.stateChanged.connect(self._on_replace_attr_textFild)
        self.apply_btn_cmsdk.clicked.connect(self.copy_sdk_apply)
        self.help_btn_cmsdk.clicked.connect(partial(self._show_img, "drive_copySDK"))
        self.infocon_block.idClicked.connect(self._on_infocon_changed)
        self.apply_btn_infocon.clicked.connect(self.transfer_info_apply)
        self.apply_btn_combine.clicked.connect(self.combine_apply)
        self.help_btn_combine.clicked.connect(partial(self._show_img, "drive_combine"))

    def show_context_driver_menu(self, position):
        self.driver_empty_space_menu.exec_(self.driver_list.mapToGlobal(position))

    def show_context_driven_menu(self, position):
        self.driven_empty_space_menu.exec_(self.driven_list.mapToGlobal(position))

    def _show_img(self, img, *args):
        Help.HelpImage("", img)

    def _on_load_driver(self):
        self._obj.load_list_widget_items(self.driver_list,True,True)

    def _on_seleted_driver(self):
        self._obj.list_widget_seleted_item(self.driver_list)

    def _on_load_driven(self):
        self._obj.load_list_widget_items(self.driven_list,True,True)

    def _on_seleted_driven(self):
        self._obj.list_widget_seleted_item(self.driven_list)

    def _optional_type_Toggled(self, btn_id):
        self.parent_closest_cbx.setEnabled(btn_id == 1)

    def _closest_cbx_Toggled(self, state):
        enabled = not bool(state)
        self.optional_block.setEnabledByIds([2, 3, 4], enabled)

    def _constrain_parent_Toggled(self, isChecked):

        if isChecked:
            self.point_cbx.setEnabled(False)
            self.orient_cbx.setEnabled(False)
            self.point_cbx.setChecked(False)
            self.orient_cbx.setChecked(False)

        else:
            self.point_cbx.setEnabled(True)
            self.orient_cbx.setEnabled(True)
            self.point_cbx.setChecked(False)
            self.orient_cbx.setChecked(False)

    def _on_replace_attr_textFild(self,state):
        if self.replace_AttrCheckbox_cmsdk.isChecked():
            self.search_Attr_text.setEnabled(True)
            self.replace_Attr_text.setEnabled(True)

            self.search_Attr_label.setStyleSheet("color: white;")
            self.replace_Attr_label.setStyleSheet("color: white;")

            self.search_Attr_text.setStyleSheet("background-color: black;")
            self.replace_Attr_text.setStyleSheet("background-color: black;")
        else:
            self.search_Attr_text.setEnabled(False)
            self.replace_Attr_text.setEnabled(False)

            self.search_Attr_label.setStyleSheet("color: black;")
            self.replace_Attr_label.setStyleSheet("color: black;")

            self.search_Attr_text.setStyleSheet("background-color: dark grey;")
            self.replace_Attr_text.setStyleSheet("background-color: dark grey;")

    def _on_infocon_changed(self, btn_id):
        self.hint_out.setVisible(btn_id == 1)
        self.hint_in.setVisible(btn_id == 2)

    def _on_radio_outINFO_Toggled(self, checked):

        if checked:
            self.hintText_infocon_out.setVisible(True)
        else:
            self.hintText_infocon_out.setVisible(False)

    def _on_radio_inINFO_Toggled(self, checked):

        if checked:
            self.hintText_infocon_in.setVisible(True)
        else:
            self.hintText_infocon_in.setVisible(False)

    def _cmsdk_block_Toggled(self, checked):
        if checked == 3:
            self.search_replace_widget.setEnabled(False)
        else:
            self.search_replace_widget.setEnabled(True)

    def mirror_selection(self, search_list_widget, replace_list_widget, LtoR = True):
        seleted_obj = self._obj.get_list_widget_seleted(search_list_widget)
        replace_name_obj = self._obj.get_lt_rt_selection(seleted_obj, LtoR)
        self._obj.write_list_widget_items(replace_list_widget, replace_name_obj, clear=False)

    def replace_string_ui(self,search_list_widget,replace_list_widget, obj="Driver"):

        if obj=="Driver":
            SearchFied_label = "Search Driver: "
            ReplaceFied_label = "Replace Driven: "
            btn_label = "Driver > Driven"
        else:
            SearchFied_label = "Search Driven: "
            ReplaceFied_label = "Replace Driver: "
            btn_label = "Driver < Driven"

        if (cmds.window(self.SearchReplaceWindow, q=True, ex=True)):
            cmds.deleteUI(self.SearchReplaceWindow)
        window = cmds.window(self.SearchReplaceWindow, title="Search and Replace UI", wh=(200, 150), s=1)
        cmds.columnLayout(adjustableColumn=True)
        cmds.text(l='TEXT: {}'.format(btn_label))
        cmds.textFieldGrp('pyConstrainSearchPrefixFied', text="", l=SearchFied_label, cw2=(80, 100), adj=2)
        cmds.textFieldGrp('pyConstrainReplacePrefixFied', text="", l=ReplaceFied_label, cw2=(80, 100), adj=2)
        cmds.text(l="")
        cmds.rowColumnLayout(cw=[(1, 25),(3, 25)], nc=3, adj=2)
        cmds.text(l="")
        cmds.button(h=20, c=lambda *args: self.replace_object_name(search_list_widget,replace_list_widget,search_name=cmds.textFieldGrp('pyConstrainSearchPrefixFied',q=True,tx=True), replace_name=cmds.textFieldGrp('pyConstrainReplacePrefixFied',q=True,tx=True)),l=btn_label)
        Help.symbolHelpImageButton(file="", name="constrain_Search_Replace", With=20)
        cmds.setParent('..')
        cmds.text(l="")
        cmds.showWindow(window)

    def replace_object_name(self,search_list_widget,replace_list_widget, search_name, replace_name):
        seleted_obj = self._obj.get_list_widget_seleted(search_list_widget)
        replace_name_obj = self._obj.get_search_replace_selection(seleted_obj, search_name, replace_name)
        self._obj.write_list_widget_items(replace_list_widget, replace_name_obj, False)
        print('Replaced all occurrences of "{}" with "{}"'.format(search_name, replace_name))

    def showHHelpImage(self):
        Value = self.optional_block.checkedId()
        imgs = ["optional_parent", "optional_connectAttr", "optional_inverseMatrix_skin", "optional_addBS"]
        Help.HelpImage("", imgs[Value-1])


    def optional_apply(self):
        closest = self.parent_closest_cbx.isChecked()
        checked_type = self.optional_block.checkedId()
        driver, driven = self._obj.driver_driven_outputItems_list(self.driver_list, self.driven_list)
        self._mfd.apply_Optional(driver, driven, checked_type, closest)


    def constraints_apply(self, connect=False, *args):
        parent = self.parent_cbx.isChecked()
        point = self.point_cbx.isChecked()
        orient = self.orient_cbx.isChecked()
        scale = self.scale_cbx.isChecked()
        driver, driven = self._obj.driver_driven_outputItems_list(self.driver_list, self.driven_list)
        print(driver, driven )
        if connect:
            self._mfd.create_connect(driver, driven, [parent, point, orient, scale])
        else:
            self._mfd.create_constraint(driver, driven, [parent, point, orient, scale])


    def set_driveKey_apply(self):
        driver_value = [self.driver_field1.value(), self.driver_field2.value(), self.driver_field3.value()]
        driven_value = [self.driven_field1.value(), self.driven_field2.value(), self.driven_field3.value()]
        pre_Cycle = self.pre_Cycle_cbx.isChecked()
        post_Cycle = self.post_Cycle_cbx.isChecked()
        driver, driven = self._obj.driver_driven_outputItems_list(self.driver_list, self.driven_list)
        driver_value, driven_value = self._mfd.sift_list_value(driver_value, driven_value)

        self._mfd.SetDrivenKey(driver, driven, driver_value, driven_value, pre_Cycle, post_Cycle)


    def copy_sdk_apply(self):
        prefix_Search = self.search_text.text()
        prefix_Replace = self.replace_text.text()
        _type = self.cmsdk_type_block.checkedId()
        is_rev = self.cmsdk_value_block.checkedId()
        ReplaceAttr_ABLE = self.replace_AttrCheckbox_cmsdk.isChecked()
        map = {1:"+", 2:"-"}

        if ReplaceAttr_ABLE:
            search_Attr = self.search_Attr_text.text()
            replace_Attr = self.replace_Attr_text.text()
        else:
            search_Attr = None
            replace_Attr = None
        driver, driven = self._obj.driver_driven_outputItems_list(self.driver_list, self.driven_list)
        self._mfd._cheek_pairs([driver, driven])
        if prefix_Search is None or prefix_Replace is None:
            mayaPrint.error(" Please enter a string to search/replace ! ")
            return

        else:
            print("------------------The following are the running results------------------")
            for dri, drn in _pair_iter(driver, driven):
                if _type != 3:
                    if "." not in dri or "." not in drn:
                        mayaPrint.error("The loaded object has no attributes, please check")
                        return
                    if _type == 1:
                        self._cysdk.copy_sdk(dri, drn, prefix_Search, prefix_Replace,
                                        search_Attr,
                                        replace_Attr)
                        print(" {} >>> {} is ok".format(dri, drn))
                    elif _type == 2:
                        self._cysdk.copy_input_sdk(dri, drn, prefix_Search, prefix_Replace, search_Attr, replace_Attr,
                                                   posneg=map[is_rev])
                        print(" {} >>> {} is ok".format(dri, drn))
                    else:
                        pass
                else:
                    self._cysdk.mirror_specify_sdk(dri, drn, map[is_rev])
                    print(" {} >>> {} is ok".format(dri, drn))

            mayaPrint.log(" SDK copy succeeded!")


    def transfer_info_apply(self):
        Type = self.infocon_block.checkedId()
        driver, driven = self._obj.driver_driven_outputItems_list(self.driver_list, self.driven_list)
        self._mfd.copy_in_out_connect(driver, driven, Type)


    def combine_apply(self):
        driver, driven = self._obj.driver_driven_outputItems_list(self.driver_list, self.driven_list)
        self._mfd.combine_dirve(driver, driven)
        mayaPrint.log("finish !")


def main():
    global DriveDialog
    try:
        DriveDialog.close() # pylint: disable=E0601
        DriveDialog.deleteLater()
    except:
        pass

    DriveDialog = PYOptionalDriveDialog()
    DriveDialog.show()

if __name__ == '__main__':

    main()
