from ngSkinTools2 import signal
from ngSkinTools2.api.python_compatibility import Object
from ngSkinTools2.api.session import Session


class Action(Object):
    name = "Action"
    tooltip = ""
    checkable = False

    def __init__(self, session):
        self.session = session  # type: Session

    def run(self):
        pass

    def enabled(self):
        return True

    def checked(self):
        return False

    def run_if_enabled(self):
        if self.enabled():
            self.run()

    def update_on_signals(self):
        return []

    def as_qt_action(self, parent):
        from ngSkinTools2.ui import actions

        result = actions.define_action(parent, self.name, callback=self.run_if_enabled, tooltip=self.tooltip)
        result.setCheckable(self.checkable)

        def update():
            result.setEnabled(self.enabled())
            if self.checkable:
                result.setChecked(self.checked())

        signal.on(*self.update_on_signals(), qtParent=parent)(update)

        update()
        return result


def qt_action(action_class, session, parent):
    """
    Wrap provided action_class into a QT action
    """
    return action_class(session).as_qt_action(parent)


def do_action_hotkey(action_class):
    from ngSkinTools2.api import session

    action_class(session.session).run_if_enabled()
