from ngSkinTools2.api import plugin
from ngSkinTools2.api.python_compatibility import Object


def suspend_updates(target):
    return SuspendUpdatesContext(target)


class SuspendUpdatesContext(Object):
    def __init__(self, target):
        self.target = target

    def __enter__(self):
        plugin.ngst2Layers(self.target, suspendUpdates=True)

    def __exit__(self, _type, value, traceback):
        plugin.ngst2Layers(self.target, suspendUpdates=False)
