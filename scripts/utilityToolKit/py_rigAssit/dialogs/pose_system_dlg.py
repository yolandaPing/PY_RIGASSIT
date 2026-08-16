# -*- coding: utf-8 -*-

# .FileName:pose_system_dlg.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/5/22 13:56
# .Finish time:

from functools import partial

import os
from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
from py_rigAssit.dialogs import Help, mayaPrint
# from py_rigAssit.common.command_dispatcher import CommandDispatcher
import saveRootPath as root
import maya.cmds as cmds

PY_WIDGEAT = Widgets()


class PoseUIMode:
    IDLE = 0
    ADDING = 1
    EDITING = 2


ICON_CONFIG = [
    {"cmd": 0, "img": "Plus.png", "ann": "Add Pose"},
    {"cmd": 1, "img": "Minus.png", "ann": "Delete Pose"},
    {"cmd": 2, "img": "Mirror.png", "ann": "Mirror Pose"},
    {"cmd": 3, "img": "Edit.png", "ann": "Edit Pose"},
    {"cmd": 4, "img": "return.png", "ann": "Return"},
]

BASE_DIR = root.IconsPath


def icon_path(name):
    return os.path.join(BASE_DIR, "label", name)


class RBFDrivePoseLayout(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(RBFDrivePoseLayout, self).__init__(parent)
        # 初始化模式
        self.mode = PoseUIMode.IDLE
        # 初始化按钮字典
        self.icon_buttons = {}

    def init_ui(self):

        root = QtWidgets.QWidget()
        main = QtWidgets.QVBoxLayout(root)
        main.setContentsMargins(6, 6, 6, 6)
        main.setSpacing(8)

        main.addWidget(self.build_system())
        main.addStretch()

        return root

    # -------------------------
    # SYSTEM PANEL
    # -------------------------
    def build_system(self):

        group = QtWidgets.QGroupBox("System")
        layout = QtWidgets.QVBoxLayout(group)
        layout.setSpacing(10)

        # ========== 1 LOAD GEO ==========
        title1 = PY_WIDGEAT.create_text("Load Geometry")
        # title1 = QtWidgets.QLabel("Load Geometry")
        layout.addWidget(title1)
        hint = QtWidgets.QLabel("Do not proceed with the shaping phase; no model loading is required.")
        hint.setWordWrap(True)
        hint.setStyleSheet("color:#888;")
        layout.addWidget(hint)

        geo_row = QtWidgets.QHBoxLayout()
        layout.addLayout(geo_row)

        geo_row.addWidget(QtWidgets.QLabel("Geo:"))
        self.geo_line = QtWidgets.QLineEdit()
        geo_row.addWidget(self.geo_line)
        self.geo_line.setEnabled(False)
        geo_row.addWidget(QtWidgets.QPushButton("<<<"))

        bs_row = QtWidgets.QHBoxLayout()
        layout.addLayout(bs_row)

        bs_row.addWidget(QtWidgets.QLabel("BS:"))
        self.bs_line = QtWidgets.QLineEdit()
        self.bs_line.setEnabled(False)
        bs_row.addWidget(self.bs_line)

        PY_WIDGEAT.separator(layout)

        # ========== 2 JOINT AXIS ==========
        title2 = PY_WIDGEAT.create_text("Set Joint Axis")
        layout.addWidget(title2)

        axis_row = QtWidgets.QHBoxLayout()
        layout.addLayout(axis_row)

        axis_row.addWidget(QtWidgets.QLabel("Joint Axis:"))
        self.axis_cb = QtWidgets.QComboBox()
        self.axis_cb.addItems(["-X", "+X", "-Y", "+Y", "-Z", "+Z"])
        axis_row.addWidget(self.axis_cb)

        self.mirror = QtWidgets.QCheckBox("Mirror")
        self.keep = QtWidgets.QCheckBox("Keep State")
        self.keep.setChecked(True)

        layout.addWidget(self.mirror)
        layout.addWidget(self.keep)

        # ========== Sculpt Type ==========
        sculpt_row = QtWidgets.QHBoxLayout()
        layout.addLayout(sculpt_row)

        sculpt_row.addWidget(QtWidgets.QLabel("Sculpt Type:"))

        self.static_rb = QtWidgets.QRadioButton("static")
        self.rt_rb = QtWidgets.QRadioButton("Real-time")
        self.static_rb.setChecked(True)

        sculpt_row.addWidget(self.static_rb)
        sculpt_row.addWidget(self.rt_rb)

        # ========== COLOR ==========
        color_row = QtWidgets.QHBoxLayout()
        layout.addLayout(color_row)

        color_row.addWidget(QtWidgets.QLabel("Sculpt Mesh Color:"))

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 100)
        color_row.addWidget(self.slider)

        self.color_btn = QtWidgets.QPushButton("update color")
        color_row.addWidget(self.color_btn)

        # ========== 3 INFO ==========
        title3 = PY_WIDGEAT.create_text("Select joint + controller + parent object")
        layout.addWidget(title3)

        # ========== CREATE ==========
        # self.create_btn = QtWidgets.QPushButton("Create System")
        # self.create_btn.setMinimumHeight(32)
        create_btn_layout, self.create_btn, self.create_btnhelp_btn = PY_WIDGEAT.create_Qbuttons(" Create System ")

        layout.addLayout(create_btn_layout)
        PY_WIDGEAT.separator(layout)

        # ========== EDIT BUTTONS ==========
        # edit_row = QtWidgets.QHBoxLayout()
        # layout.addLayout(edit_row)

        # for t in ["+", "-", "?", "?", "?"]:
        #     btn = QtWidgets.QPushButton(t)
        #     btn.setFixedSize(38, 38)
        #     edit_row.addWidget(btn)

        layout.addLayout(self.build_icon_toolbar())

        return group

    def build_icon_toolbar(self):

        self.icon_buttons = {}

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(6)
        layout.setContentsMargins(0, 6, 0, 0)

        for cfg in ICON_CONFIG:
            btn = QtWidgets.QToolButton()
            btn.setFixedSize(52, 52)
            btn.setIconSize(QtCore.QSize(52, 52))
            btn.setAutoRaise(True)

            icon_file = icon_path(cfg["img"])

            btn.setIcon(QtGui.QIcon(icon_file))
            btn.setToolTip(cfg["ann"])

            cmd = cfg["cmd"]
            # btn.clicked.connect(lambda _, i=cmd: self.on_icon_click(i))
            btn.clicked.connect(self.make_cb(cmd))

            layout.addWidget(btn)

            self.icon_buttons[cmd] = btn

        layout.addStretch()
        return layout

    def make_cb(self, cmd):
        def _cb():
            self.apply_item(cmd)

        return _cb

    def on_icon_click(self, cmd):

        print("icon click:", cmd)

        # demo state switch
        if cmd == 0:
            self.apply_mode(PoseUIMode.ADDING)
        elif cmd == 3:
            self.apply_mode(PoseUIMode.EDITING)
        elif cmd == 4:
            self.apply_mode(PoseUIMode.IDLE)

    def apply_item(self, cmd):
        """
        对应 iconTextButton 原来的 lambda 调用逻辑
        支持再次点击自身按钮回到 IDLE
        并在 ADD/EDIT 模式下禁用其他按钮
        """
        current_mode = self.mode

        # -------------------------
        # 再次点击当前模式按钮 -> 回到 IDLE
        # -------------------------
        if (cmd == 0 and current_mode == PoseUIMode.ADDING) or (cmd == 3 and current_mode == PoseUIMode.EDITING):
            self.apply_mode(PoseUIMode.IDLE)
            return

        # -------------------------
        # 处理按钮功能
        # -------------------------
        # commands = {
        #     0: self.addPose,      # +
        #     1: self.deletePose,   # -
        #     2: self.mirror_pose,  # Mirror
        #     3: self.EditPose,     # Edit
        #     4: self.returnPose,   # ?
        # }

        # if cmd in commands:
        #     commands[cmd]()  # 调用实际功能

        # -------------------------
        # 根据按钮类型设置模式和启用状态
        # -------------------------
        if cmd == 0:
            self.apply_mode(PoseUIMode.ADDING)
        elif cmd == 3:
            self.apply_mode(PoseUIMode.EDITING)
        else:
            # 普通按钮或 return 不改变模式，仍然保持 IDLE
            self.apply_mode(PoseUIMode.IDLE)

    def apply_mode(self, mode):
        self.mode = mode

        # -------------------------
        # 所有按钮先重置
        # -------------------------
        for cfg in ICON_CONFIG:
            cmd = cfg["cmd"]
            btn = self.icon_buttons.get(cmd)
            if not btn:
                continue
            btn.setEnabled(True)
            btn.setIcon(QtGui.QIcon(icon_path(cfg["img"])))
            btn.setToolTip(cfg["ann"])
            btn.setIconSize(QtCore.QSize(52, 52))

        # -------------------------
        # ADD / EDIT 模式时，禁用其他按钮
        # -------------------------
        if mode in (PoseUIMode.ADDING, PoseUIMode.EDITING):
            # 获取当前模式对应按钮
            active_btn_cmd = 0 if mode == PoseUIMode.ADDING else 3
            for cmd, btn in self.icon_buttons.items():
                if cmd != active_btn_cmd:
                    btn.setEnabled(False)

        # -------------------------
        # 覆盖图标
        # -------------------------
        state = {
            PoseUIMode.ADDING: {
                0: ("finish.png", "Exit Add Mode", True),
            },
            PoseUIMode.EDITING: {
                3: ("Editing.png", "Editing...", True),
            }
        }.get(mode, {})

        for cmd, (icon, tip, en) in state.items():
            btn = self.icon_buttons.get(cmd)
            if not btn:
                continue
            btn.setIcon(QtGui.QIcon(icon_path(icon)))
            btn.setToolTip(tip)
            btn.setEnabled(en)
            btn.setIconSize(QtCore.QSize(52, 52))


