import json

from maya import cmds

from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.python_compatibility import Object

log = getLogger("api/layers")


def __define_property__(name, conversion, doc, refresh_on_write=True):
    return property(
        lambda self: conversion(self.__load__(name)), lambda self, val: self.__save__(name, conversion(val), refresh=refresh_on_write), doc=doc
    )


# noinspection PyBroadException
class Config(Object):
    """
    per-skin-cluster configuration
    """

    influence_colors = __define_property__(
        "influence_colors",
        lambda v: {int(k): tuple(float(v[i]) for i in range(3)) for k, v in v.items()},
        doc="Influence color map [logical index]->(r,g,b)",
        refresh_on_write=True,
    )

    def __init__(self, data_node):
        self.data_node = data_node

    def __load__(self, attr):
        try:
            return json.loads(cmds.getAttr(self.data_node + ".config_" + attr))
        except:
            return None

    def __save__(self, attr, value, refresh=False):
        if not cmds.attributeQuery("config_" + attr, node=self.data_node, exists=True):
            cmds.addAttr(self.data_node, dt="string", longName="config_" + attr)
        cmds.setAttr(self.data_node + ".config_" + attr, json.dumps(value), type='string')

        if refresh:
            from ngSkinTools2.api.tools import refresh_screen

            refresh_screen(self.data_node)
