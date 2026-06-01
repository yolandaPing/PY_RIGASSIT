import copy
import json

from maya import cmds

from ngSkinTools2.api import internals, plugin
from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.pyside import QtCore
from ngSkinTools2.api.python_compatibility import Object

log = getLogger("api/paint")


# noinspection PyClassHasNoInit
class BrushProjectionMode(Object):
    surface = 0
    screen = 1


# noinspection PyClassHasNoInit
class PaintMode(Object):
    """
    Constants for paint mode
    """

    replace = 1
    add = 2
    scale = 3
    smooth = 4
    sharpen = 5

    @classmethod
    def all(cls):
        return cls.replace, cls.smooth, cls.add, cls.scale, cls.sharpen


# noinspection PyClassHasNoInit
class TabletMode(Object):
    unused = 0
    multiplyIntensity = 1
    multiplyOpacity = 2
    multiplyRadius = 3


# noinspection PyClassHasNoInit
class WeightsDisplayMode(Object):
    allInfluences = 0
    currentInfluence = 1
    currentInfluenceColored = 2


# noinspection PyClassHasNoInit
class MaskDisplayMode(Object):
    default_ = 0
    color_ramp = 1


# noinspection PyClassHasNoInit
class BrushShape(Object):
    solid = 0  # 1.0 for whole brush size
    smooth = 1  # feathered edges
    gaus = 2  # very smooth from center


# noinspection PyClassHasNoInit
class PaintModeSettings(Object):
    """
    Brush/Flood settings
    """

    __property_map = {
        "brush_projection_mode": 'brushProjectionMode',
        "mode": 'paintMode',
        "brush_radius": 'brushRadius',
        "brush_shape": 'brushShape',
        "intensity": 'brushIntensity',
        "iterations": 'brushIterations',
        "tablet_mode": 'tabletMode',
        "mirror": 'interactiveMirror',
        "influences_limit": 'influencesLimit',
        "fixed_influences_per_vertex": 'fixedInfluencesPerVertex',
        "limit_to_component_selection": 'limitToComponentSelection',
        "use_volume_neighbours": 'useVolumeNeighbours',
        "distribute_to_other_influences": 'redistributeRemovedWeight',
        "sample_joint_on_stroke_start": 'sampleJointOnStrokeStart',
    }

    mode = PaintMode.replace  #: Tool mode. One of the :py:class:`PaintMode` values.

    # varies by mode
    intensity = 1.0  #: tool intensity;
    iterations = 1
    """
     iterations; repeats the same smooth operation given number of times -
     using this parameter instead of calling `flood_weights` multiple times.
    """

    brush_shape = BrushShape.solid

    # varies by screen mode
    # can be modified inside the plugin
    brush_radius = 10

    mirror = False  #: is automatic mirroring on or off
    distribute_to_other_influences = False
    influences_limit = 0  #: influences limit per vertex to ensure while smoothing
    brush_projection_mode = BrushProjectionMode.surface  #: brush projection mode, one of :py:class:`BrushProjectionMode` values.
    sample_joint_on_stroke_start = False
    tablet_mode = TabletMode.unused
    use_volume_neighbours = False
    limit_to_component_selection = False
    fixed_influences_per_vertex = False
    """
    only applicable for smooth mode; when set to True, smoothing will not add additional influences to a vertex.
    """

    def apply_primary_brush(self):
        self.__apply(1)

    def apply_alternative_brush(self):
        self.__apply(2)

    def apply_inverted_brush(self):
        self.__apply(3)

    def __apply(self, settings_type):
        """
        apply settings to C++ plugin side.
        :param settings_type:
        """

        kwargs = {v: getattr(self, k) for k, v in self.__property_map.items()}
        kwargs['paintType'] = settings_type
        plugin.ngst2PaintSettingsCmd(**kwargs)

    def from_dict(self, values):
        # type: (dict) -> PaintModeSettings

        for k in self.__property_map.keys():
            if k in values:
                setattr(self, k, values[k])

        return self

    def to_dict(self):
        # type: () -> dict
        return {k: getattr(self, k) for k in self.__property_map.keys()}


def __make_common_property__(property_name):
    def setval(self, val):
        setattr(self.primary_settings, property_name, val)
        self.apply_settings()

    return property(lambda self: getattr(self.primary_settings, property_name), setval)


def __make_mode_property__(property_name):
    return __make_dimensional_property__(lambda self: self.mode, lambda self: self.mode_settings[self.mode], property_name)


def __make_projection_property__(property_name):
    return __make_dimensional_property__(
        lambda self: self.brush_projection_mode, lambda self: self.projection_settings[self.brush_projection_mode], property_name
    )


