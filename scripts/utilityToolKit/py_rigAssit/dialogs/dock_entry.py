# -*- coding: utf-8 -*-

# .FileName:dock_entry.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/5/2 15:25
# .Finish time:
import maya.cmds as cmds

from py_rigAssit import QtWidgets,  Widgets
from  py_rigAssit.dialogs.manager import PYRiggingDialogManager

py_widgets = Widgets()
DOCK_NAME = "PY_RIGASSITDockControl"
_DIALOG_DATA_CACHE = None


# ---------------------------------------------------------
# UI 构建
# ---------------------------------------------------------
def _build_ui(parent, dialog_data):
    ui = PYRiggingDialogManager(dialog_data, parent=parent)
    parent.layout().addWidget(ui)
    return ui


# ---------------------------------------------------------
# 清理 layout（防止叠加）
# ---------------------------------------------------------
def _clear_layout(layout):
    if not layout:
        return

    while layout.count():
        item = layout.takeAt(0)
        w = item.widget()
        if w:
            w.setParent(None)
            w.deleteLater()

    # ⭐ 强制 Qt 刷新（防残留）
    QtWidgets.QApplication.processEvents()


# ---------------------------------------------------------
# workspaceControl 回调入口（核心）
# ---------------------------------------------------------
def build_in_workspace():
    global _DIALOG_DATA_CACHE

    parent = py_widgets.workspace_control_widget(DOCK_NAME)
    if parent is None:
        return

    layout = parent.layout()
    if layout is None:
        layout = QtWidgets.QVBoxLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        parent.setLayout(layout)

    _clear_layout(layout)

    _build_ui(parent, _DIALOG_DATA_CACHE)


# ---------------------------------------------------------
# uiScript（必须无参数）
# ---------------------------------------------------------
def _ui_script():
    return (
        "import py_rigAssit.dialogs.dock_entry as de; "
        "de.build_in_workspace()"
    )


# ---------------------------------------------------------
# 对外唯一入口
# ---------------------------------------------------------
def open_dock(dialog_data):
    global _DIALOG_DATA_CACHE

    _DIALOG_DATA_CACHE = dialog_data

    if not cmds.workspaceControl(DOCK_NAME, exists=True):
        cmds.workspaceControl(
            DOCK_NAME,
            label="PY_RIGASSIT",
            retain=False,     # ⭐ 关键：禁止 Maya 缓存 UI
            floating=False,
            uiScript=_ui_script()
        )
    else:
        # ⭐ 强制 Maya 重新执行 uiScript（关键）
        cmds.workspaceControl(DOCK_NAME, e=True, restore=True)

    cmds.evalDeferred(
        lambda: cmds.workspaceControl(DOCK_NAME, e=True, r=True)
    )


# ---------------------------------------------------------
# 关闭
# ---------------------------------------------------------
def close_dock():
    try:
        if cmds.workspaceControl(DOCK_NAME, exists=True):
            cmds.deleteUI(DOCK_NAME)
    except:
        pass