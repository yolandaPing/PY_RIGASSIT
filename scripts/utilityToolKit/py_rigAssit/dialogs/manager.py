# -*- coding: utf-8 -*-

# .FileName:manager.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2025/7/24 21:19
# .Finish time:
import os, webbrowser
import traceback

from py_rigAssit import QtWidgets, QtCore, QtGui, QAction, Widgets, PyouPersistentWindow
from py_rigAssit.dialogs import base_dir, icon_dir
from py_rigAssit.dialogs.MarkingMenuLite import PYMarkingMenuLite
from py_rigAssit.dialogs.theme_manager import ThemeManager
from py_rigAssit.common.command_dispatcher import CommandDispatcher
import py_rigAssit.common.menu_commands
import py_rigAssit.common.commands

import Utils.json_info as json_info
import user_defined as ud
import maya.cmds as cmds

_widgest = Widgets()
_WINDOW_CACHE = None


def return_checkBox(item_text, state):

    key_map = {
        "Use shelfButton New": "shelfButton_New",
        "Auto import Hotkey": "hotkey",
        "Auto add sec/pri grp": "Grp_prisec",
    }

    key = key_map.get(item_text)
    if key:
        ud.set_value(key, bool(state))
        setattr(ud, key, bool(state))

def copy_to_clipboard(text, msg=None):
    QtWidgets.QApplication.clipboard().setText(text)

    try:
        cmds.inViewMessage(
            amg=msg or "Copied: <hl>{}</hl>".format(text),
            pos="midCenter",
            fade=True
        )
    except:
        print(msg or "Copied: {}".format(text))


