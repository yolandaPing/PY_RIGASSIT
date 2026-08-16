# -*- coding: utf-8 -*-

# .FileName:ui_openpipeline.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/6/30 20:37
# .Finish time:

import os
from datetime import datetime

try:
    from ui_framework.core.qtCompat import *
    from ui_framework.widgets.widgets import Widgets
except:
    from CommonUse.qtCompat import *
    from CommonUse.widgetsUse import Widgets

_widgets = Widgets()


def build_openpipeline_ui(main_window):

    self = main_window

    main_layout = QtWidgets.QVBoxLayout(self)
    main = QtWidgets.QVBoxLayout()
    main.setContentsMargins(0, 0, 0, 0)
    main.setSpacing(6)
    main_layout.addLayout(main)

    root_row = QtWidgets.QHBoxLayout()
    lbl_root = QtWidgets.QLabel(u'项目路径:')
    lbl_root.setStyleSheet("font: bold ; ")
    lbl_root.setFixedWidth(80)
    self.root_path_label = QtWidgets.QLabel(u'未设置')
    self.root_path_label.setStyleSheet(' color:black; ')
    self.root_path_label.setFixedWidth(320)

    btn_set_root = QtWidgets.QPushButton(u' [设置项目路径] ')
    btn_set_root.setStyleSheet("{} color: black;".format(_widgets.button_bgc))
    btn_set_root.clicked.connect(self.set_project_root_path)
    btn_check_root = QtWidgets.QPushButton(u' [检查项目] ')
    btn_check_root.clicked.connect(self.check_projects_in_root)
    btn_check_config = QtWidgets.QPushButton(u' [检查配置] ')
    btn_check_config.clicked.connect(self.check_config)

    root_row.addWidget(lbl_root)
    root_row.addWidget(self.root_path_label)
    root_row.addWidget(btn_set_root)
    root_row.addWidget(btn_check_root)
    root_row.addWidget(btn_check_config)
    root_row.addStretch()
    main.addLayout(root_row)

    prow = QtWidgets.QHBoxLayout()
    lbl = QtWidgets.QLabel(u'当前项目:')
    lbl.setStyleSheet("font: bold ; ")
    lbl.setFixedWidth(80)
    self.project_combo = QtWidgets.QComboBox()
    self.project_combo.setFixedWidth(200)
    self.project_combo.currentTextChanged.connect(self.on_project_changed)
    btn_new = QtWidgets.QPushButton(u' [新建] ')
    btn_new.setStyleSheet("{} color: black;".format(_widgets.button_bgc))
    btn_new.clicked.connect(self.create_project_dialog)
    btn_open = QtWidgets.QPushButton(u' [打开项目位置] ')
    btn_open.clicked.connect(self.open_existing_project)
    btn_refresh = QtWidgets.QPushButton('')
    btn_refresh.setIcon(QtGui.QIcon(":refresh.png"))
    btn_refresh.setToolTip(u"刷新")
    btn_about = QtWidgets.QPushButton('')
    btn_about.setIcon(QtGui.QIcon(":help.png"))
    btn_about.setToolTip(u"帮助")
    btn_refresh.setProperty("help", True)
    btn_about.setProperty("help", True)
    btn_refresh.clicked.connect(self.load_projects)
    btn_about.clicked.connect(about)

    prow.addWidget(lbl)
    prow.addWidget(self.project_combo)
    prow.addWidget(btn_new)
    prow.addWidget(btn_open)
    prow.addWidget(btn_refresh)
    prow.addWidget(btn_about)
    prow.addStretch()
    main.addLayout(prow)
    _widgets.separator(main, False)
    _widgets.separator(main, True)

    splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

    #资产类型 + 资产列表
    leftw = QtWidgets.QWidget()
    leftl = QtWidgets.QVBoxLayout()
    leftl.setContentsMargins(0, 0, 0, 0)
    leftl.setSpacing(0)
    type_row_group = QtWidgets.QGroupBox(u"类型")
    type_row = QtWidgets.QHBoxLayout(type_row_group)
    type_row.setContentsMargins(4, 4, 4, 4)
    self.type_combo = QtWidgets.QComboBox()
    self.type_combo.currentTextChanged.connect(self.on_asset_type_changed)
    btn_addtype = QtWidgets.QPushButton('+')
    btn_addtype.setFixedWidth(25)
    btn_addtype.setMaximumHeight(25)
    btn_addtype.setStyleSheet("font: bold 16px; {} color: green;".format(_widgets.button_bgc))
    btn_addtype.clicked.connect(self.add_asset_type)
    btn_deltype = QtWidgets.QPushButton('-')
    btn_deltype.setFixedWidth(25)
    btn_deltype.setMaximumHeight(25)
    btn_deltype.setStyleSheet("font: bold 16px; {} color: red;".format(_widgets.button_bgc))
    btn_deltype.clicked.connect(self.delete_asset_type)
    type_row.addWidget(self.type_combo, 1)
    type_row.addWidget(btn_addtype)
    type_row.addWidget(btn_deltype)
    leftl.addWidget(type_row_group)

    asset_group = QtWidgets.QGroupBox(u"对象名称")
    asset_layout = QtWidgets.QVBoxLayout(asset_group)
    asset_layout.setContentsMargins(4, 4, 4, 4)
    self.asset_sort_block = _widgets.create_radiogroup(
        "",
        [(" Name ", 1, None), (" Date ", 2, None),],
        default_id=1
    )
    self.search_edit = QtWidgets.QLineEdit()
    self.search_edit.setPlaceholderText(u'搜索资产...')
    self.search_edit.textChanged.connect(self.filter_assets)

    leftl.addWidget(asset_group)

    self.asset_list = QtWidgets.QListWidget()
    self.asset_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.asset_list.setAlternatingRowColors(True)
    self.asset_list.itemClicked.connect(self.on_asset_clicked)
    self.asset_list.customContextMenuRequested.connect(self.show_asset_context_menu)
    self.asset_sort_block.idClicked.connect(self.on_asset_sort_changed)
    asset_layout.addWidget(self.asset_sort_block)
    asset_layout.addWidget(self.search_edit)
    asset_layout.addWidget(self.asset_list)

    asset_btn_row = QtWidgets.QHBoxLayout()
    self.btn_create_asset = QtWidgets.QPushButton('Add New')
    self.btn_create_asset.clicked.connect(self.create_asset_dialog)
    self.btn_create_asset.setEnabled(False)
    self.btn_delete_asset = QtWidgets.QPushButton('Delete!!!')
    self.btn_delete_asset.clicked.connect(self.delete_asset_dialog)

    self.btn_create_asset.setStyleSheet("font: bold 12px;{} color: black;".format(_widgets.button_bgc))
    self.btn_delete_asset.setStyleSheet("font: bold 12px;{} color: red;".format(_widgets.button_bgc))
    self.btn_delete_asset.setEnabled(False)
    self.btn_delete_asset.setVisible(False)
    asset_btn_row.addWidget(self.btn_create_asset)
    asset_btn_row.addWidget(self.btn_delete_asset)
    asset_btn_row.addStretch()
    asset_layout.addLayout(asset_btn_row)

    leftw.setLayout(leftl)
    leftw.setMinimumWidth(100)

    #子类型 + 版本
    centerw = QtWidgets.QWidget()
    center_layout = QtWidgets.QVBoxLayout(centerw)
    center_layout.setContentsMargins(0, 0, 0, 0)

    subtype_frame = QtWidgets.QGroupBox(u"任务")
    subtype_layout = QtWidgets.QVBoxLayout(subtype_frame)
    subtype_layout.setContentsMargins(4, 4, 4, 4)
    subtype_layout.setSpacing(6)
    self.info_label = QtWidgets.QLabel(u'未选择资产')
    self.info_label.setWordWrap(True)
    self.info_label.setAlignment(QtCore.Qt.AlignLeft)
    self.info_label.setMaximumHeight(15)
    self.info_label.setStyleSheet('color:yellow; font-size: 12px;')
    subtype_layout.addWidget(self.info_label)

    self.subtype_list = QtWidgets.QListWidget()
    self.subtype_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.subtype_list.setAlternatingRowColors(True)
    self.subtype_list.itemClicked.connect(self.on_subtype_clicked)
    self.subtype_list.itemDoubleClicked.connect(self.on_subtype_double_clicked)
    self.subtype_list.customContextMenuRequested.connect(self.show_subtype_context_menu)
    subtype_layout.addWidget(self.subtype_list)

    sub_btns = QtWidgets.QHBoxLayout()
    self.btn_add_sub = QtWidgets.QPushButton(u'Add New')
    self.btn_del_sub = QtWidgets.QPushButton(u'Delete')
    self.btn_rename_sub = QtWidgets.QPushButton(u'Rename')
    self.btn_add_sub.setEnabled(False)
    self.btn_rename_sub.setEnabled(False)
    self.btn_del_sub.setEnabled(False)

    self.btn_add_sub.setStyleSheet('font: bold 12px;')
    self.btn_del_sub.setStyleSheet('font: bold 12px;')
    self.btn_rename_sub.setStyleSheet('font: bold 12px;')

    sub_btns.addWidget(self.btn_add_sub)
    sub_btns.addWidget(self.btn_rename_sub)
    sub_btns.addWidget(self.btn_del_sub)

    subtype_layout.addLayout(sub_btns)

    self.btn_add_sub.clicked.connect(self.add_subtype_dialog)
    self.btn_del_sub.clicked.connect(self.delete_subtype)
    self.btn_rename_sub.clicked.connect(self.rename_subtype)

    version_frame = QtWidgets.QGroupBox(u"版本")
    version_layout = QtWidgets.QVBoxLayout(version_frame)
    version_layout.setContentsMargins(4, 4, 4, 4)

    version_title_layout = QtWidgets.QHBoxLayout()
    version_title_layout.addWidget(QtWidgets.QLabel(''))
    self.version_count_text = _widgets.create_text('')
    self.version_count_text.setWordWrap(True)
    version_title_layout.addWidget(self.version_count_text)
    version_layout.addLayout(version_title_layout)

    self.version_list = QtWidgets.QListWidget()
    self.version_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.version_list.setAlternatingRowColors(True)
    self.version_list.itemDoubleClicked.connect(self.open_selected_version)
    self.version_list.customContextMenuRequested.connect(self.show_version_context_menu)
    version_layout.addWidget(self.version_list)

    vbtn_row1 = QtWidgets.QHBoxLayout()
    self.btn_save_new_version = QtWidgets.QPushButton('Save Workshop')
    self.btn_save_new_version.clicked.connect(self.save_new_version)
    self.btn_save_new_version.setProperty("main", True)
    self.btn_save_new_version.setStyleSheet("color: gray;")
    self.btn_save_new_version.setEnabled(False)
    vbtn_row1.addWidget(self.btn_save_new_version)

    vbtn_row2 = QtWidgets.QHBoxLayout()
    self.btn_set_master = QtWidgets.QPushButton('Save Master')
    self.btn_set_master.clicked.connect(self.save_new_master)
    # self.btn_set_master.setProperty("main", True)
    # self.btn_set_master.setStyleSheet("color: green;")
    self.btn_set_master.setEnabled(False)
    self.btn_open_master = QtWidgets.QPushButton('Open Master')
    self.btn_open_master.clicked.connect(self.open_master)
    self.btn_open_master.setEnabled(False)
    self.btn_reference_master = QtWidgets.QPushButton('Reference Master')
    self.btn_reference_master.clicked.connect(self.reference_master)
    self.btn_reference_master.setEnabled(False)
    self.btn_set_master.setMaximumHeight(25)
    self.btn_open_master.setMaximumHeight(25)
    self.btn_reference_master.setMaximumHeight(25)
    vbtn_row2.addWidget(self.btn_set_master)
    vbtn_row2.addWidget(self.btn_open_master)
    vbtn_row2.addWidget(self.btn_reference_master)

    version_layout.addLayout(vbtn_row1)
    version_layout.addLayout(vbtn_row2)

    vsplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
    vsplitter.addWidget(subtype_frame)
    vsplitter.addWidget(version_frame)
    vsplitter.setSizes([150, 600])
    center_layout.addWidget(vsplitter)
    centerw.setMinimumWidth(150)

    # 预览 + Notes
    rightw = QtWidgets.QWidget()
    rightw.setMinimumWidth(150)
    right_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)

    top_container = QtWidgets.QWidget()
    top_layout = QtWidgets.QVBoxLayout(top_container)
    top_layout.setContentsMargins(0, 0, 0, 0)
    pv_col_grp = QtWidgets.QGroupBox(u"预览")
    pv_col = QtWidgets.QVBoxLayout(pv_col_grp)
    pv_col.setContentsMargins(4, 6, 4, 4)

    self.preview_label = QtWidgets.QLabel()
    self.preview_label.setMinimumSize(220, 161)
    self.preview_label.setAlignment(QtCore.Qt.AlignCenter)
    self.preview_label.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken)
    self.preview_label.setStyleSheet("background-color: #2b2b2b; color: #888;")

    self.btn_snapshot = QtWidgets.QPushButton('Take Snapshot')
    self.btn_snapshot.clicked.connect(self.take_snapshot)
    self.btn_snapshot.setEnabled(False)
    pv_col.addWidget(self.btn_snapshot)
    pv_col.addWidget(self.preview_label)

    top_layout.addWidget(pv_col_grp)
    top_container.setMinimumHeight(200)
    top_container.setMaximumHeight(500)

    bottom_container = QtWidgets.QGroupBox("Notes")
    bottom_layout = QtWidgets.QVBoxLayout(bottom_container)
    bottom_layout.setContentsMargins(4, 6, 4, 4)

    self.notes_text = QtWidgets.QTextEdit()
    self.notes_text.setReadOnly(True)
    self.notes_text.setProperty("isNotes", True)
    self.notes_text.setMinimumHeight(150)
    bottom_layout.addWidget(self.notes_text)

    right_splitter.addWidget(top_container)
    right_splitter.addWidget(bottom_container)
    right_splitter.setStretchFactor(0, 0)
    right_splitter.setStretchFactor(1, 1)

    right_layout = QtWidgets.QVBoxLayout(rightw)
    right_layout.setContentsMargins(0, 0, 0, 0)
    right_layout.addWidget(right_splitter)

    splitter.addWidget(leftw)
    splitter.addWidget(centerw)
    splitter.addWidget(rightw)
    splitter.setSizes([120, 220, 160])
    main.addWidget(splitter)

    _widgets.create_copyrightText(main_layout, self.timeStamp)

    main_layout.setStretch(0, 1)
    main_layout.setStretch(1, 0)
    main_layout.setStretch(2, 0)


def about():
    import HelpImageUI as help
    help.HelpImage("", "pypenpipeline")