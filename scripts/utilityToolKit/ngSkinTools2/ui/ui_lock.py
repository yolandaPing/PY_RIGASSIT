import functools

from ngSkinTools2.api.python_compatibility import Object


class UiLock(Object):
    def __init__(self):
        self.updating = False

    def __enter__(self):
        self.updating = True

    def skip_if_updating(self, fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if self.updating:
                return
            return fn(*args, **kwargs)

        return wrapper

    def __exit__(self, _type, value, traceback):
        self.updating = False
