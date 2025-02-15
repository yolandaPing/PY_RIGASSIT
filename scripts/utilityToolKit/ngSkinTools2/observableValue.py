from ngSkinTools2.api.python_compatibility import Object
from ngSkinTools2.signal import Signal


class Undefined(Object):
    pass


class ObservableValue(Object):
    def __init__(self, default_value=Undefined):
        self.value = default_value
        self.changed = Signal("observable value")

    def set(self, value):
        self.value = value
        self.changed.emit()

    def __call__(self, default=Undefined, *args, **kwargs):
        if self.value != Undefined:
            return self.value

        if default != Undefined:
            return default

        raise Exception("using observable value before setting it")
