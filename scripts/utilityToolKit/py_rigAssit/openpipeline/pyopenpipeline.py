# -*- coding: utf-8 -*-
# .FileName: pyopenpipeline.py
# .Author  : Yolanda Ping
# .Date    : 2025/12/13

import os
import sys
import json
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime

try:
    import maya.cmds as cmds
    import maya.mel as mel

    IN_MAYA = True
except ImportError:
    cmds = None
    mel = None
    IN_MAYA = False

from py_rigAssit.openpipeline.fbx_dialog import FBXExportDialog
from py_rigAssit.openpipeline.version_context import (show_asset_context_menu, show_subtype_context_menu, show_version_context_menu)
from py_rigAssit.openpipeline.version import VERSION, TIMESTAMP
from py_rigAssit.openpipeline.asset_info import PROJECTS_XML
from Pipeline.pipelineConfig import OpenPipelineConfig
from Pipeline.projectManager import ProjectManager
from Pipeline.pipelineUtils import (load_projects_from_xml, get_projects_xml_path, ensure_projects_xml, add_project_to_xml, open_folder_in_explorer, open_file_in_explorer)

try:
    from ui_framework.core.qtCompat import *
    from ui_framework.widgets.widgets import Widgets, PyouPersistentWindow
except:
    from CommonUse.qtCompat import *
    from CommonUse.widgetsUse import Widgets, PyouPersistentWindow

_widgets = Widgets()