def __make_dimensional_property__(name, get_dimension_func, property_name):
    def setval(self, val):
        log.debug("setting dimensional property %s/%s: %r", name(self), property_name, val)
        dimension = get_dimension_func(self)
        dimension[property_name] = val
        setattr(self.primary_settings, property_name, val)
        self.apply_settings()

    def getval(self):
        return get_dimension_func(self).get(property_name, getattr(self.primary_settings, property_name))

    return property(getval, setval)


class PaintSettingsModel(Object):
    """
    Paint settings model manages paint settings persistence and storage on CPP side;
    in CPP side three states need to be maintained:
    * primary settings
    * alternative settings (used when shift is pressed)
    * inverse settings (used when ctrl is pressed)
    """

    projection_settings = None  # type: dict
    mode_settings = None  # type: dict
    primary_settings = None  # type: PaintModeSettings

    paint_mode = __make_common_property__("mode")
    mode = __make_common_property__("mode")

    intensity = __make_mode_property__("intensity")
    iterations = __make_mode_property__("iterations")
    brush_shape = __make_mode_property__("brush_shape")

    brush_radius = __make_projection_property__("brush_radius")

    mirror = __make_common_property__("mirror")
    distribute_to_other_influences = __make_common_property__("distribute_to_other_influences")
    influences_limit = __make_common_property__("influences_limit")
    brush_projection_mode = __make_common_property__("brush_projection_mode")
    sample_joint_on_stroke_start = __make_common_property__("sample_joint_on_stroke_start")
    tablet_mode = __make_common_property__("tablet_mode")
    use_volume_neighbours = __make_common_property__("use_volume_neighbours")
    limit_to_component_selection = __make_common_property__("limit_to_component_selection")
    fixed_influences_per_vertex = __make_common_property__("fixed_influences_per_vertex")

    def __init__(self):
        self.projection_settings = None
        self.mode_settings = None
        self.primary_settings = None
        self.storage_func_save = lambda data: None
        self.storage_func_load = lambda: ""
        self.apply_settings_func = self.apply_plugin_settings

        self.setup_maya_option_var_persistence()

    def __save_settings(self):
        data = {
            "common": self.primary_settings.to_dict(),
            "mode_settings": self.mode_settings,
            "projection_settings": self.projection_settings,
        }
        serialized_data = json.dumps(data)
        log.info("saving brush settings: %s", serialized_data)
        self.storage_func_save(serialized_data)

    def load_settings(self):
        def to_int_keys(d):
            return {int(k): v for k, v in d.items()}

        try:
            saved_data = self.storage_func_load()
            log.info("loading brush settings from %s", saved_data)
            if saved_data is None:
                self.initialize_defaults()
                return
            data = json.loads(saved_data)
            self.primary_settings = PaintModeSettings().from_dict(data['common'])
            self.mode_settings = to_int_keys(data['mode_settings'])
            self.projection_settings = to_int_keys(data['projection_settings'])
            self.apply_settings()
        except Exception as err:
            log.info(err)

    def setup_maya_option_var_persistence(self):
        from ngSkinTools2.ui import options

        val = options.PersistentValue(options.VAR_OPTION_PREFIX + "_brush_settings")

        self.storage_func_load = val.get
        self.storage_func_save = val.set
        self.load_settings()

    def __bake_settings(self, mode):
        result = copy.copy(self.primary_settings)
        result.mode = mode

        for k, v in self.mode_settings[mode].items():
            setattr(result, k, v)

        for k, v in self.projection_settings[self.brush_projection_mode].items():
            setattr(result, k, v)

        return result

    def apply_settings(self):
        # TODO: very inelegant here; we should not have to re-bake and re-set all settings at once
        # if we're switching any of dimensional settings, we need to reflect this
        self.primary_settings = self.__bake_settings(self.mode)
        primary = self.primary_settings

        inverted_modes = {
            PaintMode.replace: PaintMode.replace,
            PaintMode.add: PaintMode.scale,
            PaintMode.scale: PaintMode.add,
            PaintMode.smooth: PaintMode.sharpen,
            PaintMode.sharpen: PaintMode.smooth,
        }

        alternative = self.__bake_settings(PaintMode.smooth)
        inverted = self.__bake_settings(inverted_modes.get(self.mode, PaintMode.replace))

        if self.mode == PaintMode.replace:
            inverted.intensity = 0

        log.debug("normal mode intensity: %r", primary.intensity)
        self.apply_settings_func(primary, alternative, inverted)
        self.__save_settings()

    def initialize_defaults(self):
        self.primary_settings = PaintModeSettings()
        self.primary_settings.mode = PaintMode.replace
        self.primary_settings.brush_radius = 2
        self.primary_settings.intensity = 1.0
        self.primary_settings.tablet_mode = TabletMode.unused
        self.primary_settings.brush_shape = BrushShape.solid
        self.primary_settings.distribute_to_other_influences = False
        self.mode_settings = {
            PaintMode.replace: {
                "intensity": 1.0,
                "brush_shape": BrushShape.solid,
            },
            PaintMode.add: {
                "intensity": 0.1,
                "brush_shape": BrushShape.solid,
            },
            PaintMode.scale: {
                "intensity": 0.95,
                "brush_shape": BrushShape.solid,
            },
            PaintMode.smooth: {
                "intensity": 0.2,
                "iterations": 5,
                "brush_shape": BrushShape.smooth,
            },
            PaintMode.sharpen: {
                "intensity": 0.2,
                "iterations": 5,
                "brush_shape": BrushShape.smooth,
            },
        }
        self.projection_settings = {
            BrushProjectionMode.surface: {
                "brush_radius": 2,
            },
            BrushProjectionMode.screen: {
                "brush_radius": 100,
            },
        }
        self.apply_settings()

    # noinspection PyMethodMayBeStatic
    def apply_plugin_settings(self, primary, alternative, inverted):
        # type: (PaintModeSettings, PaintModeSettings, PaintModeSettings) -> None
        primary.apply_primary_brush()
        alternative.apply_alternative_brush()
        inverted.apply_inverted_brush()


