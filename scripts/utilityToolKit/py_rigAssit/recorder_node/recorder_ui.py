# -*- coding: utf-8 -*-
"""
PY_RIGASSIT BatchNodeRecorder Module

Developed by:
    YolandaPing

Based on:
    Original technology and framework by ZhiYong-H

License:
    Authorized modification and commercial use
"""

import os
from py_rigAssit import QtWidgets, QtCore, QtGui, QAction, Widgets, PyouPersistentWindow
from py_rigAssit.dialogs import Help, mayaPrint
from py_rigAssit.recorder_node.recorder_snapshot import (extract_template, save_template_to,
                               load_template, list_templates, rename_template,
                               template_dir)
from py_rigAssit.recorder_node.recorder_apply import apply_template
from Utils.undo import undo
import maya.cmds as cmds

_widgest = Widgets()

__version__ = "0.1.1"
__time__ = "2026"


class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setWindowTitle("About")
        self.resize(300, 220)
        layout = QtWidgets.QVBoxLayout(self)
        text = QtWidgets.QTextEdit()
        text.setReadOnly(True)
        text.setText(
            "Batch Node Recorder\n\n"
            "Supported Maya Versions:\n"
            "2018 - 2026\n\n"
            "===============================\n"
            "- Original Author: ZhiYong-H\n"
            "- Developed by: YolandaPing\n"
            "===============================\n"
            "- Status: Continued Development"
        )
        layout.addWidget(text)


def _pair_iter(scrs, tars):
    if len(scrs) == 1:
        for tgt in tars:
            yield scrs[0], tgt
    elif len(scrs) == len(tars):
        for src, tgt in zip(scrs, tars):
            yield src, tgt
    else:
        mayaPrint.error(u"仅支持一对一/一对多.")
        return