class PYRiggingDialogManager(PyouPersistentWindow):

    WINDOW_NAME = "PYRiggingDialogManager"
    TOOL_NAME = "PY_RIGASSITDockControl"
    VERSION = "06.0.0"

    try:
        _info = json_info.version_info("tip")
    except:
        _info = None

    if _info:
        VERSION = _info[0]
        timeStamp = _info[1]
        webs = _info[-1]
    else:
        timeStamp = "2022-2026"
        webs = None

    # ---------------- INIT ----------------
    def __init__(self, dialog_data, parent=None):

        super(PYRiggingDialogManager, self).__init__(
            self.WINDOW_NAME,
            self.WINDOW_NAME,
            parent
        )

        self.dialog_data = dialog_data
        self.ui_contents = dialog_data.get("INIT_UI", {})
        self.tab_names = dialog_data.get("TABS", ())
        self.window_size = dialog_data.get("WITHHIGHT", [320, 780])
        self.title = dialog_data.get("UI_NAME", "PY_RIGASSIT")

        self.dispatcher = CommandDispatcher()

        # FIX：防 Qt GC
        self._actions = []

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setWindowTitle(self.title)
        self.resize(*self.window_size)

        self.build_ui()

        try:
            ThemeManager.apply(self)
        except:
            pass

        self.loadWindowSettings()
        self.setFocus()


    def build_ui(self):

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setSpacing(4)
        self.main_layout.setContentsMargins(4, 4, 4, 4)
        self.build_menu_bar()
        self.build_logo_area()
        self.build_tabs()
        self.build_footer()
        self.init_marking_menu()


    def build_menu_bar(self):

        self.menu_bar = QtWidgets.QMenuBar()

        def add(menu, label, callback=None, checkable=False, checked=False, item_id=None, bold=False):

            act = QAction(label, self)  # FIX parent

            if bold:
                f = act.font()
                f.setBold(True)
                act.setFont(f)

            if checkable:
                act.setCheckable(True)
                act.setChecked(checked)

                name = item_id or label

                def _cb(*_, n=name, a=act):
                    return_checkBox(n, a.isChecked())

                act.triggered.connect(_cb)

            if callback:
                act.triggered.connect(callback)

            menu.addAction(act)

            # FIX GC
            self._actions.append(act)

            return act


        # ---------------- ABOUT ----------------
        about = self.menu_bar.addMenu("About")

        add(about, "bilibili: 我有一只猛犬",
            callback=lambda: webbrowser.open("https://space.bilibili.com/3493142019967757"))

        add(about, "pyrigassit@gmail.com", callback=self._copy_email)

        sep = about.addAction("PY_RIGASSIT")
        sep.setEnabled(False)

        about.addSeparator()

        add(about, "Update",
            callback=lambda: webbrowser.open(self._info[-2] if self._info else ""))

        add(about, u"Quark 夸克网盘",
            callback=lambda: webbrowser.open(self._info[-1] if self._info else ""))


        # ---------------- CLEAR ----------------
        clear = self.menu_bar.addMenu("Clear")

        add(clear, "Clean NameSpace",
            callback=lambda: self.dispatcher.execute("Clean NameSpace"))

        add(clear, "Optimize Scene",
            callback=lambda: self.dispatcher.execute("Optimize Scene"))

        clear.addSeparator()

        add(clear, "Check Scene Name",
            callback=lambda: self.dispatcher.execute("Check Scene Name"), bold=True)

        add(clear, "Delete Unused Nodes",
            callback=lambda: self.dispatcher.execute("Delete Unused Nodes"), bold=True)

        add(clear, "Delete unknown Node",
            callback=lambda: self.dispatcher.execute("Delete unknown Node"), bold=True)

        add(clear, "Delete unUsedOrig",
            callback=lambda: self.dispatcher.execute("Delete unUsedOrig"), bold=True)

        clear.addSeparator()

        add(clear, "Delete unDisplayPoint",
            callback=lambda: self.dispatcher.execute("Delete unDisplayPoint"))

        add(clear, "Delete unUsedPlug",
            callback=lambda: self.dispatcher.execute("Delete unUsedPlug"))

        add(clear, "Delete unUsedDagPose",
            callback=lambda: self.dispatcher.execute("Delete unUsedDagPose"))

        add(clear, "UnLockNode selected",
            callback=lambda: self.dispatcher.execute("UnLockNode selected"))

        add(clear, "UnLockNode Scene",
            callback=lambda: self.dispatcher.execute("UnLockNode Scene"), bold=True)

        add(clear, "UnLock initialShading",
            callback=lambda: self.dispatcher.execute("UnLock initialShading"), bold=True)

        # ---------------- TOOL ----------------
        tool = self.menu_bar.addMenu("Tool")
        tool.addAction("Script Editor").setEnabled(False)
        add(tool, "Maya Script Editor",
            callback=lambda: self.dispatcher.execute("Maya Script Editor"))
        add(tool, "CharcoalEditor2",
            callback=lambda: self.dispatcher.execute("CharcoalEditor2"))

        # ---------------- OPTIONS ----------------
        opt = self.menu_bar.addMenu("Options")

        opt.addAction("Convenient").setEnabled(False)

        add(opt, "Use shelfButton New",
            checkable=True, checked=ud.shelfButton_New)

        add(opt, "Auto import Hotkey",
            checkable=True, checked=ud.hotkey)

        add(opt, "Auto add sec/pri grp",
            checkable=True, checked=ud.Grp_prisec)

        opt.addSeparator()

        opt.addAction("Window Display").setEnabled(False)

        add(opt, "Dock",
            callback=self.to_dock_mode)

        add(opt, "Reload Theme",
            callback=self.reload_theme)

        self.main_layout.setMenuBar(self.menu_bar)


    def build_logo_area(self):

        wrap = QtWidgets.QWidget()
        lay = QtWidgets.QVBoxLayout(wrap)

        lay.setContentsMargins(2, 2, 2, 2)
        lay.setSpacing(2)
        lay.setAlignment(QtCore.Qt.AlignCenter)

        self.logo_img = QtWidgets.QLabel()
        self.logo_img.setFixedHeight(60)
        self.logo_img.setAlignment(QtCore.Qt.AlignCenter)

        self.logo_text = QtWidgets.QLabel("PY_RIGASSIT {}".format(self.VERSION))
        self.logo_text.setAlignment(QtCore.Qt.AlignCenter)

        self.load_logo()

        lay.addWidget(self.logo_img)
        lay.addWidget(self.logo_text)

        self.main_layout.addWidget(wrap)

    def load_logo(self):
        icon_path = os.path.join(icon_dir, "PyAssistant.png")

        if not os.path.exists(icon_path):
            return

        pix = QtGui.QPixmap(icon_path)

        if pix.isNull():
            return

        self.logo_img.setPixmap(
            pix.scaled(
                100,
                60,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
        )


    def build_tabs(self):

        self.tabs = QtWidgets.QTabWidget()
        self.main_layout.addWidget(self.tabs)

        self._tab_state = {}

        for name in self.tab_names:

            page = QtWidgets.QWidget()
            lay = QtWidgets.QVBoxLayout(page)
            lay.setContentsMargins(1, 1, 1, 1)
            lay.setSpacing(2)

            self.tabs.addTab(page, name)

            self._tab_state[name] = {
                "layout": lay,
                "loaded": False
            }

        self.tabs.currentChanged.connect(self._load_tab)
        self._load_tab(0)


    def _load_tab(self, idx):

        if idx < 0:
            return

        name = self.tabs.tabText(idx)
        state = self._tab_state.get(name)

        if not state or state["loaded"]:
            return

        builder = self.ui_contents.get(name)

        try:
            if callable(builder):
                obj = builder()

                if isinstance(obj, QtWidgets.QLayout):
                    state["layout"].addLayout(obj)
                else:
                    state["layout"].addWidget(obj)

        except:
            traceback.print_exc()

        state["loaded"] = True


    def build_footer(self):
        _widgest.create_copyrightText(
            self.main_layout,
            self.timeStamp
        )

    def _copy_email(self, *args):
        email = "pyrigassit@gmail.com"
        copy_to_clipboard(email, "Email copied")
        QtWidgets.QMessageBox.information(self, u'Email copied', u'邮箱复制成功')

    def init_marking_menu(self):

        self.mm_normal = PYMarkingMenuLite([
            (" select skin joint ", lambda: self.dispatcher.execute("Select Skin joints")),
            (" select child joint ", lambda: self.dispatcher.execute("Select Child joints")),
            (" mirror skin ", lambda: self.dispatcher.execute("Mirror Skin", False)),
            (" mirror skin l>r ", lambda: self.dispatcher.execute("Mirror Skin")),
            (" copy skin ", lambda: self.dispatcher.execute("Copy Skin")),
            (" combine skinWeight ", lambda: self.dispatcher.execute("Combine Skinweight")),
            (" Resrt Skin Pose ", lambda: self.dispatcher.execute("Resrt Skined Pose")),
            (" Remove unInfluences ", lambda: self.dispatcher.execute("Remove unInfluences")),

        ], self)

        self.mm_ctrl = PYMarkingMenuLite([
            (" curve link ", lambda: self.dispatcher.execute("Curve Keep Linked", False)),
            (" curve keep link ", lambda: self.dispatcher.execute("Curve Keep Linked", True)),
            (" surface link ", lambda: self.dispatcher.execute("Linked Surface")),
            (" select input node ", lambda: self.dispatcher.execute("Select Input Node")),
            (" delete orig node ", lambda: self.dispatcher.execute("Delete Orig Nodes")),
            (" create joint ", lambda: self.dispatcher.execute("Create Joints")),
            (" joint add shape ", lambda: self.dispatcher.execute("Joints Add Shape")),

        ], self)


    def reload_theme(self):
        try:
            ThemeManager.reload(self)
        except:
            pass


    def to_dock_mode(self):

        try:
            from py_rigAssit.dialogs.DockWindowBase import DockWindowBase

            self.close()

            QtCore.QTimer.singleShot(
                0,
                lambda: DockWindowBase.safe_dock(
                    lambda: self.__class__(self.dialog_data),
                    self.title
                )
            )

        except Exception as e:
            print("Dock Failed:", e)

    def mousePressEvent(self, event):

        if event.button() == QtCore.Qt.RightButton:

            global_pos = self.mapToGlobal(event.pos())

            if event.modifiers() & QtCore.Qt.ControlModifier:
                self.mm_ctrl.start(global_pos)
            else:
                self.mm_normal.start(global_pos)

            return

        super(PYRiggingDialogManager, self).mousePressEvent(event)


    def closeEvent(self, event):

        try:
            self.saveWindowSettings()
        except:
            pass

        PyouPersistentWindow.closeEvent(self, event)



def show(dialog_data):

    global _WINDOW_CACHE

    try:
        if _WINDOW_CACHE:
            _WINDOW_CACHE.close()
            _WINDOW_CACHE.deleteLater()
    except:
        pass

    _WINDOW_CACHE = PYRiggingDialogManager(dialog_data)
    _WINDOW_CACHE.show()

    return _WINDOW_CACHE