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


class PYRivetFolliceLayout(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(PYRivetFolliceLayout, self).__init__(parent)
        self.window_name = "Follicle/Rivet/uvPin Tool"

    def init_ui(self):
        container = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(container)
        main_layout.addWidget(self.rivet_layout())
        main_layout.addStretch()

        return container

    def rivet_layout(self):
        group = QtWidgets.QGroupBox(u"Follicle/Rivet:")
        main_layout = QtWidgets.QVBoxLayout(group)

        mayaMajorVersion = int(cmds.about(version=True)[0:4])
        self.uv_pin_en = False

        if mayaMajorVersion > 2019:
            self.uv_pin_en = True

        self.rivet_rig_wtg = PY_WIDGEAT.create_section("Rig Type:")
        self.rivet_rig_block = PY_WIDGEAT.create_radiogroup(
            "",
            [
                ("Parent", 1, ""),
                ("Contrain", 2, u"约束"),
                ("Input", 3, u"(无transform创建) uvpin矩阵直接输出给对象的offsetParentMatrix"),
                ("connect", 4, u"(无transform创建) 拆解uvpin的矩阵,链接给对象位移旋转,且保持当前对象的数值")
            ],
            default_id=1,
            enabled_map={3: False, 4: False}
        )
        self.rivet_constrain_block = PY_WIDGEAT.create_radiogroup(
            "约束:",
            [
                ("parent", 1, u"父约束"),
                ("point", 2, u"点约束"),
                ("orient", 3, u"方向约束"),
            ],
            default_id=1,
            enabled_map={1: False, 2: False, 3: False}
        )

        self.rivet_cons_block = PY_WIDGEAT.create_radiogroup(
            "",
            [
                ("Follicle", 1, u"毛囊"),
                ("Rivet", 2, u"Rivet"),
                ("UV Pin", 3, u"Maya2020+ UV Pin"),
                ("Skin con", 4, u"获取对象到mesh最近的点权重关节创建约束"),
            ],
            default_id=1,
            enabled_map={3: self.uv_pin_en}
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
        # frame.addWidget(group)
        return group


    def _rivet_cons_toggled(self, btn_id):

        if btn_id == 4:
            self.rivet_rig_wtg.setEnabled(False)
        else:
            self.rivet_rig_wtg.setEnabled(True)
            if btn_id in [3]:
                self.rivet_rig_block.setEnabledByIds([1, 2, 3, 4], True)
            else:
                self.rivet_rig_block.setEnabledByIds([3, 4], False)


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


class PYRivetFolliceUI(PyouPersistentWindow):

    def __init__(self, parent=None):
        super(PYRivetFolliceUI, self).__init__("PYRivetFolliceUI", "PYRivetFolliceUI", parent=parent)
        self.window_name = "Follicle/Rivet/uvPin Tool"
        self.setWindowTitle(self.window_name)
        self.setMinimumWidth(220)
        self._build_ui()
        self.loadWindowSettings()


    def _build_ui(self):
        main = QtWidgets.QVBoxLayout(self)
        main.setContentsMargins(4, 4, 4, 4)
        main.setSpacing(4)
        main.addWidget(PY_WIDGEAT.create_title(self.window_name, 18, None))

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setContentsMargins(0, 0, 0, 0)

        cld_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(cld_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(4)

        scroll.setWidget(cld_widget)
        main.addWidget(scroll)

        widget = PYRivetFolliceLayout(parent=self)
        scroll_layout.addWidget(widget.init_ui())

        PY_WIDGEAT.create_copyrightText(main, "2022-2026")
        # main.addWidget(widget.init_ui())

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
