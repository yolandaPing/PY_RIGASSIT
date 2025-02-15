from ngSkinTools2.api import Layer, Layers
from ngSkinTools2.api import layers as api_layers
from ngSkinTools2.api import plugin
from ngSkinTools2.api.layers import generate_layer_name
from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.paint import PaintModeSettings
from ngSkinTools2.api.target_info import list_influences
from ngSkinTools2.decorators import undoable

log = getLogger("tools")


def assign_from_closest_joint(target, layer, influences=None):
    # type: (str, Layer, List[int]) -> None
    """
    For each selected vertex, picks a nearest joint and assigns 1.0 weight to that joint.

    Operates on the currently active component selection, or whole mesh, depending on selection.

    :param str target: skinned mesh or skin cluster node name;
    :param Layer layer: int or :py:class:`Layer` object to apply weights to;
    :param List[int] influences: selects only from provided subset of skinCluster influences.
    """

    if influences is None:
        influences = [i.logicalIndex for i in list_influences(target)]

    if len(influences) == 0:
        # nothing to do?
        return

    plugin.ngst2tools(
        tool="closestJoint",
        target=target,
        layer=api_layers.as_layer_id(layer),
        influences=[int(i) for i in influences],
    )


def unify_weights(target, layer, overall_effect, single_cluster_mode):
    """
    For all selected vertices, calculates average weights and assigns that value to each vertice. The effect is that all vertices end up having same weights.

    Operates on the currently active component selection, or whole mesh, depending on selection.

    :param str target: skinned mesh or skin cluster node name;
    :param Layer layer: int or :py:class:`Layer` object to apply weights to;
    :param float overall_effect: value between `0.0` and `1.0`, intensity of the operation. When applying newly calculated weights to the skin cluster,
       the formula is `weights = lerp(originalWeights, newWeights, overallEffect)`.
    :param bool single_cluster_mode: if `true`, all weights will receive the same average. If `false`, each connected mesh shell will be computed independently.
    """
    plugin.ngst2tools(
        tool="unifyWeights",
        target=target,
        layer=api_layers.as_layer_id(layer),
        overallEffect=overall_effect,
        singleClusterMode=single_cluster_mode,
    )


def flood_weights(target, influence=None, influences=None, settings=None):
    """
    Apply paint tool in the layer with the given settings.

    :param target: layer or mesh to set the weights in.
    :param influence: target influence: either an int for the logical index of the influence, or one of :py:class:`NamedPaintTarget` constants. Can be skipped if tool mode is Smooth or Sharpen.
    :param influences: if specified, overrides "influence" and allows passing multiple influences instead. Only supported by flood and sharpen at the moment.
    :type settings: PaintModeSettings
    """

    if settings is None:
        settings = PaintModeSettings()  # just use default settings

    args = {
        'tool': "floodWeights",
        'influences': influences if influences is not None else [influence],
        'mode': settings.mode,
        'intensity': settings.intensity,
        'iterations': int(settings.iterations),
        'influencesLimit': int(settings.influences_limit),
        'mirror': bool(settings.mirror),
        'distributeRemovedWeight': settings.distribute_to_other_influences,
        'limitToComponentSelection': settings.limit_to_component_selection,
        'useVolumeNeighbours': settings.use_volume_neighbours,
        'fixedInfluencesPerVertex': bool(settings.fixed_influences_per_vertex),
    }
    layer = None if not isinstance(target, Layer) else target  # type: Layer
    if layer:
        args['layer'] = api_layers.as_layer_id(layer)

    args['target'] = target if layer is None else layer.mesh

    plugin.ngst2tools(**args)


@undoable
def merge_layers(layers):
    """
    :type layers: list[Layer]
    :rtype: Layer
    """
    if len(layers) > 1:
        # verify that all layers are from the same parent
        for i, j in zip(layers[:-1], layers[1:]):
            if i.mesh != j.mesh:
                raise Exception("layers are not from the same mesh")

    result = plugin.ngst2tools(
        tool="mergeLayers",
        target=layers[0].mesh,
        layers=[api_layers.as_layer_id(i) for i in layers],
    )

    target_layer = Layer.load(layers[0].mesh, result['layerId'])
    target_layer.set_current()

    return target_layer


@undoable
def duplicate_layer(layer):
    """

    :type layer: Layer
    :rtype: Layer
    """

    result = plugin.ngst2tools(
        tool="duplicateLayer",
        target=layer.mesh,
        sourceLayer=layer.id,
    )

    target_layer = Layer.load(layer.mesh, result['layerId'])

    import re

    base_name = re.sub(r"( \(copy\))?( \(\d+\))*", "", layer.name)
    other_layers = [l for l in Layers(target_layer.mesh).list() if l.id != target_layer.id]
    target_layer.name = generate_layer_name(other_layers, base_name + " (copy)")

    target_layer.set_current()

    return target_layer


@undoable
def fill_transparency(layer):
    """

    :type layer: Layer
    """

    plugin.ngst2tools(
        tool="fillLayerTransparency",
        target=layer.mesh,
        layer=layer.id,
    )


def copy_component_weights(layer):
    """
    :type layer: Layer
    """

    plugin.ngst2tools(
        tool="copyComponentWeights",
        target=layer.mesh,
        layer=layer.id,
    )


def paste_average_component_weights(layer):
    """
    :type layer: Layer
    """

    plugin.ngst2tools(
        tool="pasteAverageComponentWeights",
        target=layer.mesh,
        layer=layer.id,
    )


def refresh_screen(target):
    plugin.ngst2tools(
        tool="refreshScreen",
        target=target,
    )
