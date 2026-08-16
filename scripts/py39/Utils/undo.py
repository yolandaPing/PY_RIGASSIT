# -*- coding: utf-8 -*-
# .FileName:undo
# .Date....:2025-02-17 : 16 :37
# .@Author:You P
# .
# .Finish time:

import maya.cmds as cmds
from functools import wraps

def undo(func):
    """装饰器：将函数执行包装为 Maya 撤销块"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            cmds.undoInfo(openChunk=True, chunkName=func.__name__)
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            cmds.undoInfo(closeChunk=True)
            raise e
        finally:
            cmds.undoInfo(closeChunk=True)
    return wrapper