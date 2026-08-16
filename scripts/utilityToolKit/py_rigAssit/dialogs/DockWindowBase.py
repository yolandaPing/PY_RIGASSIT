# -*- coding: utf-8 -*-

from __future__ import print_function

import maya.cmds as cmds
import maya.OpenMayaUI as omui

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from py_rigAssit import QtWidgets, QtCore, wrapInstance


def maya_main_window():
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(ptr, QtWidgets.QWidget)


class _DockRegistry(object):
    _instances = {}

    @classmethod
    def get(cls, name):
        return cls._instances.get(name)

    @classmethod
    def set(cls, name, obj):
        cls._instances[name] = obj

    @classmethod
    def remove(cls, name):
        if name in cls._instances:
            cls._instances.pop(name)


class DockWindowBase(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    TOOL_NAME = "PY_RIGASSITDockControl"
    DEFAULT_AREA = "left"

    def __init__(self, widget_cls=None, title="PY_RIGASSIT", parent=None):
        super(DockWindowBase, self).__init__(parent or maya_main_window())

        self.setObjectName(self.TOOL_NAME)
        self.setWindowTitle(title)
        self.resize(420, 700)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(2, 2, 2, 2)
        self.main_layout.setSpacing(2)

        self.ui = None
        if widget_cls:
            try:
                self.ui = widget_cls() if callable(widget_cls) else widget_cls
                self.main_layout.addWidget(self.ui)
            except Exception as e:
                print("UI Build Error:", e)

    @classmethod
    def _force_cleanup(cls):
        """彻底清理所有残留的 UI 和 workspaceControl"""
        # 1. 清理 workspaceControl
        workspace_names = [
            cls.TOOL_NAME,
            cls.TOOL_NAME + "WorkspaceControl",
            cls.TOOL_NAME + "WorkspaceControl"
        ]
        for name in set(workspace_names):
            try:
                if cmds.workspaceControl(name, exists=True):
                    cmds.workspaceControl(name, e=True, close=True)
                    cmds.deleteUI(name, control=True)
            except:
                pass
            try:
                cmds.workspaceControlState(name, remove=True)
            except:
                pass

        # 2. 清理可能存在的普通 Maya 窗口
        try:
            if cmds.window(cls.TOOL_NAME, exists=True):
                cmds.deleteUI(cls.TOOL_NAME, window=True)
        except:
            pass

        # 3. 清理 Qt 顶层窗口
        app = QtWidgets.QApplication.instance()
        if app:
            for w in app.topLevelWidgets():
                try:
                    if w.objectName() == cls.TOOL_NAME:
                        w.setParent(None)
                        w.deleteLater()
                except:
                    pass
            app.processEvents()

        # 4. 清除注册表
        _DockRegistry.remove(cls.TOOL_NAME)

    @classmethod
    def _get_or_create(cls, widget_cls, title):
        exist = _DockRegistry.get(cls.TOOL_NAME)

        if exist:
            try:
                exist.raise_()
                exist.activateWindow()
                return exist
            except:
                cls._force_cleanup()

        win = cls(widget_cls, title)
        _DockRegistry.set(cls.TOOL_NAME, win)
        return win

    @classmethod
    def safe_dock(cls, widget_cls=None, title="PY_RIGASSIT"):
        """
        安全地将窗口停靠到 Maya 界面。
        采用直接停靠模式，避免先浮动再吸附导致的闪烁或崩溃。
        """
        # 彻底清理旧实例
        cls._force_cleanup()

        # 创建新窗口
        win = cls._get_or_create(widget_cls, title)

        # 延迟一点显示，确保清理完全生效
        def show_docked():
            # 再次确认窗口没有被意外删除
            if _DockRegistry.get(cls.TOOL_NAME) is None:
                return
            try:
                win.show(
                    dockable=True,
                    floating=False,
                    area=cls.DEFAULT_AREA,
                    allowedArea="all",
                    retain=False
                )
            except Exception as e:
                print("Dock show error:", e)
                # 备用方案
                try:
                    win.show(dockable=True, floating=True)
                except:
                    pass

        QtCore.QTimer.singleShot(10, show_docked)
        return win

    def to_float(self):
        """切换到浮动模式"""
        try:
            self.show(dockable=True, floating=True)
        except:
            pass

    def tabify_to(self, target="AttributeEditor"):
        """将窗口合并到指定的标签页（例如属性编辑器）"""
        try:
            cmds.workspaceControl(self.TOOL_NAME, e=True, tabToControl=(target, -1))
        except:
            pass

    def save_state(self):
        """保存当前停靠区域，以便下次恢复"""
        try:
            area = cmds.workspaceControl(self.TOOL_NAME, q=True, dockArea=True)
            if area:
                cmds.optionVar(sv=("PY_RIGASSIT_DOCK_AREA", area))
        except:
            pass

    def restore_state(self):
        """恢复上次停靠区域"""
        try:
            area = cmds.optionVar(q="PY_RIGASSIT_DOCK_AREA")
            if area:
                self.DEFAULT_AREA = area
        except:
            pass

    def closeEvent(self, event):
        self.save_state()
        # 清理注册表，避免下次打开时引用已销毁的对象
        _DockRegistry.remove(self.TOOL_NAME)
        # 调用父类 closeEvent 完成关闭
        super(DockWindowBase, self).closeEvent(event)