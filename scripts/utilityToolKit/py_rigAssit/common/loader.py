# -*- coding: utf-8 -*-

# .FileName:loader.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/12 19:49
# .Finish time:

import maya.cmds as cmds
from py_rigAssit import QtWidgets


class SelectionLoader(object):

    @classmethod
    def load_lineedit(cls,
                      parent,
                      field,
                      obj_type="any",
                      multiple=False,
                      separator=", ",
                      full_path=False):
        """
        field      : QLineEdit
        obj_type   : str / list / tuple
        multiple   : 是否多选写入
        separator  : 分隔符
        full_path  : 是否返回长路径
        """

        objs = cmds.ls(sl=True, long=full_path) or []

        if not objs:
            cls.warning(parent, u"请先选择对象")
            return []

        result = cls.filter_objects(objs, obj_type)

        if not result:
            cls.warning(parent, u"没有符合类型的对象")
            return []

        if multiple:
            field.setText(separator.join(result))
        else:
            field.setText(result[0])

        return result

    # =====================================================
    # 核心过滤器
    # =====================================================

    @classmethod
    def filter_objects(cls, objs, obj_type):
        """
        obj_type 支持:

        "joint"
        "mesh"
        "curve"
        "surface"
        "locator"
        "transform"
        "group"

        ["joint", "mesh"]
        ("joint", "curve")
        """

        if obj_type in [None, "", "any"]:
            return objs

        if not isinstance(obj_type, (list, tuple)):
            obj_type = [obj_type]

        result = []

        for obj in objs:
            for t in obj_type:
                if cls.match_type(obj, t):
                    result.append(obj)
                    break

        return result

    @classmethod
    def match_type(cls, obj, t):

        node_type = cmds.nodeType(obj)

        # ----------------------
        # transform
        # ----------------------
        if t == "transform":
            return node_type == "transform"

        # ----------------------
        # joint
        # ----------------------
        if t == "joint":
            return node_type == "joint"

        # ----------------------
        # group（无shape的transform）
        # ----------------------
        if t == "group":
            if node_type != "transform":
                return False
            shapes = cmds.listRelatives(obj, s=True) or []
            return len(shapes) == 0

        # ----------------------
        # locator
        # ----------------------
        if t == "locator":
            return cls.has_shape(obj, "locator")

        # ----------------------
        # mesh
        # ----------------------
        if t == "mesh":
            return cls.has_shape(obj, "mesh")

        # ----------------------
        # curve
        # ----------------------
        if t == "curve":
            return cls.has_shape(obj, "nurbsCurve")

        # ----------------------
        # surface
        # ----------------------
        if t == "surface":
            return cls.has_shape(obj, "nurbsSurface")

        # ----------------------
        # 原生 nodeType
        # ----------------------
        return node_type == t

    @classmethod
    def has_shape(cls, obj, shape_type):
        shapes = cmds.listRelatives(obj, s=True, ni=True) or []
        for shp in shapes:
            if cmds.nodeType(shp) == shape_type:
                return True
        return False

    @classmethod
    def warning(cls, parent, msg):
        QtWidgets.QMessageBox.warning(parent, u"警告", msg)


if __name__ == '__main__':
    pass
    # #1
    # SelectionLoader.load_lineedit(
    #     self,
    #     self.lineEdit,
    #     "mesh"
    # )
    # #2
    # SelectionLoader.load_lineedit(
    #     self,
    #     self.lineEdit,
    #     "joint",
    #     multiple=True
    # )