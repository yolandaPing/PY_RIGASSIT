# -*- coding: utf-8 -*-

"""
Hotbox Designer (Modified Version)

Original project:
    Hotbox Designer
    Author: luckylyk
    Source: https://github.com/luckylyk/hotbox_designer

Modifications:
    Copyright (c) 2026 Yolanda Ping (You P)
    - Added PY_RIGASSIT integration
    - Qt6 compatibility layer
    - UI/UX improvements
    - Bug fixes and performance optimizations

License:
    This project is based on the original license.
"""

import json
import os
from functools import partial
try:
    from ui_framework.core.qtCompat import *

except ImportError:
    from CommonUse.qtCompat import *

import hotbox_designer
from hotbox_designer.commands import OPEN_COMMAND, CLOSE_COMMAND, SWITCH_COMMAND
from hotbox_designer.reader import HotboxReader
from hotbox_designer.designer.application import HotboxEditor
from hotbox_designer.applications import Nuke, Maya, Houdini
from hotbox_designer.widgets import BoolCombo, Title, CommandButton
from hotbox_designer.qtutils import icon
from hotbox_designer.dialog import (
    import_hotbox, export_hotbox, import_hotbox_link, CreateHotboxDialog,
    CommandDisplayDialog, HotkeySetter, warning)
from hotbox_designer.data import (
    get_valid_name, TRIGGERING_TYPES, save_datas, load_hotboxes_datas,
    hotbox_data_to_html, load_json, ensure_old_data_compatible)
from hotbox_designer.data import save_nested_hotbox,load_nested_hotbox
from hotbox_designer.nested_hotbox import NestedHotboxReader
from hotbox_designer.common.translator import tr
from hotbox_designer.common import translator

translator.set_language("en")


def get_py_rigassit_root():
    """
    返回当前工具所在 PY_RIGASSIT 根目录
    """
    current_dir = os.path.dirname(__file__)
    utility_dir = os.path.dirname(current_dir)
    scripts_dir = os.path.dirname(utility_dir)
    py_rigassit_root = os.path.dirname(scripts_dir)
    return py_rigassit_root

PY_RIGASSIT_ROOT = get_py_rigassit_root()
UTILITY_DIR = os.path.join(PY_RIGASSIT_ROOT, 'scripts', 'utilityToolKit')
TEMPLATE_DIR = os.path.join(UTILITY_DIR, 'py_rigassit_hottemp')
TEMPLATE_FILE = os.path.join(TEMPLATE_DIR, 'PY_RIGASSIT.json')
TARGET_FILE = os.path.join(UTILITY_DIR, 'PY_RIGASSIT_hotboxes.json')

hotboxes = {}
hotbox_manager = None
APPLICATIONS = {'maya': Maya, 'nuke': Nuke, 'houdini': Houdini}

BOXTITLE = 'Hotbox Designer (modified | Maya 2019–2026)'


def launch_manager(application):
    global hotbox_manager
    if hotbox_manager is None:
        hotbox_manager = HotboxManager(APPLICATIONS[application]())
    hotbox_manager.show()


def initialize(application):
    if hotboxes:
        return
    load_hotboxes(application)


def load_hotboxes(application):
    hotboxes_datas = load_hotboxes_datas(application.local_file)
    file_ = application.shared_file

    print("shared_file:", file_)
    # print("shared_data raw:", load_json(file_))

    shared_raw = load_json(file_, default=[])

    if not isinstance(shared_raw, list):
        shared_raw = []

    hotboxes_datas += [
        ensure_old_data_compatible(load_json(f, default={}))
        for f in shared_raw if f
    ]

    # hotboxes_datas += [
    #     ensure_old_data_compatible(load_json(f)) for f in load_json(file_)]

    for hotboxes_data in hotboxes_datas:
        name = hotboxes_data['general']['name']
        reader = HotboxReader(hotboxes_data, parent=None)
        reader.hideSubmenusRequested.connect(hide_submenus)
        hotboxes[name] = reader
    
    for hotboxes_data in hotboxes_datas:
        hotboxes_data = load_nested_hotbox(hotboxes_data)
        name = hotboxes_data['general']['name']
        reader = NestedHotboxReader(hotboxes_data, parent=None)  # 增强版
        reader.hideSubmenusRequested.connect(hide_submenus)
        hotboxes[name] = reader


