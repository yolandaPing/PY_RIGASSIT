"""

## Event handling brainstorm

# Usecase: when selection changes, handlers need to update to this.

Handlers are interested in same data (what's the selected mesh, are layers available, etc). When even is received
by handler, all data to handle the even is there. Data is mostly pre-fetched (assuming that someone will eventually
need it anyway), but for some events lazy-loading might be needed.

# Usecase: event handlers need to respond only when data actually changes (state goes from "layers available"
to "layers unavailable")

Even handlers store that information on heir side. Signal has no way of knowing prevous state of the handler.

# Usecase: event can be fired as a source of multiple other events (layer availability changed: could come from
data transformation or undo/redo event)

Events have their own hierarchy, "layers availability changed" signal stores information about it's previous state
and emits if state changes.




## Events hierarchy complexity

Whenever possible, keep event tree localized in single place for easier refactoring.
"""
from maya import cmds

from ngSkinTools2 import api, cleanup, signal
from ngSkinTools2.api import target_info
from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.python_compatibility import Object
from ngSkinTools2.signal import Signal

log = getLogger("events")


class ConditionalEmit(Object):
    def __init__(self, name, check):
        self.signal = Signal(name)
        self.check = check

    def emitIfChanged(self):
        if self.check():
            self.signal.emit()

    def addHandler(self, handler, **kwargs):
        self.signal.addHandler(handler, **kwargs)

    def removeHandler(self, handler):
        self.signal.removeHandler(handler)


def script_job(*args, **kwargs):
    """
    a proxy on top of cmds.scriptJob for scriptJob creation;
    will register an automatic cleanup procedure to kill the job
    """
    job = cmds.scriptJob(*args, **kwargs)

    def kill():
        # noinspection PyBroadException
        try:
            cmds.scriptJob(kill=job)
        except:
            # should be no issue if we cannot kill the job anymore (e.g., killing from the
            # import traceback; traceback.print_exc()
            pass

    cleanup.registerCleanupHandler(kill)

    return job


class Events(Object):
    """
    root tree of events signaling each other
    """

    def __init__(self, state):
        """

        :type state: ngSkinTools2.api.session.State
        """

        def script_job_signal(name):
            result = Signal(name + "_scriptJob")
            script_job(e=[name, result.emit])
            return result

        self.mayaDeleteAll = script_job_signal('deleteAll')

        self.nodeSelectionChanged = script_job_signal('SelectionChanged')

        self.undoExecuted = script_job_signal('Undo')
        self.redoExecuted = script_job_signal('Redo')
        self.undoRedoExecuted = Signal('undoRedoExecuted')
        self.undoExecuted.addHandler(self.undoRedoExecuted.emit)
        self.redoExecuted.addHandler(self.undoRedoExecuted.emit)

        self.toolChanged = script_job_signal('ToolChanged')
        self.quitApplication = script_job_signal('quitApplication')

        def check_target_changed():
            """
            verify that currently selected mesh is changed, and this means a change in LayersManager.
            """
            selection = cmds.ls(selection=True, objectsOnly=True) or []
            selected_skin_cluster = None if not selection else target_info.get_related_skin_cluster(selection[-1])

            if selected_skin_cluster is not None:
                layers_available = api.get_layers_enabled(selected_skin_cluster)
            else:
                layers_available = False

            if state.selectedSkinCluster == selected_skin_cluster and state.layersAvailable == layers_available:
                return False

            state.selection = selection
            state.set_skin_cluster(selected_skin_cluster)
            state.skin_cluster_dq_channel_used = (
                False if selected_skin_cluster is None else cmds.getAttr(selected_skin_cluster + ".skinningMethod") == 2
            )
            state.layersAvailable = layers_available
            state.all_layers = []  # reset when target has actually changed
            log.info("target changed, layers available: %s", state.layersAvailable)

            return True

        self.targetChanged = event = ConditionalEmit("targetChanged", check_target_changed)

        for source in [self.mayaDeleteAll, self.undoRedoExecuted, self.nodeSelectionChanged]:
            source.addHandler(event.emitIfChanged)

        def check_layers_list_changed():
            state.all_layers = [] if not state.layersAvailable else api.Layers(state.selectedSkinCluster).list()
            return True

        self.layerListChanged = ConditionalEmit("layerListChanged", check_layers_list_changed)
        signal.on(self.targetChanged, self.undoRedoExecuted)(self.layerListChanged.emitIfChanged)

        def check_current_layer_changed():
            # current layer changed if current mesh changed,
            # or id within the mesh changed
            current_layer = None
            if state.selectedSkinCluster is not None and state.layersAvailable:
                current_layer = api.Layers(state.selectedSkinCluster).current_layer()

            if state.selectedSkinCluster == state.currentLayer.selectedSkinCluster and state.currentLayer.layer == current_layer:
                return False

            state.currentLayer.selectedSkinCluster = state.selectedSkinCluster
            state.currentLayer.layer = current_layer
            return True

        self.currentLayerChanged = event = ConditionalEmit("currentLayerChanged", check_current_layer_changed)
        self.targetChanged.addHandler(event.emitIfChanged)
        self.undoRedoExecuted.addHandler(event.emitIfChanged)

        def check_current_paint_target_changed():
            skin_cluster = state.selectedSkinCluster
            new_layer = state.currentLayer.layer
            new_targets = None
            if new_layer is not None:
                new_targets = new_layer.paint_targets

            log.info("[%s] checking current influence changed to %s %r", skin_cluster, new_layer, new_targets)
            if (
                skin_cluster == state.currentInfluence.skinCluster
                and new_layer == state.currentInfluence.layer
                and new_targets == state.currentInfluence.targets
            ):
                return False

            log.info("[%s] current influence changed to %s %r", skin_cluster, new_layer, new_targets)

            state.currentInfluence.skinCluster = skin_cluster
            state.currentInfluence.layer = new_layer
            state.currentInfluence.targets = new_targets
            return True

        self.currentInfluenceChanged = event = ConditionalEmit("currentInfluenceChanged", check_current_paint_target_changed)
        self.currentLayerChanged.addHandler(event.emitIfChanged)

        self.influencesListUpdated = Signal("influencesListUpdated")

        # now get initial state
        self.targetChanged.emitIfChanged()