class DisplaySettings(Object):
    def __init__(self):
        from ngSkinTools2.ui import options

        self.persistence = options.PersistentDict("paint_display_settings")

    weights_display_mode = internals.make_editable_property('weightsDisplayMode')
    mask_display_mode = internals.make_editable_property('maskDisplayMode')
    layer_effects_display = internals.make_editable_property('layerEffectsDisplay')
    display_masked = internals.make_editable_property('displayMasked')
    show_selected_verts_only = internals.make_editable_property('showSelectedVertsOnly')
    wireframe_color = internals.make_editable_property('wireframeColor')
    wireframe_color_single_influence = internals.make_editable_property('wireframeColorSingleInfluence')

    # noinspection PyMethodMayBeStatic
    def __edit__(self, **kwargs):
        plugin.ngst2PaintSettingsCmd(**kwargs)
        for k, v in kwargs.items():
            self.persistence[k] = v

    @property
    def display_node_visible(self):
        """
        gets/sets visibility of temporary node that displays weight colors. when set to false, displays original mesh instead.
        """
        return plugin.ngst2PaintSettingsCmd(q=True, displayNodeVisible=True)

    @display_node_visible.setter
    def display_node_visible(self, value):
        plugin.ngst2PaintSettingsCmd(displayNodeVisible=value)

    # noinspection PyMethodMayBeStatic
    def __query__(self, **kwargs):
        for k in kwargs:
            persisted = self.persistence[k]
            if persisted is not None:
                return persisted
        return plugin.ngst2PaintSettingsCmd(q=True, **kwargs)


class PaintTool(PaintSettingsModel):
    __paint_context = None

    def __init__(self):
        PaintSettingsModel.__init__(self)
        self.display_settings = DisplaySettings()

    def update_plugin_brush_radius(self):
        new_value = plugin.ngst2PaintSettingsCmd(q=True, brushRadius=True)
        if self.brush_radius != new_value:
            self.brush_radius = new_value

    @classmethod
    def start(cls):
        if cls.__paint_context is None:
            cls.__paint_context = plugin.ngst2PaintContext()
        cmds.setToolTo(cls.__paint_context)

    def flood(self, layer, influence=None, influences=None):
        from ngSkinTools2.api import tools

        tools.flood_weights(target=layer, influence=influence, influences=influences, settings=self.primary_settings)

    @classmethod
    def is_painting(cls):
        return cmds.contextInfo(cmds.currentCtx(), c=True) == 'ngst2PaintContext'


class Popups(Object):
    def __init__(self):
        self.windows = []

    def add(self, w):
        self.windows.append(w)
        w.destroyed.connect(lambda *args: self.remove(w))

    def remove(self, w):
        self.windows = [i for i in self.windows if i != w]

    def close_all(self):
        for i in self.windows:
            i.close()
        self.windows = []


popups = Popups()


class TabletEventFilter(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.pressure = 1.0

    def eventFilter(self, obj, event):
        if event.type() in [QtCore.QEvent.TabletPress, QtCore.QEvent.TabletMove]:
            self.pressure = event.pressure()
            # log.info("tablet pressure: %r", self.pressure)

        return QtCore.QObject.eventFilter(self, obj, event)

    def install(self):
        from ngSkinTools2.ui import qt

        log.info("installing event filter...")
        qt.mainWindow.installEventFilter(self)
        log.info("...done")

    def uninstall(self):
        from ngSkinTools2.ui import qt

        qt.mainWindow.removeEventFilter(self)
        log.info("event filter uninstalled")


tabletEventFilter = TabletEventFilter()
