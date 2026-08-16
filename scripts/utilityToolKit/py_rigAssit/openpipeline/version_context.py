# -*- coding: utf-8 -*-
# .FileName:version_context.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2025/12/13 13:02

import os
import shutil
from datetime import datetime

try:
    from importlib import reload
except ImportError:
    pass

try:
    from ui_framework.core.qtCompat import *
except ImportError:
    from CommonUse.qtCompat import *

from Pipeline import file_operations as file_ops
from Pipeline.pipelineConfig import OpenPipelineConfig
from Pipeline.projectManager import ProjectManager

try:
    from Pipeline.pipelineUtils import *
    from Pipeline.pipelineUtils import (
        load_projects_from_xml,
        get_projects_xml_path,
        ensure_projects_xml,
        add_project_to_xml,
        open_folder_in_explorer,
        open_file_in_explorer
    )
except ImportError:
    try:
        from .pipelineUtils import *
    except ImportError:
        print(u"version_context导入工具pipeline_utils模块失败")

try:
    import maya.cmds as cmds
    import maya.mel as mel
    import maya.OpenMaya as om

    IN_MAYA = True
except Exception:
    IN_MAYA = False

_cfg = OpenPipelineConfig()


def _show_info_inview(title=u"Finished", color='yellow'):
    import HelpImageUI as help
    help.inView_Message(color, u"{}".format(title))


def add_menu_label(menu, text):
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QHBoxLayout(widget)

    label = QtWidgets.QLabel(text)
    label.setStyleSheet("color: yellow;")

    layout.addWidget(label)
    layout.setContentsMargins(20, 2, 5, 2)
    widget.setLayout(layout)

    label_action = QtWidgets.QWidgetAction(menu)
    label_action.setDefaultWidget(widget)
    menu.addAction(label_action)


class PipelineContext(object):

    def __init__(self, main_window):
        self.ui = main_window

    @property
    def pm(self):
        return self.ui.pm

    @property
    def asset_type(self):
        return self.ui.current_asset_type

    @property
    def asset(self):
        return self.ui.selected_asset

    @property
    def subtype(self):
        return self.ui.selected_subtype

    def validate_asset(self):
        return bool(self.pm and self.asset_type)

    def validate_subtype(self):
        return bool(
            self.pm and
            self.asset_type and
            self.asset and
            self.subtype
        )


class PathService(PipelineContext):

    def asset_dir(self, asset_name=None):
        asset_name = asset_name or self.asset
        return self.pm.get_asset_dir(
            self.asset_type,
            asset_name
        )

    def subtype_dir(self, subtype_name=None):
        subtype_name = subtype_name or self.subtype
        return os.path.join(
            self.asset_dir(),
            'components',
            subtype_name
        )

    def workshop_dir(self):
        return os.path.join(
            self.subtype_dir(),
            'workshop'
        )

    def version_path(self, version_name):
        return os.path.join(
            self.workshop_dir(),
            version_name
        )

    def open_asset_path(self, asset_name):
        if not self.validate_asset():
            self.ui.show_warning(
                u'错误',
                u'请先选择资产类型'
            )
            return

        path = self.asset_dir(asset_name)

        if os.path.exists(path):
            open_folder_in_explorer(path.replace("/", "\\"))
        else:
            self.ui.show_warning(
                u'错误',
                u'资产路径不存在:\n{}'.format(path)
            )

    def open_subtype_path(self, subtype_name):
        if not self.validate_subtype():
            self.ui.show_warning(
                u'错误',
                u'请先选择资产和任务'
            )
            return

        path = os.path.join(
            self.asset_dir(),
            'components',
            subtype_name
        )

        if os.path.exists(path):
            open_folder_in_explorer(path.replace("/", "\\"))
        else:
            self.ui.show_warning(
                u'错误',
                u'任务路径不存在:\n{}'.format(path)
            )

    def open_version_path(self, version_name):
        if not self.validate_subtype():
            self.ui.show_warning(
                u'错误',
                u'请先选择资产和任务'
            )
            return

        path = self.version_path(version_name)

        if os.path.exists(path):
            open_file_in_explorer(path.replace("/", "\\"))
        else:
            self.ui.show_warning(
                u'错误',
                u'版本文件不存在:\n{}'.format(path)
            )

    def get_file_info(self, version_filename):
        file_path = self.version_path(version_filename)

        if not os.path.exists(file_path):
            return ""

        try:
            size_bytes = os.path.getsize(file_path)
            mod_time = os.path.getmtime(file_path)

            return u"\n\n文件大小: {:.1f} KB\n最后修改: {}".format(
                size_bytes / 1024.0,
                datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M')
            )
        except:
            return u"\n\n(无法获取文件信息)"