def clear_loaded_hotboxes():
    global hotboxes
    hotboxes = {}


def show(name):
    hb = hotboxes.get(name)
    if hb:
        hb.show()


def hide(name):
    hb = hotboxes.get(name)
    if hb:
        hb.hide()


def switch(name):
    hb = hotboxes.get(name)
    if not hb:
        return

    if hb.isVisible():
        hb.hide()
    else:
        hb.show()


def hide_submenus():
    for name in hotboxes:
        if hotboxes[name].is_submenu:
            hide(name)


def replace_image_paths(hotbox_data):
    """
    image.path，将 PY_RIGASSIT 前的路径替换为当前工具的 PY_RIGASSIT 根目录。
    """
    for shape in hotbox_data.get('shapes', []):
        img_path = shape.get('image.path', '')

        if img_path and '/icons' in img_path:
            rel_path = img_path.split("/icons")[0]
            suf_path = "/icons" + img_path.split("/icons")[-1]
            # new_path = os.path.join(PY_RIGASSIT_ROOT, rel_path).replace('\\', '/')
            new_path = PY_RIGASSIT_ROOT + suf_path
            shape['image.path'] = new_path

        if shape.get('submenu_data'):
            replace_image_paths(shape['submenu_data'])
    return hotbox_data


class HotboxManager(QtWidgets.QWidget):
    def __init__(self, application):
        parent = application.main_window
        super(HotboxManager, self).__init__(parent, QtCore.Qt.Tool)
        self.setWindowTitle(BOXTITLE)
        self.application = application
        self.hotbox_designer = None

        hotboxes_data = load_hotboxes_datas(self.application.local_file)
        self.personnal_model = HotboxPersonalTableModel(hotboxes_data)
        self.personnal_view = HotboxTableView()
        self.personnal_view.set_model(self.personnal_model)
        method = self._personnal_selected_row_changed
        self.personnal_view.selectedRowChanged.connect(method)

        self.toolbar = HotboxManagerToolbar()
        self.toolbar.link.setEnabled(False)
        self.toolbar.unlink.setEnabled(False)
        self.toolbar.newRequested.connect(self._call_create)
        self.toolbar.linkRequested.connect(self._call_add_link)
        self.toolbar.unlinkRequested.connect(self._call_unlink)
        self.toolbar.editRequested.connect(self._call_edit)
        self.toolbar.deleteRequested.connect(self._call_remove)
        self.toolbar.importRequested.connect(self._call_import)
        self.toolbar.exportRequested.connect(self._call_export)
        self.toolbar.setHotkeyRequested.connect(self._call_set_hotkey)
        setter_enabled = bool(application.available_set_hotkey_modes)
        self.toolbar.hotkeyset.setEnabled(setter_enabled)
        self.toolbar.importPyRigassitRequested.connect(self._call_import_py_rigassit)
        self.toolbar.aboutRequested.connect(self._show_about)

        self.edit = HotboxGeneralSettingWidget()
        self.edit.optionSet.connect(self._call_option_set)
        self.edit.setEnabled(False)
        self.edit.open_command.released.connect(self._call_open_command)
        method = self._call_play_open_command
        self.edit.open_command.playReleased.connect(method)
        self.edit.close_command.released.connect(self._call_close_command)
        method = self._call_play_close_command
        self.edit.close_command.playReleased.connect(method)
        self.edit.switch_command.released.connect(self._call_switch_command)
        method = self._call_play_switch_command
        self.edit.switch_command.playReleased.connect(method)

        self.personnal = QtWidgets.QWidget()
        self.hlayout = QtWidgets.QHBoxLayout(self.personnal)
        self.hlayout.setContentsMargins(8, 0, 8, 8)
        self.hlayout.setSpacing(4)
        self.hlayout.addWidget(self.personnal_view)
        self.hlayout.addWidget(self.edit)

        links = load_json(application.shared_file, default=[])
        self.shared_model = HotboxSharedTableModel(links)
        self.shared_view = HotboxTableView()
        self.shared_view.set_model(self.shared_model)
        method = self._shared_selected_row_changed
        self.shared_view.selectedRowChanged.connect(method)

        self.infos = HotboxGeneralInfosWidget()
        self.infos.setEnabled(False)
        self.infos.open_command.released.connect(self._call_open_command)
        method = self._call_play_open_command
        self.infos.open_command.playReleased.connect(method)
        self.infos.close_command.released.connect(self._call_close_command)
        method = self._call_play_close_command
        self.infos.close_command.playReleased.connect(method)
        self.infos.switch_command.released.connect(self._call_switch_command)
        method = self._call_play_switch_command
        self.infos.switch_command.playReleased.connect(method)

        self.shared = QtWidgets.QWidget()
        self.hlayout2 = QtWidgets.QHBoxLayout(self.shared)
        self.hlayout2.setContentsMargins(8, 0, 8, 8)
        self.hlayout2.setSpacing(4)
        self.hlayout2.addWidget(self.shared_view)
        self.hlayout2.addWidget(self.infos)

        self.tabwidget = QtWidgets.QTabWidget()
        self.tabwidget.addTab(self.personnal, "Personal")
        self.tabwidget.addTab(self.shared, "Shared")
        self.tabwidget.currentChanged.connect(self.tab_index_changed)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.tabwidget)

    def retranslateUi(self):
        self.setWindowTitle(tr("window.title"))
        self.tabwidget.setTabText(0, tr("tab.personal"))
        self.tabwidget.setTabText(1, tr("tab.shared"))

    def _show_about(self):
        dlg = AboutDialog(self)
        dlg.exec_()

    def get_selected_hotbox(self):
        index = self.tabwidget.currentIndex()
        table = self.shared_view if index else self.personnal_view
        model = self.shared_model if index else self.personnal_model
        row = table.get_selected_row()
        if row is None:
            return
        return model.hotboxes[row]

    def save_hotboxes(self, *_):
        
        # 保存个人热盒
        personnal_data = [save_nested_hotbox(hb) for hb in self.personnal_model.hotboxes]
        save_datas(self.application.local_file, personnal_data)
        # 共享热盒只是链接，不需要递归保存
        save_datas(self.application.shared_file, self.shared_model.hotboxes_links)

    def _personnal_selected_row_changed(self):
        hotbox = self.get_selected_hotbox()
        if hotbox is not None:
            self.edit.set_hotbox_settings(hotbox['general'])
            self.edit.setEnabled(True)
        else:
            self.edit.setEnabled(False)

    def tab_index_changed(self):
        index = self.tabwidget.currentIndex()
        self.toolbar.edit.setEnabled(index == 0)
        self.toolbar.delete.setEnabled(index == 0)
        self.toolbar.link.setEnabled(index == 1)
        self.toolbar.unlink.setEnabled(index == 1)

    def hotbox_data_modified(self, hotbox_data):
        row = self.personnal_view.get_selected_row()
        self.personnal_model.set_hotbox(row, hotbox_data)
        clear_loaded_hotboxes()
        self.save_hotboxes()

    def _shared_selected_row_changed(self):
        index = self.shared_view.get_selected_row()
        hotbox = self.shared_model.hotboxes[index]
        if hotbox is not None:
            self.infos.set_hotbox_data(hotbox)
            self.infos.setEnabled(True)
        else:
            self.infos.setEnabled(False)

    def _get_open_command(self):
        hotbox = self.get_selected_hotbox()
        if not hotbox:
            return warning('Hotbox designer', 'No hotbox selected')
        return OPEN_COMMAND.format(
            application=self.application.name,
            name=hotbox['general']['name'])

    def _call_open_command(self):
        CommandDisplayDialog(self._get_open_command(), self).exec_()

    def _call_play_open_command(self):
        exec(self._get_open_command())

    def _get_close_command(self):
        hotbox = self.get_selected_hotbox()
        if not hotbox:
            return warning('Hotbox designer', 'No hotbox selected')
        return CLOSE_COMMAND.format(name=hotbox['general']['name'])

    def _call_close_command(self):
        CommandDisplayDialog(self._get_close_command(), self).exec_()

    def _call_play_close_command(self):
        exec(self._get_close_command())

    def _get_switch_command(self):
        hotbox = self.get_selected_hotbox()
        if not hotbox:
            return warning('Hotbox designer', 'No hotbox selected')
        return SWITCH_COMMAND.format(
            application=self.application.name,
            name=hotbox['general']['name'])

    def _call_switch_command(self):
        CommandDisplayDialog(self._get_switch_command(), self).exec_()

    def _call_play_switch_command(self):
        exec(self._get_switch_command())

    def _call_edit(self):
        if self.tabwidget.currentIndex():
            return

        hotbox_data = self.get_selected_hotbox()
        if hotbox_data is None:
            return warning('Hotbox designer', 'No hotbox selected')

        # print(hotbox_data)

        if self.hotbox_designer is not None:
            self.hotbox_designer.close()

        self.hotbox_designer = HotboxEditor(
            hotbox_data,
            self.application,
            parent=self.application.main_window)
        method = self.hotbox_data_modified
        self.hotbox_designer.hotboxDataModified.connect(method)
        self.hotbox_designer.show()

    def _call_create(self):
        hotboxes_ = self.personnal_model.hotboxes + self.shared_model.hotboxes
        dialog = CreateHotboxDialog(hotboxes_, self)
        result = dialog.exec_()
        if result == QtWidgets.QDialog.Rejected:
            return

        self.personnal_model.layoutAboutToBeChanged.emit()
        self.personnal_model.hotboxes.append(dialog.hotbox())
        self.personnal_model.layoutChanged.emit()
        # retrieve and selected last hotbox in the list (who's the new one)
        hotbox_count = len(self.personnal_model.hotboxes) - 1
        if hotbox_count > -1:
            self.personnal_view.selectRow(hotbox_count)

        self.save_hotboxes()
        clear_loaded_hotboxes()

    def _call_add_link(self):
        filename = import_hotbox_link()
        if not filename:
            return
        self.shared_model.add_link(filename)
        # retrieve and selected last hotbox in the list (who's the new one)
        hotbox_count = len(self.shared_model.hotboxes) - 1
        if hotbox_count > -1:
            self.shared_view.selectRow(hotbox_count)

        self.save_hotboxes()
        clear_loaded_hotboxes()

    def _call_unlink(self):
        index = self.shared_view.get_selected_row()
        if index is None:
            return warning('Hotbox designer', 'No hotbox selected')
        self.shared_model.remove_link(index)
        self.save_hotboxes()
        clear_loaded_hotboxes()

    def _call_remove(self):
        hotbox = self.get_selected_hotbox()
        if hotbox is None:
            return warning('Hotbox designer', 'No hotbox selected')

        areyousure = QtWidgets.QMessageBox.question(
            self,
            'remove',
            'remove a hotbox is definitive, are you sure to continue',
            buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            defaultButton=QtWidgets.QMessageBox.No)

        if areyousure == QtWidgets.QMessageBox.No:
            return

        self.personnal_model.layoutAboutToBeChanged.emit()
        self.personnal_model.hotboxes.remove(hotbox)
        self.personnal_model.layoutChanged.emit()
        self.save_hotboxes()
        clear_loaded_hotboxes()

    def _call_option_set(self, option, value):
        self.personnal_model.layoutAboutToBeChanged.emit()
        hotbox = self.get_selected_hotbox()
        if option == 'name':
            value = get_valid_name(self.personnal_model.hotboxes, value)

        if hotbox is not None:
            hotbox['general'][option] = value
        self.personnal_model.layoutChanged.emit()
        self.save_hotboxes()
        clear_loaded_hotboxes()

    def _call_set_hotkey(self):
        hotbox = self.get_selected_hotbox()
        if not hotbox:
            return warning('Hotbox designer', 'No hotbox selected')
        modes = self.application.available_set_hotkey_modes
        dialog = HotkeySetter(modes)
        result = dialog.exec_()
        name = hotbox['general']['name']
        open_cmd = OPEN_COMMAND.format(
            name=name,
            application=self.application.name)
        switch_cmd = SWITCH_COMMAND.format(
            name=name,
            application=self.application.name)
        if result == QtWidgets.QDialog.Rejected:
            return
        self.application.set_hotkey(
            name=name,
            mode=dialog.mode(),
            sequence=dialog.get_key_sequence(),
            open_cmd=open_cmd,
            close_cmd=CLOSE_COMMAND.format(name=name),
            switch_cmd=switch_cmd)

    def _call_export(self):
        hotbox = self.get_selected_hotbox()
        if not hotbox:
            return warning('Hotbox designer', 'No hotbox selected')
        export_hotbox(hotbox)

    def _call_import(self):
        hotbox = import_hotbox()
        if not hotbox:
            return warning('Hotbox designer', 'No hotbox selected')
        hotboxes = self.personnal_model.hotboxes
        name = get_valid_name(hotboxes, hotbox['general']['name'])
        hotbox['general']['name'] = name

        self.personnal_model.layoutAboutToBeChanged.emit()
        self.personnal_model.hotboxes.append(hotbox)
        self.personnal_model.layoutChanged.emit()
        self.save_hotboxes()
        clear_loaded_hotboxes()

    def _call_import_py_rigassit(self):
        """导入 PY_RIGASSIT 模板：添加到个人模型，并生成默认文件"""

        if not os.path.exists(TEMPLATE_FILE):
            QtWidgets.QMessageBox.warning(self, 'Import Error', 'Template file not found:\n{}'.format(TEMPLATE_FILE))
            return

        target_dir = os.path.dirname(TARGET_FILE)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        try:
            with open(TEMPLATE_FILE, 'r') as f:
                template_data = json.load(f)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Import Error', 'Failed to read template file:\n{}'.format(e))
            return

        #  确保数据是列表
        if isinstance(template_data, dict):
            template_data = [template_data]
        elif not isinstance(template_data, list):
            QtWidgets.QMessageBox.warning(self, 'Import Error', 'Invalid template data format (must be a list or dict).')
            return

        # print("PY_RIGASSIT_ROOT: ", PY_RIGASSIT_ROOT)
        processed_hotboxes = []
        for hotbox_data in template_data:
            hotbox_data = replace_image_paths(hotbox_data)
            name = get_valid_name(self.personnal_model.hotboxes, hotbox_data['general']['name']) 
            hotbox_data['general']['name'] = name
            processed_hotboxes.append(hotbox_data)

        self.personnal_model.layoutAboutToBeChanged.emit()
        self.personnal_model.hotboxes.extend(processed_hotboxes)
        self.personnal_model.layoutChanged.emit()

        save_datas(self.application.local_file, self.personnal_model.hotboxes)

        #将处理后的数据写入默认文件 (PY_RIGASSIT_hotboxes.json)
        try:
            with open(TARGET_FILE, 'w') as f:
                json.dump(processed_hotboxes, f, indent=2)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Failed to write default file:\n{}'.format(e))

        clear_loaded_hotboxes()
        load_hotboxes(self.application)  

        self.shared_view.update()

        new_row = len(self.personnal_model.hotboxes) - len(processed_hotboxes)
        if new_row >= 0:
            self.personnal_view.selectRow(new_row)

        QtWidgets.QMessageBox.information(self, 'Import Success', 'PY_RIGASSIT template has been imported to:\n{}'.format(TARGET_FILE))


