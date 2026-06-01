# -*- coding: utf-8 -*-

# .FileName:mayaPrint.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/18 1:19
# .Finish time:
import maya.OpenMaya as om


def log(msg):
    om.MGlobal.displayInfo(msg)


def warning(msg):
    om.MGlobal.displayWarning(msg)


def error(msg):
    om.MGlobal.displayError(msg)