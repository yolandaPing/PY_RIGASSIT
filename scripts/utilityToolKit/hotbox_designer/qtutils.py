# -*- coding: utf-8 -*-
try:
    from ui_framework.core.qtCompat import *

except ImportError:
    from CommonUse.qtCompat import *
import os

VALIGNS = {
    'top': QtAlign('AlignTop'),
    'center': QtAlign('AlignVCenter'),
    'bottom': QtAlign('AlignBottom')
}

HALIGNS = {
    'left': QtAlign('AlignLeft'),
    'center': QtAlign('AlignHCenter'),
    'right': QtAlign('AlignRight')
}


ICONDIR = os.path.dirname(__file__)


def icon(filename):
    return QtGui.QIcon(os.path.join(ICONDIR, 'resources', 'icons', filename))


def get_cursor(widget):
    return widget.mapFromGlobal(QtGui.QCursor.pos())


def set_shortcut(keysequence, parent, method):
    """
    Qt Shortcut 兼容（PySide1 / 2 / 6）
    """
    shortcut = QtShortcut()(QtGui.QKeySequence(keysequence), parent)
    shortcut.activated.connect(method)
    return shortcut