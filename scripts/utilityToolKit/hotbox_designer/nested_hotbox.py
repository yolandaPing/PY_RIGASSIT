# -*- coding: utf-8 -*-

# .FileName:nested_hotbox.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/3/24 21:19
# .Finish time:
try:
    from ui_framework.core.qtCompat import *

except ImportError:
    from CommonUse.qtCompat import *

from hotbox_designer.reader import HotboxReader
from hotbox_designer.geometry import segment_cross_rect, distance
from hotbox_designer.qtutils import get_cursor

class NestedHotboxReader(HotboxReader):
    submenuOpened = QtCore.Signal(object, object)
    submenuClosed = QtCore.Signal()

    def __init__(self, hotbox_data, parent=None, parent_shape=None, depth=0):
        super(NestedHotboxReader, self).__init__(hotbox_data, parent)
        self.parent_shape = parent_shape
        self.depth = depth
        self.active_submenu = None
        self.active_submenu_shape = None

        for shape in self.shapes:
            shape.has_submenu = shape.submenu_data is not None

    def mouseMoveEvent(self, event):
        cursor = get_cursor(self)
    
        if self.aiming:
            set_crossed_shapes_hovered_nested(self.center, cursor, self.interactive_shapes, cursor)
        else:
            set_shapes_hovered_nested(self.interactive_shapes, cursor, self.clicked)

        self._check_submenu_activation(cursor)

        self.repaint()

    def _check_submenu_activation(self, cursor):
        hovered_shape = None
        for shape in self.interactive_shapes:
            if shape.hovered and shape.has_submenu:
                hovered_shape = shape
                break

        if hovered_shape != self.active_submenu_shape:
            self._close_active_submenu()
            if hovered_shape:
                self._open_submenu(hovered_shape)

    def _open_submenu(self, shape):
        submenu = NestedHotboxReader(
            shape.submenu_data,
            parent=None,
            parent_shape=shape,
            depth=self.depth + 1
        )

        submenu.setWindowFlags(
            QtCore.Qt.Tool |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint
        )

        submenu.setMouseTracking(True)
        submenu.adjustSize()
        submenu.resize(submenu.sizeHint())

        pos = self.mapToGlobal(QtCore.QPoint(shape.rect.right(), shape.rect.top()))
        try:
            screen = QtWidgets.QApplication.screenAt(pos)
        except:
            screen = QtWidgets.QApplication.primaryScreen()
        # if not screen:
        #     screen = QtWidgets.QApplication.primaryScreen()
        screen_geo = screen.geometry()

        size = submenu.size()

        if pos.x() + size.width() > screen_geo.right():
            pos.setX(pos.x() - size.width() - shape.rect.width())

        if pos.y() + size.height() > screen_geo.bottom():
            pos.setY(screen_geo.bottom() - size.height())

        submenu.move(pos)
        submenu.show()

        # 防止被 GC
        if not hasattr(self, "_submenu_pool"):
            self._submenu_pool = []
        self._submenu_pool.append(submenu)

        self.active_submenu = submenu
        self.active_submenu_shape = shape

    def _close_active_submenu(self):
        if self.active_submenu:
            self.active_submenu.close()
            self.active_submenu = None
            self.active_submenu_shape = None
            self.submenuClosed.emit()

    def hide(self):
        self._close_active_submenu()
        super(NestedHotboxReader, self).hide()


def set_shapes_hovered_nested(shapes, cursor, clicked):
    for shape in shapes:
        if shape.is_interactive():
            shape.set_hovered(cursor)
            shape.clicked = shape.hovered and clicked

def set_crossed_shapes_hovered_nested(point1, point2, shapes, cursor):
    for shape in shapes:
        shape.hovered = False
    for shape in shapes:
        if shape.rect.contains(cursor):
            shape.hovered = True
            return
    cshapes = [s for s in shapes if segment_cross_rect(point1, point2, s.rect)]
    if not cshapes:
        return
    shapedistances = {
        distance(shape.rect.center(), cursor): shape
        for shape in cshapes}
    shapedistances[min(shapedistances.keys())].hovered = True