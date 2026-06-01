from functools import wraps

from maya import cmds

from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.python_compatibility import Object

log = getLogger("decorators")


def preserve_selection(function):
    """
    decorator for function;
    saves selection prior to execution and restores it
    after function finishes
    """

    @wraps(function)
    def undoable_wrapper(*args, **kargs):
        selection = cmds.ls(sl=True, fl=True)
        highlight = cmds.ls(hl=True, fl=True)
        try:
            return function(*args, **kargs)
        finally:
            if selection:
                cmds.select(selection)
            else:
                cmds.select(clear=True)
            if highlight:
                cmds.hilite(highlight)

    return undoable_wrapper


def undoable(function):
    """
    groups function contents into one undo block
    """

    @wraps(function)
    def result(*args, **kargs):
        with Undo(name=function.__name__):
            return function(*args, **kargs)

    return result


class Undo(Object):
    """
    an undo context for use "with Undo():"
    """

    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        log.debug("UNDO chunk %r: start", self.name)
        cmds.undoInfo(openChunk=True, chunkName=self.name)
        return self

    def __exit__(self, _type, value, traceback):
        log.debug("UNDO chunk %r: end", self.name)
        cmds.undoInfo(closeChunk=True)


def trace_exception(function):
    @wraps(function)
    def result(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            import sys
            import traceback

            traceback.print_exc(file=sys.__stderr__)
            raise

    return result