class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)

        self.text = QtWidgets.QTextEdit()
        self.text.setReadOnly(True)

        self.lang_switch = QtWidgets.QComboBox()
        self.lang_switch.addItems(["English", u"中文"])
        self.lang_switch.currentIndexChanged.connect(self.change_lang)

        self.close_btn = QtWidgets.QPushButton()
        self.close_btn.clicked.connect(self.close)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.lang_switch)
        layout.addWidget(self.text)
        layout.addWidget(self.close_btn)

        self.refresh()


    def change_lang(self):
        lang = "en" if self.lang_switch.currentIndex() == 0 else "zh"
        translator.set_language(lang)
        self.refresh()

    def refresh(self):
        self.setWindowTitle(tr("about.title"))
        self.close_btn.setText(tr("ui.close"))

        html = u"""
        <h2>Hotbox Designer (modified)</h2>

        <p><b>{version}:</b> v1.0</p>
        <p><b>{compat}:</b> Maya 2019 – 2026</p>

        <hr>

        <p><b>Original Project:</b><br>
        Hotbox Designer<br>
        Author: luckylyk<br>
        Source: https://github.com/luckylyk/hotbox_designer</p>
        
        <hr>

        <p><b>{modified}:</b><br>
        Yolanda Ping (You P)</p>

        <p><b>{features}:</b></p>
        <ul>
        <li>{nested}</li>
        <li>{editor}</li>
        <li>{rigassit}</li>
        <li>{qt6}</li>
        <li>{ui}</li>
        </ul>

        <hr>

        <p><b>{license}:</b><br>
        Based on original project.</p>
        """.format(
            version=tr("about.version"),
            compat=tr("about.compat"),
            modified=tr("about.modified"),
            features=tr("about.features"),
            nested=tr("feature.nested"),
            editor=tr("feature.editor"),
            rigassit=tr("feature.rigassit"),
            qt6=tr("feature.qt6"),
            ui=tr("feature.ui"),
            license=tr("about.license"),
            license_desc=tr("about.license_desc"),
        )

        self.text.setHtml(html)


