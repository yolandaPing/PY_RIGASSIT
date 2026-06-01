from maya import OpenMaya as om

from ngSkinTools2.api.pyside import QtCore, QtWidgets

openDialogs = []
messagesCallbacks = []

# main window will set itself here
promptsParent = None


def __baseMessageBox(message):
    msg = QtWidgets.QMessageBox(promptsParent)
    msg.setWindowTitle("ngSkinTools2")
    msg.setText(message)

    for i in messagesCallbacks:
        i(message)

    openDialogs.append(msg)
    return msg


def displayError(message):
    """
    displays error in script editor and in a dialog box
    """

    message = str(message)
    om.MGlobal.displayError('[ngSkinTools2] ' + message)

    msg = __baseMessageBox(message)
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.exec_()


def info(message):
    msg = __baseMessageBox(message)
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.exec_()


def yesNo(message):
    msg = __baseMessageBox(message)
    msg.setIcon(QtWidgets.QMessageBox.Question)
    msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    msg.setDefaultButton(QtWidgets.QMessageBox.Yes)
    return msg.exec_() == QtWidgets.QMessageBox.Yes


def closeAllAfterTimeout(timeout, result=0):
    def closeAll():
        while openDialogs:
            msg = openDialogs.pop()
            msg.done(result)

    QtCore.QTimer.singleShot(timeout, closeAll)
