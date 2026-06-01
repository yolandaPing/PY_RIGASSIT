# -*- coding: utf-8 -*-

# .FileName:command_dispatcher.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/12 17:03
# .Finish time:
import maya.cmds as cmds


class CommandDispatcher(object):
    _commands = {}

    @classmethod
    def register(cls, name):
        def deco(func):
            cls._commands[name] = func
            return func
        return deco

    def __init__(self, ui=None):
        self.ui = ui

    def execute(self, name, *args, **kwargs):
        func = self._commands.get(name)
        if not func:
            print("No command:", name)
            return

        return func(self.ui, *args, **kwargs)


# class CommandDispatcher(object):
#
#     _registry = {}
#
#     # =========================================================
#     # decorator：自动注册
#     # =========================================================
#     @classmethod
#     def register(cls, name):
#         def deco(func):
#             cls._registry[name] = func
#             return func
#         return deco
#
#     # =========================================================
#     # 执行入口
#     # =========================================================
#     def run(self, name, *args, **kwargs):
#         func = self._registry.get(name)
#         if not func:
#             print("[Dispatcher] No command:", name)
#             return None
#         return func(self, *args, **kwargs)