class HotboxManagerToolbar(QtWidgets.QToolBar):
    newRequested = QtCore.Signal()
    editRequested = QtCore.Signal()
    deleteRequested = QtCore.Signal()
    linkRequested = QtCore.Signal()
    unlinkRequested = QtCore.Signal()
    importRequested = QtCore.Signal()
    exportRequested = QtCore.Signal()
    setHotkeyRequested = QtCore.Signal()
    importPyRigassitRequested = QtCore.Signal()
    aboutRequested = QtCore.Signal()

    def __init__(self, parent=None):
        super(HotboxManagerToolbar, self).__init__(parent)
        self.setIconSize(QtCore.QSize(16, 16))

        self.new = QAction(icon('manager-new.png'), '', self)
        self.edit = QAction(icon('manager-edit.png'), '', self)
        self.delete = QAction(icon('manager-delete.png'), '', self)
        self.link = QAction(icon('link.png'), '', self)
        self.unlink = QAction(icon('unlink.png'), '', self)
        self.import_ = QAction(icon('manager-import.png'), '', self)
        self.export = QAction(icon('manager-export.png'), '', self)
        self.hotkeyset = QAction(icon('touch.png'), '', self)
        self.import_py_rigassit = QAction(icon('py_rigassit.png'), '', self)
        self.about = QAction(icon('help.png'), '', self)

        self.new.triggered.connect(self.newRequested.emit)
        self.edit.triggered.connect(self.editRequested.emit)
        self.delete.triggered.connect(self.deleteRequested.emit)
        self.link.triggered.connect(self.linkRequested.emit)
        self.unlink.triggered.connect(self.unlinkRequested.emit)
        self.import_.triggered.connect(self.importRequested.emit)
        self.export.triggered.connect(self.exportRequested.emit)
        self.hotkeyset.triggered.connect(self.setHotkeyRequested.emit)
        self.import_py_rigassit.triggered.connect(self.importPyRigassitRequested.emit)
        self.about.triggered.connect(self.aboutRequested.emit)

        self.addAction(self.new)
        self.addAction(self.edit)
        self.addAction(self.delete)
        self.addSeparator()
        self.addAction(self.link)
        self.addAction(self.unlink)
        self.addSeparator()
        self.addAction(self.import_)
        self.addAction(self.export)
        self.addSeparator()
        self.addAction(self.hotkeyset)
        self.addSeparator()
        self.addAction(self.import_py_rigassit)
        self.addSeparator()
        self.addAction(self.about)

        self.retranslateUi()

    def retranslateUi(self):
        self.new.setToolTip(tr("toolbar.new"))
        self.edit.setToolTip(tr("toolbar.edit"))
        self.delete.setToolTip(tr("toolbar.delete"))
        self.link.setToolTip(tr("toolbar.link"))
        self.unlink.setToolTip(tr("toolbar.unlink"))
        self.import_.setToolTip(tr("toolbar.import"))
        self.export.setToolTip(tr("toolbar.export"))
        self.hotkeyset.setToolTip(tr("toolbar.hotkey"))
        self.import_py_rigassit.setToolTip(tr("toolbar.import_rigassit"))
        self.about.setToolTip(tr("toolbar.about"))

    @staticmethod
    def refresh_ui(widget):
        for child in widget.findChildren(QtWidgets.QWidget):
            if hasattr(child, "retranslateUi"):
                child.retranslateUi()


