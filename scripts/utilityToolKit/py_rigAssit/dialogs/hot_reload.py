# -*- coding: utf-8 -*-

# .FileName:hot_reload.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/12 23:01
# .Finish time:

import importlib
import sys


class HotReloader(object):

    @staticmethod
    def reload_module(module_name):
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])

    @staticmethod
    def reload_many(*mods):
        for m in mods:
            HotReloader.reload_module(m)