# -*- coding: utf-8 -*-

# .FileName:menu.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/3/24 21:50
# .Finish time:
'''添加Hotbox editor模板导入和数据导入导出 布局'''
try:
    from ui_framework.core.qtCompat import *

except ImportError:
    from CommonUse.qtCompat import *
from hotbox_designer.qtutils import icon


class MenuWidget(QtWidgets.QWidget):

    deleteRequested = QtCore.Signal()
    copyRequested = QtCore.Signal()
    pasteRequested = QtCore.Signal()
    undoRequested = QtCore.Signal()
    redoRequested = QtCore.Signal()
    sizeChanged = QtCore.Signal()
    useSnapToggled = QtCore.Signal(bool)
    snapValuesChanged = QtCore.Signal()
    editCenterToggled = QtCore.Signal(bool)
    centerValuesChanged = QtCore.Signal(int, int)
    addButtonRequested = QtCore.Signal()
    addTextRequested = QtCore.Signal()
    addBackgroundRequested = QtCore.Signal()
    onBottomRequested = QtCore.Signal()
    moveDownRequested = QtCore.Signal()
    moveUpRequested = QtCore.Signal()
    onTopRequested = QtCore.Signal()
    importRequested = QtCore.Signal()
    exportRequested = QtCore.Signal()
    importTemplateRequested = QtCore.Signal()

    def __init__(self, parent=None):
        super(MenuWidget, self).__init__(parent=parent)
        self.delete = QAction(icon('delete.png'), '', self)
        self.delete.setToolTip('Delete selection')
        self.delete.triggered.connect(self.deleteRequested.emit)
        self.copy = QAction(icon('copy.png'), '', self)
        self.copy.setToolTip('Copy selection')
        self.copy.triggered.connect(self.copyRequested.emit)
        self.paste = QAction(icon('paste.png'), '', self)
        self.paste.setToolTip('Paste')
        self.paste.triggered.connect(self.pasteRequested.emit)

        self.undo = QAction(icon('undo.png'), '', self)
        self.undo.setToolTip('Undo')
        self.undo.triggered.connect(self.undoRequested.emit)
        self.redo = QAction(icon('redo.png'), '', self)
        self.redo.setToolTip('Redo')
        self.redo.triggered.connect(self.redoRequested.emit)

        validator = QtGui.QIntValidator()
        self.hbwidth = QtWidgets.QLineEdit('600')
        self.hbwidth.setFixedWidth(35)
        self.hbwidth.setValidator(validator)
        self.hbwidth.textEdited.connect(self.size_changed)
        self.hbheight = QtWidgets.QLineEdit('300')
        self.hbheight.setFixedWidth(35)
        self.hbheight.setValidator(validator)
        self.hbheight.textEdited.connect(self.size_changed)

        icon_ = icon('center.png')
        self.editcenter = QAction(icon_, '', self)
        self.editcenter.setToolTip('Edit center')
        self.editcenter.setCheckable(True)
        self.editcenter.triggered.connect(self.edit_center_toggled)
        validator = QtGui.QIntValidator()
        self.editcenterx = QtWidgets.QLineEdit('10')
        self.editcenterx.setFixedWidth(35)
        self.editcenterx.setValidator(validator)
        self.editcenterx.textEdited.connect(self.center_values_changed)
        self.editcentery = QtWidgets.QLineEdit('10')
        self.editcentery.setFixedWidth(35)
        self.editcentery.setValidator(validator)
        self.editcentery.textEdited.connect(self.center_values_changed)

        self.snap = QAction(icon('snap.png'), '', self)
        self.snap.setToolTip('Snap grid enable')
        self.snap.setCheckable(True)
        self.snap.triggered.connect(self.snap_toggled)
        validator = QtGui.QIntValidator(5, 150)
        self.snapx = QtWidgets.QLineEdit('10')
        self.snapx.setFixedWidth(35)
        self.snapx.setValidator(validator)
        self.snapx.setEnabled(False)
        self.snapx.textEdited.connect(self.snap_value_changed)
        self.snapy = QtWidgets.QLineEdit('10')
        self.snapy.setFixedWidth(35)
        self.snapy.setValidator(validator)
        self.snapy.setEnabled(False)
        self.snapy.textEdited.connect(self.snap_value_changed)
        self.snap.toggled.connect(self.snapx.setEnabled)
        self.snap.toggled.connect(self.snapy.setEnabled)

        icon_ = icon('addbutton.png')
        self.addbutton = QAction(icon_, '', self)
        self.addbutton.setToolTip('Add button')
        self.addbutton.triggered.connect(self.addButtonRequested.emit)
        self.addtext = QAction(icon('addtext.png'), '', self)
        self.addtext.setToolTip('Add text')
        self.addtext.triggered.connect(self.addTextRequested.emit)
        self.addbg = QAction(icon('addbg.png'), '', self)
        self.addbg.setToolTip('Add background shape')
        self.addbg.triggered.connect(self.addBackgroundRequested.emit)

        self.import_action = QAction(icon('manager-import.png'), '', self)
        self.import_action.setToolTip('Import menu data')
        self.import_action.triggered.connect(self.importRequested.emit)

        self.export_action = QAction(icon('manager-export.png'), '', self)
        self.export_action.setToolTip('Export menu data')
        self.export_action.triggered.connect(self.exportRequested.emit)

        self.template_combo = QtWidgets.QComboBox()
        self.template_combo.setToolTip('Select template')
        self.template_combo = QtWidgets.QComboBox()
        self.template_combo.setFixedWidth(100)
        self.populate_templates()

        self.import_template_btn = QtWidgets.QPushButton('Import')
        self.import_template_btn.setToolTip(u'从选择的模板导入')
        self.import_template_btn.clicked.connect(self.importTemplateRequested.emit)

        template_widget = QtWidgets.QWidget()
        template_layout = QtWidgets.QHBoxLayout(template_widget)
        template_layout.setContentsMargins(0, 0, 0, 0)
        template_layout.setSpacing(2)
        template_layout.addWidget(self.template_combo)
        template_layout.addWidget(self.import_template_btn)

        icon_ = icon('onbottom.png')
        self.onbottom = QAction(icon_, '', self)
        self.onbottom.setToolTip('Set selected shapes on bottom')
        self.onbottom.triggered.connect(self.onBottomRequested.emit)
        icon_ = icon('movedown.png')
        self.movedown = QAction(icon_, '', self)
        self.movedown.setToolTip('Move down selected shapes')
        self.movedown.triggered.connect(self.moveDownRequested.emit)
        self.moveup = QAction(icon('moveup.png'), '', self)
        self.moveup.setToolTip('Move up selected shapes')
        self.moveup.triggered.connect(self.moveUpRequested.emit)
        self.ontop = QAction(icon('ontop.png'), '', self)
        self.ontop.setToolTip('Set selected shapes on top')
        self.ontop.triggered.connect(self.onTopRequested.emit)

        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.addAction(self.delete)
        self.toolbar.addAction(self.copy)
        self.toolbar.addAction(self.paste)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.undo)
        self.toolbar.addAction(self.redo)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.snap)
        self.toolbar.addWidget(self.snapx)
        self.toolbar.addWidget(self.snapy)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(QtWidgets.QLabel('size'))
        self.toolbar.addWidget(self.hbwidth)
        self.toolbar.addWidget(self.hbheight)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.editcenter)
        self.toolbar.addWidget(self.editcenterx)
        self.toolbar.addWidget(self.editcentery)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.addbutton)
        self.toolbar.addAction(self.addtext)
        self.toolbar.addAction(self.addbg)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.import_action)
        self.toolbar.addAction(self.export_action)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(template_widget)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.onbottom)
        self.toolbar.addAction(self.movedown)
        self.toolbar.addAction(self.moveup)
        self.toolbar.addAction(self.ontop)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 10, 0)
        self.layout.addWidget(self.toolbar)

    def size_changed(self, *_):
        self.sizeChanged.emit()

    def edit_center_toggled(self):
        self.editCenterToggled.emit(self.editcenter.isChecked())

    def snap_toggled(self):
        self.useSnapToggled.emit(self.snap.isChecked())

    def snap_values(self):
        x = int(self.snapx.text()) if self.snapx.text() else 1
        y = int(self.snapy.text()) if self.snapy.text() else 1
        x = x if x > 0 else 1
        y = y if y > 0 else 1
        return x, y

    def snap_value_changed(self, _):
        self.snapValuesChanged.emit()

    def set_center_values(self, x, y):
        self.editcenterx.setText(str(x))
        self.editcentery.setText(str(y))

    def center_values_changed(self, _):
        x = int(self.editcenterx.text()) if self.editcenterx.text() else 0
        y = int(self.editcentery.text()) if self.editcentery.text() else 0
        self.centerValuesChanged.emit(x, y)

    def set_size_values(self, width, height):
        self.hbwidth.setText(str(width))
        self.hbheight.setText(str(height))
        self.sizeChanged.emit()

    def get_size(self):
        width = int(self.hbwidth.text()) if self.hbwidth.text() else 1
        height = int(self.hbheight.text()) if self.hbheight.text() else 1
        return QtCore.QSize(width, height)

    def populate_templates(self):
        """从资源中加载模板名称并填充下拉框"""
        from hotbox_designer.data import load_templates
        templates = load_templates()
        names = [hb['general']['name'] for hb in templates]
        self.template_combo.addItems(names)

    def selected_template(self):
        """返回当前选中的模板名称"""
        return self.template_combo.currentText()