class HotboxTableView(QtWidgets.QTableView):
    selectedRowChanged = QtCore.Signal()

    def __init__(self, parent=None):
        super(HotboxTableView, self).__init__(parent)
        self.selection_model = None
        vheader = self.verticalHeader()
        vheader.hide()
        vheader.setSectionResizeMode(QtHeaderResizeMode("ResizeToContents"))
        hheader = self.horizontalHeader()
        hheader.setStretchLastSection(True)
        hheader.hide()
        self.setAlternatingRowColors(True)
        self.setWordWrap(True)
        self.setShowGrid(False)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def selection_changed(self, *_):
        return self.selectedRowChanged.emit()

    def set_model(self, model):
        self.setModel(model)
        self.selection_model = self.selectionModel()
        self.selection_model.selectionChanged.connect(self.selection_changed)

    def get_selected_row(self):
        indexes = self.selection_model.selectedIndexes()
        rows = list({index.row() for index in indexes})
        if not rows:
            return None
        return rows[0]


class HotboxPersonalTableModel(QtCore.QAbstractTableModel):

    def __init__(self, hotboxes, parent=None):
        super(HotboxPersonalTableModel, self).__init__(parent=parent)
        self.hotboxes = hotboxes

    def columnCount(self, _):
        return 1

    def rowCount(self, _):
        return len(self.hotboxes)

    def set_hotbox(self, row, hotbox):
        self.layoutAboutToBeChanged.emit()
        self.hotboxes[row] = hotbox
        self.layoutChanged.emit()

    def data(self, index, role):
        row, col = index.row(), index.column()
        hotbox = self.hotboxes[row]
        if role == QtCore.Qt.DisplayRole:
            if col == 0:
                return hotbox['general']['name']


