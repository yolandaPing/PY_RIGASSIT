"""
UI session is running as long as any of the ngSkinTools UI windows are open.

"""
import functools

from ngSkinTools2 import cleanup, signal
from ngSkinTools2.api import Layers, PaintTool, events, mirror, plugin
from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.python_compatibility import Object
from ngSkinTools2.licenseClient import LicenseClient
from ngSkinTools2.observableValue import ObservableValue
from ngSkinTools2.signal import SignalHub

log = getLogger("events")


class CurrentLayerState(Object):
    def __init__(self):
        self.selectedSkinCluster = None

        # will be None, when no current layer is available
        self.layer = None  # type: ngSkinTools2.api.Layer


class CurrentPaintTargetState(Object):
    def __init__(self):
        self.skinCluster = None
        self.layerId = None
        self.targets = None


class State(Object):
    def __init__(self):
        self.layersAvailable = False
        self.selection = []
        self.selectedSkinCluster = None
        self.skin_cluster_dq_channel_used = False

        self.all_layers = []  # type: List[ngSkinTools2.api.Layer]
        self.currentLayer = CurrentLayerState()
        self.currentInfluence = CurrentPaintTargetState()

    def set_skin_cluster(self, cluster):
        self.selectedSkinCluster = cluster
        self.layers = None if cluster is None else Layers(cluster)

    def mirror(self):
        # type: () -> mirror.Mirror
        return mirror.Mirror(self.selectedSkinCluster)


class Context(Object):
    def __init__(self):
        self.selected_layers = ObservableValue()  # [] layerId


class Session(Object):
    def __init__(self):
        # reference objects that are keeping the session
        self.references = set()
        self.state = None  # type: State
        self.events = None  # type: events.Events
        self.signal_hub = None  # type: SignalHub
        self.context = None  # type: Context
        self.licenseClient = LicenseClient()

        self.referenceId = 0

    def active(self):
        return len(self.references) > 0

    def start(self):
        log.info("STARTING SESSION")
        plugin.load_plugin()

        self.paint_tool = PaintTool()

        self.licenseClient.load_deferred()

        self.state = State()
        self.events = events.Events(self.state)
        self.signal_hub = SignalHub()
        self.signal_hub.activate()
        cleanup.registerCleanupHandler(self.signal_hub.deactivate)
        self.context = Context()

        @signal.on(self.events.targetChanged)
        def on_target_change():
            log.info("target changed: clearing target context")
            self.context.selected_layers.set([])

        self.events.nodeSelectionChanged.emit()

    def end(self):
        log.info("ENDING SESSION")
        cleanup.cleanup()
        self.state = None
        self.events = None
        self.context = None
        self.signal_hub = None
        pass

    def addReference(self):
        """
        returns unique ID for this added reference; this value needs to be passed into removeReference();
        this ensures that reference holder does not remove other references rather than his own.
        :return:
        """
        self.referenceId += 1
        if not self.active():
            self.start()

        self.references.add(self.referenceId)
        return self.referenceId

    def removeReference(self, referenceId):
        try:
            self.references.remove(referenceId)
        except KeyError:
            pass

        if not self.active():
            self.end()

    def addQtWidgetReference(self, widget):
        ref = self.addReference()

        widget.destroyed.connect(lambda: self.removeReference(ref))

    def reference(self):
        class Context(Object):
            def __init__(self, session):
                """
                :type session: Session
                :type refObj: object
                """

                self.session = session

            def __enter__(self):
                self.ref = self.session.addReference()

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.session.removeReference(self.ref)

        return Context(self)


session = Session()


def withSession(func):
    """
    decorator makes sure that single session is running throughout function's lifetime
    """

    @functools.wraps(func)
    def result(*args, **kwargs):
        ref = session.addReference()
        try:
            return func(*args, **kwargs)
        finally:
            session.removeReference(ref)

    return result
