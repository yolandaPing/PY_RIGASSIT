# -*- coding: utf-8 -*-

# .FileName:manager.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2025/7/24 21:19
# .Finish time:
import os, webbrowser
import traceback
import xml.etree.ElementTree as ET

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

_MENU_CONFIG_CACHE = None
_MENU_CONFIG_FILE = "menu_config.xml"


try:
    text_type = unicode  # noqa: F821  (Python 2)
except NameError:
    text_type = str      # Python 3


def _to_text(s):
    """统一转成 text_type（Py2: unicode, Py3: str），用于 Qt / XML。"""
    if s is None:
        return None
    if isinstance(s, text_type):
        return s
    # bytes -> text
    try:
        return s.decode("utf-8")
    except Exception:
        try:
            return s.decode("gbk")
        except Exception:
            return s



def load_menu_config(force_reload=False):
    """
    读取 menu_config.xml（带缓存）。
    返回: { menu_name: [item_dict, ...] }

    item_dict:
        {"type": "separator"}
        {
            "type": "item",
            "label": text_type,
            "command": text_type or None,
            "bold": bool,
            "enabled": bool,
            "checkable": bool,
            "checked": bool,
            "item_id": text_type or None,
        }
    """
    global _MENU_CONFIG_CACHE
    if _MENU_CONFIG_CACHE is not None and not force_reload:
        return _MENU_CONFIG_CACHE

    xml_path = os.path.join(os.path.dirname(__file__), _MENU_CONFIG_FILE)
    data = {}

    if not os.path.exists(xml_path):
        print("[menu_config] not found: {}".format(xml_path))
        _MENU_CONFIG_CACHE = data
        return data

    try:
        # Py2.7 / Py3 的 ElementTree 会自动识别 XML 声明的 encoding
        root = ET.parse(xml_path).getroot()
    except Exception as e:
        print("[menu_config] parse failed: {}".format(e))
        _MENU_CONFIG_CACHE = data
        return data

    def _bool(el, key, default=False):
        v = el.get(key)
        if v is None:
            return default
        # ElementTree 返回 text_type；lower 后跟 str 比较在 Py2/Py3 都安全
        return v.strip().lower() in ("1", "true", "yes", "on")

    for menu_el in root.findall("menu"):
        menu_name = _to_text(menu_el.get("name"))
        if not menu_name:
            continue
        menu_name = menu_name.strip()
        if not menu_name:
            continue

        items = []
        for child in menu_el:
            tag = child.tag.lower()

            if tag == "separator":
                items.append({"type": "separator"})
                continue

            if tag != "item":
                continue

            label = _to_text(child.get("label")) or u""
            command = _to_text(child.get("command"))
            if command is not None:
                command = command.strip() or None

            item_id = _to_text(child.get("id"))
            if item_id is not None:
                item_id = item_id.strip() or None

            items.append({
                "type": "item",
                "label": label.strip(),
                "command": command,
                "bold": _bool(child, "bold", False),
                "enabled": _bool(child, "enabled", True),
                "checkable": _bool(child, "checkable", False),
                "checked": _bool(child, "checked", False),
                "item_id": item_id,
            })

        data[menu_name] = items

    _MENU_CONFIG_CACHE = data
    return data


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
    QtWidgets.QApplication.clipboard().setText(_to_text(text))

    try:
        cmds.inViewMessage(
            amg=msg or u"Copied: <hl>{}</hl>".format(text),
            pos="midCenter",
            fade=True
        )
    except:
        print(msg or u"Copied: {}".format(text))


class PYAboutDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PYAboutDialog, self).__init__(parent)
        self.setWindowTitle(u"About")
        self.resize(200, 220)
        layout = QtWidgets.QVBoxLayout(self)
        text = QtWidgets.QTextEdit()
        text.setReadOnly(True)
        text.setText(
            u"PY_RIGASSIT\n\n"
            u"Supported Maya Versions:\n"
            u"2018 - 2026\n\n"
            u"Features:\n"
            u"- Joint\n"
            u"- IKFK\n"
            u"- Copy Weight/BlendShape/FFD/UV/SDK/Deform\n"
            u"- Copy Attribute\n"
            u"- Mirror Attribute/SDK/Deform Weight\n"
            u"- Editor BlendShape/SDK\n"
            u"- Dirver Pose system\n"
            u"- Openpipeline\n"
            u"- Rivet Follice Tool\n"
            u"- Combine SDK Driven\n"
            u"- Transfer uv shader Tool\n"
            u"- Animation Tool\n"
            u"- Hotbox Designer\n"
            u"- ......\n"
            u"Rebuilt for production pipeline."
        )
        layout.addWidget(text)


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

        # 单个 QAction 生成器
        def add(menu, label, callback=None, checkable=False, checked=False,
                item_id=None, bold=False):

            label = _to_text(label) or u""
            act = QAction(label, self)  # FIX parent

            if bold:
                f = act.font()
                f.setBold(True)
                act.setFont(f)

            if checkable:
                act.setCheckable(True)
                act.setChecked(checked)

                name = item_id or label

                def _cb(n=name, a=act, *args):
                    return_checkBox(n, a.isChecked())

                act.triggered.connect(_cb)

            if callback:
                act.triggered.connect(callback)

            menu.addAction(act)

            # FIX GC
            self._actions.append(act)

            return act

        # 根据 XML 生成一个菜单 
        def build_from_config(menu_name):
            menu = self.menu_bar.addMenu(_to_text(menu_name))
            items = load_menu_config().get(menu_name, [])

            for item in items:
                if item["type"] == "separator":
                    menu.addSeparator()
                    continue

                cmd = item.get("command")
                callback = (
                    (lambda *a, **kw: self.dispatcher.execute(cmd))
                    if cmd else None
                )

                act = add(
                    menu,
                    item["label"],
                    callback=callback,
                    checkable=item.get("checkable", False),
                    checked=item.get("checked", False),
                    item_id=item.get("item_id"),
                    bold=item.get("bold", False),
                )

                if not item.get("enabled", True):
                    act.setEnabled(False)

            return menu

        # ---------------- ABOUT ----------------
        about = self.menu_bar.addMenu(u"About")

        add(about, u"bilibili: 我有一只猛犬",
            callback=lambda: webbrowser.open("https://space.bilibili.com/3493142019967757"))
        add(about, u"pyrigassit@gmail.com", callback=self._copy_email)
        sep = about.addAction(u"PY_RIGASSIT")
        sep.setEnabled(False)
        about.addSeparator()
        add(about, u"Update",
            callback=lambda: webbrowser.open(self._info[-2] if self._info else ""))
        add(about, u"Quark 夸克网盘",
            callback=lambda: webbrowser.open(self._info[-1] if self._info else ""))
        add(about, u"About", callback=self.show_about)

        # ---------------- CLEAR  (XML driven) ----------------
        build_from_config("Clear")

        # ---------------- TOOL   (XML driven) ----------------
        build_from_config("Tool")

        # ---------------- OPTIONS ----------------
        opt = self.menu_bar.addMenu(u"Options")
        opt.addAction(u"Convenient").setEnabled(False)
        add(opt, u"Use shelfButton New",
            checkable=True, checked=ud.shelfButton_New)
        add(opt, u"Auto import Hotkey",
            checkable=True, checked=ud.hotkey)
        add(opt, u"Auto add sec/pri grp",
            checkable=True, checked=ud.Grp_prisec)
        opt.addSeparator()
        opt.addAction(u"Window Display").setEnabled(False)
        add(opt, u"Dock",
            callback=self.to_dock_mode)
        add(opt, u"Reload Theme",
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

        self.logo_text = QtWidgets.QLabel(u"PY_RIGASSIT {}".format(self.VERSION))
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

            self.tabs.addTab(page, _to_text(name))

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
        if state is None:
            
            for k, v in self._tab_state.items():
                if _to_text(k) == name:
                    state = v
                    break

        if not state or state["loaded"]:
            return

        builder = self.ui_contents.get(name)
        if builder is None:
            for k, v in self.ui_contents.items():
                if _to_text(k) == name:
                    builder = v
                    break

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
        email = u"pyrigassit@gmail.com"
        copy_to_clipboard(email, u"Email copied")
        QtWidgets.QMessageBox.information(self, u'Email copied', u'邮箱复制成功')

    def init_marking_menu(self):

        self.mm_normal = PYMarkingMenuLite([
            (u" select skin joint ", lambda: self.dispatcher.execute("Select Skin joints")),
            (u" select child joint ", lambda: self.dispatcher.execute("Select Child joints")),
            (u" mirror skin ", lambda: self.dispatcher.execute("Mirror Skin", False)),
            (u" mirror skin l>r ", lambda: self.dispatcher.execute("Mirror Skin")),
            (u" copy skin ", lambda: self.dispatcher.execute("Copy Skin")),
            (u" combine skinWeight ", lambda: self.dispatcher.execute("Combine Skinweight")),
            (u" Resrt Skin Pose ", lambda: self.dispatcher.execute("Resrt Skined Pose")),
            (u" Remove unInfluences ", lambda: self.dispatcher.execute("Remove unInfluences")),

        ], self)

        self.mm_ctrl = PYMarkingMenuLite([
            (u" curve link ", lambda: self.dispatcher.execute("Curve Keep Linked", False)),
            (u" curve keep link ", lambda: self.dispatcher.execute("Curve Keep Linked", True)),
            (u" surface link ", lambda: self.dispatcher.execute("Linked Surface")),
            (u" select input node ", lambda: self.dispatcher.execute("Select Input Node")),
            (u" delete orig node ", lambda: self.dispatcher.execute("Delete Orig Nodes")),
            (u" create joint ", lambda: self.dispatcher.execute("Create Joints")),
            (u" joint add shape ", lambda: self.dispatcher.execute("Joints Add Shape")),
            (u" curve create joints ", lambda: self.dispatcher.execute("Curve Create Joint")),

        ], self)

        self.mm_shift = PYMarkingMenuLite([
            (u" OLD PY_RIGASSIT", lambda: self.dispatcher.execute("OLD PY_RIGASSIT")),
            (u" Rename", lambda: self.dispatcher.execute("Rename")),
            (u" Joint Orient ", lambda: self.dispatcher.execute("Joint Orient")),
            (u" InsertJoints ", lambda: self.dispatcher.execute("InsertJoints")),
            (u" IKFK Rigging ", lambda: self.dispatcher.execute("IKFK Rigging")),
            (u" Follow World ", lambda: self.dispatcher.execute("Follow World")),
            (u" Attribute Edit ", lambda: self.dispatcher.execute("Attribute Edit")),
            (u" Convert Drivenkeys ", lambda: self.dispatcher.execute("Convert Drivenkeys")),

        ], self)

    def show_about(self):
        dlg = PYAboutDialog(self)
        dlg.show()

    def reload_theme(self):
        # 重新加载 XML 菜单配置（下次重建窗口生效）
        load_menu_config(force_reload=True)
        try:
            ThemeManager.reload(self)
        except:
            pass

    def to_dock_mode(self):

        try:

            from py_rigAssit.dialogs.DockWindowBase import DockWindowBase

            # ---------------------------------
            dialog_data = self.dialog_data
            title = self.title
            widget_cls = self.__class__

            # ---------------------------------
            self.close()

            # ---------------------------------
            QtCore.QTimer.singleShot(
                0,
                lambda: DockWindowBase.safe_dock(
                    lambda: widget_cls(dialog_data),
                    title
                )
            )

        except Exception as e:

            print("Dock Failed: {}".format(e))

    def mousePressEvent(self, event):

        if event.button() == QtCore.Qt.RightButton:

            global_pos = self.mapToGlobal(event.pos())

            if event.modifiers() & QtCore.Qt.ControlModifier:
                self.mm_ctrl.start(global_pos)
            elif event.modifiers() & QtCore.Qt.ShiftModifier:
                self.mm_shift.start(global_pos)
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