class HotboxSharedTableModel(QtCore.QAbstractTableModel):

    def __init__(self, hotboxes_links, parent=None):
        super(HotboxSharedTableModel, self).__init__(parent=parent)
        self.hotboxes_links = hotboxes_links
        self.hotboxes = [load_json(l) for l in hotboxes_links]

    def columnCount(self, _):
        return 1

    def rowCount(self, _):
        return len(self.hotboxes_links)

    def add_link(self, hotbox_link):
        self.layoutAboutToBeChanged.emit()
        self.hotboxes_links.append(hotbox_link)
        self.hotboxes.append(load_json(hotbox_link))
        self.layoutChanged.emit()

    def remove_link(self, index):
        self.layoutAboutToBeChanged.emit()
        self.hotboxes_links.pop(index)
        self.hotboxes.pop(index)
        self.layoutChanged.emit()

    def data(self, index, role):
        row, col = index.row(), index.column()
        hotbox = self.hotboxes_links[row]
        if role == QtCore.Qt.DisplayRole:
            if col == 0:
                return hotbox


class HotboxGeneralInfosWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(HotboxGeneralInfosWidget, self).__init__(parent)
        self.setFixedWidth(200)
        self.label = QtWidgets.QLabel()
        self.open_command = CommandButton('show')
        self.close_command = CommandButton('hide')
        self.switch_command = CommandButton('switch')

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(Title('Infos'))
        self.layout.addSpacing(8)
        self.layout.addWidget(self.label)
        self.layout.addSpacing(8)
        self.layout.addStretch(1)
        self.layout.addWidget(Title('Commands'))
        self.layout.addSpacing(8)
        self.layout.addWidget(self.open_command)
        self.layout.addWidget(self.close_command)
        self.layout.addWidget(self.switch_command)

    def set_hotbox_data(self, hotbox_data):
        self.label.setText(hotbox_data_to_html(hotbox_data))


