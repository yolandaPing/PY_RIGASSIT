# -*- coding: utf-8 -*-

# .FileName:pyopenpipeline.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2025/6/30 20:23
# .Finish time:

import os
import json
import shutil
import xml.etree.ElementTree as ET
import xml.sax.saxutils
# import html
from datetime import datetime

try:
    import maya.cmds as cmds
    import maya.mel as mel
    IN_MAYA = True
except ImportError:
    cmds = None
    mel = None
    IN_MAYA = False

try:
    from importlib import reload
except ImportError:
    pass
from py_rigAssit.openpipeline import ui_openpipeline
reload(ui_openpipeline)

from py_rigAssit.openpipeline.version_context import (show_asset_context_menu, show_subtype_context_menu, show_version_context_menu)
from py_rigAssit.openpipeline.version import VERSION, TIMESTAMP
from py_rigAssit.openpipeline.asset_info import PROJECTS_XML
from py_rigAssit.openpipeline.ui_openpipeline import build_openpipeline_ui
from Pipeline import file_operations as fops
from Pipeline.pipelineConfig import OpenPipelineConfig
from Pipeline.projectManager import ProjectManager
from Pipeline.pipelineUtils import (
    load_projects_from_xml, get_projects_xml_path, ensure_projects_xml,
    add_project_to_xml, open_folder_in_explorer, open_file_in_explorer
)

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
        self.maya_version = cmds.about(version=True) if IN_MAYA and cmds else 'Unknown'

        self.timeStamp = TIMESTAMP
        self.WINDOW_NAME = 'OpenPipeline v{} (Maya{})'.format(VERSION, self.maya_version)

        self.pm = None
        self.current_project_path = u''
        self.current_project_name = u''
        self.current_asset_type = u''
        self.selected_asset = None
        self.selected_subtype = None
        self.new_proj_name = None
        self.new_proj_path = None
        self.new_asset_name = None
        self.fbx_config = None
        self._fbx_dialog = None

        self.setWindowTitle(self.WINDOW_NAME)
        self.loadWindowSettings()

        build_openpipeline_ui(self)
        self.update_root_path_label()
        self.load_projects()
        self.select_last_project()
        self.load_fbx_config()

    def show_info(self, title, message):
        QtWidgets.QMessageBox.information(self, title, message)

    def show_warning(self, title, message):
        QtWidgets.QMessageBox.warning(self, title, message)

    def show_critical(self, title, message):
        QtWidgets.QMessageBox.critical(self, title, message)

    def show_info_delayed(self, title, message, delay=500):
        QtCore.QTimer.singleShot(delay, lambda: QtWidgets.QMessageBox.information(self, title, message))

    def show_warning_delayed(self, title, message, delay=500):
        QtCore.QTimer.singleShot(delay, lambda: QtWidgets.QMessageBox.warning(self, title, message))

    def show_critical_delayed(self, title, message, delay=500):
        QtCore.QTimer.singleShot(delay, lambda: QtWidgets.QMessageBox.critical(self, title, message))

    def show_info_inview(self, title=u"Finished", color='yellow'):
        import HelpImageUI as help
        help.inView_Message(color, u"{}".format(title))

    def show_asset_context_menu(self, position):
        show_asset_context_menu(self, position)

    def show_subtype_context_menu(self, position):
        show_subtype_context_menu(self, position)

    def show_version_context_menu(self, position):
        show_version_context_menu(self, position)

    def update_root_path_label(self):
        root_path = self.cfg.get_project_root_path()
        if root_path:
            normalized_path = root_path.replace('\\', '/')
            self.root_path_label.setText(normalized_path)
            self.root_path_label.setToolTip(normalized_path)
        else:
            self.root_path_label.setText(u'未设置')
            self.root_path_label.setToolTip('')

    def check_config(self):
        try:
            config_file = self.cfg.get_config_file_path()
            config_exists = os.path.exists(config_file)
            config_content = u"配置文件不存在"
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

    #FBX配置管理
    def load_fbx_config(self):
        try:
            self.fbx_config = self.cfg.get_fbx_export_info()
            if not self.fbx_config:
                self.fbx_config = ['Geo_grp', 'root_jnt']
                self.save_fbx_config(self.fbx_config)
        except Exception as e:
            print(u"加载FBX配置失败: {}".format(str(e)))

    def save_fbx_config(self, fbx_export):
        try:
            self.cfg.set_fbx_export_info(fbx_export)
        except Exception as e:
            print(u"保存FBX配置失败: {}".format(str(e)))

    def set_fbx_export_objects(self):
        from py_rigAssit.openpipeline.fbx_dialog import FBXExportDialog

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
        new_settings = dialog.get_settings()
        if new_settings[0] and new_settings[1]:
            self.fbx_config = new_settings
            self.save_fbx_config(self.fbx_config)
            self.show_info(u'成功',
                           u'FBX导出设置已保存:\n\n几何体组: {}\n根关节: {}'.format(
                               new_settings[0], new_settings[1]))
        self._fbx_dialog = None

    def set_project_root_path(self):
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
        self.project_combo.addItem('', '')

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
        last_project_path, last_assetType, last_asset = self.cfg.get_last_info(self.maya_version)

        if last_project_path:
            normalized_last_path = last_project_path.replace('\\', '/').rstrip('/')
            print(u"尝试选择上次的项目: {}".format(normalized_last_path))

            for i in range(self.project_combo.count()):
                item_data = self.project_combo.itemData(i)
                if item_data:
                    normalized_item_data = item_data.replace('\\', '/').rstrip('/')
                    if normalized_item_data == normalized_last_path:
                        self.project_combo.setCurrentIndex(i)
                        print(u"已自动选择上次的项目: {}".format(self.project_combo.itemText(i)))
                        QtCore.QTimer.singleShot(100,lambda: self._select_last_type_and_asset(last_assetType, last_asset))
                        break

    def _select_last_type_and_asset(self, last_assetType, last_asset):
        if last_assetType:
            for t in range(self.type_combo.count()):
                type_text = self.type_combo.itemText(t)
                if type_text == last_assetType:
                    self.type_combo.setCurrentIndex(t)
                    print(u"已自动选择上次的项目类型: {}".format(last_assetType))
                    QtCore.QTimer.singleShot(100, lambda: self._select_last_asset(last_asset))
                    break

    def _select_last_asset(self, last_asset):
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
        if not text or text == '-- 选择项目 --' or text == u'请先设置项目根路径' or text == u'没有找到项目':
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
                # self.cfg.set_last_project(normalized_path)
                self.cfg.update_last_info(self.maya_version, project=normalized_path)
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
        lay.addWidget(_widgets.create_text(u'输入项目名称'))
        row1 = QtWidgets.QHBoxLayout()
        row1.addWidget(QtWidgets.QLabel(u'项目名称:'))
        self.new_proj_name = QtWidgets.QLineEdit()
        row1.addWidget(self.new_proj_name)

        row2 = QtWidgets.QHBoxLayout()
        row2.addWidget(QtWidgets.QLabel(u'项目根路径:'))
        self.new_proj_path = QtWidgets.QLabel(root_path)
        self.new_proj_path.setStyleSheet('background: gray; padding:4px; color: black; border:1px solid #ccc;')
        row2.addWidget(self.new_proj_path, 1)

        row3 = QtWidgets.QHBoxLayout()
        row3.addWidget(QtWidgets.QLabel(u'库文件夹:'))
        self.new_proj_lib = QtWidgets.QLineEdit()
        self.new_proj_lib.setText(self.cfg.config.get('library_folder', 'lib'))
        self.new_proj_lib.setEnabled(False)
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

    def get_current_asset_types(self):
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
        self.type_combo.clear()
        if not self.pm:
            return

        asset_types = self.get_current_asset_types()
        if asset_types:
            for asset_type in asset_types:
                self.type_combo.addItem(asset_type, asset_type)
            if asset_types:
                self.current_asset_type = asset_types[0]
        else:
            self.type_combo.addItem(u'暂无资产类型')
            self.current_asset_type = ''

    def add_asset_type(self):
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

    def on_asset_sort_changed(self, index):
        self.load_assets(index)

    def load_assets(self, sort_mode=1, *args):
        self.asset_list.clear()
        self.subtype_list.clear()
        self.clear_right()
        if not self.pm or not self.current_asset_type:
            return

        assets = self.pm.list_assets(self.current_asset_type)
        if not assets:
            return

        if sort_mode == 2:
            asset_with_time = []
            for asset in assets:
                asset_path = self.pm.get_asset_dir(self.current_asset_type, asset)
                mtime = os.path.getmtime(asset_path) if os.path.exists(asset_path) else 0
                asset_with_time.append((asset, mtime))
            asset_with_time.sort(key=lambda x: x[1], reverse=True)
            sorted_assets = [item[0] for item in asset_with_time]
        else:
            sorted_assets = sorted(assets)

        self.asset_list.addItems(sorted_assets)

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
        # self.cfg.set_last_select_type(self.current_asset_type)
        self.cfg.update_last_info(self.maya_version, asset_type=self.current_asset_type)

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
        self.info_label.setText(u'资产: {asset}'.format(asset=self.selected_asset))
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
        # self.cfg.set_last_select_asset(self.selected_asset)
        self.cfg.update_last_info(self.maya_version, asset=self.selected_asset)

    def load_subtypes(self):
        self.subtype_list.clear()
        if not (self.pm and self.selected_asset):
            return
        subs = self.pm.list_subtypes(self.current_asset_type, self.selected_asset)
        self.subtype_list.addItems(subs)

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
            self.show_warning(u'提示', u'请先选择资产')
            return
        text, ok = QtWidgets.QInputDialog.getText(self, u'删除子类型', u'输入子类型名称:')
        if ok and text.strip():
            p = os.path.join(self.pm.get_asset_dir(self.current_asset_type, self.selected_asset), 'components',
                             text.strip())
            if os.path.exists(p):
                r = QtWidgets.QMessageBox.question(self, u'确认', u'将删除该子类型及其所有内容，是否继续?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if r == QtWidgets.QMessageBox.Yes:
                    try:
                        shutil.rmtree(p)
                        self.show_info(u'已删除', u'{text} 已删除'.format(text=text))
                        self.load_subtypes()
                    except Exception as e:
                        self.show_warning(u'删除失败', u'删除失败: {error}'.format(error=str(e)))
            else:
                self.show_warning(u'失败', u'找不到该子类型')

    def rename_subtype(self):
        if not (self.pm and self.selected_asset and self.selected_subtype):
            self.show_warning(u'提示', u'请先选择资产和子类型')
            return

        new_name, ok = QtWidgets.QInputDialog.getText(self, u'重命名子类型',
                                                      u'重命名 "{old}" 为:'.format(old=self.selected_subtype),
                                                      text=self.selected_subtype)

        if ok and new_name.strip():
            new_name = new_name.strip()
            if new_name == self.selected_subtype:
                self.show_warning(u'提示', u'新名称与当前名称相同')
                return

            existing_subs = self.pm.list_subtypes(self.current_asset_type, self.selected_asset)
            if new_name in existing_subs:
                self.show_warning(u'失败', u'子类型 "{new_name}" 已存在'.format(new_name=new_name))
                return

            success, message = self.pm.rename_subtype(
                self.current_asset_type,
                self.selected_asset,
                self.selected_subtype,
                new_name
            )

            if success:
                self.show_info(u'成功', message)
                self.load_subtypes()
                self.selected_subtype = new_name
            else:
                self.show_warning(u'失败', message)

    def format_notes_text(self, text):
        if not text:
            return ""

        lines = text.splitlines()
        html_parts = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("[MASTER SET]"):
                color = "yellow"
            elif stripped.startswith("Note: Delete"):
                color = "#e68b86"
            elif stripped.startswith("Note:"):
                color = "#80fcca"
            else:
                color = "#abc4d2"
            escaped = xml.sax.saxutils.escape(line)
            html_parts.append('<span style="color:{};">{}</span>'.format(color, escaped))
        return "<br>".join(html_parts)

    def on_subtype_clicked(self, item):
        st = item.text()
        self.selected_subtype = st
        self.info_label.setText(u'选中: {asset}.{subtype}'.format(asset=self.selected_asset, subtype=st))

        versions = self.pm.get_workshop_versions(self.current_asset_type, self.selected_asset, st)
        self.version_list.clear()
        if versions:
            self.version_list.addItems(versions)

        self.show_version_count(len(versions))
        notes = self.pm.get_notes(self.current_asset_type, self.selected_asset, st)
        # self.notes_text.setPlainText("{}".format(notes))
        self.notes_text.setHtml(self.format_notes_text(notes))
        has_versions = bool(versions)
        self.btn_save_new_version.setEnabled(True)
        self.btn_save_new_version.setStyleSheet("color: green;")
        self.btn_set_master.setEnabled(has_versions)
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
                    fname = latest.split('\\')[-1]
                    print("double clicked latest: ", fname)
                    fops.open_file(latest)
                    self.show_info_inview('The latest version has been opened', 'yellow')
                except Exception as e:
                    self.show_warning(u'错误', str(e))
            else:
                self.show_info(u'打开', u'最新版本路径:\n' + latest)
        else:
            self.show_warning(u'提示', u'未找到任何版本')

    def safe_run(self, func):
        try:
            func()
        except Exception as e:
            self.show_critical(u'错误', str(e))

    def open_selected_version(self):
        item = self.version_list.currentItem()
        if not item:
            latest = self.pm.get_latest_workshop(self.current_asset_type, self.selected_asset, self.selected_subtype)
            if latest:
                try:
                    fname = latest.split('\\')[-1]
                    print("latest: ", fname)
                    fops.open_file(latest)
                    self.show_info_inview('The latest version has been opened', 'yellow')
                except Exception as e:
                    self.show_warning(u'失败', str(e))
            else:
                self.show_warning(u'提示', u'没有可用的版本')
            return

        fname = item.text()
        try:
            fops.open_latest_or_selected_version(
                self.pm, self.current_asset_type, self.selected_asset, self.selected_subtype, fname
            )
            self.show_info_inview('The version has been opened', 'yellow')
        except Exception as e:
            self.show_warning(u'失败', str(e))

    def open_master(self):
        try:
            fops.open_master_file(self.pm, self.current_asset_type, self.selected_asset, self.selected_subtype)
            self.show_info_inview('Master has been opened', 'yellow')
        except Exception as e:
            self.show_warning(u'错误', str(e))

    def import_selected_version(self):
        item = self.version_list.currentItem()
        if not item:
            self.show_warning(u'提示', u'请先选择一个版本')
            return
        fname = item.text()
        try:
            fops.import_selected_version(
                self.pm, self.current_asset_type, self.selected_asset, self.selected_subtype,
                fname, namespace=None
            )
            self.show_info_inview('Import Finished')
        except Exception as e:
            self.show_warning(u'失败', str(e))

    def reference_selected_version(self):
        item = self.version_list.currentItem()
        if not item:
            self.show_warning(u'提示', u'请先选择一个版本')
            return
        fname = item.text()
        try:
            ns = fname.split(".")[0]
            fops.reference_selected_version(
                self.pm, self.current_asset_type, self.selected_asset, self.selected_subtype,
                fname, namespace=ns, group_locator=True, merge_namespaces=False
            )
            self.show_info_inview('Reference Finished')
        except Exception as e:
            self.show_warning(u'失败', str(e))

    def reference_master(self, namespace=True):

        try:
            mf = self.pm.get_master_file(
                self.current_asset_type,
                self.selected_asset,
                self.selected_subtype
            )
            if not mf or not os.path.exists(mf):
                self.show_warning(u'错误', u'Master 文件不存在')
                return

            if namespace:
                ns = os.path.basename(mf).split(".")[0]
                fops.reference_file(
                    mf,
                    namespace=ns,
                    group_locator=True
                )
            else:
                fops.reference_file(
                    mf,
                    namespace=":",
                    group_locator=True
                )

            self.show_info_inview('Reference Master Finished')
        except Exception as e:
            self.show_warning(u'失败', str(e))

    def save_new_version(self):
        if not (self.pm and self.selected_asset and self.selected_subtype):
            self.show_warning(u'提示', u'请先选择资产与子类型')
            return
        notes, ok = QtWidgets.QInputDialog.getText(self, u'保存新版本', u'输入版本备注:')
        if not ok:
            return
        try:
            if fops.save_workshop(None, notes, self.pm, self.current_asset_type, self.selected_asset, self.selected_subtype):
                self.show_info_inview('The new version has been saved', 'green')
                versions = self.pm.get_workshop_versions(self.current_asset_type, self.selected_asset, self.selected_subtype)
                self.version_list.clear()
                if versions:
                    self.version_list.addItems(versions)
            else:
                self.show_warning(u'失败', u'保存新版本失败')
        except Exception as e:
            self.show_warning(u'失败', str(e))

    def save_new_master(self):
        if not (self.pm and self.selected_asset and self.selected_subtype):
            self.show_warning(u'提示', u'请先选择资产与子类型')
            return
        confirm_msg = u"确认保存当前场景为Master？？？\n\n建议: 如有旧的master请去往{}下的master备份\n".format(
            self.selected_subtype)
        reply = QtWidgets.QMessageBox.question(
            self, u'确认保存Master', confirm_msg,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.No:
            return
        try:
            if fops.save_master(None, self.pm, self.current_asset_type, self.selected_asset, self.selected_subtype):
                self.show_info_inview('Master has been saved', 'green')
            else:
                self.show_warning(u'失败', u'Master保存失败')
        except Exception as e:
            self.show_warning(u'失败', str(e))

    def show_version_count(self, counts):
        if counts:
            self.version_count_text.setText("总数量: {}".format(str(counts)))
        else:
            self.version_count_text.setText("")

    def take_snapshot(self):
        if not (self.pm and self.selected_asset or self.selected_subtype):
            self.show_warning(u'提示', u'请先选择资产与子类型')
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
                        self.show_warning(u'失败', u'生成的预览图无效')
                else:
                    self.show_warning(u'失败', u'预览保存失败')
            except Exception as e:
                self.show_warning(u'失败', u'截图过程中发生错误: {error}'.format(error=str(e)))
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
                        self.show_warning(u'失败', u'生成的预览图无效')
                else:
                    self.show_warning(u'失败', u'预览保存失败')
            except Exception as e:
                self.show_warning(u'失败', u'截图过程中发生错误: {error}'.format(error=str(e)))

    def clear_right(self):
        self.version_list.clear()
        self.notes_text.clear()
        self.btn_save_new_version.setEnabled(False)
        self.btn_save_new_version.setStyleSheet("color: gray;")
        self.btn_set_master.setEnabled(False)
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
        py_Penpipeline.close()
        py_Penpipeline.deleteLater()
    except:
        pass

    py_Penpipeline = PYPenpipelineDialog()
    py_Penpipeline.show()
    return py_Penpipeline


if __name__ == '__main__':
    main()