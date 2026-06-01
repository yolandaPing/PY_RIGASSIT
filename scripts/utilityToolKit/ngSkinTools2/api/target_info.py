import json

from maya import cmds

from ngSkinTools2.api import plugin


def get_related_skin_cluster(target):
    """
    Returns skinCluster if provided node name represents skinned mesh. Returns true for shapes that have
    skinCLuster in their deformation stack, or it's a skinCluster node itself.

    For invalid targets, returns None
    """

    return plugin.ngst2Layers(target, q=True, layerDataAttachTarget=True)


def get_related_data_node(target):
    """
    :returns: ngSkinTools data node name for this target
    """
    return plugin.ngst2Layers(target, q=True, layerDataNode=True)


def unserialize_influences_from_json_data(info):
    from .influenceMapping import InfluenceInfo

    def as_influence_info(data):
        influence = InfluenceInfo()
        influence.pivot = data['pivot']
        influence.path = data.get('path', None)
        influence.name = data.get('name', None)
        influence.labelText = data['labelText']
        influence.labelSide = InfluenceInfo.SIDE_MAP[data['labelSide']]
        influence.logicalIndex = data['index']

        return influence

    if not info:
        return []

    return [as_influence_info(i) for i in info]


def list_influences(target):
    """
    List influences in the given skin cluster as InfluenceInfo objects

    :param str target: target mesh or skin cluster
    :rtype: list[InfluenceInfo]
    """
    info = json.loads(plugin.ngst2Layers(target, q=True, influenceInfo=True))
    return unserialize_influences_from_json_data(info)


def add_influences(influences, target):
    """
    A shortcut for adding additional influences to a skincluster, without impacting existing weights

    :param list[str] influences: list of influence paths
    :param str target: target mesh or skin cluster
    """

    skin_cluster = get_related_skin_cluster(target)

    def long_names(names):
        result = set(cmds.ls(names, long=True))
        if len(result) != len(names):
            raise Exception("could not convert to a list of influences names: " + str(names))
        return result

    existing = long_names([i.name if not i.path else i.path for i in list_influences(skin_cluster)])
    influences = long_names(influences)
    for i in influences - existing:
        cmds.skinCluster(skin_cluster, edit=True, addInfluence=i, weight=0)


def is_slow_mode_skin_cluster(target):
    """
    returns true, if ngSkinTools chose to use slow ngSkinTools api for this target. Right now this only happens when skinCluster has non-transform
    nodes as influences (e.g. inverseMatrix node).

    :param str target: target mesh or skin cluster
    """
    return plugin.ngst2Layers(target, q=True, skinClusterWriteMode=True) == "plug"
