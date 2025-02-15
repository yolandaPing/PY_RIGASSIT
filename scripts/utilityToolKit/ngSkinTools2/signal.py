"""
Signal is the previous method of emiting/subscribing to signals.
* Subscribers are dependant on emiter's instances
* There's only one global queue

New system is changing to allow decoupling subscribers and receivers, and allowing the code to work even when there's no need to process signals
* Subscribers need to be able to subsribe prior to instantiation of emitters


"""
from functools import partial

from ngSkinTools2 import cleanup
from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.python_compatibility import Object

log = getLogger("signal")


class SignalQueue(Object):
    def __init__(self):
        self.max_length = 100
        self.queue = []

    def emit(self, handler):
        if len(self.queue) > self.max_length:
            log.error("queue max length reached: emitting too many events?")
            raise Exception("queue max length reached: emitting too many events?")

        should_start = len(self.queue) == 0

        self.queue.append(handler)
        if should_start:
            self.process()

    def process(self):
        current_handler = 0
        queue = self.queue

        while current_handler < len(queue):
            # noinspection PyBroadException
            try:
                queue[current_handler]()
            except Exception:
                import ngSkinTools2

                if ngSkinTools2.DEBUG_MODE:
                    import sys
                    import traceback

                    traceback.print_exc(file=sys.__stderr__)

            current_handler += 1

        if len(self.queue) > 50:
            log.info("handler queue finished with %d items", len(self.queue))
        self.queue = []


# noinspection PyBroadException
class Signal(Object):
    """
    Signal class collects observers, interested in some particular event,and handles
    signaling them all when some event occurs. Both handling and signaling happens outside
    of signal's own code


    Handlers are processed breath first, in a queue based system.
    1. root signal fires, adds all it's handlers to the queue;
    2. queue starts being processed
    3. handlers fire more signals, in turn adding more handlers to the end of the queue.
    """

    all = []

    queue = SignalQueue()

    def __init__(self, name):
        if name is None:
            raise Exception("need name for debug purposes later")
        self.name = name
        self.handlers = []
        self.executing = False
        self.enabled = True

        self.reset()
        Signal.all.append(self)
        cleanup.registerCleanupHandler(self.reset)

    def reset(self):
        self.handlers = []
        self.executing = False

    def emit_deferred(self, *args):
        import maya.utils as mu

        mu.executeDeferred(self.emit, *args)

    def emit(self, *args):
        """
        emit mostly just adds handlers to the processing queue,
        but if nobody is processing handlers at the emit time,
        it is started here as well.
        """
        if not self.enabled:
            return

        # log.info("emit: %s", self.name)
        if self.executing:
            raise Exception('Nested emit on %s detected' % self.name)

        for i in self.handlers[:]:
            Signal.queue.emit(partial(i, *args))

    def addHandler(self, handler, qtParent=None):
        if hasattr(handler, 'emit'):
            handler = handler.emit

        self.handlers.append(handler)

        def remove():
            return self.removeHandler(handler)

        if qtParent is not None:
            qtParent.destroyed.connect(remove)

        return remove

    def removeHandler(self, handler):
        try:
            self.handlers.remove(handler)
        except ValueError:
            # not found in list? no biggie.
            pass


def on(*signals, **kwargs):
    """
    decorator for function: list signals that should fire for this function.

        @signal.on(signalReference)
        def something():
            ...
    """

    def decorator(fn):
        for i in signals:
            i.addHandler(fn, **kwargs)
        return fn

    return decorator


# --------------------------------------
# rework:
#  * decoupled emitters and subscribers
#  * subscribers are resolved only at the time of event
#  * can emit events even when there's no active sessions (acts as no-op)


class Event(Object):
    def __init__(self, name):
        self.name = name

    def __or__(self, other):
        return EventList() | self | other

    def __iter__(self):
        yield self

    def emit(self, *args, **kwargs):
        for hub in SignalHub.active_hubs:
            hub.emit(self, *args, **kwargs)


class EventList(Object):
    """
    helper to build and iterate over a list of "or"-ed events
    """

    def __init__(self):
        self.items = []

    def __or__(self, other):
        self.items.append(other)
        return self

    def __iter__(self):
        return iter(self.items)


class SignalHub(Object):
    active_hubs = set()

    def __init__(self):
        self.handlers = {}
        self.queue = SignalQueue()

    def activate(self):
        self.active_hubs.add(self)

    def deactivate(self):
        self.active_hubs.remove(self)

    def subscribe(self, event, handler):
        """
        :param Event event: event to subscribe to
        :param Callable handler: callback which will be called when event is emitted
        :return: unsubscribe function: call it to terminate this subscription
        """
        self.handlers.setdefault(event, []).append(handler)

        def unsubscribe():
            try:
                self.handlers[event].remove(handler)
            except ValueError:
                # not found in list? no biggie.
                pass

        return unsubscribe

    def emit(self, event):
        if not event in self.handlers:
            return

        for i in self.handlers[event]:
            self.queue.emit(i)

    def on(self, events, scope=None):
        """
        decorator for function: bind function to signals

        @hub.on(event1 | event2, scope=qt_object)
        def something():
            ...
        """

        def decorator(fn):
            unsubscribe_handlers = []
            try:
                unsubscribe_handlers.append(scope.destroyed.connect)
            except:
                pass

            for e in events:
                unsub = self.subscribe(e, fn)
                if unsubscribe_handlers:
                    for i in unsubscribe_handlers:
                        i(unsub)

            return fn

        return decorator
