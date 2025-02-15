pyside6 = False
try:
    from PySide6 import QtCore, QtGui, QtSvg, QtWidgets
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QAction, QActionGroup
    from PySide6.QtSvgWidgets import QSvgWidget
    from PySide6.QtWidgets import QWidget

    pyside6 = True
except:
    from PySide2 import QtCore, QtGui, QtSvg, QtWidgets
    from PySide2.QtCore import Qt
    from PySide2.QtSvg import QSvgWidget
    from PySide2.QtWidgets import QAction, QActionGroup, QWidget


def get_main_window():
    from maya import OpenMayaUI as omui

    return wrap_instance(omui.MQtUtil.mainWindow(), QWidget)


def wrap_instance(ptr, widget):
    if pyside6:
        from shiboken6 import wrapInstance
    else:
        from shiboken2 import wrapInstance

    return wrapInstance(int(ptr), widget)
