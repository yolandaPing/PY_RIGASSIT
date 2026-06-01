import itertools

from maya import cmds

from ngSkinTools2.api import influenceMapping, internals, plugin, target_info
from ngSkinTools2.api.cmd_wrappers import get_source_node
from ngSkinTools2.api.layers import Layers
from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.python_compatibility import Object

log = getLogger("mirror")


class Mirror(Object):
    """
    query and configure mirror options for provided target
    """

    axis = internals.make_editable_property('mirrorAxis')
    seam_width = internals.make_editable_property('mirrorWidth')
    vertex_transfer_mode = internals.make_editable_property('vertexTransferMode')

    def __init__(self, target):
        """
        :type target: skin target (skinCluster or mesh)
        """
        self.target = target
        self.__skin_cluster__ = None
        self.__data_node__ = None

    # noinspection PyMethodMayBeStatic
    def __query__(self, **kwargs):
        return plugin.ngst2Layers(self.target, q=True, **kwargs)

    # noinspection PyMethodMayBeStatic
    def __edit__(self, **kwargs):
        plugin.ngst2Layers(self.target, configureMirrorMapping=True, **kwargs)
        self.recalculate_influences_mapping()

    def __mapper_config_attr(self):
        return self.__get_data_node__() + ".influenceMappingOptions"

    def build_influences_mapper(self, defaults=None):
        mapper = influenceMapping.InfluenceMapping()
        layers = Layers(self.target)
        mapper.influences = layers.list_influences()

        mapper.config.load_json(cmds.getAttr(self.__mapper_config_attr()))
        mapper.config.mirror_axis = self.axis

        return mapper

    def save_influences_mapper(self, mapper):
        """
        :type mapper: influenceMapping.InfluenceMapping
        """
        self.set_mirror_config(mapper.config.as_json())

    def set_mirror_config(self, config_as_json):
        cmds.setAttr(self.__mapper_config_attr(), config_as_json, type='string')

    def set_influences_mapping(self, mapping):
        """
        :type mapping: map[int] -> int
        """
        log.info("mapping updated: %r", mapping)

        mapping_as_string = ','.join(str(k) + "," + str(v) for (k, v) in list(mapping.items()))
        plugin.ngst2Layers(self.target, configureMirrorMapping=True, influencesMapping=mapping_as_string)

    def recalculate_influences_mapping(self):
        """
        loads current influence mapping settings, and update influences mapping with these values
        """
        m = self.build_influences_mapper().calculate()
        self.set_influences_mapping(influenceMapping.InfluenceMapping.asIntIntMapping(m))

    def mirror(self, options):
        """
        :type options: MirrorOptions
        """
        plugin.ngst2Layers(
            self.target,
            mirrorLayerWeights=options.mirrorWeights,
            mirrorLayerMask=options.mirrorMask,
            mirrorLayerDq=options.mirrorDq,
            mirrorDirection=options.direction,
        )

    def set_reference_mesh(self, mesh_shape):
        dest = self.__get_data_node__() + ".mirrorMesh"
        if mesh_shape:
            cmds.connectAttr(mesh_shape + ".outMesh", dest)
        else:
            for i in cmds.listConnections(dest, source=True, plugs=True):
                cmds.disconnectAttr(i, dest)

    def get_reference_mesh(self):
        return get_source_node(self.__get_data_node__() + '.mirrorMesh')

    def __get_skin_cluster__(self):
        if self.__skin_cluster__ is None:
            self.__skin_cluster__ = target_info.get_related_skin_cluster(self.target)
        return self.__skin_cluster__

    def __get_data_node__(self):
        if self.__data_node__ is None:
            self.__data_node__ = target_info.get_related_data_node(self.target)
        return self.__data_node__

    # noinspection PyStatementEffect
    def build_reference_mesh(self):
        sc = self.__get_skin_cluster__()
        dn = self.__get_data_node__()

        if sc is None or dn is None:
            return

        existing_ref_mesh = self.get_reference_mesh()
        if existing_ref_mesh:
            cmds.select(existing_ref_mesh)
            raise Exception("symmetry mesh already configured for %s: %s" % (str(sc), existing_ref_mesh))

        def get_shape(node):
            return cmds.listRelatives(node, shapes=True)[0]

        result, _ = cmds.polyCube()
        g = cmds.group(empty=True, name="ngskintools_mirror_mesh_setup")
        cmds.parent(result, g)
        result = cmds.rename(g + "|" + result, "mirror_reference_mesh")

        cmds.delete(result, ch=True)
        cmds.connectAttr(sc + ".input[0].inputGeometry", get_shape(result) + ".inMesh")
        cmds.delete(result, ch=True)

        (mirrored,) = cmds.duplicate(result)
        mirrored = cmds.rename(g + "|" + mirrored, 'flipped_preview')
        mirrored_shape = get_shape(mirrored)

        cmds.setAttr(mirrored + ".sx", -1)
        cmds.setAttr(mirrored + ".overrideEnabled", 1)
        cmds.setAttr(mirrored + ".overrideDisplayType", 2)
        cmds.setAttr(mirrored + ".overrideShading", 0)
        cmds.setAttr(mirrored + ".overrideTexturing", 1)

        (blend,) = cmds.blendShape(result, mirrored_shape)
        cmds.setAttr(blend + ".weight[0]", 1.0)

        # lock accidental transformations
        for c, t, m in itertools.product('xyz', 'trs', (result, mirrored)):
            cmds.setAttr(m + "." + t + c, lock=True)

        # shift setup to the right by slightly more than bounding box width

        bb = cmds.exactWorldBoundingBox(g)
        cmds.move((bb[3] - bb[0]) * 1.2, 0, 0, g, r=True)

        self.set_reference_mesh(str(result))
        cmds.select(result)
        return result


class MirrorOptions(Object):
    directionNegativeToPositive = 0
    directionPositiveToNegative = 1
    directionGuess = 2
    directionFlip = 3

    def __init__(self):
        self.mirrorWeights = True
        self.mirrorMask = True
        self.mirrorDq = True
        self.direction = MirrorOptions.directionPositiveToNegative


def set_reference_mesh_from_selection():
    selection = cmds.ls(sl=True, long=True)

    if len(selection) != 2:
        log.debug("wrong selection size")
        return

    m = Mirror(selection[1])
    m.set_reference_mesh(selection[0])
