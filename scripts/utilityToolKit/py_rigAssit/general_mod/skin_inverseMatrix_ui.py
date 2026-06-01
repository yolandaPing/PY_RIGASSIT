# -*- coding: utf-8 -*-

# .FileName:skin_inverseMatrix_ui.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2025/12/4 21:10
# .Finish time:
# Qt wrapper for Maya 2017–2025
from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
from JointEdit.skin_inverseMatrix import InverseSkinMatrix

import maya.cmds as cmds

_widgest = Widgets()


def _information_Dialog(text):
    cmds.confirmDialog(icn="information", title='Skin Inverse Dialog', message=' >>> {} !!!'.format(text))


class SkinInvertMatrixWindow(PyouPersistentWindow):


    def __init__(self, parent=_widgest.maya_main_window()):
        super(SkinInvertMatrixWindow, self).__init__("SkinInvertMatrixApp", "SkinInvertMatrixWindow", parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.WINDOW_NAME = 'skin Inverse Matrix'
        self.timeStamp = "2025"
        self.InverseSkinMatrix = InverseSkinMatrix()

        self.setWindowTitle(self.WINDOW_NAME)
        self.setMinimumWidth(300)
        self.loadWindowSettings()

        self.skinNodes = []

        self.init_ui()
        self.create_connections()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocus()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(_widgest.create_title(self.WINDOW_NAME, 16, 30))
        self.setup_ui(main_layout)
        main_layout.addStretch()
        _widgest.create_copyrightText(main_layout, self.timeStamp)

    def setup_ui(self, parent):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(_widgest.create_bold_label(u"运行Inverse前 ，先移除skinCluster没有影响的关节"))
        layout.addWidget(_widgest.create_text(u"PY_RIGASSIT > joint模块 > Remove scence unSkin Jnt", 11, "left"))

        ctrl_layout = QtWidgets.QHBoxLayout()
        geo_layout = QtWidgets.QHBoxLayout()

        btn_layout = QtWidgets.QHBoxLayout()

        self.ctrl_field_grp = QtWidgets.QLineEdit()
        ctrl_field_layout = QtWidgets.QFormLayout()
        ctrl_field_layout.addRow('Ctrl :', self.ctrl_field_grp)

        self.load_ctrl_btn = QtWidgets.QPushButton("  <<<  ")

        self.ctrl_field_grp.setText('master_ctrl')
        self.ctrl_field_grp.setToolTip(u'master ctrl')
        self.load_ctrl_btn.setToolTip(u'载入master ctrl/root。')

        self.geo_field_grp = QtWidgets.QLineEdit()
        geo_field_layout = QtWidgets.QFormLayout()
        geo_field_layout.addRow('Geo :', self.geo_field_grp)
        self.load_geo_btn = QtWidgets.QPushButton("  <<<  ")

        self.geo_field_grp.setText('Geo_grp')
        self.geo_field_grp.setToolTip(u'Geo grp')
        self.load_geo_btn.setToolTip(u'载入Geo group。')

        self.Inverse_btn = QtWidgets.QPushButton("Inverse")
        self.Restore_btn = QtWidgets.QPushButton("Restore ")

        self.Inverse_btn.setProperty("main", True)
        self.Restore_btn.setProperty("main", True)

        _widgest.separator(layout, False)

        ctrl_layout.addLayout(ctrl_field_layout)
        ctrl_layout.addWidget(self.load_ctrl_btn)
        geo_layout.addLayout(geo_field_layout)
        geo_layout.addWidget(self.load_geo_btn)

        btn_layout.addWidget(self.Inverse_btn)
        btn_layout.addWidget(self.Restore_btn)

        layout.addLayout(ctrl_layout)
        layout.addLayout(geo_layout)
        _widgest.separator(layout, False)

        layout.addLayout(btn_layout)

        parent.addLayout(layout)

    def create_connections(self):

        self.load_ctrl_btn.clicked.connect(lambda: self.load_object(self.ctrl_field_grp))
        self.load_geo_btn.clicked.connect(lambda: self.load_object(self.geo_field_grp))
        self.Inverse_btn.clicked.connect(self.run_inverseMatrix)
        self.Restore_btn.clicked.connect(self.restore_skin_matrixIn)

    def load_object(self, field):

        obj = cmds.ls(sl=True)
        if obj:
            field.setText(obj[0])


    # @_decorator.undo
    def run_inverseMatrix(self, *args):
        # root_jnt = 'root_jnt'
        master_ctrl = self.ctrl_field_grp.text()
        Geo_grp = self.geo_field_grp.text()

        indo = self.InverseSkinMatrix.run_inverseMatrix(master_ctrl, Geo_grp)
        if indo:
            _information_Dialog("skin worldInverseMatrix")

    # @_decorator.undo
    def restore_skin_matrixIn(self, *args):
        Geo_grp = self.geo_field_grp.text()

        indo = self.InverseSkinMatrix.restore_skin_matrixIn(Geo_grp)
        if indo:
            _information_Dialog("skin matrixIn restore")


def main():
    global pySkinInvert_ui

    try:
        pySkinInvert_ui.close()  # pylint: disable=E0601
        pySkinInvert_ui.deleteLater()
    except:
        pass

    pySkinInvert_ui = SkinInvertMatrixWindow(parent=_widgest.maya_main_window())
    pySkinInvert_ui.show()


if __name__ == "__main__":
    main()
