# -*- coding: utf-8 -*-

# .FileName:__init__.py.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2025/7/24 22:34
# .Finish time:
import saveRootPath as Root
import HelpImageUI as Help
import mayaPrint as mayaPrint
import Utils.Decorator as Decorator

base_dir = Root.ParentPath.replace("\\", "/")
icon_dir = Root.IconsPath.replace("\\", "/")
Help = Help
decorator = Decorator
mayaPrint = mayaPrint

__all__ = [
    "base_dir",
    "icon_dir",
    "Help",
    "decorator",
    "mayaPrint",
]