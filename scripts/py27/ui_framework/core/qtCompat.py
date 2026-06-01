# -*- coding: utf-8 -*-

# .FileName:qtCompat.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2025/12/7 17:29
# .Finish time:
"""
QtCompat.py – 统一兼容  PySide / PySide2 / PySide6
"""

from __future__ import absolute_import, print_function
import sys

try:
    long
except NameError:
    long = int


# -----------------------------------------------------------
# 按顺序尝试 PySide6 → PySide2 → PySide1
# -----------------------------------------------------------

PYSIDE_VERSION = None
QtCore = None
QtGui = None
QtWidgets = None
QAction = None
wrapInstance = None


# -----------------------------------------------------------
# Maya环境智能判断
# -----------------------------------------------------------
PYSIDE_VERSION = None

try:
    import maya.cmds as cmds
    maya_ver = int(cmds.about(v=True))
except:
    maya_ver = 2024


# Maya2025+
if maya_ver >= 2025:

    try:
        from PySide6 import QtCore, QtGui, QtWidgets
        from shiboken6 import wrapInstance
        from PySide6.QtGui import QAction
        PYSIDE_VERSION = 6

    except:
        from PySide2 import QtCore, QtGui, QtWidgets
        from shiboken2 import wrapInstance
        from PySide2.QtWidgets import QAction
        PYSIDE_VERSION = 2

# Maya2024-
else:

    try:
        from PySide2 import QtCore, QtGui, QtWidgets
        from shiboken2 import wrapInstance
        from PySide2.QtWidgets import QAction
        PYSIDE_VERSION = 2

    except:
        from PySide6 import QtCore, QtGui, QtWidgets
        from shiboken6 import wrapInstance
        from PySide6.QtGui import QAction
        PYSIDE_VERSION = 6


# -----------------------------------------------------------
# Qt 枚举兼容层（PySide1 / 2 / 6 全覆盖）
# -----------------------------------------------------------

def _get_enum(container, name, sub=None):
    """
    通用枚举获取：
    - PySide2/1: Qt.AlignLeft
    - PySide6:   Qt.AlignmentFlag.AlignLeft
    """
    # 旧版（PySide1 / PySide2）
    if hasattr(container, name):
        return getattr(container, name)

    # Qt6 新枚举结构
    if sub and hasattr(container, sub):
        sub_obj = getattr(container, sub)
        if hasattr(sub_obj, name):
            return getattr(sub_obj, name)

    raise AttributeError("Qt enum not found: {}.{}".format(container, name))


# ----------------------------
# Alignment（对齐）
# ----------------------------
def QtAlign(name):
    """
    Qt 对齐枚举兼容：
    PySide6: Qt.AlignmentFlag.AlignXXX
    PySide2/PySide1: Qt.AlignXXX
    """
    if PYSIDE_VERSION >= 6:
        return getattr(QtCore.Qt.AlignmentFlag, name)
    return getattr(QtCore.Qt, name)


# ----------------------------
# Orientation（方向）
# ----------------------------
def QtOrientation(name):
    if PYSIDE_VERSION >= 6:
        return getattr(QtCore.Qt.Orientation, name)
    return getattr(QtCore.Qt, name)


# ----------------------------
# ItemFlag（item flags）
# ----------------------------
def QtItemFlag(name):
    """
    示例:
        QtItemFlag("ItemIsSelectable")
        QtItemFlag("ItemIsEditable")
    """
    return _get_enum(QtCore.Qt, name, "ItemFlag")


# ----------------------------
# CheckState（勾选状态）
# ----------------------------
def QtCheckState(name):
    if PYSIDE_VERSION >= 6:
        return getattr(QtCore.Qt.CheckState, name)
    return getattr(QtCore.Qt, name)



# ----------------------------
# SortOrder（排序）
# ----------------------------
def QtSortOrder(name):
    return _get_enum(QtCore.Qt, name, "SortOrder")


# ----------------------------
# KeyboardModifier（键盘修饰键）
# ----------------------------
def QtModifier(name):
    return _get_enum(QtCore.Qt, name, "KeyboardModifier")