class HotboxGeneralSettingWidget(QtWidgets.QWidget):
    optionSet = QtCore.Signal(str, object)
    applyRequested = QtCore.Signal()

    def __init__(self, parent=None):
        super(HotboxGeneralSettingWidget, self).__init__(parent)
        self.setFixedWidth(200)
        self.name = QtWidgets.QLineEdit()
        self.name.textEdited.connect(partial(self.optionSet.emit, 'name'))
        self.submenu = BoolCombo(False)
        self.submenu.valueSet.connect(partial(self.optionSet.emit, 'submenu'))
        self.triggering = QtWidgets.QComboBox()
        self.triggering.addItems(TRIGGERING_TYPES)
        self.triggering.currentIndexChanged.connect(self._triggering_changed)
        self.aiming = BoolCombo(False)
        self.aiming.valueSet.connect(partial(self.optionSet.emit, 'aiming'))
        self.leaveclose = BoolCombo(False)
        method = partial(self.optionSet.emit, 'leaveclose')
        self.leaveclose.valueSet.connect(method)

        self.open_command = CommandButton('show')
        self.close_command = CommandButton('hide')
        self.switch_command = CommandButton('switch')

        self.layout = QtWidgets.QFormLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setHorizontalSpacing(5)
        self.layout.addRow(Title('Options'))
        self.layout.addItem(QtWidgets.QSpacerItem(0, 8))
        self.layout.addRow('name', self.name)
        self.layout.addItem(QtWidgets.QSpacerItem(0, 8))
        self.layout.addRow('is submenu', self.submenu)
        self.layout.addRow('triggering', self.triggering)
        self.layout.addRow('aiming', self.aiming)
        self.layout.addRow('close on leave', self.leaveclose)
        self.layout.addItem(QtWidgets.QSpacerItem(0, 8))
        self.layout.addRow(Title('Commands'))
        self.layout.addItem(QtWidgets.QSpacerItem(0, 8))
        self.layout.addRow(self.open_command)
        self.layout.addRow(self.close_command)
        self.layout.addRow(self.switch_command)

    def _triggering_changed(self, _):
        self.optionSet.emit('triggering', self.triggering.currentText())

    def _touch_changed(self, _):
        self.optionSet.emit('touch', self.touch.text())

    def set_hotbox_settings(self, hotbox_settings):
        self.blockSignals(True)
        self.submenu.setCurrentText(str(hotbox_settings['submenu']))
        self.name.setText(hotbox_settings['name'])
        self.triggering.setCurrentText(hotbox_settings['triggering'])
        self.aiming.setCurrentText(str(hotbox_settings['aiming']))
        self.leaveclose.setCurrentText(str(hotbox_settings['leaveclose']))
        self.blockSignals(False)
