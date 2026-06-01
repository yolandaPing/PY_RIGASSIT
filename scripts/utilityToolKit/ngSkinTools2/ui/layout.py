from maya import cmds

from ngSkinTools2.api.pyside import QtCore, QtWidgets
from ngSkinTools2.api.python_compatibility import Object
from ngSkinTools2.ui import qt

try:
    scale_multiplier = cmds.mayaDpiSetting(q=True, realScaleValue=True)
except:
    #  the command is not available on macos, using 1.0 for fallback
    scale_multiplier = 1


def createTitledRow(title, contents, *additional_rows):
    row = QtWidgets.QFormLayout()
    row.setContentsMargins(0, 0, 0, 0)
    label = QtWidgets.QLabel(title)
    # label.setAlignment(QtCore.Qt.AlignRight |QtCore.Qt.)
    label.setFixedWidth(100 * scale_multiplier)

    if contents is None:
        row.addRow(label, QtWidgets.QWidget())
        return row

    row.addRow(label, contents)
    for i in additional_rows:
        row.addRow(None, i)
    return row


class TabSetup(Object):
    def __init__(self):
        self.innerLayout = innerLayout = QtWidgets.QVBoxLayout()
        innerLayout.setContentsMargins(0, 0, 0, 0)
        innerLayout.setSpacing(3 * scale_multiplier)

        self.scrollArea = scrollArea = QtWidgets.QScrollArea()
        scrollArea.setFocusPolicy(QtCore.Qt.NoFocus)
        scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        scrollArea.setWidget(qt.wrap_layout_into_widget(innerLayout))
        scrollArea.setWidgetResizable(True)

        self.lowerButtonsRow = lowerButtonsRow = QtWidgets.QHBoxLayout()

        self.mainLayout = mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(scrollArea)
        mainLayout.addLayout(lowerButtonsRow)
        mainLayout.setContentsMargins(7, 7, 7, 7)

        self.tabContents = qt.wrap_layout_into_widget(mainLayout)
