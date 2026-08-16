# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import re
import json
import codecs
import subprocess

from functools import partial

from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
from ui_framework.widgets.button import GridButtons
from py_rigAssit.dialogs import decorator, mayaPrint
from py_rigAssit.common.command_dispatcher import CommandDispatcher
import py_rigAssit.common.img_commands
import maya.cmds as mc
import maya.mel as mel


PY_WIDGEAT = Widgets()


class PYScriptManagerCore(object):

    CONFIG_NAME = "py_melScriptManagerPath_config.json"

    def __init__(self):
        self.script_type = "mel"

        self.root_path = self.get_root_path()
        self.config_path = os.path.join(
            self.root_path,
            self.CONFIG_NAME
        )

        self.mel_dir, self.py_dir = self.load_dirs()

    def get_root_path(self):
        from py_rigAssit.dialogs import base_dir
        path = os.path.join(base_dir, "scripts")

        if not os.path.exists(path):
            os.makedirs(path)

        return path.replace("\\", "/")

    def load_dirs(self):
        mel_dir = ""
        py_dir = ""

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    data = json.load(f)

                mel_dir = data.get("mel_script_path", "")
                py_dir = data.get("py_script_path", "")
            except:
                pass

        default_mel = os.path.join(
            self.root_path,
            "custom_MEL_Scripts"
        ).replace("\\", "/")

        default_py = os.path.join(
            self.root_path,
            "custom_PY_Scripts"
        ).replace("\\", "/")

        mel_dir = mel_dir or default_mel
        py_dir = py_dir or default_py

        for d in (mel_dir, py_dir):
            if not os.path.exists(d):
                os.makedirs(d)

        self.save_dirs(mel_dir, py_dir)

        return mel_dir, py_dir

    def save_dirs(self, mel_dir, py_dir):
        try:
            with open(self.config_path, "w") as f:
                json.dump({
                    "mel_script_path": mel_dir,
                    "py_script_path": py_dir
                }, f, indent=4)
        except:
            pass

    def current_dir(self):
        return self.mel_dir if self.script_type == "mel" else self.py_dir

    def current_ext(self):
        return ".mel" if self.script_type == "mel" else ".py"

    # -----------------------------------------------------
    def clean_name(self, text):
        text = re.sub(r"\W+", "_", text.strip())

        if not text:
            return None

        if text[0].isdigit():
            text = "tool_" + text

        return text

    def list_scripts(self):
        """原方法保留，供管理器内部使用"""
        path = self.current_dir()
        ext = self.current_ext()

        if not os.path.exists(path):
            return []

        data = []

        for f in os.listdir(path):
            if f.endswith(ext):
                data.append(f[:-len(ext)])

        data.sort()
        return data

    def save_script(self, name, content):
        name = self.clean_name(name)

        if not name:
            mayaPrint.error("Invalid Name")
            return

        path = os.path.join(
            self.current_dir(),
            name + self.current_ext()
        )

        try:
            codecs.open(path, "w", "utf-8").write(content)
        except:
            open(path, "w").write(content)

    def run_script(self, full_path, script_type):
        """原运行方法，保留兼容"""
        # path = os.path.join(
        #     self.current_dir(),
        #     name + self.current_ext()
        # )
        #
        # if not os.path.exists(path):
        #     mayaPrint.error("Script not found")
        #     return
        mc.undoInfo(openChunk=True)
        try:
            self.run_script_file(full_path, script_type)
        finally:
            mc.undoInfo(closeChunk=True)

    def run_script_file(self, full_path, script_type):
        """通用脚本执行方法，根据类型执行 mel 或 python 脚本"""
        if not os.path.exists(full_path):
            mayaPrint.error("Script not found: {}".format(full_path))
            return

        if script_type == "mel":
            mel.eval('source "{}";'.format(full_path.replace("\\", "/")))
        else:  # python
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    code = f.read()
            except:
                with open(full_path, "r") as f:
                    code = f.read()
            exec(compile(code, full_path, "exec"), {})

            # try:
            #     code = codecs.open(full_path, "r", "utf-8").read()
            # except:
            #     code = open(full_path, "r").read()
            #
            # exec(compile(code, full_path, "exec"), {})

    def open_folder(self):
        path = self.current_dir()

        if os.name == "nt":
            os.startfile(path)
        else:
            subprocess.Popen(["open", path])

    def gui_open_folder(self, type):
        path =  self.mel_dir if type == "mel" else self.py_dir
        if os.name == "nt":
            os.startfile(path)
        else:
            subprocess.Popen(["open", path])


