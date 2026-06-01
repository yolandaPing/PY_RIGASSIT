# -*- coding: utf-8 -*-

# .FileName:rivet_follice_dlg.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/25 18:21
# .Finish time:
from functools import partial

from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
from py_rigAssit.dialogs import base_dir, Help, decorator , mayaPrint
from py_rigAssit.common.command_dispatcher import CommandDispatcher
import py_rigAssit.common.commands
import maya.cmds as cmds, maya.mel as mel

PY_WIDGEAT = Widgets()


class PYRivetFolliceUI(PyouPersistentWindow):

    def __init__(self, parent=None):
        super(PYRivetFolliceUI, self).__init__("PYRivetFolliceUI", "PYRivetFolliceUI",parent=parent)
        self.window_name = "Follicle/Rivet Tool"
        self.setWindowTitle(self.window_name)
        self.setMinimumWidth(260)
        self.init_ui(True)
        self.loadWindowSettings()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocus()

    def init_ui(self, copyright=False):

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(PY_WIDGEAT.create_title(self.window_name, 16, None))
        main_layout.addWidget(self.rivet_layout())
        main_layout.addStretch()
        if copyright:
            PY_WIDGEAT.create_copyrightText(main_layout, "2024-2026")

        return main_layout

    def rivet_layout(self):
        frame = PY_WIDGEAT.create_collapsible_frame(u" Follicle/Rivet 钉子", True)
        group = QtWidgets.QGroupBox(u"Follicle/Rivet:")
        main_layout = QtWidgets.QVBoxLayout(group)

        self.rivet_rig_wtg = PY_WIDGEAT.create_section("Rig Type:")
        self.rivet_rig_block = PY_WIDGEAT.create_radiogroup(
            "",
            [
                ("Parent", 1, None),
                ("Contrain", 2, u"约束"),
            ],
            default_id=1
        )
        self.rivet_constrain_block = PY_WIDGEAT.create_radiogroup(
            "约束:",
            [
                ("parentConstrain", 1, u"父约束"),
                ("pointConstrain", 2, u"点约束"),
                ("orientConstrain", 3, u"方向约束"),
            ],
            default_id=1,
            enabled_map={1: False, 2: False, 3: False}
        )

        self.rivet_cons_block = PY_WIDGEAT.create_radiogroup(
            "Type:",
            [
                ("Follicle", 1, u"毛囊"),
                ("Matrix", 2, u"locator"),
                ("Constrain", 3, u"获取最近的权重关节创建约束"),
            ],
            default_id=1
        )
        self.rivet_hint = PY_WIDGEAT.create_text("select objects and then Surface/Mesh\n选择需要钉的对象+Surface/Mesh")
        btn_layout, self.rivet_apple_btn, self.rivet_help_btn = PY_WIDGEAT.create_Qbuttons(" Apply ")

        main_layout.addWidget(self.rivet_hint)
        self.rivet_rig_wtg.addWidget(self.rivet_rig_block)
        self.rivet_rig_wtg.addWidget(self.rivet_constrain_block)
        main_layout.addWidget(self.rivet_rig_wtg)
        main_layout.addWidget(self.rivet_cons_block)

        main_layout.addLayout(btn_layout)
        self.rivet_rig_block.idClicked.connect(self._rivet_rig_toggled)
        self.rivet_cons_block.idClicked.connect(self._rivet_cons_toggled)
        self.rivet_apple_btn.clicked.connect(self.follicle_rivet_constrain)
        self.rivet_help_btn.clicked.connect(partial(Help.HelpImage, "", "create_follicle_rivet"))
        frame.addWidget(group)
        return frame


    def _rivet_cons_toggled(self, btn_id):
        if btn_id == 3:
            self.rivet_rig_wtg.setEnabled(False)
        else:
            self.rivet_rig_wtg.setEnabled(True)


    def _rivet_rig_toggled(self, btn_id):
        if btn_id == 2:
            self.rivet_constrain_block.setEnabledByIds([1, 2, 3], True)
        else:
            self.rivet_constrain_block.setEnabledByIds([1, 2, 3], False)


    def follicle_rivet_constrain(self):
        dispatcher = CommandDispatcher()

        obj = cmds.ls(sl=1)
        if len(obj) < 2:
            mayaPrint.error(' Please add NurbsSurface/Mesh. ')
            return

        datas = {
            "cons_block": self.rivet_cons_block.checkedId(),
            "rig_block": self.rivet_rig_block.checkedId(),
            "constrain_block": self.rivet_constrain_block.checkedId()
        }

        dispatcher.execute("follicle rivet Rig", datas)

def main():
    global py_rivetfollice_ui

    try:
        py_rivetfollice_ui.close()  # pylint: disable=E0601
        py_rivetfollice_ui.deleteLater()
    except:
        pass

    py_rivetfollice_ui = PYRivetFolliceUI()
    py_rivetfollice_ui.show()


if __name__ == '__main__':

    main()
