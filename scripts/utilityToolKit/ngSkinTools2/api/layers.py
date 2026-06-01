import json

from maya import mel

from ngSkinTools2.api import internals, plugin, target_info
from ngSkinTools2.api.config import Config
from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.python_compatibility import Object, is_string
from ngSkinTools2.api.suspend_updates import suspend_updates
from ngSkinTools2.decorators import undoable

logger = getLogger("api/layers")


class NamedPaintTarget(Object):
    MASK = "mask"
    DUAL_QUATERNION = "dq"


class LayerEffects(Object):
    def __init__(self, layer, state=None):
        self.__layer = layer  # type: Layer
        if state is not None:
            self.__set_state__(state)

    def __set_state__(self, state):
        from ngSkinTools2.api import MirrorOptions

        self.mirror_mask = state.get("mirrorMask", False)
        self.mirror_weights = state.get("mirrorWeights", False)
        self.mirror_dq = state.get("mirrorDq", False)
        self.mirror_direction = state.get("mirrorDirection", MirrorOptions.directionPositiveToNegative)

    def configure_mirror(self, everything=None, mirror_mask=None, mirror_weights=None, mirror_dq=None, mirror_direction=None):
        """
        Enable/disable components for mirror effect:

        >>> layer.effects.configure_mirror(mirror_mask=True)
        >>> layer.effects.configure_mirror(mirror_dq=False)
        >>> # equivalent of setting all flags to False
        >>> layer.effects.configure_mirror(everything=False)

        Mirroring direction must be set explicitly.

        >>> from ngSkinTools2.api import MirrorOptions
        >>> layer.effects.configure_mirror(mirror_mask=True,mirror_direction=MirrorOptions.directionPositiveToNegative)


        :arg bool mirror_mask: should mask be mirrored with this effect?
        :arg bool mirror_weights: should influence weights be mirrored with this effect?
        :arg bool mirror_dq: should dq weights be mirrored with this effect?
        :arg int mirror_direction: mirroring direction. Use `MirrorOptions.directionPositiveToNegative`, `MirrorOptions.directionNegativeToPositive`
          or `MirrorOptions.directionFlip`
        """
        if everything is not None:
            mirror_mask = mirror_dq = mirror_weights = everything

        logger.info(
            "configure mirror: layer %s mask %r weights %r dq %r direction %r",
            self.__layer.name,
            mirror_mask,
            mirror_weights,
            mirror_dq,
            mirror_direction,
        )

        args = {'mirrorLayerDq': mirror_dq, 'mirrorLayerMask': mirror_mask, 'mirrorLayerWeights': mirror_weights, "mirrorDirection": mirror_direction}

        self.__layer.__edit__(configureMirrorEffect=True, **{k: v for k, v in list(args.items()) if v is not None})


def _build_layer_property(name, doc, edit_name=None, default_value=None):
    if edit_name is None:
        edit_name = name

    def getter(self):
        return self.__get_state__(name, default_value=default_value)

    def setter(self, val):
        if isinstance(val, (list, tuple)):
            val = ",".join([str(i) for i in val])
        self.__edit__(**{edit_name: val})

    return property(getter, setter, doc=doc)