class PYScriptManagerWindow(object):

    WIN = "pymelScriptManagerDialog"

    def __init__(self, core, refresh_callback=None):
        self.core = core
        self.refresh_callback = refresh_callback   # 外部刷新回调（无参）

    # -----------------------------------------------------
    def show(self):

        if mc.window(self.WIN, q=True, ex=True):
            mc.deleteUI(self.WIN)

        mc.window(
            self.WIN,
            t="MEL / Python Script Manager",
            wh=(420, 500)
        )

        self.build_ui()
        self._update_template()
        mc.showWindow(self.WIN)

    # -----------------------------------------------------
    def build_ui(self):

        form = mc.formLayout()

        top = mc.columnLayout(adj=True, rs=6)

        mc.text(l="Script Manager")

        self.type_radio = mc.radioButtonGrp(
            label="Script Type:  ",
            labelArray2=["MEL", "Python"],
            numberOfRadioButtons=2,
            select=1,
            cc=self.on_type_changed
        )

        mc.rowColumnLayout(nc=2, adj=2)
        mc.text(l="Name:")
        self.name_field = mc.textField()
        mc.setParent("..")

        mc.text(l="Script Content")
        mc.setParent("..")

        # editor
        mid = mc.frameLayout(lv=0)

        self.content_field = mc.scrollField(
            text="// global proc yourProc(){\n// }\n"
        )

        mc.setParent("..")

        # bottom
        bottom = mc.columnLayout(adj=True, rs=6)

        self.path_txt = mc.text(
            l="Save Path: " + self.core.current_dir()
        )

        mc.button(
            l="Save",
            h=32,
            c=self.save_script
        )

        mc.rowColumnLayout(nc=4, adj=1)

        self.search_field = mc.textField(
            placeholderText="Search...",
            cc=self.refresh_buttons
        )

        mc.button(
            l="Refresh",
            c=self.refresh_buttons
        )

        mc.text(l="")

        mc.button(
            l="Open Folder",
            c=lambda *_: self.core.open_folder()
        )

        mc.setParent("..")
        mc.setParent("..")

        mc.formLayout(
            form,
            e=True,

            attachForm=[
                (top, "top", 5),
                (top, "left", 5),
                (top, "right", 5),

                (mid, "left", 5),
                (mid, "right", 5),

                (bottom, "left", 5),
                (bottom, "right", 5),
                (bottom, "bottom", 5),
            ],

            attachControl=[
                (mid, "top", 5, top),
                (mid, "bottom", 5, bottom),
            ]
        )

    # -----------------------------------------------------
    def on_type_changed(self, *_):

        idx = mc.radioButtonGrp(
            self.type_radio,
            q=True,
            select=True
        )

        self.core.script_type = "mel" if idx == 1 else "py"

        mc.text(
            self.path_txt,
            e=True,
            l="Save Path: " + self.core.current_dir()
        )

        self._update_template()
        self.refresh_buttons()

    # -----------------------------------------------------
    def save_script(self, *_):

        name = mc.textField(
            self.name_field,
            q=True,
            text=True
        )

        content = mc.scrollField(
            self.content_field,
            q=True,
            text=True
        )

        self.core.save_script(name, content)

        mc.textField(
            self.name_field,
            e=True,
            text=""
        )

        self.refresh_buttons()

    def _update_template(self):

        if self.core.script_type == "mel":
            text = "// global proc yourProcName() {\n// }\n"
        else:
            text = "# -*- coding: utf-8 -*-\n\n"

        if hasattr(self, "content_field"):
            mc.scrollField(
                self.content_field,
                e=True,
                text=text
            )

    # -----------------------------------------------------
    def refresh_buttons(self, *_):
        if self.refresh_callback:
            self.refresh_callback()


