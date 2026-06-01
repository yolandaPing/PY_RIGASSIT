import itertools

from ngSkinTools2.api.python_compatibility import Object
from ngSkinTools2.decorators import undoable

from . import plugin
from .influenceMapping import InfluenceMapping, InfluenceMappingConfig
from .layers import init_layers, target_info
from .mirror import Mirror
from .suspend_updates import suspend_updates


class VertexTransferMode(Object):
    """
    Constants for vertex_transfer_mode argument
    """

    closestPoint = 'closestPoint'  #: When vertices from two surface are matched, each destination mesh vertex finds a closest point on source mesh, and weights are calculated based on the triangle weights of that closest point.
    uvSpace = 'uvSpace'  #: Similar to closestPoint strategy, but matching is done in UV space instead of XYZ space.
    vertexId = 'vertexId'  #: Vertices are matched by ID. Not usable for mirroring; this is used for transfer/import cases where meshes are known to be identical


class LayersTransfer(Object):
    def __init__(self):
        self.source = None
        self.target = None
        self.source_file = None
        self.vertex_transfer_mode = VertexTransferMode.closestPoint
        self.influences_mapping = InfluenceMapping()
        self.influences_mapping.config = InfluenceMappingConfig.transfer_defaults()
        self.keep_existing_layers = True
        self.customize_callback = None

    def load_source_from_file(self, file, format):
        from .import_export import FileFormatWrapper

        with FileFormatWrapper(file, format=format, read_mode=True) as f:
            data = plugin.ngst2tools(
                tool="importJsonFile",
                file=f.plain_file,
            )

        self.source = "-reference-mesh-"
        self.source_file = file
        influences = target_info.unserialize_influences_from_json_data(data['influences'])

        self.influences_mapping.influences = influences

    def calc_influences_mapping_as_flat_list(self):
        mapping_pairs = list(self.influences_mapping.asIntIntMapping(self.influences_mapping.calculate()).items())
        if len(mapping_pairs) == 0:
            raise Exception("no mapping between source and destination influences")
        # convert dict to flat array
        return list(itertools.chain.from_iterable(mapping_pairs))

    def execute(self):
        # sanity check: destination must be skinnable target
        if target_info.get_related_skin_cluster(self.target) is None:
            return False

        if not self.influences_mapping.influences:
            if target_info.get_related_skin_cluster(self.source) is None:
                return False
            self.influences_mapping.influences = target_info.list_influences(self.source)
        self.influences_mapping.destinationInfluences = target_info.list_influences(self.target)

        if self.customize_callback is None:
            self.complete_execution()
        else:
            self.customize_callback(self)

    @undoable
    def complete_execution(self):
        l = init_layers(self.target)
        Mirror(self.target).recalculate_influences_mapping()

        with suspend_updates(self.target):
            if not self.keep_existing_layers:
                l.clear()

            plugin.ngst2tools(
                tool="transfer",
                source=self.source,
                target=self.target,
                vertexTransferMode=self.vertex_transfer_mode,
                influencesMapping=self.calc_influences_mapping_as_flat_list(),
            )


def transfer_layers(
    source, destination, vertex_transfer_mode=VertexTransferMode.closestPoint, influences_mapping_config=InfluenceMappingConfig.transfer_defaults()
):
    """
    Transfer skinning layers from source to destination mesh.

    :param str source: source mesh or skin cluster node name
    :param str destination: destination mesh or skin cluster node name
    :param str vertex_transfer_mode: describes how source mesh vertices are mapped to destination vertices. Defaults to `closestPoint`
    :param InfluenceMappingConfig influences_mapping_config: configuration for InfluenceMapping; supply this, or `influences_mapping` instance; default settings for transfer are used if this is not supplied.
    :param InfluenceMapping influences_mapping: mapper instance to use for matching influences; if this is provided, `influences_mapping_config` is ignored.
    :return:
    """

    t = LayersTransfer()
    t.source = source
    t.target = destination
    t.vertex_transfer_mode = vertex_transfer_mode
    t.influences_mapping.config = influences_mapping_config

    t.execute()