# ----------------------------
# QHeaderView ResizeMode（你刚才那个坑）
# ----------------------------
def QtHeaderResizeMode(name):
    header = QtWidgets.QHeaderView

    if hasattr(header, name):
        return getattr(header, name)

    if hasattr(header, "ResizeMode"):
        return getattr(header.ResizeMode, name)

    raise AttributeError("QHeaderView ResizeMode not found: {}".format(name))


def get_header_resize_mode(mode_name="ResizeToContents"):
    """
    统一 QHeaderView ResizeMode 获取方式

    mode_name 可选：
        - ResizeToContents
        - Stretch
        - Interactive
        - Fixed
    """
    header = QtWidgets.QHeaderView

    # PySide2 / PySide1
    if hasattr(header, mode_name):
        return getattr(header, mode_name)

    # PySide6
    if hasattr(header, "ResizeMode"):
        return getattr(header.ResizeMode, mode_name)

    raise AttributeError("QHeaderView 无法找到 ResizeMode: {}".format(mode_name))


def QtShortcut():
    if PYSIDE_VERSION >= 6:
        return QtGui.QShortcut
    return QtWidgets.QShortcut


def QtPenStyle(name):
    """
    Qt PenStyle 兼容
    Qt5: QtCore.Qt.SolidLine
    Qt6: QtCore.Qt.PenStyle.SolidLine
    """
    if PYSIDE_VERSION >= 6:
        return getattr(QtCore.Qt.PenStyle, name)
    return getattr(QtCore.Qt, name)


def QtBrushStyle(name):
    """
    Qt BrushStyle 兼容
    Qt5: QtCore.Qt.FDiagPattern
    Qt6: QtCore.Qt.BrushStyle.FDiagPattern
    """
    if PYSIDE_VERSION >= 6:
        return getattr(QtCore.Qt.BrushStyle, name)
    return getattr(QtCore.Qt, name)


def QtCursorShape(name):
    if PYSIDE_VERSION >= 6:
        return getattr(QtCore.Qt.CursorShape, name)
    return getattr(QtCore.Qt, name)


def QtMouseButton(name):
    if PYSIDE_VERSION >= 6:
        return getattr(QtCore.Qt.MouseButton, name)
    return getattr(QtCore.Qt, name)


def QtKeyboardModifier(name):
    if PYSIDE_VERSION >= 6:
        return getattr(QtCore.Qt.KeyboardModifier, name)
    return getattr(QtCore.Qt, name)


def QtRegex(pattern):
    if PYSIDE_VERSION >= 6:
        return QtCore.QRegularExpression(pattern)
    return QtCore.QRegExp(pattern)


def regex_finditer(regex, text):
    """
    统一 QRegExp / QRegularExpression
    返回 (start, length)
    """
    if PYSIDE_VERSION >= 6:
        it = regex.globalMatch(text)
        while it.hasNext():
            m = it.next()
            yield m.capturedStart(), m.capturedLength()
    else:
        index = regex.indexIn(text)
        while index >= 0:
            length = regex.matchedLength()
            yield index, length
            index = regex.indexIn(text, index + length)


_raw_wrapInstance = wrapInstance

def wrapInstance_safe(ptr, base_class):
    if PYSIDE_VERSION == 1:
        return _raw_wrapInstance(long(ptr), base_class)
    return _raw_wrapInstance(int(ptr), base_class)

wrapInstance = wrapInstance_safe

__all__ = [
    "PYSIDE_VERSION",
    "QtCore",
    "QtGui",
    "QtWidgets",
    "wrapInstance",
    "QAction",
    "QtAlign",
    "QtOrientation",
    "QtItemFlag",
    "QtCheckState",
    "QtSortOrder",
    "QtMouseButton",
    "QtModifier",
    "QtHeaderResizeMode",
    "get_header_resize_mode",
    "QtShortcut",
    "QtRegex",
    "regex_finditer",
    "QtPenStyle",
    "QtBrushStyle",
    "QtCursorShape",
    "QtMouseButton",
    "QtKeyboardModifier"

]