class PYPenpipelineDialog(PyouPersistentWindow):
    def __init__(self, parent=_widgets.maya_main_window()):
        super(PYPenpipelineDialog, self).__init__("PYPenpipelineDlgApp", "PYPenpipelineDialog", parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.setWindowFlags(QtCore.Qt.Window |
                            QtCore.Qt.WindowMinimizeButtonHint |
                            QtCore.Qt.WindowMaximizeButtonHint |
                            QtCore.Qt.WindowCloseButtonHint)

        self.cfg = OpenPipelineConfig()

        self.timeStamp = TIMESTAMP
        self.WINDOW_NAME = 'OpenPipeline v{} (Maya{})'.format(VERSION, cmds.about(version=True))

        self.pm = None
        self.current_project_path = ''
        self.current_project_name = ''
        self.current_asset_type = ''
        self.selected_asset = None
        self.selected_subtype = None
        self.new_proj_name = None
        self.new_proj_path = None
        self.new_asset_name = None
        self.fbx_config = None
        self._fbx_dialog = None

        self.setWindowTitle(self.WINDOW_NAME)
        self.loadWindowSettings()

        self.init_ui()

        self.load_projects()
        self.select_last_project()
        self.load_fbx_config()

    def show_info(self, title, message):
        QtWidgets.QMessageBox.information(self, title, message)

    def show_warning(self, title, message):
        QtWidgets.QMessageBox.warning(self, title, message)

    def show_critical(self, title, message):
        QtWidgets.QMessageBox.critical(self, title, message)

    def show_info_delayed(self, title, message, delay=2000):
        QtCore.QTimer.singleShot(delay, lambda: QtWidgets.QMessageBox.information(self, title, message))

    def show_warning_delayed(self, title, message, delay=2000):
        QtCore.QTimer.singleShot(delay, lambda: QtWidgets.QMessageBox.warning(self, title, message))

    def show_critical_delayed(self, title, message, delay=2000):
        QtCore.QTimer.singleShot(delay, lambda: QtWidgets.QMessageBox.critical(self, title, message))

    def init_ui(self):

        main_layout = QtWidgets.QVBoxLayout(self)
        main = QtWidgets.QVBoxLayout()
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

        # project row
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
        btn_open = QtWidgets.QPushButton(' [打开项目] ')
        btn_open.clicked.connect(self.open_existing_project)
        btn_refresh = QtWidgets.QPushButton('')
        btn_refresh.setIcon(QtGui.QIcon(":refresh.png"))
        btn_refresh.setToolTip(u"刷新")
        btn_refresh.clicked.connect(self.load_projects)

        prow.addWidget(lbl)
        prow.addWidget(self.project_combo)
        prow.addWidget(btn_new)
        prow.addWidget(btn_open)
        prow.addWidget(btn_refresh)
        prow.addStretch()
        main.addLayout(prow)

        _widgets.separator(main, True)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # left: asset types + asset list
        leftw = QtWidgets.QWidget()

        leftl = QtWidgets.QVBoxLayout()
        leftl.setContentsMargins(0, 0, 0, 0)
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

        self.search_edit = QtWidgets.QLineEdit()
        self.search_edit.setPlaceholderText(u'搜索资产...')
        self.search_edit.textChanged.connect(self.filter_assets)

        leftl.addWidget(asset_group)

        self.asset_list = QtWidgets.QListWidget()
        self.asset_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.asset_list.setAlternatingRowColors(True)
        self.asset_list.itemClicked.connect(self.on_asset_clicked)
        self.asset_list.customContextMenuRequested.connect(self.show_asset_context_menu)

        asset_layout.addWidget(self.search_edit)
        asset_layout.addWidget(self.asset_list)

        asset_btn_row = QtWidgets.QHBoxLayout()
        self.btn_create_asset = QtWidgets.QPushButton('New')
        self.btn_create_asset.clicked.connect(self.create_asset_dialog)
        self.btn_create_asset.setEnabled(False)
        self.btn_delete_asset = QtWidgets.QPushButton('Delete!!!')
        self.btn_delete_asset.clicked.connect(self.delete_asset_dialog)

        self.btn_create_asset.setProperty("main", True)
        self.btn_delete_asset.setProperty("main", True)
        self.btn_delete_asset.setStyleSheet("color: red;")
        self.btn_delete_asset.setEnabled(False)
        self.btn_delete_asset.setVisible(False)
        asset_btn_row.addWidget(self.btn_create_asset)
        asset_btn_row.addWidget(self.btn_delete_asset)
        asset_btn_row.addStretch()
        asset_layout.addLayout(asset_btn_row)
        leftw.setLayout(leftl)
        leftw.setMinimumWidth(100)

        centerw = QtWidgets.QWidget()
        center_layout = QtWidgets.QVBoxLayout(centerw)
        center_layout.setContentsMargins(0, 0, 0, 0)

        subtype_frame = QtWidgets.QGroupBox(u"任务")
        subtype_layout = QtWidgets.QVBoxLayout(subtype_frame)

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
        self.btn_add_sub = QtWidgets.QPushButton(u'New')

        self.btn_add_sub.setEnabled(False)
        self.btn_del_sub = QtWidgets.QPushButton(u'Delete')

        self.btn_del_sub.setEnabled(False)
        self.btn_rename_sub = QtWidgets.QPushButton(u'Rename')

        self.btn_add_sub.setProperty("main", True)
        self.btn_add_sub.setStyleSheet("color: green;")
        self.btn_del_sub.setProperty("main", True)
        self.btn_rename_sub.setProperty("main", True)
        self.btn_rename_sub.setEnabled(False)

        sub_btns.addWidget(self.btn_add_sub)
        sub_btns.addWidget(self.btn_del_sub)
        sub_btns.addWidget(self.btn_rename_sub)
        subtype_layout.addLayout(sub_btns)

        self.btn_add_sub.clicked.connect(self.add_subtype_dialog)
        self.btn_del_sub.clicked.connect(self.delete_subtype)
        self.btn_rename_sub.clicked.connect(self.rename_subtype)

        version_frame = QtWidgets.QGroupBox("版本")
        version_layout = QtWidgets.QVBoxLayout(version_frame)
        version_layout.setContentsMargins(4, 4, 4, 4)

        version_title_layout = QtWidgets.QHBoxLayout()
        version_title_layout.addWidget(QtWidgets.QLabel(''))
        self.version_count_text = _widgets.create_text('')
        self.version_count_text.setWordWrap(True)
        version_title_layout.addWidget(self.version_count_text)
        version_layout.addLayout(version_title_layout)
        # version_layout.addWidget(self.version_count_text)

        self.version_list = QtWidgets.QListWidget()
        self.version_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.version_list.setAlternatingRowColors(True)
        self.version_list.itemDoubleClicked.connect(self.open_selected_version)
        self.version_list.customContextMenuRequested.connect(self.show_version_context_menu)
        version_layout.addWidget(self.version_list)

        vbtn_row1 = QtWidgets.QHBoxLayout()
        self.btn_save_new_version = QtWidgets.QPushButton('Save Workshop')
        self.btn_save_new_version.clicked.connect(self.save_new_version)
        self.btn_save_new_version.setStyleSheet("{} color: red;".format(_widgets.button_bgc))
        self.btn_save_new_version.setEnabled(False)
        self.btn_import_version = QtWidgets.QPushButton('Import')
        self.btn_import_version.clicked.connect(self.import_selected_version)
        self.btn_import_version.setEnabled(False)
        self.btn_reference_version = QtWidgets.QPushButton('Reference')
        self.btn_reference_version.clicked.connect(self.reference_selected_version)
        self.btn_reference_version.setEnabled(False)
        self.btn_save_new_version.setMaximumHeight(25)
        self.btn_import_version.setMaximumHeight(25)
        self.btn_reference_version.setMaximumHeight(25)
        vbtn_row1.addWidget(self.btn_save_new_version)
        vbtn_row1.addWidget(self.btn_import_version)
        vbtn_row1.addWidget(self.btn_reference_version)

        vbtn_row2 = QtWidgets.QHBoxLayout()
        self.btn_set_master = QtWidgets.QPushButton('Save Master')
        self.btn_set_master.clicked.connect(self.save_new_master)
        self.btn_set_master.setStyleSheet("{} color: green;".format(_widgets.button_bgc))
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

        # right: info, preview, notes
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

        self.setLayout(main_layout)

        _widgets.create_copyrightText(main_layout, self.timeStamp)

        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 0)
        main_layout.setStretch(2, 0)

        self.update_root_path_label()

    # ================== 右键菜单功能 ==================
    def show_asset_context_menu(self, position):
        show_asset_context_menu(self, position)

    def show_subtype_context_menu(self, position):
        show_subtype_context_menu(self, position)

    def show_version_context_menu(self, position):
        show_version_context_menu(self, position)

    # ================== 配置文件管理 ==================
    def update_root_path_label(self):
        """更新项目根路径显示"""
        root_path = self.cfg.get_project_root_path()
        if root_path:
            normalized_path = root_path.replace('\\', '/')
            self.root_path_label.setText(normalized_path)
            self.root_path_label.setToolTip(normalized_path)
        else:
            self.root_path_label.setText(u'未设置')
            self.root_path_label.setToolTip('')

    def check_config(self):
        """检查配置信息"""
        try:
            config_file = self.cfg.get_config_file_path()
            config_exists = os.path.exists(config_file)
            config_content = "配置文件不存在"
            if config_exists:
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config_content = json.load(f)
                except:
                    try:
                        with open(config_file, 'r') as f:
                            config_content = json.load(f)

                    except Exception as e:
                        config_content = u"读取配置文件失败: {}".format(str(e))

            message = u"配置文件路径: {}\n".format(config_file)
            message += u"配置文件存在: {}\n".format(config_exists)
            message += u"项目根路径: {}\n".format(self.cfg.get_project_root_path())
            message += u"上次选择的项目: {}\n".format(self.cfg.get_last_project())
            message += u"配置文件内容:\n{}\n".format(json.dumps(config_content, indent=4) if isinstance(config_content, dict) else config_content)
            self.show_info(u'配置检查', message)
        except Exception as e:
            self.show_warning(u'错误', u"检查配置时出错: {}".format(str(e)))

    # ================== FBX配置管理 ==================
    def load_fbx_config(self):
        """从配置文件加载FBX导出设置"""
        try:
            self.fbx_config = self.cfg.get_fbx_export_info()
            if not self.fbx_config:
                self.fbx_config = ['Geo_grp', 'root_jnt']
                self.save_fbx_config(self.fbx_config)
        except Exception as e:
            print(u"加载FBX配置失败: {}".format(str(e)))

    def save_fbx_config(self, fbx_export):
        """保存FBX导出设置到配置文件"""
        try:
            self.cfg.set_fbx_export_info(fbx_export)
        except Exception as e:
            print(u"保存FBX配置失败: {}".format(str(e)))

    def set_fbx_export_objects(self):
        """设置FBX导出对象对话框（使用独立的非模态对话框类）"""
        if hasattr(self, '_fbx_dialog') and self._fbx_dialog:
            self._fbx_dialog.raise_()
            self._fbx_dialog.activateWindow()
            return

        dialog = FBXExportDialog(parent=self, fbx_config=self.fbx_config)
        dialog.setWindowFlags(QtCore.Qt.Window)
        self._fbx_dialog = dialog

        dialog.accepted.connect(lambda: self._on_fbx_dialog_accepted(dialog))
        dialog.rejected.connect(lambda: setattr(self, '_fbx_dialog', None))
        dialog.finished.connect(lambda: setattr(self, '_fbx_dialog', None))

        dialog.show()

    def _on_fbx_dialog_accepted(self, dialog):
        """FBX对话框确认后的处理函数"""
        new_settings = dialog.get_settings()
        if new_settings[0] and new_settings[1]:
            self.fbx_config = new_settings
            self.save_fbx_config(self.fbx_config)
            self.show_info(u'成功',
                           u'FBX导出设置已保存:\n\n几何体组: {}\n根关节: {}'.format(
                               new_settings[0], new_settings[1]))
        self._fbx_dialog = None

    # ================== 项目管理 ==================
    def set_project_root_path(self):
        """设置项目根路径"""
        current_root = self.cfg.get_project_root_path()
        start_dir = current_root if current_root else ''
        root_path = QtWidgets.QFileDialog.getExistingDirectory(self, u'选择项目根路径', start_dir)
        if root_path:
            normalized_path = root_path.replace('\\', '/')
            success = self.cfg.set_project_root_path(normalized_path)
            if success:
                self.cfg = OpenPipelineConfig()
            else:
                self.show_warning(u'错误', u'保存配置失败，请检查文件权限')
                return

            self.update_root_path_label()
            xml_path = os.path.join(normalized_path, PROJECTS_XML)
            if os.path.exists(xml_path):
                try:
                    self.load_projects()
                except Exception as e:
                    self.show_warning(u'错误', u'加载项目配置文件失败:\n{}'.format(str(e)))
            else:
                reply = QtWidgets.QMessageBox.question(self, u'未找到项目配置文件',
                                                       u'在{path}中未找到{PROJECTS_XML}文件，是否创建新的项目配置文件？'.format(
                                                           path=normalized_path, PROJECTS_XML=PROJECTS_XML),
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    ensure_projects_xml(self.cfg)
                    self.load_projects()

    def check_projects_in_root(self):
        """检查项目根路径下的项目"""
        root_path = self.cfg.get_project_root_path()
        if not root_path:
            self.show_warning(u'提示', u'请先设置项目根路径')
            return

        xml_path = os.path.join(root_path, PROJECTS_XML)
        if not os.path.exists(xml_path):
            self.show_info(u'检查结果',
                           u'在{path}中未找到{PROJECTS_XML}文件'.format(path=root_path,
                                                                        PROJECTS_XML=PROJECTS_XML))
            return

        projects = load_projects_from_xml(self.cfg)
        missing_projects = []
        valid_projects = []

        for name, path in projects.items():
            if os.path.exists(path):
                valid_projects.append(u'✓ {name}: {path}'.format(name=name, path=path))
            else:
                missing_projects.append(u'✗ {name}: {path} (路径不存在)'.format(name=name, path=path))

        message = u'项目根路径: {root_path}\n'.format(root_path=root_path)
        message += u'XML文件: {xml_path}\n'.format(xml_path=xml_path)
        message += u'找到 {count} 个项目定义\n\n'.format(count=len(projects))

        if valid_projects:
            message += u'有效项目 ({count}个):\n'.format(count=len(valid_projects))
            message += '\n'.join(valid_projects) + u'\n\n'
        else:
            message += u'无有效项目\n\n'

        if missing_projects:
            message += u'无效项目 ({count}个):\n'.format(count=len(missing_projects))
            message += '\n'.join(missing_projects)

        self.show_info(u'项目检查结果', message)

    def load_projects(self):
        self.project_combo.clear()
        self.project_combo.addItem(u'', '')

        root_path = self.cfg.get_project_root_path()
        if not root_path:
            self.project_combo.addItem(u'请先设置项目根路径', '')
            return

        xml_projects = load_projects_from_xml(self.cfg)
        if not xml_projects:
            self.project_combo.addItem(u'没有找到项目', '')
            return

        for name, path in xml_projects.items():
            self.project_combo.addItem(name, path)

    def select_last_project(self):
        """选择上次打开的项目（通过项目完整路径查找）"""
        last_project_path = self.cfg.get_last_project()
        last_assetType = self.cfg.get_last_select_type()
        last_asset = self.cfg.get_last_select_asset()

        if last_project_path:
            # 规范化路径用于比较
            normalized_last_path = last_project_path.replace('\\', '/').rstrip('/')
            print(u"尝试选择上次的项目: {}".format(normalized_last_path))

            # 在组合框中查找对应的项目名称
            for i in range(self.project_combo.count()):
                item_data = self.project_combo.itemData(i)

                if item_data:
                    normalized_item_data = item_data.replace('\\', '/').rstrip('/')
                    if normalized_item_data == normalized_last_path:
                        self.project_combo.setCurrentIndex(i)
                        print(u"已自动选择上次的项目: {}".format(self.project_combo.itemText(i)))

                        QtCore.QTimer.singleShot(100,
                                                 lambda: self._select_last_type_and_asset(last_assetType, last_asset))
                        break

    def _select_last_type_and_asset(self, last_assetType, last_asset):
        """选择上次的资产类型和资产"""
        if last_assetType:
            # 等待类型组合框加载完成
            for t in range(self.type_combo.count()):
                type_text = self.type_combo.itemText(t)  # 使用 itemText 而不是 itemData
                if type_text == last_assetType:
                    self.type_combo.setCurrentIndex(t)
                    print(u"已自动选择上次的项目类型: {}".format(last_assetType))
                    QtCore.QTimer.singleShot(100, lambda: self._select_last_asset(last_asset))
                    break

    def _select_last_asset(self, last_asset):
        """选择上次的资产"""
        if last_asset:
            for a in range(self.asset_list.count()):
                item = self.asset_list.item(a)
                if item and item.text() == last_asset:
                    self.asset_list.setCurrentRow(a)
                    self.selected_asset = last_asset
                    self.load_subtypes()
                    self.show_asset_preview(self.current_asset_type, last_asset)
                    print(u"已自动选择上次的项目资产: {}".format(last_asset))
                    break

    def on_project_changed(self, text):
        if not text or text == u'-- 选择项目 --' or text == u'请先设置项目根路径' or text == u'没有找到项目':
            self.pm = None
            self.current_project_path = ''
            self.current_project_name = ''
            self.btn_create_asset.setEnabled(False)
            self.btn_delete_asset.setEnabled(False)
            self.btn_delete_asset.setVisible(False)
            self.btn_add_sub.setEnabled(False)
            self.btn_del_sub.setEnabled(False)
            self.btn_rename_sub.setEnabled(False)
            self.btn_snapshot.setEnabled(False)
            self.asset_list.clear()
            self.subtype_list.clear()
            self.clear_right()
            self.type_combo.clear()
            return

        path = self.project_combo.currentData()
        if path:
            normalized_path = path.replace('\\', '/')
            if os.path.exists(normalized_path):
                self.current_project_path = normalized_path
                self.current_project_name = text
                self.cfg.set_last_project(normalized_path)
                lib = self.get_library_folder_from_xml(text)
                self.pm = ProjectManager(normalized_path, text, lib)
                self.update_asset_type_combo()
                self.btn_create_asset.setEnabled(True)
                self.btn_add_sub.setEnabled(False)
                self.btn_del_sub.setEnabled(False)
                self.btn_rename_sub.setEnabled(False)
                self.btn_snapshot.setEnabled(False)
                self.cfg.add_project_path(normalized_path)
                self.load_assets()
            else:
                self.show_warning(u'错误',
                                  u'项目路径不存在:\n{path}\n\n请检查项目是否被移动或删除。'.format(
                                      path=normalized_path))

    def get_library_folder_from_xml(self, project_name):
        """从XML获取项目的library_folder配置"""
        xml_path = get_projects_xml_path(self.cfg)
        if not xml_path or not os.path.exists(xml_path):
            return self.cfg.config.get('library_folder', 'lib')

        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            for proj in root.findall('project'):
                name_elem = proj.find('name')
                if name_elem is not None and name_elem.text == project_name:
                    lf_elem = proj.find('libraryfolder')
                    if lf_elem is not None and lf_elem.text:
                        return lf_elem.text
        except Exception as e:
            print(u"从XML读取library_folder失败: {}".format(e))

        return self.cfg.config.get('library_folder', 'lib')

    def open_existing_project(self):
        """打开现有项目：选择项目文件夹"""
        root_path = self.cfg.get_project_root_path()
        if not root_path:
            self.show_warning(u'提示', u'请先设置项目根路径')
            return

        project_dir = QtWidgets.QFileDialog.getExistingDirectory(self, u'选择项目文件夹', root_path)
        if project_dir:
            normalized_dir = project_dir.replace('\\', '/')
            if not normalized_dir.startswith(root_path.replace('\\', '/')):
                self.show_warning(u'错误',
                                  u'选择的项目不在项目根路径下:\n\n项目根路径: {root}\n项目路径: {project}'.format(
                                      root=root_path, project=normalized_dir))
                return

            project_name = os.path.basename(normalized_dir.rstrip('/'))
            xml_projects = load_projects_from_xml(self.cfg)

            if project_name in xml_projects:
                idx = self.project_combo.findText(project_name)
                if idx >= 0:
                    self.project_combo.setCurrentIndex(idx)
            else:
                reply = QtWidgets.QMessageBox.question(self, u'项目未注册',
                                                       u'项目"{name}"未在系统中注册，是否现在注册？'.format(
                                                           name=project_name),
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    if not normalized_dir.endswith('/'):
                        normalized_dir = normalized_dir + '/'

                    add_project_to_xml(self.cfg, project_name, normalized_dir)
                    self.load_projects()
                    idx = self.project_combo.findText(project_name)
                    if idx >= 0:
                        self.project_combo.setCurrentIndex(idx)

    def create_project_dialog(self):
        root_path = self.cfg.get_project_root_path()
        if not root_path:
            self.show_warning(u'提示', u'请先设置项目根路径')
            return

        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle('创建项目')
        dlg.setFixedSize(420, 180)
        lay = QtWidgets.QVBoxLayout()

        row1 = QtWidgets.QHBoxLayout()
        row1.addWidget(QtWidgets.QLabel(u'项目名称:'))
        self.new_proj_name = QtWidgets.QLineEdit()
        row1.addWidget(self.new_proj_name)

        row2 = QtWidgets.QHBoxLayout()
        row2.addWidget(QtWidgets.QLabel(u'项目根路径:'))
        self.new_proj_path = QtWidgets.QLabel(root_path)
        self.new_proj_path.setStyleSheet('background:#eee; padding:4px; border:1px solid #ccc;')
        row2.addWidget(self.new_proj_path)

        row3 = QtWidgets.QHBoxLayout()
        row3.addWidget(QtWidgets.QLabel(u'库文件夹:'))
        self.new_proj_lib = QtWidgets.QLineEdit()
        self.new_proj_lib.setText(self.cfg.config.get('library_folder', 'lib'))
        row3.addWidget(self.new_proj_lib)

        btn_row = QtWidgets.QHBoxLayout()
        ok = QtWidgets.QPushButton(u'创建')
        ok.clicked.connect(lambda: self._create_project(dlg))
        cancel = QtWidgets.QPushButton(u'取消')
        cancel.clicked.connect(dlg.reject)
        btn_row.addStretch()
        btn_row.addWidget(ok)
        btn_row.addWidget(cancel)

        lay.addLayout(row1)
        lay.addLayout(row2)
        lay.addLayout(row3)
        lay.addLayout(btn_row)
        dlg.setLayout(lay)
        dlg.exec_()

    def _create_project(self, dlg):
        name = self.new_proj_name.text().strip()
        root_path = self.cfg.get_project_root_path()
        lib = self.new_proj_lib.text().strip()

        if not name:
            self.show_warning(u'错误', u'请填写项目名称')
            return

        if not lib:
            lib = 'lib'

        project_root = os.path.join(root_path, name)
        project_root = project_root.replace('\\', '/')
        if not project_root.endswith('/'):
            project_root = project_root + '/'

        xml_projects = load_projects_from_xml(self.cfg)
        if name in xml_projects:
            self.show_warning(u'错误', u'项目"{name}"已存在'.format(name=name))
            return

        project_dir = project_root.rstrip('/')
        if os.path.exists(project_dir):
            reply = QtWidgets.QMessageBox.question(self, u'文件夹已存在',
                                                   u'文件夹"{name}"已存在于项目根路径下，是否继续？'.format(name=name),
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No:
                return

        os.makedirs(project_dir, exist_ok=True)
        os.makedirs(os.path.join(project_dir, lib), exist_ok=True)

        ensure_projects_xml(self.cfg)
        add_project_to_xml(self.cfg, name, project_root, libraryfolder=lib)
        self.cfg.add_project_path(project_root)
        self.load_projects()
        idx = self.project_combo.findText(name)
        if idx >= 0:
            self.project_combo.setCurrentIndex(idx)

        dlg.accept()
        self.show_info(u'成功', u'项目 {name} 创建并记录'.format(name=name))

    # ================== 资产管理 ==================
    def get_current_asset_types(self):
        """动态获取当前项目的资产类型（lib路径下的文件夹名称）"""
        asset_types = []
        if not self.pm:
            return asset_types

        try:
            lib_path = os.path.join(self.pm.project_root, self.pm.library_folder)
            if os.path.exists(lib_path):
                for item in os.listdir(lib_path):
                    item_path = os.path.join(lib_path, item)
                    if os.path.isdir(item_path):
                        asset_types.append(item)
                asset_types.sort()
        except Exception as e:
            print(u"获取资产类型失败: {}".format(e))

        return asset_types

    def update_asset_type_combo(self):
        """更新资产类型下拉框"""
        self.type_combo.clear()
        if not self.pm:
            return

        asset_types = self.get_current_asset_types()
        if asset_types:
            for asset_type in asset_types:
                self.type_combo.addItem(asset_type, asset_type)  # 设置 itemData
            if asset_types:
                self.current_asset_type = asset_types[0]
        else:
            self.type_combo.addItem(u'暂无资产类型')
            self.current_asset_type = ''

    def add_asset_type(self):
        """添加资产类型（在lib路径下创建文件夹）"""
        if not self.pm:
            self.show_warning(u'错误', u'请先选择项目')
            return

        text, ok = QtWidgets.QInputDialog.getText(self, u'添加资产类型', u'输入资产类型名称:')
        if ok and text.strip():
            t = text.strip()
            existing_types = self.get_current_asset_types()
            if t in existing_types:
                self.show_warning(u'提示', u'资产类型 {t} 已存在'.format(t=t))
                return

            try:
                lib_path = os.path.join(self.pm.project_root, self.pm.library_folder)
                new_type_path = os.path.join(lib_path, t)
                if not os.path.exists(lib_path):
                    os.makedirs(lib_path)
                os.makedirs(new_type_path)
                self.update_asset_type_combo()
                index = self.type_combo.findText(t)
                if index >= 0:
                    self.type_combo.setCurrentIndex(index)
                self.show_info(u'成功', u'资产类型 {t} 已添加'.format(t=t))
            except Exception as e:
                self.show_warning(u'错误', u'创建资产类型失败: {error}'.format(error=str(e)))

    def delete_asset_type(self):
        """删除资产类型（删除lib路径下的文件夹）"""
        if not self.pm:
            self.show_warning(u'错误', u'请先选择项目')
            return

        current_type = self.type_combo.currentText()
        if not current_type or current_type == u'暂无资产类型':
            self.show_warning(u'提示', u'请先选择一个资产类型')
            return

        lib_path = os.path.join(self.pm.project_root, self.pm.library_folder)
        type_path = os.path.join(lib_path, current_type)

        if not os.path.exists(type_path):
            self.show_warning(u'错误', u'资产类型文件夹不存在')
            return

        try:
            items = os.listdir(type_path)
            if items:
                reply = QtWidgets.QMessageBox.question(self, u'确认删除',
                                                       u'资产类型 "{current_type}" 文件夹不为空，包含 {count} 个文件/文件夹。确定要删除吗？'.format(
                                                           current_type=current_type, count=len(items)),
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if reply != QtWidgets.QMessageBox.Yes:
                    return
        except:
            pass

        reply = QtWidgets.QMessageBox.question(self, u'确认删除',
                                               u'确定要删除资产类型 "{current_type}" 吗？此操作不可撤销。'.format(
                                                   current_type=current_type),
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                shutil.rmtree(type_path)
                self.update_asset_type_combo()
                self.asset_list.clear()
                self.subtype_list.clear()
                self.clear_right()
                self.show_info(u'成功',
                               u'资产类型 "{current_type}" 已删除'.format(current_type=current_type))
            except Exception as e:
                self.show_warning(u'错误', u'删除失败: {error}'.format(error=str(e)))

    def load_assets(self):
        self.asset_list.clear()
        self.subtype_list.clear()
        self.clear_right()
        if not self.pm or not self.current_asset_type:
            return
        assets = self.pm.list_assets(self.current_asset_type)
        for a in assets:
            self.asset_list.addItem(a)

    def on_asset_type_changed(self, text):
        if not text or text == u'暂无资产类型':
            self.current_asset_type = ''
            self.asset_list.clear()
            self.subtype_list.clear()
            self.clear_right()
            self.btn_delete_asset.setEnabled(False)
            self.btn_delete_asset.setVisible(False)
            return

        self.current_asset_type = text
        self.load_assets()
        self.btn_delete_asset.setEnabled(False)
        self.btn_delete_asset.setVisible(False)
        self.cfg.set_last_select_type(self.current_asset_type)

    def filter_assets(self, text):
        for i in range(self.asset_list.count()):
            it = self.asset_list.item(i)
            it.setHidden(text.lower() not in it.text().lower())

    def create_asset_dialog(self):
        if not self.pm or not self.current_asset_type:
            self.show_warning(u'提示', u'请先选择有效的资产类型')
            return
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle(u'创建资产')
        dlg.setFixedSize(320, 120)
        lay = QtWidgets.QVBoxLayout()

        r = QtWidgets.QHBoxLayout()
        r.addWidget(QtWidgets.QLabel(u'资产名称:'))
        self.new_asset_name = QtWidgets.QLineEdit()
        r.addWidget(self.new_asset_name)

        btn_row = QtWidgets.QHBoxLayout()
        ok = QtWidgets.QPushButton(u'创建')
        ok.clicked.connect(lambda: self._create_asset(dlg))
        cancel = QtWidgets.QPushButton(u'取消')
        cancel.clicked.connect(dlg.reject)
        btn_row.addStretch()
        btn_row.addWidget(ok)
        btn_row.addWidget(cancel)

        lay.addLayout(r)
        lay.addLayout(btn_row)
        dlg.setLayout(lay)
        dlg.exec_()

    def _create_asset(self, dlg):
        name = self.new_asset_name.text().strip()
        self.btn_delete_asset.setEnabled(False)
        self.btn_delete_asset.setVisible(False)
        if not name:
            self.show_warning(u'错误', u'请输入资产名称')
            return
        if self.pm.create_asset(self.current_asset_type, name):
            dlg.accept()
            self.load_assets()
            self.show_info(u'成功', u'资产 {name} 创建完成'.format(name=name))
        else:
            self.show_warning(u'失败', u'资产已存在或创建失败')

    def delete_asset_dialog(self):
        """删除资产对话框"""
        if not self.pm or not self.current_asset_type:
            self.show_warning(u'错误', u'请先选择项目及资产类型')
            return

        if not self.selected_asset:
            self.show_warning(u'错误', u'请先选择要删除的资产')
            return

        asset_dir = self.pm.get_asset_dir(self.current_asset_type, self.selected_asset)
        if not os.path.exists(asset_dir):
            self.show_warning(u'错误', u'资产路径不存在:\n{}'.format(asset_dir))
            return

        try:
            item_count = 0
            asset_size = 0
            for root, dirs, files in os.walk(asset_dir):
                item_count += len(dirs) + len(files)
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        asset_size += os.path.getsize(file_path)
                    except:
                        pass

            asset_size_mb = asset_size / (1024 * 1024)
            confirm_msg = u'确定要删除资产 "{asset_name}" 吗？\n\n'.format(asset_name=self.selected_asset)
            confirm_msg += u'资产类型: {asset_type}\n'.format(asset_type=self.current_asset_type)
            confirm_msg += u'资产路径: {asset_path}\n'.format(asset_path=asset_dir)
            confirm_msg += u'包含内容: {count} 个文件/文件夹\n'.format(count=item_count)
            confirm_msg += u'总大小: {size:.2f} MB\n\n'.format(size=asset_size_mb)
            confirm_msg += u'警告: 此操作不可逆！所有相关的子类型、版本、预览图等都会被永久删除。'

            reply = QtWidgets.QMessageBox.question(
                self,
                u'确认删除资产',
                confirm_msg,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )

            if reply == QtWidgets.QMessageBox.Yes:
                success, message = self._delete_asset(asset_dir)
                if success:
                    self.show_info(u'成功', message)
                    self.load_assets()
                    self.clear_right()
                    self.selected_asset = None
                    self.selected_subtype = None
                    self.info_label.setText(u'未选择资产')
                else:
                    self.show_warning(u'删除失败', message)
        except Exception as e:
            self.show_warning(u'错误', u'检查资产信息时出错:\n{}'.format(str(e)))

    def _delete_asset(self, asset_dir):
        """实际删除资产文件夹"""
        try:
            if not os.path.exists(asset_dir):
                return False, u'资产文件夹不存在'
            shutil.rmtree(asset_dir)
            if os.path.exists(asset_dir):
                return False, u'资产删除失败，文件夹仍然存在'
            return True, u'资产已成功删除'
        except OSError as e:
            return False, u'操作系统错误: {}'.format(str(e))
        except Exception as e:
            return False, u'删除过程中发生错误: {}'.format(str(e))

    def show_asset_preview(self, asset_type, asset):
        """显示资产预览图"""
        preview = os.path.join(self.pm.get_asset_dir(asset_type, asset), 'preview.png')
        if os.path.exists(preview):
            pix = QtGui.QPixmap(preview)
            self.preview_label.setPixmap(pix.scaled(self.preview_label.size(),
                                                    QtCore.Qt.KeepAspectRatio,
                                                    QtCore.Qt.SmoothTransformation))
        else:
            preview = os.path.join(self.pm.get_asset_dir(asset_type, asset), 'preview.jpg')
            if os.path.exists(preview):
                pix = QtGui.QPixmap(preview)
                self.preview_label.setPixmap(pix.scaled(self.preview_label.size(),
                                                        QtCore.Qt.KeepAspectRatio,
                                                        QtCore.Qt.SmoothTransformation))
            else:
                self.preview_label.clear()
                self.preview_label.setText('No Preview')

    def on_asset_clicked(self, item):
        self.selected_asset = item.text()
        self.selected_subtype = None
        self.info_label.setText('资产: {asset}'.format(asset=self.selected_asset))
        self.load_subtypes()
        self.btn_delete_asset.setEnabled(True)
        self.btn_delete_asset.setVisible(True)
        self.btn_add_sub.setEnabled(True)
        self.btn_del_sub.setEnabled(False)
        self.btn_rename_sub.setEnabled(False)
        self.btn_snapshot.setEnabled(True)
        self.show_asset_preview(self.current_asset_type, self.selected_asset)
        self.clear_right()
        self.show_version_count(0)
        self.cfg.set_last_select_asset(self.selected_asset)

    # ================== 子类型管理 ==================
    def load_subtypes(self):
        self.subtype_list.clear()
        if not (self.pm and self.selected_asset):
            return
        subs = self.pm.list_subtypes(self.current_asset_type, self.selected_asset)
        for s in subs:
            self.subtype_list.addItem(s)

    def add_subtype_dialog(self):
        if not (self.pm and self.selected_asset):
            self.show_warning(u'提示', u'请先选择资产')
            return
        text, ok = QtWidgets.QInputDialog.getText(self, u'添加子类型', u'输入子类型名称:')
        if ok and text.strip():
            if self.pm.create_subtype(self.current_asset_type, self.selected_asset, text.strip()):
                self.show_info(u'成功', u'子类型创建成功')
                self.load_subtypes()
            else:
                self.show_warning(u'失败', u'创建失败或已存在')

    def delete_subtype(self):
        if not (self.pm and self.selected_asset):
            self.show_warning('提示', '请先选择资产')
            return
        text, ok = QtWidgets.QInputDialog.getText(self, '删除子类型', '输入子类型名称:')
        if ok and text.strip():
            p = os.path.join(self.pm.get_asset_dir(self.current_asset_type, self.selected_asset), 'components',
                             text.strip())
            if os.path.exists(p):
                r = QtWidgets.QMessageBox.question(self, '确认', '将删除该子类型及其所有内容，是否继续?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if r == QtWidgets.QMessageBox.Yes:
                    try:
                        shutil.rmtree(p)
                        self.show_info('已删除', '{text} 已删除'.format(text=text))
                        self.load_subtypes()
                    except Exception as e:
                        self.show_warning('删除失败', '删除失败: {error}'.format(error=str(e)))
            else:
                self.show_warning('失败', '找不到该子类型')

    def rename_subtype(self):
        """重命名子类型"""
        if not (self.pm and self.selected_asset and self.selected_subtype):
            self.show_warning('提示', '请先选择资产和子类型')
            return

        new_name, ok = QtWidgets.QInputDialog.getText(self, '重命名子类型',
                                                      '重命名 "{old}" 为:'.format(old=self.selected_subtype),
                                                      text=self.selected_subtype)

        if ok and new_name.strip():
            new_name = new_name.strip()
            if new_name == self.selected_subtype:
                self.show_warning('提示', '新名称与当前名称相同')
                return

            existing_subs = self.pm.list_subtypes(self.current_asset_type, self.selected_asset)
            if new_name in existing_subs:
                self.show_warning('失败', '子类型 "{new_name}" 已存在'.format(new_name=new_name))
                return

            success, message = self.pm.rename_subtype(
                self.current_asset_type,
                self.selected_asset,
                self.selected_subtype,
                new_name
            )

            if success:
                self.show_info('成功', message)
                self.load_subtypes()
                self.selected_subtype = new_name
            else:
                self.show_warning('失败', message)

    def on_subtype_clicked(self, item):
        st = item.text()
        self.selected_subtype = st
        self.info_label.setText('选中: {asset}.{subtype}'.format(asset=self.selected_asset, subtype=st))

        versions = self.pm.get_workshop_versions(self.current_asset_type, self.selected_asset, st)
        self.version_list.clear()
        for v in versions:
            self.version_list.addItem(v)
        self.show_version_count(len(versions))
        notes = self.pm.get_notes(self.current_asset_type, self.selected_asset, st)
        self.notes_text.setPlainText("{}".format(notes))

        has_versions = bool(versions)
        self.btn_save_new_version.setEnabled(True)
        self.btn_set_master.setEnabled(has_versions)
        self.btn_import_version.setEnabled(has_versions)
        self.btn_reference_version.setEnabled(has_versions)
        self.btn_snapshot.setEnabled(True)
        self.btn_open_master.setEnabled(True)
        self.btn_reference_master.setEnabled(True)
        self.btn_del_sub.setEnabled(True)
        self.btn_rename_sub.setEnabled(True)

        preview = os.path.join(self.pm.get_asset_dir(self.current_asset_type, self.selected_asset), 'components', st,
                               'preview.png')
        if os.path.exists(preview):
            pix = QtGui.QPixmap(preview)
            self.preview_label.setPixmap(pix.scaled(self.preview_label.size(),
                                                    QtCore.Qt.KeepAspectRatio,
                                                    QtCore.Qt.SmoothTransformation))
        else:
            preview = os.path.join(self.pm.get_asset_dir(self.current_asset_type, self.selected_asset), 'components',
                                   st, 'preview.jpg')
            if os.path.exists(preview):
                pix = QtGui.QPixmap(preview)
                self.preview_label.setPixmap(pix.scaled(self.preview_label.size(),
                                                        QtCore.Qt.KeepAspectRatio,
                                                        QtCore.Qt.SmoothTransformation))
            else:
                self.preview_label.clear()
                self.preview_label.setText('No Preview')

    def on_subtype_double_clicked(self, item):
        st = item.text()
        self.selected_subtype = st
        latest = self.pm.get_latest_workshop(self.current_asset_type, self.selected_asset, st)
        if latest:
            if IN_MAYA:
                try:
                    cmds.file(latest, open=True, force=True, options="v=0;")
                    self.show_info_delayed('成功', '已在 Maya 中打开最新版本')
                except Exception as e:
                    self.show_warning('错误', str(e))
            else:
                self.show_info('打开', '最新版本路径:\n' + latest)
        else:
            self.show_warning('提示', '未找到任何版本')

    # ================== 版本操作 ==================
    def open_master(self):
        if not (self.pm and self.selected_asset and self.selected_subtype):
            return
        mf = self.pm.get_master_file(self.current_asset_type, self.selected_asset, self.selected_subtype)
        if not mf or not os.path.exists(mf):
            self.show_warning('错误', 'Master 文件不存在')
            return
        if IN_MAYA:
            try:
                cmds.file(mf, open=True, force=True, options="v=0;")
                self.show_info_delayed('成功', 'Master 已打开')
            except Exception as e:
                self.show_warning('失败', str(e))
        else:
            self.show_info('路径', mf)

    def open_selected_version(self):
        item = self.version_list.currentItem()
        if not item:
            if not (self.pm and self.selected_asset and self.selected_subtype):
                return
            latest = self.pm.get_latest_workshop(self.current_asset_type, self.selected_asset, self.selected_subtype)
            if latest:
                fpath = latest
            else:
                self.show_warning('提示', '没有可用的版本')
                return
        else:
            fname = item.text()
            fpath = os.path.join(self.pm.get_asset_dir(self.current_asset_type, self.selected_asset),
                                 'components', self.selected_subtype, 'workshop', fname)

        if os.path.exists(fpath):
            if IN_MAYA:
                try:
                    cmds.file(fpath, open=True, force=True, options="v=0;")
                    self.show_info_delayed('成功', '版本已打开')
                except Exception as e:
                    self.show_warning('失败', str(e))
            else:
                self.show_info('路径', fpath)
        else:
            self.show_warning('错误', '找不到文件')

    def set_master(self):
        item = self.version_list.currentItem()
        if not item:
            self.show_warning('提示', '请先选择一个版本')
            return
        fname = item.text()
        ok = self.pm.set_master(self.current_asset_type, self.selected_asset, self.selected_subtype, fname)
        if ok:
            self.show_info('成功', '已设为 Master')
        else:
            self.show_warning('失败', '设 Master 失败')

    def save_new_master(self):
        """另存新master"""
        if not (self.pm and self.selected_asset and self.selected_subtype):
            self.show_warning('提示', '请先选择资产与子类型')
            return

        confirm_msg = u"确认保存当前场景为Master？？？\n\n建议: 如有旧的master请去往{}下的master备份\n".format(
            self.selected_subtype)
        reply = QtWidgets.QMessageBox.question(
            self, u'确认保存Master', confirm_msg,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.No:
            return

        if self.pm.save_master(self.current_asset_type, self.selected_asset, self.selected_subtype):
            self.show_info_delayed('成功', 'Master已保存')
        else:
            self.show_warning('失败', 'Master保存失败')

    def save_new_version(self):
        """另存新版本"""
        if not (self.pm and self.selected_asset and self.selected_subtype):
            self.show_warning('提示', '请先选择资产与子类型')
            return

        notes, ok = QtWidgets.QInputDialog.getText(self, '保存新版本', '输入版本备注:')
        if not ok:
            return

        if self.pm.save_version(self.current_asset_type, self.selected_asset, self.selected_subtype, notes=notes):
            self.show_info_delayed('成功', '新版本已保存')
            versions = self.pm.get_workshop_versions(self.current_asset_type, self.selected_asset,
                                                     self.selected_subtype)
            self.version_list.clear()
            for v in versions:
                self.version_list.addItem(v)
        else:
            self.show_warning('失败', '保存新版本失败')

    def import_selected_version(self):
        """Import选中版本"""
        item = self.version_list.currentItem()
        if not item:
            self.show_warning('提示', '请先选择一个版本')
            return

        fname = item.text()
        fpath = os.path.join(self.pm.get_asset_dir(self.current_asset_type, self.selected_asset),
                             'components', self.selected_subtype, 'workshop', fname)

        if not os.path.exists(fpath):
            self.show_warning('错误', '找不到文件')
            return

        if IN_MAYA:
            try:
                cmds.file(fpath, i=True, options="v=0;")
                self.show_info('成功', 'Import 完成')
            except Exception as e:
                self.show_warning('失败', str(e))
        else:
            self.show_info('路径', fpath)

    def reference_selected_version(self):
        """Reference选中版本"""
        item = self.version_list.currentItem()
        if not item:
            self.show_warning('提示', '请先选择一个版本')
            return

        fname = item.text()
        fpath = os.path.join(self.pm.get_asset_dir(self.current_asset_type, self.selected_asset),
                             'components', self.selected_subtype, 'workshop', fname)

        if not os.path.exists(fpath):
            self.show_warning('错误', '找不到文件')
            return

        if IN_MAYA:
            try:
                cmds.file(fpath, ignoreVersion=1, namespace=fname.split(".")[0], r=1, gl=1,
                          mergeNamespacesOnClash=False, options="v=0;")
                self.show_info('成功', 'Reference 完成')
            except Exception as e:
                self.show_warning('失败', str(e))
        else:
            self.show_info('路径', fpath)

    def reference_master(self):
        """Reference Master文件"""
        if not (self.pm and self.selected_asset and self.selected_subtype):
            return
        mf = self.pm.get_master_file(self.current_asset_type, self.selected_asset, self.selected_subtype)
        if not mf or not os.path.exists(mf):
            self.show_warning('错误', 'Master 文件不存在')
            return

        if IN_MAYA:
            try:
                fname = mf.split("master")[-1]
                cmds.file(mf, ignoreVersion=1, namespace=fname.split(".ma")[0], r=1, gl=1,
                          mergeNamespacesOnClash=False, options="v=0;")
                self.show_info('成功', 'Reference Master 完成')
            except Exception as e:
                self.show_warning('失败', str(e))
        else:
            self.show_info('路径', mf)

    # ================== 辅助方法 ==================
    def show_version_count(self, counts):
        if counts == 0:
            self.version_count_text.setText("")
        else:
            self.version_count_text.setText("总数量: {}".format(str(counts)))

    def take_snapshot(self):
        if not (self.pm and self.selected_asset or self.selected_subtype):
            self.show_warning('提示', '请先选择资产与子类型')
            return

        if self.pm and self.selected_asset and self.selected_subtype:
            try:
                path = self.pm.take_snapshot(self.current_asset_type, self.selected_asset, self.selected_subtype)
                if os.path.exists(path):
                    pix = QtGui.QPixmap(path)
                    if not pix.isNull():
                        self.preview_label.setPixmap(pix.scaled(self.preview_label.size(),
                                                                QtCore.Qt.KeepAspectRatio,
                                                                QtCore.Qt.SmoothTransformation))
                    else:
                        self.show_warning('失败', '生成的预览图无效')
                else:
                    self.show_warning('失败', '预览保存失败')
            except Exception as e:
                self.show_warning('失败', '截图过程中发生错误: {error}'.format(error=str(e)))
        elif self.pm and self.selected_asset and not self.selected_subtype:
            try:
                path = self.pm.take_snapshot(self.current_asset_type, self.selected_asset)
                if os.path.exists(path):
                    pix = QtGui.QPixmap(path)
                    if not pix.isNull():
                        self.preview_label.setPixmap(pix.scaled(self.preview_label.size(),
                                                                QtCore.Qt.KeepAspectRatio,
                                                                QtCore.Qt.SmoothTransformation))
                    else:
                        self.show_warning('失败', '生成的预览图无效')
                else:
                    self.show_warning('失败', '预览保存失败')
            except Exception as e:
                self.show_warning('失败', '截图过程中发生错误: {error}'.format(error=str(e)))

    def clear_right(self):
        self.version_list.clear()
        self.notes_text.clear()
        self.btn_save_new_version.setEnabled(False)
        self.btn_set_master.setEnabled(False)
        self.btn_import_version.setEnabled(False)
        self.btn_reference_version.setEnabled(False)
        self.btn_open_master.setEnabled(False)
        self.btn_reference_master.setEnabled(False)
        self.btn_del_sub.setEnabled(False)
        self.btn_rename_sub.setEnabled(False)
        if not self.selected_asset:
            self.btn_delete_asset.setEnabled(False)
            self.btn_delete_asset.setVisible(False)
            self.btn_snapshot.setEnabled(False)
            self.preview_label.clear()
            self.preview_label.setText('No Preview')


def main():
    global py_Penpipeline
    try:
        py_Penpipeline.close()  # pylint: disable=E0601
        py_Penpipeline.deleteLater()
    except:
        pass

    py_Penpipeline = PYPenpipelineDialog()
    py_Penpipeline.show()
    return py_Penpipeline


if __name__ == '__main__':
    main()