class RBFDrivePoseUI(PyouPersistentWindow):
    VERSION = " v2.6.6"

    def __init__(self, parent=None):
        super(RBFDrivePoseUI, self).__init__("RBFDrivePoseUI", "RBFDrivePoseUI", parent=parent)

        self.setWindowTitle("RBF Drive Pose")
        self.setMinimumWidth(320)

        self._build_ui()
        self.loadWindowSettings()

    def _build_ui(self):

        main = QtWidgets.QVBoxLayout(self)
        main.setContentsMargins(4, 4, 4, 4)
        main.setSpacing(4)

        self.logo_img = QtWidgets.QLabel()
        self.logo_img.setFixedHeight(60)
        self.logo_img.setAlignment(QtCore.Qt.AlignCenter)

        self.logo_text = QtWidgets.QLabel("RBF Drive Pose {}".format(self.VERSION))
        self.logo_text.setAlignment(QtCore.Qt.AlignCenter)

        self.load_logo()

        main.addWidget(self.logo_img)
        main.addWidget(self.logo_text)

        # main.addWidget(PY_WIDGEAT.create_title("RBF Drive Pose v2.6.5", 20))

        tab = QtWidgets.QTabWidget()

        system_widget = RBFDrivePoseLayout(parent=self).init_ui()
        tab.addTab(system_widget, "System")
        tab.addTab(QtWidgets.QWidget(), "Copy")
        tab.addTab(QtWidgets.QWidget(), "Exp/Imp")

        main.addWidget(tab)

        PY_WIDGEAT.create_copyrightText(main, "2024-2026")

    def load_logo(self):
        icon_path = os.path.join(BASE_DIR, "label", "rbfDirveLabel.png")

        if not os.path.exists(icon_path):
            return

        pix = QtGui.QPixmap(icon_path)

        if pix.isNull():
            return

        self.logo_img.setPixmap(
            pix.scaled(
                220,
                130,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
        )


def main():
    global rbf_drive_pose_ui

    try:
        rbf_drive_pose_ui.close()
        rbf_drive_pose_ui.deleteLater()
    except:
        pass

    rbf_drive_pose_ui = RBFDrivePoseUI()
    rbf_drive_pose_ui.show()


if __name__ == "__main__":
    main()