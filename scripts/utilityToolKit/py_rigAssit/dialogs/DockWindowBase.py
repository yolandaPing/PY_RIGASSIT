# -*- coding: utf-8 -*-

from __future__ import print_function

import maya.cmds as cmds
import maya.OpenMayaUI as omui

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from py_rigAssit import QtWidgets, QtCore, wrapInstance


# ---------------------------------------------------------
# Maya Main Window
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# Pro Dock Base
# ---------------------------------------------------------
class DockWindowBase(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    TOOL_NAME = "PY_RIGASSITDockControl"
    DEFAULT_AREA = "left"

    # -----------------------------------------------------
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

        names = [
            cls.TOOL_NAME,
            cls.TOOL_NAME + "WorkspaceControl"
        ]

        # ---- Maya UI ----
        for name in names:
            try:
                if cmds.workspaceControl(name, exists=True):
                    cmds.workspaceControl(name, e=True, close=True)
            except:
                pass

            try:
                cmds.deleteUI(name, control=True)
            except:
                pass

            try:
                cmds.workspaceControlState(name, remove=True)
            except:
                pass

        # ---- Qt UI ----
        app = QtWidgets.QApplication.instance()
        for w in app.topLevelWidgets():
            try:
                if w.objectName() == cls.TOOL_NAME:
                    w.setParent(None)
                    w.deleteLater()
            except:
                pass

        app.processEvents()

        # ---- registry ----
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

        cls._force_cleanup()

        win = cls._get_or_create(widget_cls, title)

        def do_show():
            try:
                win.show(
                    dockable=True,
                    floating=False,
                    area=cls.DEFAULT_AREA,
                    allowedArea="all"
                )
            except Exception as e:
                print("Dock Failed:", e)

        QtWidgets.QApplication.processEvents()
        QtCore.QTimer.singleShot(0, do_show)

        return win


    def to_float(self):
        try:
            self.show(dockable=True, floating=True)
        except:
            pass


    def tabify_to(self, target="AttributeEditor"):

        try:
            cmds.workspaceControl(
                self.TOOL_NAME,
                e=True,
                tabToControl=(target, -1)
            )
        except:
            pass


    def save_state(self):
        try:
            area = cmds.workspaceControl(
                self.TOOL_NAME,
                q=True,
                dockArea=True
            )
            cmds.optionVar(sv=("PY_RIGASSIT_DOCK_AREA", area))
        except:
            pass

    def restore_state(self):
        try:
            area = cmds.optionVar(q="PY_RIGASSIT_DOCK_AREA")
            if area:
                self.DEFAULT_AREA = area
        except:
            pass

    # -----------------------------------------------------
    def closeEvent(self, event):

        try:
            self.save_state()
        except:
            pass

        try:
            self.setParent(None)
            self.deleteLater()
        except:
            pass

        _DockRegistry.remove(self.TOOL_NAME)

        super(DockWindowBase, self).closeEvent(event)