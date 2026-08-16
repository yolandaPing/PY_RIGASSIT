# -*- coding: utf-8 -*-

# .FileName:saveRootPath
# .Date....:2023-01-09 : 16 :37
# .@Author:You P
# .
# .Finish time:
import os


def get_py_rigassit_dirs():
    """
    查找当前工具所在 PY_RIGASSIT 目录
    """
    current_dir = os.path.dirname(__file__)
    scripts_dir = os.path.dirname(current_dir)
    utility_dir = os.path.dirname(scripts_dir)
    py_rigassit_root = utility_dir
    icons_dir = os.path.join(py_rigassit_root, "icons")
    curve_data_dir = os.path.join(py_rigassit_root, "files", "CurveData")
    return py_rigassit_root, scripts_dir, current_dir, icons_dir, curve_data_dir


py_rigassit_dir, scripts_dir, current_dir, icons_dir, curve_data_dir = get_py_rigassit_dirs()

ParentPath = os.path.split(__file__)[0].split('scripts')[0]
ScriptsPath = os.path.split(__file__)[0].split(' ')[0]
IconsPath = ParentPath+"icons"
CurveDataPath = ParentPath+"files/CurveData"


# print(ParentPath,ScriptsPath,IconsPath,CurveDataPath)

# print("py_rigassit:", get_py_rigassit_root())