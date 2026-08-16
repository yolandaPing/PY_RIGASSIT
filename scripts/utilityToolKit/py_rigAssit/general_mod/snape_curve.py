# -*- coding: utf-8 -*-
# .FileName:snape_curve.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2025/11/14 23:52
# .Finish time:
"""
Snape Curve
Curve adsorption editor

PY_RIGASSIT Tool
"""

import maya.cmds as cmds

from ui_framework.core.qtCompat import *
from ui_framework.widgets.widgets import Widgets, PyouPersistentWindow
from py_rigAssit.dialogs import Help, mayaPrint
from ControllerTool.snape_curve_core import CurveSnapManager
from Utils.undo import undo

_widgets = Widgets()


curve_manager = CurveSnapManager()


@undo
def run_snape_edit():
    selection = cmds.ls(selection=True)
    if len(selection) < 2:
        mayaPrint.warning("请先选择两条曲线：第一条为引导线，第二条为目标曲线")
        return
    curve_manager.set_objects(selection[0], selection[1])
    if curve_manager.exists():
        curve_manager.stop()
    curve_manager.start()
    cmds.inViewMessage(assistMessage="Entered curve Edit Mode", statusColor="red")

@undo
def run_delete_curve_edit():
    curve_manager.stop()
    cmds.inViewMessage(assistMessage="Exited curve Edit Mode", statusColor="yellow")
    mayaPrint.log("// Exited curve Edit Mode\n")


class SnapeCurveUI(PyouPersistentWindow):
    def __init__(self, parent=_widgets.maya_main_window()):
        super(SnapeCurveUI, self).__init__("SnapeCurveUI", "SnapeCurveUI", parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setWindowTitle("曲线吸附编辑器 (Snape Curve)")
        self.setMinimumWidth(320)
        self.loadWindowSettings()
        self.create_ui()
        self.update_status()

    def create_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(_widgets.create_text(u"选择引导线和需要编辑的曲线"))
        form = QtWidgets.QFormLayout()
        _, self.leader_line = _widgets.create_QLineEdit_grp("引导线:")
        _, self.target_line = _widgets.create_QLineEdit_grp("目标曲线:")
        self.leader_line.setEnabled(False)
        self.target_line.setEnabled(False)
        self.leader_line.setPlaceholderText("引导线名称")
        self.target_line.setPlaceholderText("目标曲线名称")
        form.addRow("引导线:", self.leader_line)
        form.addRow("目标曲线:", self.target_line)
        layout.addLayout(form)

        self.status = QtWidgets.QLabel("状态: 未激活")
        self.status.setAlignment(QtCore.Qt.AlignCenter)

        self.enter_btn = QtWidgets.QPushButton("进入编辑模式")
        self.exit_btn = QtWidgets.QPushButton("退出编辑模式")
        self.enter_btn.clicked.connect(self.get_selection)
        self.exit_btn.clicked.connect(self.exit_edit)

        buttons = QtWidgets.QHBoxLayout()
        buttons.addWidget(self.enter_btn)
        buttons.addWidget(self.exit_btn)

        layout.addWidget(self.status)
        layout.addLayout(buttons)
        layout.addStretch()
        _widgets.create_copyrightText(layout, "2024")

    def get_selection(self):
        selection = cmds.ls(selection=True)
        if len(selection) >= 2:
            self.leader_line.setText(selection[0])
            self.target_line.setText(selection[1])
            self.enter_edit()
        elif len(selection) == 1:
            self.leader_line.setText(selection[0])
            mayaPrint.warning("请再选择一条目标曲线")
        else:
            mayaPrint.warning("请先选择两条曲线")

    def enter_edit(self):
        leader = self.leader_line.text().strip()
        target = self.target_line.text().strip()
        if not leader or not target:
            mayaPrint.warning("请填写曲线名称")
            return
        if not cmds.objExists(leader):
            mayaPrint.warning("{} 不存在".format(leader))
            return
        if not cmds.objExists(target):
            mayaPrint.warning("{} 不存在".format(target))
            return
        curve_manager.set_objects(leader, target)
        curve_manager.start()
        self.update_status()

    def exit_edit(self):
        curve_manager.stop()
        self.update_status()

    def update_status(self):
        if curve_manager.exists():
            self.status.setText("状态: 编辑中 ({})".format(curve_manager.leader))
            self.status.setStyleSheet("color:green;font-weight:bold;")
            self.enter_btn.setEnabled(False)
            self.exit_btn.setEnabled(True)
        else:
            self.status.setText("状态: 未激活")
            self.status.setStyleSheet("color:gray;font-weight:bold;")
            self.enter_btn.setEnabled(True)
            self.exit_btn.setEnabled(False)


def show():
    global ui_instance
    try:
        ui_instance.close()
        ui_instance.deleteLater()
    except:
        pass
    ui_instance = SnapeCurveUI(parent=_widgets.maya_main_window())
    ui_instance.show()
    return ui_instance

if __name__ == "__main__":
    show()