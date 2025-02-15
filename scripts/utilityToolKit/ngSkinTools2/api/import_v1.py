# for same mesh, convert from v1 layers to v2
from maya import cmds, mel

from ngSkinTools2.api.log import getLogger
from ngSkinTools2.decorators import undoable

logger = getLogger("import v1")

__has_v1 = None


def has_v1():
    global __has_v1
    if __has_v1 is not None:
        return __has_v1

    __has_v1 = False
    try:
        cmds.loadPlugin('ngSkinTools')
        __has_v1 = True
    except:
        pass


def can_import(target):
    if not has_v1():
        return False
    try:
        result = cmds.ngSkinLayer(target, q=True, lda=True)
        return result == 1
    except Exception as err:
        logger.error(err)
        return False


def cleanup(selection):
    """
    Delete V1 data from provided list of nodes. Must be a v1 compatible target


    :type selection: list[string]
    """
    for s in selection:
        hist = cmds.listHistory(s) or []
        skinClusters = [i for i in hist if cmds.nodeType(i) in ('skinCluster')]
        cmds.delete(
            [
                i
                for skinCluster in skinClusters
                for i in cmds.listHistory(skinCluster, future=True, levels=1)
                if cmds.nodeType(i) in ('ngSkinLayerDisplay', 'ngSkinLayerData')
            ]
        )


@undoable
def import_layers(target):
    if not has_v1():
        return False

    import ngSkinTools2.api as ngst_api

    layers = ngst_api.init_layers(target)

    layerList = cmds.ngSkinLayer(target, q=True, listLayers=True)
    layerList = [layerList[i : i + 3] for i in range(0, len(layerList), 3)]

    layerIdMap = {0: None}

    def get_layer_influences(layerId):
        influences = mel.eval("ngSkinLayer -id {0} -q -listLayerInfluences -activeInfluences {1}".format(layerId, target)) or []
        return zip(influences[0::2], map(int, influences[1::2]))

    def get_layer_weights(layerId, infl):
        return mel.eval("ngSkinLayer -id {0:d} -paintTarget {1} -q -w {2:s}".format(layerId, infl, target))

    def copy_layer(oldLayerId, newLayer):
        """

        :type oldLayerId: int
        :type newLayer: ngSkinTools2.api.layers.Layer
        """

        newLayer.opacity = mel.eval("ngSkinLayer -id {0:d} -q -opacity {1:s}".format(oldLayerId, target))
        newLayer.enabled = mel.eval("ngSkinLayer -id {0:d} -q -enabled {1:s}".format(oldLayerId, target))

        newLayer.set_weights(ngst_api.NamedPaintTarget.MASK, get_layer_weights(oldLayerId, "mask"))
        newLayer.set_weights(ngst_api.NamedPaintTarget.DUAL_QUATERNION, get_layer_weights(oldLayerId, "dq"))

        for inflPath, inflId in get_layer_influences(oldLayerId):
            logger.info("importing influence %s for layer %s", inflPath, oldLayerId)
            weights = get_layer_weights(oldLayerId, inflId)
            newLayer.set_weights(inflId, weights)

    with ngst_api.suspend_updates(target):
        for layerId, layerName, layerParent in layerList:
            layerId = int(layerId)
            layerParent = int(layerParent)
            newLayer = layers.add(name=layerName, force_empty=True, parent=layerIdMap[layerParent])
            newLayer.index = 0
            layerIdMap[layerId] = newLayer.id

            copy_layer(layerId, newLayer)