class Layer(Object):
    """ """

    name = _build_layer_property('name', "str: Layer name")  # type: str
    enabled = _build_layer_property('enabled', "bool: is layer enabled or disabled")  # type: bool
    opacity = _build_layer_property('opacity', "float: value between 1.0 and 0")  # type: float
    paint_target = _build_layer_property(
        'paintTarget', "str or int: currently active paint target for this layer (either an influence or one of named targets)"
    )  # type: Union(str, int)
    index = _build_layer_property('index', edit_name='layerIndex', doc="int: layer index in parent's child list; set to reorder")  # type: int
    locked_influences = _build_layer_property(
        'lockedInfluences',
        doc="list[int]: list of locked influence indexes",
        default_value=[],
    )  # type: list[int]

    @classmethod
    def load(cls, mesh, layer_id):
        if layer_id < 0:
            raise Exception("invalid layer ID: %s" % layer_id)
        result = Layer(mesh, layer_id)
        result.reload()
        return result

    def __init__(self, mesh, id, state=None):
        self.mesh = mesh
        self.id = id
        self.effects = LayerEffects(self)  # type: LayerEffects
        "configure effects for this layer"

        self.__state = None
        if state is not None:
            self.__set_state(state)

    def __get_state__(self, k, default_value=None):
        return self.__state.get(k, default_value)

    def __query__(self, arg, **kwargs):
        keys = " ".join(["-{k} {v}".format(k=k, v=v) for k, v in list(kwargs.items())])
        return mel.eval("ngst2Layers -id {id} {keys} -q -{arg} {mesh}".format(id=self.id, mesh=self.mesh, keys=keys, arg=arg))

    def __edit__(self, **kwargs):
        self.__set_state(plugin.ngst2Layers(self.mesh, e=True, id=as_layer_id(self), **kwargs))

    def __set_state(self, state):
        if state is None:
            # some plugin functions still return empty result after edits - nevermind those
            return
        if is_string(state):
            try:
                state = json.loads(state)
            except Exception as err:
                raise Exception(str(err) + "; input body was: " + repr(state))

        self.__state = state

        # logger.info("setting layer state %r: %r", self.id, state)

        self.parent_id = state['parentId']
        self.__parent = None
        self.children_ids = state['children']
        self.__children = []

        self.effects.__set_state__(state['effects'])

    def reload(self):
        """
        Refresh layer data from plugin.
        """
        self.__set_state(self.__query__('layerAttributesJson'))

    def __eq__(self, other):
        if not isinstance(other, Layer):
            return False

        return self.mesh == other.mesh and self.id == other.id and self.__state == other.__state

    def __repr__(self):
        return "[Layer #{id} '#{name}']".format(id=self.id, name=self.name)

    @property
    def paint_targets(self):
        """
        list[str or int]: list of paint targets to be set as current for this layer
        """
        return self.__get_state__("paintTargets")

    @paint_targets.setter
    def paint_targets(self, targets):
        self.__edit__(**{"paintTarget": ",".join([str(target) for target in targets])})

    @property
    def parent(self):
        """
        Layer: layer parent, or None, if layer is at root level.
        """
        if self.__parent is None:
            if self.parent_id is not None:
                self.__parent = Layer.load(self.mesh, self.parent_id)

        return self.__parent

    @parent.setter
    def parent(self, parent):
        if parent is None:
            parent = 0

        self.__edit__(parent=as_layer_id(parent))

    @property
    def num_children(self):
        """
        int: a bit more lightweight method to count number of child layers than len(children()), as it does not
        prefetch children data.
        """
        return len(self.children_ids)

    @property
    def children(self):
        """
        list[Layer]: lazily load children if needed, and return as Layer objects
        """
        if len(self.children_ids) != 0:
            if len(self.__children) == 0:
                self.__children = [Layer.load(self.mesh, i) for i in self.children_ids]

        return self.__children

    def set_current(self):
        """

        Set as "default" layer for other operations.


        .. warning::
            Scheduled for removal. API calls should specify target layer explicitly



        """
        plugin.ngst2Layers(self.mesh, currentLayer=self.id)

    def set_weights(self, influence, weights_list, undo_enabled=True):
        """
        Modify weights in the layer.

        :arg int/str influence: either index of an influence, or named paint target (one of :py:class:`NamedPaintTarget` values)
        :arg list[int] weights_list: weights for each vertex (must match number of vertices in skin cluster)
        :arg bool undo_enabled: set to False if you don't need undo, for slight performance boost
        """
        self.__edit__(paintTarget=influence, vertexWeights=internals.float_list_as_string(weights_list), undoEnabled=undo_enabled)

    def get_weights(self, influence):
        """
        get influence (or named paint target) weights for all vertices
        """
        result = self.__query__('vertexWeights', paintTarget=influence)
        if result is None:
            return []
        return [float(i) for i in result]

    def get_used_influences(self):
        """

        :rtype: list[int]
        """
        result = self.__query__('usedInfluences')
        return result or []


def as_layer_id(layer):
    """
    converts given input to layer ID. If input is a Layer object, returns it's ID, otherwise assumes that input is already a layer ID

    Returns:
        int: layer ID
    """
    if isinstance(layer, Layer):
        return layer.id

    return int(layer)