class BatchNodeRecorderUI(PyouPersistentWindow):
    BTN_A = ["", u"加载A(一个)", u"加载A(可批量)"]
    BTN_B = ["", u"加载B(可指定属性)", u"加载B(可批量)"]

    def __init__(self, parent=None):
        super(BatchNodeRecorderUI, self).__init__("PyouPersistentWindow", "PyouPersistentWindow", parent)
        self.setWindowTitle(u"Recorder Node " + __version__)
        self.resize(400, 460)
        self.template = None
        self.tem_name = None
        self.loadWindowSettings()
        self._settings = QtCore.QSettings("RecorderNode", "driveChain")
        self.build_ui()


    def build_ui(self):

        self.lbl_template = _widgest.create_text(u"模板：（未加载）")
        tpl_row = QtWidgets.QHBoxLayout()
        tpl_row.addWidget(self.lbl_template, 1)

        self.btn_load_tpl = QtWidgets.QPushButton(u"加载模板")
        self.list_tpl = QtWidgets.QListWidget()
        self.list_tpl.setToolTip(u"双击加载；右键：加载并应用/重命名/保存/删除")
        self.btn_refresh_tpl = QtWidgets.QPushButton(u"刷 新 列 表")
        self.dir_edit = QtWidgets.QLineEdit()
        self.dir_edit.setToolTip(u"模板目录，可直接修改，回车生效")

        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 4, 0)
        left_sec = _widgest.create_section(u"模板列表:")
        left_layout.addWidget(left_sec)
        left_sec.addWidget(self.btn_load_tpl)
        left_sec.addWidget(self.list_tpl)
        left_sec.addWidget(self.btn_refresh_tpl)
        left_sec.addWidget(self.dir_edit)

        self.list_a = QtWidgets.QListWidget()
        self.btn_load_a = QtWidgets.QPushButton(self.BTN_A[1])
        col_a = QtWidgets.QVBoxLayout()
        col_a.addWidget(self.btn_load_a)
        col_a.addWidget(self.list_a)

        self.list_b = QtWidgets.QListWidget()
        self.btn_load_b = QtWidgets.QPushButton(self.BTN_B[1])
        col_b = QtWidgets.QVBoxLayout()

        col_b.addWidget(self.btn_load_b)
        col_b.addWidget(self.list_b)

        self.node_block = _widgest.create_radiogroup(
            "",
            [("extract", 1, None),("import", 2, None)],default_id=1)
        list_sec = _widgest.create_section(u"载入对象: A 驱动源, B 被驱动目标")
        ab_layout = QtWidgets.QHBoxLayout()
        ab_layout.addLayout(col_a)
        ab_layout.addLayout(col_b)
        list_sec.addLayout(ab_layout)
        list_sec.addWidget(self.node_block)

        self.chk_allow_third = QtWidgets.QCheckBox(u'链接第三方')
        self.btn_extract = QtWidgets.QPushButton(u"提取模板")
        self.btn_save_tpl = QtWidgets.QPushButton(u"保存模板")
        self.btn_apply = QtWidgets.QPushButton(u" [应 用] ")

        mid_widget = QtWidgets.QWidget()
        mid_widget.setFixedHeight(40)
        mid_layout = QtWidgets.QHBoxLayout(mid_widget)
        mid_layout.setContentsMargins(0, 0, 0, 0)
        mid_layout.setSpacing(6)
        mid_layout.addWidget(self.chk_allow_third)
        mid_layout.addWidget(self.btn_extract)
        mid_layout.addWidget(self.btn_save_tpl)
        mid_layout.addStretch(1)
        mid_layout.addWidget(self.btn_apply)

        top_widget = QtWidgets.QWidget()
        top_layout = QtWidgets.QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(list_sec, 1)
        top_layout.addWidget(mid_widget, 0)

        text_sec = _widgest.create_section(u"信息:")
        self.text = QtWidgets.QTextEdit()
        self.text.setReadOnly(True)
        self.text.setMinimumHeight(80)
        text_sec.addWidget(self.text)
        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(top_widget)
        splitter.addWidget(text_sec)
        splitter.setSizes([100, 300])
        splitter.setHandleWidth(5)

        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)
        right_layout.setContentsMargins(4, 0, 0, 0)
        right_layout.addWidget(splitter)

        splitter_h = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter_h.addWidget(left_widget)
        splitter_h.addWidget(right_widget)
        splitter_h.setSizes([100, 300])
        splitter_h.setHandleWidth(5)

        overall = QtWidgets.QVBoxLayout(self)
        self.create_menu_bar(overall)
        overall.setContentsMargins(8, 0, 8, 8)
        overall.addWidget(_widgest.create_title("Recorder Node", 14))
        overall.addLayout(tpl_row)
        overall.addWidget(splitter_h, 1)
        _widgest.create_copyrightText(overall, "{} ZhiYong-H".format(__time__))

        self.node_block.idClicked.connect(self._on_type_toggled)
        self.btn_load_a.clicked.connect(self.load_a)
        self.btn_load_b.clicked.connect(self.load_b)
        self.dir_edit.returnPressed.connect(self.apply_dir_edit)
        self.btn_extract.clicked.connect(self.extract)
        self.btn_save_tpl.clicked.connect(self.save_tpl)
        self.btn_load_tpl.clicked.connect(self.load_tpl)
        self.btn_refresh_tpl.clicked.connect(self.refresh_tpl_list)
        self.list_tpl.itemDoubleClicked.connect(self.load_tpl_from_list)
        self.list_tpl.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list_tpl.customContextMenuRequested.connect(self.tpl_context_menu)
        self.btn_apply.clicked.connect(self.apply)

        self.refresh_tpl_list()
        self._restore_state()

    def create_menu_bar(self, parent_layout):
        menu_bar = QtWidgets.QMenuBar()
        about_menu = menu_bar.addMenu("About")
        act = about_menu.addAction("about")
        act.triggered.connect(self.show_about)
        parent_layout.setMenuBar(menu_bar)

    def show_about(self):
        dlg = AboutDialog(self)
        dlg.show()

    def _append_colored_text(self, text, color):
        cursor = self.text.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        fmt = QtGui.QTextCharFormat()
        fmt.setForeground(QtGui.QColor(color))
        cursor.insertText(text + "\n", fmt)
        self.text.setTextCursor(cursor)
        self.text.ensureCursorVisible()

    def log(self, msg):
        """根据消息前缀设置颜色：问题/警告=黄，错误=红，模板/加载/保存=绿，其他=白"""
        if u"[问题]" in msg or u"[警告]" in msg:
            color = "yellow"
        elif u"[错误]" in msg:
            color = "red"
        elif u"[模板]" in msg or u"加载成功" in msg or u"已加载" in msg or u"已保存" in msg:
            color = "green"
        else:
            color = "white"
        self._append_colored_text(msg, color)

    def _on_type_toggled(self, btn_id):
        self.btn_load_a.setText(self.BTN_A[btn_id])
        self.btn_load_b.setText(self.BTN_B[btn_id])

    def _last_dir(self):
        """上次保存/加载模板的目录（QSettings 记忆），默认 驱动链模板/"""
        d = self._settings.value("lastTemplateDir")
        if not d or not os.path.isdir(d):
            d = template_dir()
        return d

    @staticmethod
    def _items(listw):
        return [listw.item(i).text() for i in range(listw.count())]

    def _first_a(self):
        items = self._items(self.list_a)
        return items[0] if items else None

    # ---------- 列表操作 ----------

    def load_a(self):
        sels = cmds.ls(sl=True)
        if not sels:
            self.log(u"[提示] 请先选择物体")
            return
        node = sels[0]
        self.list_a.clear()
        if self.node_block.checkedId() == 1:
            self.list_a.addItem(node)
        else:
            self.list_a.addItems(sels)

    def load_b(self):
        sels = cmds.ls(sl=True)
        if not sels:
            self.log(u"[提示] 请先选择物体")
            return
        node = sels[0]
        self.list_b.clear()

        if self.node_block.checkedId() == 1:
            attrs = cmds.channelBox("mainChannelBox", q=True, sma=True) or []
            if attrs:
                for attr in attrs:
                    self.list_b.addItem("%s.%s" % (node, attr))
            else:
                self.list_b.addItem(node)
        else:
            self.list_b.addItems(sels)

    def parse_node_attrs(self, widget):
        nodes = []
        attrs = []
        for i in range(widget.count()):
            text = widget.item(i).text()
            if "." in text:
                node, attr = text.split(".", 1)
                nodes.append(node)
                attrs.append(attr)
            else:
                nodes.append(text)
        return (nodes[0] if nodes else None, attrs if attrs else None)

    # ---------- 状态记忆 ----------

    def _restore_state(self):
        """恢复上次的面板状态：仅当前模板和目录（A/B 列表每次开面板都清空）"""
        # 安全删除残留键
        if self._settings.contains("listA"):
            self._settings.remove("listA")
        if self._settings.contains("listB"):
            self._settings.remove("listB")
        tpl_path = self._settings.value("currentTemplatePath") or u""
        if tpl_path and os.path.isfile(tpl_path):
            self._load_tpl_path(tpl_path)

    def apply_dir_edit(self):
        d = self.dir_edit.text().strip()
        if not d:
            return
        if not os.path.isdir(d):
            self.log(u"[提示] 目录不存在: %s" % d)
            self.dir_edit.setText(self._last_dir())
            return
        self._settings.setValue("lastTemplateDir", d)
        self.refresh_tpl_list()
        self.log(u"[模板] 目录已切换: %s" % d)

    # ---------- 模板 ----------

    def extract(self):
        allow = self.chk_allow_third.isChecked()
        a, source_attrs = self.parse_node_attrs(self.list_a)
        b, target_attrs = self.parse_node_attrs(self.list_b)
        if not a or not b:
            self.log(u"[提示] 提取模板需要 A 列表第一个 + B 列表第一个（样本对）")
            return
        try:
            self.template = extract_template(
                a, b,
                target_attrs=target_attrs,
                log=self.log,
                allow_third_party=allow
            )
        except Exception as e:
            self.log(u"[错误] 提取失败: %s" % e)
            return
        self._settings.setValue("currentTemplatePath", "")
        self._refresh_template_label()
        mayaPrint.log(u"模板提取完成！")

    def _refresh_template_label(self):
        if not self.template:
            self.lbl_template.setText(u"当前模板：（未加载）")
            return
        t = self.template
        self.lbl_template.setText(u"当前模板：%s ｜ %s → [%d 节点] → %s" % (
            t.get("template_name", u"未命名"),
            t.get("sample_A", "?"),
            len(t.get("nodes", [])),
            t.get("sample_B", "?")))

    def save_tpl(self):
        if not self.template:
            self.log(u"[提示] 没有可保存的模板，请先提取或加载")
            return
        cur = self.template.get("template_name", u"未命名模板")
        default_path = os.path.join(self._last_dir(), cur + ".json")
        path, _flt = QtWidgets.QFileDialog.getSaveFileName(
            self, u"保存模板", default_path, u"模板文件 (*.json)",
            options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if not path:
            return
        if not path.lower().endswith(".json"):
            path += ".json"
        try:
            save_template_to(self.template, path)
        except Exception as e:
            self.log(u"[错误] 保存失败: %s" % e)
            return
        self._settings.setValue("lastTemplateDir", os.path.dirname(path))
        self._settings.setValue("currentTemplatePath", path)
        self._refresh_template_label()
        self.refresh_tpl_list()
        self.log(u"[模板] 已保存: %s" % path)

    def load_tpl(self):
        path, _flt = QtWidgets.QFileDialog.getOpenFileName(
            self, u"加载模板", self._last_dir(), u"模板文件 (*.json)",
            options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if not path:
            return
        self._load_tpl_path(path)
        self.refresh_tpl_list()

    def _load_tpl_path(self, path):
        try:
            self.template = load_template(path)
        except Exception as e:
            self.log(u"[错误] 加载失败: %s" % e)
            return

        self._settings.setValue("lastTemplateDir", os.path.dirname(path))
        self._settings.setValue("currentTemplatePath", path)
        self._refresh_template_label()
        self.log(u"[模板] 已加载: %s" % path)

    # ---------- 模板列表 ----------

    def refresh_tpl_list(self):
        self.list_tpl.clear()
        d = self._last_dir()
        self.dir_edit.setText(d)
        self.dir_edit.setToolTip(d)
        for name, path in list_templates(d):
            item = QtWidgets.QListWidgetItem(name)
            item.setData(QtCore.Qt.UserRole, path)
            item.setToolTip(path)
            self.list_tpl.addItem(item)

    def load_tpl_from_list(self, *args):
        item = self.list_tpl.currentItem()
        if item:
            self._load_tpl_path(item.data(QtCore.Qt.UserRole))

    def tpl_context_menu(self, pos):
        item = self.list_tpl.itemAt(pos)
        menu = QtWidgets.QMenu(self)
        if item is None:
            # 没有选中任何模板：仅显示"保存当前模板…"
            act_new = menu.addAction(u"保存当前模板…")
            act = menu.exec_(self.list_tpl.mapToGlobal(pos))
            if act == act_new:
                self.save_tpl_as()
            return

        # 有选中模板
        act_open_folder = menu.addAction(u"打开文件位置")
        menu.addSeparator()
        act_load = menu.addAction(u"加载")
        act_load_apply = menu.addAction(u"应用")
        menu.addSeparator()
        act_rename = menu.addAction(u"重命名")
        act_save = menu.addAction(u"保存（覆盖此项）")
        act_del = menu.addAction(u"删除")
        act = menu.exec_(self.list_tpl.mapToGlobal(pos))
        if act is None:
            return
        if act == act_load:
            self._load_tpl_path(item.data(QtCore.Qt.UserRole))
            self.tem_name = item.text()
            # print(self.tem_name)
        if act == act_load_apply:
            self._load_tpl_path(item.data(QtCore.Qt.UserRole))
            self.tem_name = item.text()
            self.apply()   # 加载后自动应用
        elif act == act_rename:
            self.rename_tpl_item(item)
        elif act == act_save:
            self.save_tpl_to_item(item)
        elif act == act_del:
            self.delete_tpl_item(item)
        elif act == act_open_folder:
            self.open_template_folder(item)



    def save_tpl_as(self):
        """右键-保存当前模板：命名后存到当前模板目录并进入列表"""
        if not self.template:
            self.log(u"[提示] 没有可保存的模板，请先提取或加载")
            return
        cur = self.template.get("template_name", u"未命名模板")
        name, ok = QtWidgets.QInputDialog.getText(
            self, u"保存当前模板", u"模板名：", text=cur)
        if not ok or not name.strip():
            return
        name = name.strip()
        for ch in '\\/:*?"<>|':
            name = name.replace(ch, "_")
        path = os.path.join(self._last_dir(), name + ".json")
        if os.path.exists(path):
            ok2 = QtWidgets.QMessageBox.question(
                self, u"覆盖确认", u"已存在同名模板，覆盖？\n%s" % path,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No)
            if ok2 != QtWidgets.QMessageBox.Yes:
                return
        try:
            save_template_to(self.template, path)
        except Exception as e:
            self.log(u"[错误] 保存失败: %s" % e)
            return
        self._settings.setValue("currentTemplatePath", path)
        self._refresh_template_label()
        self.refresh_tpl_list()
        self.log(u"[模板] 已保存: %s" % path)

    def rename_tpl_item(self, item):
        path = item.data(QtCore.Qt.UserRole)
        old = item.text()
        name, ok = QtWidgets.QInputDialog.getText(
            self, u"重命名模板", u"新名字：", text=old)
        if not ok or not name.strip() or name.strip() == old:
            return
        try:
            new_path = rename_template(path, name.strip())
        except Exception as e:
            self.log(u"[错误] 重命名失败: %s" % e)
            return
        if self.template and self.template.get("template_name") == old:
            self.template["template_name"] = name.strip()
            self._refresh_template_label()
        if (self._settings.value("currentTemplatePath") or u"") == path:
            self._settings.setValue("currentTemplatePath", new_path)
        self.refresh_tpl_list()
        self.log(u"[模板] 已重命名: %s -> %s" % (old, name.strip()))

    def open_template_folder(self, item):
        import subprocess,sys
        path = item.data(QtCore.Qt.UserRole)
        folder = os.path.dirname(path)
        if not os.path.isdir(folder):
            self.log(u"[错误] 文件夹不存在: %s" % folder)
            return
        if sys.platform == 'win32':
            os.startfile(folder)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', folder])
        else:
            subprocess.Popen(['xdg-open', folder])

    def save_tpl_to_item(self, item):
        if not self.template:
            self.log(u"[提示] 没有可保存的模板，请先提取或加载")
            return
        path = item.data(QtCore.Qt.UserRole)
        try:
            save_template_to(self.template, path)
        except Exception as e:
            self.log(u"[错误] 保存失败: %s" % e)
            return
        self._settings.setValue("currentTemplatePath", path)
        self._refresh_template_label()
        self.log(u"[模板] 已覆盖保存: %s" % path)

    def delete_tpl_item(self, item):
        path = item.data(QtCore.Qt.UserRole)
        ok = QtWidgets.QMessageBox.question(
            self, u"删除模板", u"确定删除模板文件？\n%s" % path,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        if ok != QtWidgets.QMessageBox.Yes:
            return
        try:
            os.remove(path)
        except Exception as e:
            self.log(u"[错误] 删除失败: %s" % e)
            return
        if (self._settings.value("currentTemplatePath") or u"") == path:
            self._settings.setValue("currentTemplatePath", "")
        self.refresh_tpl_list()
        self.log(u"[模板] 已删除: %s" % path)

    @undo
    def apply(self):
        if not self.template:
            self.log(u"[提示] 请先提取或加载模板")
            return
        # a = self._first_a()
        srcs = self._items(self.list_a)
        tgts = self._items(self.list_b)

        if not srcs:
            self.log(u"[提示] A 列表为空（驱动源，取第一个）")
            return
        if not tgts:
            self.log(u"[提示] B 列表为空（被驱动，可多个）")
            return

        self.log(u"==== 套用模板：%s ->  %s个Source %s个Target ====" % (self.tem_name, len(srcs), len(tgts)))
        for src, tgt in _pair_iter(srcs, tgts):
            apply_template(self.template, src, [tgt], log=self.log)

        mayaPrint.log(u"模板导入成功！")


def show():
    """批量应用驱动链面板（模板套用）"""
    global batch_apply_ui
    try:
        batch_apply_ui.close()
        batch_apply_ui.deleteLater()
    except (NameError, AttributeError, RuntimeError):
        pass
    batch_apply_ui = BatchNodeRecorderUI()
    batch_apply_ui.show()
    return batch_apply_ui


if __name__ == '__main__':
    show()