class VersionService(PathService):

    def refresh_version_list(self):
        if not self.validate_subtype():
            return

        versions = self.pm.get_workshop_versions(
            self.asset_type,
            self.asset,
            self.subtype
        ) or []

        version_list = self.ui.version_list
        version_list.clear()

        for version in versions:
            version_list.addItem(version)

    def backup_to_deleted_folder(self, file_path):
        if not os.path.exists(file_path):
            return False

        deleted_dir = os.path.join(
            self.subtype_dir(),
            "deleted"
        )

        if not os.path.exists(deleted_dir):
            os.makedirs(deleted_dir)

        filename = os.path.basename(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        backup_name = "{}_{}".format(timestamp, filename)
        backup_path = os.path.join(
            deleted_dir,
            backup_name
        )

        shutil.copy2(file_path, backup_path)
        return True

    def is_master_version(self, version_filename):
        try:
            master_path = self.pm.get_master_file(
                self.asset_type,
                self.asset,
                self.subtype
            )

            if not master_path:
                return False

            master_name = os.path.basename(master_path)
            return master_name == version_filename
        except:
            return False

    def delete_selected_version(self, version_filename):
        if not self.validate_subtype():
            self.ui.show_warning(
                u'错误',
                u'请先选择资产和任务'
            )
            return False

        file_path = self.version_path(version_filename)

        if not os.path.exists(file_path):
            self.ui.show_warning(
                u'错误',
                u'文件不存在:\n{}'.format(file_path)
            )
            return False

        if self.is_master_version(version_filename):
            reply = QtWidgets.QMessageBox.question(
                self.ui,
                u'警告',
                u'该版本是 Master，删除后 Master 将失效。\n确定继续？',
                QtWidgets.QMessageBox.Yes |
                QtWidgets.QMessageBox.No
            )

            if reply != QtWidgets.QMessageBox.Yes:
                return False
        else:
            reply = QtWidgets.QMessageBox.question(
                self.ui,
                u'确认删除',
                u'确定删除版本？\n{}'.format(version_filename),
                QtWidgets.QMessageBox.Yes |
                QtWidgets.QMessageBox.No
            )

            if reply != QtWidgets.QMessageBox.Yes:
                return False

        try:
            self.backup_to_deleted_folder(file_path)
        except Exception as e:
            print(u"备份删除文件失败: {}".format(e))

        try:
            os.remove(file_path)
        except Exception as e:
            self.ui.show_critical(
                u'删除失败',
                str(e)
            )
            return False

        note_path = file_path + ".note"
        if os.path.exists(note_path):
            try:
                os.remove(note_path)
            except:
                pass

        self.refresh_version_list()

        if hasattr(self.ui, "show_info"):
            try:
                self.ui.show_info(u'文件删除成功',
                                  u"已删除 {}".format(version_filename)
                                  )
            except:
                pass

        return True


class FBXExporter(PathService):

    def ensure_scene_safe(self):
        if not IN_MAYA:
            return False

        modified = cmds.file(q=True, modified=True)

        if not modified:
            return True

        reply = QtWidgets.QMessageBox.question(
            self.ui,
            u"警告",
            u"当前场景有未保存内容。\n继续导出会清空当前场景，是否继续？",
            QtWidgets.QMessageBox.Yes |
            QtWidgets.QMessageBox.No
        )

        return reply == QtWidgets.QMessageBox.Yes

    def get_export_objects(self):
        if not hasattr(self.ui, "fbx_config"):
            raise RuntimeError("fbx_config missing")

        config = self.ui.fbx_config

        if len(config) < 2:
            raise RuntimeError("FBX config invalid")

        geo_grp = config[0]
        root_joint = config[1]

        export_objects = []

        if geo_grp and cmds.objExists(geo_grp):
            export_objects.append(geo_grp)

        if root_joint and cmds.objExists(root_joint):
            export_objects.append(root_joint)

        if not export_objects:
            raise RuntimeError("Export objects missing")
        self.geo_grp = geo_grp
        self.root_joint = root_joint
        return export_objects

    def delete_matrix_nodes(self):
        skins = cmds.ls(type="skinCluster") or []
        for skin in skins:
            attrs = cmds.listAttr(skin, multi=True) or []
            matrix_attrs = [a for a in attrs if a.startswith("matrix")]
            for mx in matrix_attrs:
                cons = cmds.listConnections(
                    "{}.{}".format(skin, mx),
                    d=True
                ) or []

                if not cons:
                    continue

                matrix_node = cons[0]

                if cmds.objExists(matrix_node):
                    try:
                        cmds.delete(matrix_node)
                    except:
                        pass

    def delete_blendshape_nodes(self):
        meshes = cmds.ls(type="mesh", long=True) or []

        transforms = []

        for mesh in meshes:
            parent = cmds.listRelatives(mesh, parent=True, fullPath=True) or []
            if parent:
                transforms.extend(parent)

        transforms = list(set(transforms))

        for obj in transforms:
            history = cmds.listHistory(obj) or []
            blend_nodes = cmds.ls(history, type='blendShape') or []

            for bs in blend_nodes:
                if cmds.objExists(bs):
                    try:
                        cmds.delete(bs)
                    except:
                        pass

    def cleanup_scene(self):
        self.delete_matrix_nodes()
        self.delete_blendshape_nodes()

    def build_fbx_path(self, version_filename):
        fbx_dir = os.path.join(
            self.subtype_dir(),
            "fbx"
        )

        if not os.path.exists(fbx_dir):
            os.makedirs(fbx_dir)

        base_name = os.path.splitext(version_filename)[0]

        fbx_path = os.path.join(
            fbx_dir,
            base_name + ".fbx"
        )

        return fbx_path.replace("\\", "/")

    def export_selected_to_fbx(self, fbx_path):
        export_objects = self.get_export_objects()
        cmds.select(clear=True)
        cmds.select(export_objects, r=True)
        mel.eval('file -force -options "v=0;" -typ "FBX export" -pr -es "{}";'.format(fbx_path))
        return os.path.exists(fbx_path)

    def _export_to_unreal(self, fbx_path):
        try:
            import work_patch.project_asset_browser.fbx_to_unreal as fbx_to_unreal
            reload(fbx_to_unreal)
            obj_fold = {"chr": "Chr",
                        "Chr": "Chr",
                        "char": "Chr",
                        "prp": "Prp",
                        "Prp": "Prp"}
            ue_content_path = "/Game/{}/{}".format(CONTENT, obj_fold.get(self.asset_type, "Chr"))
            fbx_to_unreal.export_to_unreal(fbx_path, UnrealEditor, UE_PROJECT, ue_content_path, self.asset)
        except Exception as e:
            self.ui.show_warning_delayed(u'UE 导出警告', u'{}\n前往ue手动运行ue_importer.py移动材质贴图即可'.format(e))

    def _save_json_for_ue(self, fbx_path):
        try:
            import work_patch.project_asset_browser.fbx_to_unreal as fbx_to_unreal
            reload(fbx_to_unreal)
            obj_fold = {"chr": "Chr",
                        "Chr": "Chr",
                        "char": "Chr",
                        "prp": "Prp",
                        "Prp": "Prp"}
            ue_content_path = "/Game/{}/{}".format(CONTENT, obj_fold.get(self.asset_type, "Chr"))
            fbx_to_unreal.save_json(fbx_path, ue_content_path, self.asset)
        except:
            pass

    def export_fbx_for_version(self, version_filename, to_ue=False):
        if not IN_MAYA:
            self.ui.show_critical(u"错误", u"只能在 Maya 中运行")
            return False

        if not self.ensure_scene_safe():
            return False

        version_path = self.version_path(version_filename)

        if not os.path.exists(version_path):
            raise RuntimeError(
                "Version file missing:\n{}".format(version_path)
            )

        fbx_path = self.build_fbx_path(version_filename)

        try:
            cmds.file(new=True, force=True)
            file_ops.import_file(version_path)

            self.cleanup_scene()

            ok = self.export_selected_to_fbx(fbx_path)
            if ok:
                cmds.file(new=True, force=True)
                base_name = self.asset

                if to_ue:
                    self._export_to_unreal(fbx_path)
                else:
                    self._save_json_for_ue(fbx_path)
                    self.ui.show_info_delayed(u'导出成功', u'FBX导出完成:\n\n导出对象: {} 和 {}\n导出路径: {}'.format(
                        self.geo_grp, self.root_joint,
                        fbx_path))
            if not ok:
                raise RuntimeError("FBX export failed")

            return fbx_path

        except Exception as e:
            self.ui.show_warning_delayed(u'导出失败', str(e))
            return False


class FileOperationService(PathService):

    def open_version(self, version_name):
        path = self.version_path(version_name)
        return file_ops.open_file(path)

    def import_version(self, version_name, namespace=None):
        path = self.version_path(version_name)
        return file_ops.import_file(
            path,
            namespace=namespace
        )

    def reference_version(self, version_name, namespace=None):
        path = self.version_path(version_name)
        # 若未指定命名空间，则使用文件名前缀（与原有行为一致）
        if namespace is None:
            namespace = version_name.split('.')[0]
        return file_ops.reference_file(
            path,
            namespace=namespace,
            group_locator=True
        )

    def open_master(self):
        return file_ops.open_master_file(
            self.pm,
            self.asset_type,
            self.asset,
            self.subtype
        )

    def import_master(self, namespace=None):
        return file_ops.import_master_file(
            self.pm,
            self.asset_type,
            self.asset,
            self.subtype,
            namespace=namespace
        )

    def reference_master(self, namespace=None):
        """
        引用 Master。
        若 namespace 为 None（默认），则无命名空间（使用 ":" 合并到根）。
        若指定 namespace，则使用该命名空间。
        """
        mf = self.pm.get_master_file(
            self.asset_type,
            self.asset,
            self.subtype
        )

        if not mf or not os.path.exists(mf):
            raise FileNotFoundError("Master file not found")

        # 默认无命名空间：使用 ":"（表示根命名空间）
        if namespace is None:
            # 使用 ":" 并设置 group_locator=True，但不合并命名空间merge_namespaces
            return file_ops.reference_file(
                mf,
                namespace=":",
                group_locator=True
            )
        else:
            return file_ops.reference_file(
                mf,
                namespace=namespace,
                group_locator=True
            )

    def set_master(self, version_name):
        return file_ops.set_master_from_version(
            self.pm, self.asset_type, self.asset, self.subtype, version_name
        )

    def write_note_info(self, subtype_name, version_filename, info="", workshop=True):
        task_dir = os.path.join(
            self.asset_dir(),
            'components',
            subtype_name
        )
        self.pm.write_note_info(task_dir, version_filename, info, workshop)


class VersionContextMenu(PipelineContext):

    def __init__(self, main_window):
        super(VersionContextMenu, self).__init__(main_window)

        self.path_service = PathService(main_window)
        self.version_service = VersionService(main_window)
        self.exporter = FBXExporter(main_window)
        self.file_ops = FileOperationService(main_window)

    def show_asset_menu(self, position):
        list_widget = self.ui.asset_list
        item = list_widget.itemAt(position)

        if not item:
            return

        asset_name = item.text()

        menu = QtWidgets.QMenu(list_widget)

        open_path_action = menu.addAction(u"📂 打开资产目录")

        def _open():
            self.path_service.open_asset_path(asset_name)

        open_path_action.triggered.connect(_open)
        menu.exec_(list_widget.mapToGlobal(position))

    def show_subtype_menu(self, position):
        list_widget = self.ui.subtype_list
        item = list_widget.itemAt(position)

        if not item:
            return

        subtype_name = item.text()

        menu = QtWidgets.QMenu(list_widget)

        open_path_action = menu.addAction(u"📂 打开任务目录")
        menu.addSeparator()
        open_master_action = menu.addAction(u"打开 Master")
        import_master_action = menu.addAction(u"导入 Master")
        reference_master_action = menu.addAction(u"引用 Master")

        def safe_run(func):
            try:
                func()
            except Exception as e:
                QtWidgets.QMessageBox.warning(
                    self.ui,
                    u"错误",
                    str(e)
                )

        def _open():
            self.path_service.open_subtype_path(subtype_name)

        def _open_master():
            safe_run(lambda: self.file_ops.open_master())
            _show_info_inview('Master opened', 'yellow')

        def _import_master():
            safe_run(lambda: self.file_ops.import_master())
            _show_info_inview('Master imported', 'yellow')

        def _reference_master():
            # 引用 Master 无命名空间（默认 None → 无命名空间）
            safe_run(lambda: self.file_ops.reference_master())
            _show_info_inview('Master referenced', 'yellow')

        open_path_action.triggered.connect(_open)
        open_master_action.triggered.connect(_open_master)
        import_master_action.triggered.connect(_import_master)
        reference_master_action.triggered.connect(_reference_master)
        menu.exec_(list_widget.mapToGlobal(position))

    def show_version_menu(self, position):
        list_widget = self.ui.version_list
        item = list_widget.itemAt(position)

        if not item:
            return

        version_name = item.text()
        menu = QtWidgets.QMenu(list_widget)

        add_menu_label(menu, u'📋 版本信息: {}'.format(version_name))
        locate_action = menu.addAction(u"📂 打开版本路径")
        menu.addSeparator()
        open_action = menu.addAction(u" 打开")
        import_action = menu.addAction(u" 导入")
        reference_action = menu.addAction(u" 引用")
        menu.addSeparator()
        set_master_action = menu.addAction(u"⚙ Set Master ")
        menu.addSeparator()
        add_menu_label(menu, "⭐ fbx:")

        set_fbx_action = menu.addAction(u'⚙ 设置FBX导出对象')
        menu.addSeparator()
        fbx_menu = menu.addMenu(u"Export FBX")
        export_fbx_action = fbx_menu.addAction(u"📤 导出 FBX")
        export_fbx_ue_action = fbx_menu.addAction(u'📤 导出FBX to UE')
        menu.addSeparator()
        add_menu_label(menu, u"  删除:")
        delete_action = menu.addAction(u"🗑️ 删除当前选择")

        def safe_run(func):
            try:
                func()
            except Exception as e:
                QtWidgets.QMessageBox.warning(
                    self.ui,
                    u"错误",
                    str(e)
                )

        def _open():
            safe_run(lambda: self.file_ops.open_version(version_name))
            _show_info_inview('The selected version has been opened', 'yellow')

        def _import():
            safe_run(lambda: self.file_ops.import_version(version_name))
            _show_info_inview('The selected version has been imported', 'yellow')

        def _reference():
            ns = version_name.split('.')[0]
            safe_run(
                lambda: self.file_ops.reference_version(version_name, namespace=ns)
            )
            _show_info_inview('The selected version has been reference', 'yellow')

        def _locate():
            safe_run(lambda: self.path_service.open_version_path(version_name))

        def _set_master():
            safe_run(lambda: self.file_ops.set_master(version_name))
            if hasattr(self.ui, "show_info"):
                self.ui.show_info(u'设置Master成功', u'{} 设置Master完成'.format(version_name))

        def _export(to_ue=False):
            safe_run(lambda: self.exporter.export_fbx_for_version(version_name, to_ue))

        def _delete():
            ok = self.version_service.delete_selected_version(version_name)
            if ok:
                safe_run(lambda: self.file_ops.write_note_info(self.subtype, version_name, "Delete", True))
            if ok and hasattr(self.ui, "refresh_all"):
                self.ui.refresh_all()

        open_action.triggered.connect(_open)
        import_action.triggered.connect(_import)
        reference_action.triggered.connect(_reference)
        locate_action.triggered.connect(_locate)
        set_master_action.triggered.connect(_set_master)
        set_fbx_action.triggered.connect(self.ui.set_fbx_export_objects)
        export_fbx_action.triggered.connect(_export)
        export_fbx_ue_action.triggered.connect(lambda: _export(True))
        delete_action.triggered.connect(_delete)

        menu.exec_(list_widget.mapToGlobal(position))


def show_asset_context_menu(main_window, position):
    ctx = VersionContextMenu(main_window)
    ctx.show_asset_menu(position)


def show_subtype_context_menu(main_window, position):
    ctx = VersionContextMenu(main_window)
    ctx.show_subtype_menu(position)


def show_version_context_menu(main_window, position):
    ctx = VersionContextMenu(main_window)
    ctx.show_version_menu(position)


__all__ = [
    'show_asset_context_menu',
    'show_subtype_context_menu',
    'show_version_context_menu'
]