def as_layer_id_list(layers):
    """
    maps a given layer list with `as_layer_id`

    Args:
        layers (list[Any]): objects representing a list of layers

    :rtype: list[int]
    """
    return (as_layer_id(i) for i in layers)


def generate_layer_name(existing_layers, base_name):
    """
    A little utility to generate a unique layer name. For example, if base_name="test", it will try to use values in sequence "test", "test (1)",
    "test (2)" and will return first value that is not a name for any layer in the given layers list.

    :arg existing_layers Layer: whatever
    """
    name = base_name
    currentLayerNames = [i.name for i in existing_layers]
    index = 1
    while name in currentLayerNames:
        index += 1
        name = base_name + " ({0})".format(index)

    return name


class Layers(Object):
    """
    Layers manages skinning layers on provided target (skinCluster or a mesh)
    """

    prune_weights_filter_threshold = internals.make_editable_property('pruneWeightsFilterThreshold')
    influence_limit_per_vertex = internals.make_editable_property('influenceLimitPerVertex')

    def __init__(self, target):
        """

        :param str target:  name of skin cluster node or skinned mesh.
        """
        if not target:
            raise Exception("target must be specified")

        self.__target = target
        self.__cached_data_node = None

    def add(self, name, force_empty=False, parent=None):
        """
        creates new layer with given name and returns its ID; when force_empty flag is set to true,
        layer weights will not be populated from skin cluster.
        """
        layer_id = plugin.ngst2Layers(self.mesh, name=name, add=True, forceEmpty=force_empty)
        result = Layer.load(self.mesh, layer_id)
        result.parent = parent
        return result

    def delete(self, layer):
        plugin.ngst2Layers(self.mesh, removeLayer=True, id=as_layer_id(layer))

    def list(self):
        """

        returns all layers as Layer objects.
        :rtype list[Layer]
        """
        data = json.loads(plugin.ngst2Layers(self.mesh, q=True, listLayers=True))
        return [Layer(self.mesh, id=l['id'], state=l) for l in data]

    @undoable
    def clear(self):
        """
        delete all layers
        """
        with suspend_updates(self.data_node):
            for i in self.list():
                if i.parent_id is None:
                    self.delete(i)

    def list_influences(self):
        """
        Wraps :py:meth:`target_info.list_influences`
        """
        return target_info.list_influences(self.mesh)

    def current_layer(self):
        """
        get current layer that was previously marked as current with :py:meth:`Layer.set_current`.

        .. warning::
            Scheduled for removal. API calls should specify target layer explicitly

        """
        layer_id = plugin.ngst2Layers(self.mesh, q=True, currentLayer=True)
        if layer_id < 0:
            return None
        return Layer.load(self.mesh, layer_id)

    def __edit__(self, **kwargs):
        plugin.ngst2Layers(self.mesh, e=True, **kwargs)

    def __query__(self, **kwargs):
        return plugin.ngst2Layers(self.mesh, q=True, **kwargs)

    def set_influences_mirror_mapping(self, influencesMapping):
        plugin.ngst2Layers(self.mesh, configureMirrorMapping=True, influencesMapping=internals.influences_map_to_list(influencesMapping))

    @property
    def mesh(self):
        return self.__target

    def is_enabled(self):
        """
        returns true if skinning layers are enabled for the given mesh
        :return:
        """
        return get_layers_enabled(self.mesh)

    @property
    def data_node(self):
        if not self.__cached_data_node:
            self.__cached_data_node = target_info.get_related_data_node(self.mesh)
        return self.__cached_data_node

    @property
    def config(self):
        return Config(self.data_node)


def init_layers(target):
    """Attach ngSkinTools data node to given target. Does nothing if layers are already attached.


    :arg str target: skin cluster or mesh node to attach layers to
    :rtype: Layers
    """
    plugin.ngst2Layers(target, layerDataAttach=True)

    return Layers(target)


def get_layers_enabled(selection):
    """
    return true if layers are enabled on this selection
    """
    return plugin.ngst2Layers(selection, q=True, lda=True)
