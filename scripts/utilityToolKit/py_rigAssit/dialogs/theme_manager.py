# -*- coding: utf-8 -*-

# .FileName:theme_manager.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/12 23:01
# .Finish time:
import os
from py_rigAssit.dialogs import base_dir


class ThemeManager(object):
    _cache = ""

    @classmethod
    def qss_path(cls):
        return os.path.join(base_dir, "scripts", "styles", "style.qss")

    @classmethod
    def load(cls):
        path = os.path.abspath(cls.qss_path())
        if not os.path.exists(path):
            cls._cache = ""
            return ""

        with open(path, "r") as f:
            cls._cache = f.read()

        return cls._cache

    @classmethod
    def apply(cls, widget):
        if not cls._cache:
            cls.load()

        widget.setStyleSheet(cls._cache)

    @classmethod
    def reload(cls, widget=None):
        cls.load()
        if widget:
            cls.apply(widget)