class PYScriptButtonsPanel(object):

    def __init__(self, layout, core):
        self.layout = layout
        self.core = core

    def clear(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            w = item.widget()

            if w:
                w.deleteLater()

    def build_buttons(self, scripts_info):
        """
        scripts_info: list of dict or tuple (display_name, script_type, full_path)
        """
        self.clear()

        if not scripts_info:
            return

        row = 0
        col = 0
        max_col = 4

        for i, info in enumerate(scripts_info):
            # 兼容两种传入格式
            if isinstance(info, dict):
                display = info['display']
                stype = info['type']
                path = info['path']
            else:
                display, stype, path = info

            btn = QtWidgets.QPushButton(display)
            btn.setFixedHeight(28)
            btn.setProperty("cld_custom", True)
            # btn.clicked.connect(partial(self.core.run_script_file, path, stype))
            btn.clicked.connect(partial(self.core.run_script, path, stype))
            self.layout.addWidget(btn, row, col)
            col += 1
            if col >= max_col:
                col = 0
                row += 1


class PYCustomLayout(QtWidgets.QWidget):


    def __init__(self, parent=None):
        super(PYCustomLayout, self).__init__( parent)


    def init_ui(self):
        container = QtWidgets.QWidget()
        main = QtWidgets.QVBoxLayout(container)
        main.setContentsMargins(2, 2, 2, 2)
        main.setSpacing(2)

        main.addWidget(PY_WIDGEAT.create_title("Custom", 15, None))
        # main.addWidget(
        #     self.build_artist_tab()
        # )
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setContentsMargins(0, 0, 0, 0)

        cld_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(cld_widget)
        scroll_layout.setContentsMargins(6, 0, 6, 0)
        scroll_layout.setSpacing(6)

        scroll.setWidget(cld_widget)
        main.addWidget(scroll)
        scroll_layout.addWidget(self.build_artist_tab())

        scroll_layout.addStretch()

        return container

    def build_artist_tab(self):

        self.dispatcher = CommandDispatcher()

        page = QtWidgets.QWidget()
        lay = QtWidgets.QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 4, 0)
        lay.setSpacing(4)

        sec1 = PY_WIDGEAT.create_section("Artist:")
        sec1.setContentsMargins(0, 0, 4, 0)
        grid1 = GridButtons("artist_tool", 3)
        grid1.clicked.connect(self.run_action)
        sec1.addWidget(grid1)

        # Custom 区域
        sec2 = PY_WIDGEAT.create_section("Custom:")
        sec2.setContentsMargins(0, 0, 4, 0)
        sec2.addWidget(PY_WIDGEAT.create_text(u"> 下面是用户自定义脚本管理 <"))
        wrapper = QtWidgets.QVBoxLayout()
        self.core = PYScriptManagerCore()
        sc_bth_layout = QtWidgets.QHBoxLayout()
        browse_btn = QtWidgets.QPushButton()
        browse_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        browse_btn.setToolTip(U"打开脚本路径")
        btn_layout, self.open_manager_btn, manager_help_btn = PY_WIDGEAT.create_Qbuttons(" Scripts Manager ")
        sc_bth_layout.addWidget(browse_btn)
        sc_bth_layout.addLayout(btn_layout)
        wrapper.addLayout(sc_bth_layout)
        filter_group = QtWidgets.QWidget()
        filter_layout = QtWidgets.QHBoxLayout(filter_group)
        filter_layout.setContentsMargins(4, 0, 4, 0)

        self.filter_buttons = QtWidgets.QButtonGroup()
        self.radio_mel = QtWidgets.QRadioButton(" MEL ")
        self.radio_py = QtWidgets.QRadioButton("PYTHON")
        self.radio_all = QtWidgets.QRadioButton("  ALL  ")
        self.radio_all.setChecked(True)
        self.current_filter = "all"
        for i, rb in enumerate([self.radio_mel, self.radio_py, self.radio_all]):
            filter_layout.addWidget(rb)
            self.filter_buttons.addButton(rb, (i+1))
        self.radio_mel.toggled.connect(lambda checked: self.on_filter_changed('mel', checked))
        self.radio_py.toggled.connect(lambda checked: self.on_filter_changed('py', checked))
        self.radio_all.toggled.connect(lambda checked: self.on_filter_changed('all', checked))
        wrapper.addWidget(filter_group)
        PY_WIDGEAT.separator(wrapper, True)
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 4, 0)
        self.grid_layout.setSpacing(2)
        wrapper.addLayout(self.grid_layout)
        sec2.addLayout(wrapper)
        self.panel = PYScriptButtonsPanel(self.grid_layout, self.core)
        self.manager = PYScriptManagerWindow(
            self.core,
            refresh_callback=self.refresh_custom_buttons
        )

        self.refresh_custom_buttons()
        # -------------------------------------------------
        self.open_manager_btn.clicked.connect(self.manager.show)
        browse_btn.clicked.connect(self.browse_path)
        manager_help_btn.clicked.connect(lambda: self.dispatcher.execute("Show Help", 18))
        lay.addWidget(sec1)
        lay.addWidget(sec2)
        lay.addStretch()

        return page

    # -----------------------------------------------------
    def on_filter_changed(self, filter_name, checked):
        if checked:
            self.current_filter = filter_name
            self.refresh_custom_buttons()

    # -----------------------------------------------------
    def refresh_custom_buttons(self):
        """根据当前过滤模式，收集脚本信息并刷新按钮面板"""
        scripts_info = []
        if self.current_filter == 'mel':
            scripts_info = self._collect_scripts_from_dir(self.core.mel_dir, 'mel')
        elif self.current_filter == 'py':
            scripts_info = self._collect_scripts_from_dir(self.core.py_dir, 'py')
        else:  # all
            mel_scripts = self._collect_scripts_from_dir(self.core.mel_dir, 'mel')
            py_scripts = self._collect_scripts_from_dir(self.core.py_dir, 'py')
            scripts_info = self._merge_with_suffix(mel_scripts, py_scripts)

        self.panel.build_buttons(scripts_info)

    # -----------------------------------------------------
    def _collect_scripts_from_dir(self, directory, script_type):
        if not os.path.exists(directory):
            return []
        ext = '.mel' if script_type == 'mel' else '.py'
        scripts = []
        for f in os.listdir(directory):
            if f.endswith(ext):
                name = f[:-len(ext)]
                full_path = os.path.join(directory, f).replace('\\', '/')
                scripts.append((name, script_type, full_path))
        scripts.sort(key=lambda x: x[0])
        return scripts

    # -----------------------------------------------------
    def _merge_with_suffix(self, mel_list, py_list):
        """
        合并 mel 和 py 脚本列表，如果有同名脚本则在显示名称上添加后缀。
        返回格式: [{'display': 'xxx', 'type': 'mel', 'path': '...'}, ...]
        """
        # 收集所有名称
        name_count = {}
        for name, typ, path in mel_list + py_list:
            name_count[name] = name_count.get(name, 0) + 1

        result = []
        for name, typ, path in mel_list:
            display = name
            if name_count[name] > 1:
                display = "{} [MEL]".format(name)
            result.append({'display': display, 'type': typ, 'path': path})

        for name, typ, path in py_list:
            display = name
            if name_count[name] > 1:
                display = "{} [PY]".format(name)
            result.append({'display': display, 'type': typ, 'path': path})

        # 按显示名称排序
        result.sort(key=lambda x: x['display'])
        return result


    def run_action(self, text):
        if hasattr(self, "dispatcher"):
            self.dispatcher.execute(text)

    def browse_path(self):
        id = self.filter_buttons.checkedId()
        if id == 3:
            mayaPrint.log(u"选择前面两者")
            return

        maps = {1: "mel",
         2:"python"}
        self.core.gui_open_folder(maps[id])


class PYCustomDiadlg(PyouPersistentWindow):

    def __init__(self, parent=None):
        super(PYCustomDiadlg, self).__init__("PYIKFKLayoutDlg", "PYIKFKLayoutDlg", parent)

        self.setWindowTitle("IFKF Rigging Dialog")
        self.resize(360, 680)

        self._build_ui()


    def _build_ui(self):
        main = QtWidgets.QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(4)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setContentsMargins(0, 0, 0, 0)

        cld_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(cld_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(4)

        scroll.setWidget(cld_widget)
        main.addWidget(scroll)

        widget = PYCustomLayout(parent=self)
        scroll_layout.addWidget(widget.init_ui())


def main():

    global py_custom_dialog
    try:
        py_custom_dialog.close()  # pylint: disable=E0601
        py_custom_dialog.deleteLater()
    except:
        pass

    py_custom_dialog = PYCustomDiadlg()
    py_custom_dialog.show()


if __name__ == "__main__":
    main()