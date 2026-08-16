# -*- coding: utf-8 -*-

# .FileName:copy_deform_weight.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2025/8/24 2:01
# .Finish time:
import os

from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
from selectOrRemove import SelectOrremoveObj
from GeneralTools.deform_weight_edit import DeformersWeightsEditor
import mayaPrint as mayaPrint
import HelpImageUI as Help

import pymel.core as pm


_widgest = Widgets()
_obj = SelectOrremoveObj()


class DeformersWeightsEditorWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(DeformersWeightsEditorWidget, self).__init__(parent)
        self._color_green = [0, 0.8, 0.8]

        self.input_mesh = []
        self.working_dir = pm.workspace(query=True, directory=True)
        if int(pm.about(version=True)) < 2018:
            self.valid_deformers = ['blendShape', 'cluster', 'nonLinear', 'shrinkWrap', 'wire', 'deltaMush']
        else:
            self.valid_deformers = ['blendShape', 'cluster', 'ffd', 'nonLinear', 'shrinkWrap', 'wire', 'deltaMush']
        self.symmetry_axis = {1: 0, 2: 1, 3: 2}
        self.copy_source_info = []
        self.copy_target_info = []
        self.defEditor_win_name = 'defEditor_window'

        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        scroll_area = QtWidgets.QScrollArea()
        scroll_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(0)
        scroll_layout.setContentsMargins(0, 0, 0, 0)

        self.create_deform_section(scroll_layout)

        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)


    def create_deform_section(self, parent_layout):

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 4, 0)

        mesh_group = QtWidgets.QGroupBox("Mesh:")
        mesh_layout = QtWidgets.QVBoxLayout(mesh_group)

        self.mesh_list = QtWidgets.QListWidget()
        self.mesh_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.mesh_list.itemSelectionChanged.connect(self.on_mesh_selected)
        mesh_layout.addWidget(self.mesh_list)

        load_mesh_btn = QtWidgets.QPushButton("Load Mesh")
        load_mesh_btn.setProperty("green", True)
        load_mesh_btn.clicked.connect(lambda: self.load_target(self.mesh_list, True))

        mesh_layout.addWidget(load_mesh_btn)
        left_layout.addWidget(mesh_group)

        deformers_group = QtWidgets.QGroupBox("Deform:")
        deformers_layout = QtWidgets.QVBoxLayout(deformers_group)

        self.deformers_list = QtWidgets.QListWidget()
        self.deformers_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        deformers_layout.addWidget(self.deformers_list)

        left_layout.addWidget(deformers_group)

        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)
        right_layout.setContentsMargins(4, 0, 0, 0)

        self.create_import_export_section(right_layout)
        self.create_mirror_section(right_layout)
        self.create_copy_section(right_layout)
        splitter.setHandleWidth(1)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([200, 400])

        parent_layout.addWidget(splitter)

    def create_import_export_section(self, parent_layout):
        group = QtWidgets.QGroupBox("Weights Import/Export 导入/导出权重")
        layout = QtWidgets.QVBoxLayout(group)

        path_layout = QtWidgets.QHBoxLayout()
        path_layout.addWidget(QtWidgets.QLabel("Path:"))

        self.path_edit = QtWidgets.QLineEdit()
        self.path_edit.textChanged.connect(self.dir_field_command)
        path_layout.addWidget(self.path_edit)

        browse_btn = QtWidgets.QPushButton("Browse")
        browse_btn.clicked.connect(self.dir_button_command)
        path_layout.addWidget(browse_btn)

        layout.addLayout(path_layout)

        layout.addWidget(QtWidgets.QLabel("Load Parameters:"))

        algorithm_layout = QtWidgets.QHBoxLayout()
        algorithm_layout.addWidget(QtWidgets.QLabel("ALGORITHM:"))

        self.algorithm_group = QtWidgets.QButtonGroup()
        self.vertex_index_radio = QtWidgets.QRadioButton("index")
        self.vertex_position_radio = QtWidgets.QRadioButton("position")
        self.vertex_index_radio.setChecked(True)

        self.algorithm_group.addButton(self.vertex_index_radio, 1)
        self.algorithm_group.addButton(self.vertex_position_radio, 2)

        self.vertex_index_radio.toggled.connect(self.index_algorithm)
        self.vertex_position_radio.toggled.connect(self.position_algorithm)

        algorithm_layout.addWidget(self.vertex_index_radio)
        algorithm_layout.addWidget(self.vertex_position_radio)
        layout.addLayout(algorithm_layout)

        # 容差
        tolerance_layout = QtWidgets.QHBoxLayout()
        tolerance_layout.addWidget(QtWidgets.QLabel("TOLERANCE:"))

        self.tolerance_edit = QtWidgets.QLineEdit("0.1")
        self.tolerance_edit.setEnabled(False)
        self.tolerance_edit.textChanged.connect(self.set_tolerance)
        tolerance_layout.addWidget(self.tolerance_edit)

        layout.addLayout(tolerance_layout)

        buttons_layout = QtWidgets.QHBoxLayout()

        self.save_btn = QtWidgets.QPushButton("Export")
        self.save_btn.clicked.connect(self.save_weights)
        buttons_layout.addWidget(self.save_btn)

        self.load_btn = QtWidgets.QPushButton("Import")
        self.load_btn.clicked.connect(self.load_weights)
        buttons_layout.addWidget(self.load_btn)

        layout.addLayout(buttons_layout)

        parent_layout.addWidget(group)

    def create_mirror_section(self, parent_layout):
        group = QtWidgets.QGroupBox("Weights Mirror 镜像权重")
        layout = QtWidgets.QVBoxLayout(group)
        layout.setContentsMargins(5, 10, 5, 10)

        plane_layout = QtWidgets.QHBoxLayout()
        plane_layout.addWidget(QtWidgets.QLabel("Symmetry:"))

        self.plane_group = QtWidgets.QButtonGroup()
        self.yz_radio = QtWidgets.QRadioButton("YZ")
        self.xz_radio = QtWidgets.QRadioButton("XZ")
        self.xy_radio = QtWidgets.QRadioButton("XY")
        self.yz_radio.setChecked(True)

        self.plane_group.addButton(self.yz_radio, 1)  # ID = 1
        self.plane_group.addButton(self.xz_radio, 2)  # ID = 2
        self.plane_group.addButton(self.xy_radio, 3)  # ID = 3

        plane_layout.addWidget(self.yz_radio)
        plane_layout.addWidget(self.xz_radio)
        plane_layout.addWidget(self.xy_radio)
        layout.addLayout(plane_layout)

        direction_layout = QtWidgets.QHBoxLayout()
        direction_layout.addWidget(QtWidgets.QLabel("Direction:"))

        self.direction_group = QtWidgets.QButtonGroup()
        self.positive_radio = QtWidgets.QRadioButton("+ > - ")
        self.negative_radio = QtWidgets.QRadioButton("- > + ")
        self.positive_radio.setChecked(True)

        self.direction_group.addButton(self.positive_radio, 1)  # ID = 1
        self.direction_group.addButton(self.negative_radio, 2)  # ID = 2

        direction_layout.addWidget(self.positive_radio)
        direction_layout.addWidget(self.negative_radio)
        layout.addLayout(direction_layout)

        buttons_layout = QtWidgets.QHBoxLayout()

        self.mirror_btn = QtWidgets.QPushButton("Mirror 镜像")
        self.mirror_btn.clicked.connect(self.mirror_weights)
        buttons_layout.addWidget(self.mirror_btn)

        self.flip_btn = QtWidgets.QPushButton("Flip 反转")
        self.flip_btn.clicked.connect(self.flip_weights)
        buttons_layout.addWidget(self.flip_btn)

        layout.addLayout(buttons_layout)

        parent_layout.addWidget(group)

    def create_copy_section(self, parent_layout):
        group = QtWidgets.QGroupBox("Weights Copy 拷贝权重")
        layout = QtWidgets.QVBoxLayout(group)

        source_layout = QtWidgets.QHBoxLayout()
        self.source_btn = QtWidgets.QPushButton("Source")
        self.source_btn.clicked.connect(self.copy_source)
        source_layout.addWidget(self.source_btn)

        self.source_label = QtWidgets.QLabel("从上面的列表中选择一个有效的变形器")
        source_layout.addWidget(self.source_label)
        layout.addLayout(source_layout)

        target_layout = QtWidgets.QHBoxLayout()
        self.target_btn = QtWidgets.QPushButton("Target")
        self.target_btn.clicked.connect(self.copy_target)
        target_layout.addWidget(self.target_btn)

        self.target_label = QtWidgets.QLabel("从上面列表中选择一个变形器")
        target_layout.addWidget(self.target_label)
        layout.addLayout(target_layout)

        self.copy_btn = QtWidgets.QPushButton("Copy")
        self.copy_btn.clicked.connect(self.copy_weights)
        layout.addWidget(self.copy_btn)

        parent_layout.addWidget(group)

    def on_mesh_selected(self):
        selected_items = self.mesh_list.selectedItems()
        if selected_items:
            mesh_name = selected_items[0].text()
            pm.select(mesh_name, replace=True)
            self.mesh_button_command()

    def load_target(self, list_widget, clear=True):
        if clear:
            list_widget.clear()
        sel = pm.ls(sl=True) or []
        if sel:
            sel = [obj.name() for obj in sel]
            list_widget.addItems(sel)

    def dir_button_command(self):
        current_dir = self.path_edit.text() or self.working_dir
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Start Directory", current_dir)
        if directory:
            self.path_edit.setText(directory)

    def dir_field_command(self):
        current_dir = self.path_edit.text()
        if not os.path.isdir(current_dir):
            print('Directory not found: default start directory will be used instead')

    def index_algorithm(self, checked):
        if checked:
            self.tolerance_edit.setEnabled(False)

    def position_algorithm(self, checked):
        if checked:
            self.tolerance_edit.setEnabled(True)

    def set_tolerance(self):
        tolerance_text = self.tolerance_edit.text()
        try:
            tolerance_val = float(tolerance_text)
            if tolerance_val <= 0:
                raise ValueError
        except ValueError:
            print('Tolerance must be of type "float". Only positive, non-zero values are allowed.')

    def mesh_button_command(self):
        self.input_mesh = []
        self.input_transform_name = None
        selection = pm.ls(selection=True)
        if selection:
            target = selection[-1]
            target_shape = self.get_target_shape(target)
            if target_shape is not None:
                if self.is_a_mesh(target_shape):
                    self.input_mesh = target_shape
                    self.input_transform_name = target
                    self.deformers_scroll_list()
                    return
        print('Select a valid mesh')

    def deformers_scroll_list(self):
        self.deformers_list.clear()
        if 'findDeformers' in dir(pm):
            deformers_list = self.get_deformers()
        else:
            deformers_list = self.get_deformers_legacy()

        if deformers_list:
            for d_item in deformers_list:
                list_entry = d_item['Type'] + ' - ' + d_item['Name']
                self.deformers_list.addItem(list_entry)
        else:
            mayaPrint.warning('No valid deformer affects the selected mesh')

    def get_deformers(self):
        deformers_list = []
        deformer_names = pm.findDeformers(self.input_mesh)
        if deformer_names:
            for d_name in deformer_names:
                d_type = pm.objectType(d_name)
                if d_type in self.valid_deformers:
                    deformers_list.append({'Name': d_name, 'Type': d_type})
            if deformers_list:
                def custom_sort(list_element):
                    return list_element['Type'] + list_element['Name']
                deformers_list.sort(key=custom_sort)
                return deformers_list
        return None

    def get_deformers_legacy(self):
        deformers_list = []
        deformer_sets = pm.listSets(type=2, object=self.input_mesh)
        deformer_names = [deformer_sets[index].getAttr('usedBy[0]') for index in range(0, len(deformer_sets))]
        for d_name in deformer_names:
            d_type = pm.objectType(d_name)
            if d_type in self.valid_deformers:
                deformers_list.append({'Name': d_name, 'Type': d_type})
        if deformers_list:
            def custom_sort(list_element):
                return list_element['Type'] + list_element['Name']

            deformers_list.sort(key=custom_sort)
            return deformers_list
        return None

    def get_target_shape(self, target):
        target_shape = None
        if pm.objExists(target):
            sel_list = pm.ls(target)
            shape_list = pm.listRelatives(sel_list[0], shapes=True, path=True, noIntermediate=True)
            if shape_list:
                target_shape = shape_list[0]
            else:
                target_shape = sel_list[0]
        return target_shape

    def is_a_mesh(self, target_shape):
        return_value = False
        target_type = pm.objectType(target_shape)
        if target_type == 'mesh':
            return_value = True
        return return_value

    def get_algorithm_selection_by_id(self):
        """
        """
        return self.algorithm_group.checkedId()

    def get_direction_selection_by_id(self):
        """
        使用 ID 获取对称方向的选中状态
        返回值: 1 表示 "+ > - (正 > 负)", 2 表示 "- > + (负 > 正)"
        """
        return self.direction_group.checkedId()

    def get_plane_selection_by_id(self):
        """
        使用 ID 获取对称平面的选中状态
        返回值: 1 表示 "YZ", 2 表示 "XZ", 3 表示 "XY"
        """
        return self.plane_group.checkedId()


    def save_weights(self, *args):
        current_dir = self.path_edit.text()
        deformers_list_entry = _obj.get_list_widget_seleted(self.deformers_list)
        try:
            if self.input_transform_name:
                vtxs = pm.select("{}.vtx[0:]".format(self.input_transform_name), r=1)
        except:
            mayaPrint.error(u"Check whether mesh is loaded.检查是否正确载入mesh.")
            return
        if not self.input_mesh:
            raise ValueError('Select a valid mesh')

        deform_edit = DeformersWeightsEditor(self.input_mesh, self.input_transform_name, deformers_list_entry, path=current_dir)
        deform_edit.save_weights()

        return

    def load_weights(self, *args):
        current_dir = self.path_edit.text()
        deformers_list_entry = _obj.get_list_widget_seleted(self.deformers_list)
        loadTolerance = self.get_algorithm_selection_by_id()
        try:
            if self.input_transform_name:
                vtxs = pm.select("{}.vtx[0:]".format(self.input_transform_name), r=1)
        except:
            mayaPrint.error(u"Check whether mesh is loaded.检查是否正确载入mesh.")
            return

        if not self.input_mesh:
            raise ValueError('Select a valid mesh')

        deform_edit = DeformersWeightsEditor(self.input_mesh, self.input_transform_name, deformers_list_entry,
                                             path=current_dir, loadTolerance=loadTolerance)

        pm.undoInfo(openChunk=True)
        try:
            deform_edit.load_weights()
        finally:
            pm.undoInfo(closeChunk=True)

        return

    def mirror_weights(self, *args):
        deformers_list_entry = _obj.get_list_widget_seleted(self.deformers_list)
        arix = self.symmetry_axis[self.get_plane_selection_by_id()]
        direction = self.get_direction_selection_by_id()
        deform_edit = DeformersWeightsEditor(self.input_mesh, self.input_transform_name, deformers_list_entry, None, None, arix, direction)

        pm.undoInfo(openChunk=True)
        try:
            deform_edit.mirror_weights()
        finally:
            pm.undoInfo(closeChunk=True)

        return

    def flip_weights(self, *args):
        deformers_list_entry = _obj.get_list_widget_seleted(self.deformers_list)
        arix = self.symmetry_axis[self.get_plane_selection_by_id()]
        direction = self.get_direction_selection_by_id()
        deform_edit = DeformersWeightsEditor(self.input_mesh, self.input_transform_name, deformers_list_entry, None, None, arix,
                                             direction)
        pm.undoInfo(openChunk=True)
        try:
            deform_edit.flip_weights()
        finally:
            pm.undoInfo(closeChunk=True)

        return

    def copy_source(self, *args):
        if not self.input_mesh:
            raise ValueError('Select a valid mesh')

        selected_items = self.deformers_list.selectedItems()
        if not selected_items:
            raise ValueError('Select a valid deformer')

        deformer_entry = selected_items[0].text()
        deformer_type = deformer_entry.split(' - ')[0]
        selected_deformer = deformer_entry.split(' - ')[1]

        user_message = '{}  ->  {}'.format(self.input_mesh, selected_deformer)
        self.source_label.setText(user_message)
        self.copy_source_info = [self.input_mesh, (deformer_type, selected_deformer)]

    def copy_target(self, *args):
        if not self.input_mesh:
            raise ValueError('Select a valid mesh')

        selected_items = self.deformers_list.selectedItems()
        if not selected_items:
            raise ValueError('Select a valid deformer')

        deformer_entry = selected_items[0].text()
        deformer_type = deformer_entry.split(' - ')[0]
        selected_deformer = deformer_entry.split(' - ')[1]

        user_message = '{}  ->  {}'.format(self.input_mesh, selected_deformer)
        self.target_label.setText(user_message)
        self.copy_target_info = [self.input_mesh, (deformer_type, selected_deformer)]

    def copy_weights(self, *args):
        print([self.copy_source_info, self.copy_target_info])
        deform_edit = DeformersWeightsEditor(self.input_mesh, self.input_transform_name, copyweightInfo=[self.copy_source_info, self.copy_target_info])
        deform_edit.copy_weights()


class CopyDeformWeightUI(PyouPersistentWindow):

    def __init__(self, parent=_widgest.maya_main_window()):
        super(CopyDeformWeightUI, self).__init__("EditDeformWeightApp", "EditDeformWeightUI", parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.WINDOW_NAME = 'Edit Deform Weight '
        self.timeStamp = "2024-2026"
        self.name = "None"
        self._text_font = "font: bold 12px"

        self.setWindowTitle(self.WINDOW_NAME)
        self.setMinimumWidth(260)
        self.loadWindowSettings()

        self.init_ui()
        self.create_connections()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(_widgest.create_title(self.WINDOW_NAME, 15, 30))
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.main_tab_widget = QtWidgets.QTabWidget()
        layout.addWidget(self.main_tab_widget)
        self.main_tab_widget.setContentsMargins(0, 0, 0, 0)

        copy_tab = QtWidgets.QWidget()
        copy_tab_layout = QtWidgets.QVBoxLayout(copy_tab)
        self.scroll_layout(copy_tab_layout)
        self.main_tab_widget.addTab(copy_tab, 'Copy')

        edit_tab = QtWidgets.QWidget()
        edit_tab_layout = QtWidgets.QVBoxLayout(edit_tab)

        self.deform_editor = DeformersWeightsEditorWidget()
        edit_tab_layout.addWidget(self.deform_editor)
        edit_tab_layout.setContentsMargins(0, 0, 0, 0)
        edit_tab_layout.setSpacing(0)
        self.main_tab_widget.addTab(edit_tab, 'Edit')

        self.type_group = _widgest.create_radiogroup(
            "copy type",
            [
                ("not node", 1, u"target对象没有可指定的变形节点"),
                ("assign node", 2, u"target有可指定的节点"),
            ],
            default_id=1
        )

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.setSpacing(2)

        self.apply_btn = QtWidgets.QPushButton("Copy")
        self.apply_btn.setProperty("main", True)
        self.apply_btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.help_btn = QtWidgets.QPushButton()
        self.help_btn.setIcon(QtGui.QIcon(":/help.png"))
        self.help_btn.setProperty("help", True)

        btn_layout.addWidget(self.apply_btn)
        btn_layout.addWidget(self.help_btn)
        copy_tab_layout.addWidget(self.type_group )

        copy_tab_layout.addWidget(_widgest.create_text(
            u"支持一对一/一对多; 支持不同节点权重相互拷贝['blendShape', 'cluster', 'ffd', 'nonLinear', 'shrinkWrap', 'wire', 'deltaMush']\n使用: 载入source deform node; target 对象如果没有变形节点，就直接载入模型，如果有选择节点载入\n"))
        copy_tab_layout.addLayout(btn_layout)
        main_layout.addLayout(layout)
        _widgest.create_copyrightText(main_layout, self.timeStamp)

    def scroll_layout(self, parent):
        layout = QtWidgets.QVBoxLayout()

        source_label = _widgest.create_text(u" source ", 12, "center")
        target_label = _widgest.create_text(u" target ", 12, "center")

        self.cls_layout = QtWidgets.QHBoxLayout()
        source_deform_layout = QtWidgets.QVBoxLayout()

        source_deform_layout.addWidget(source_label)

        self.source_deform_scroll_list = QtWidgets.QListWidget(self)
        self.source_deform_scroll_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        source_deform_layout.addWidget(self.source_deform_scroll_list)

        target_deform_layout = QtWidgets.QVBoxLayout()
        target_deform_layout.addWidget(target_label)

        self.target_deform_scroll_list = QtWidgets.QListWidget(self)
        self.target_deform_scroll_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        target_deform_layout.addWidget(self.target_deform_scroll_list)

        scr_btn_lay = QtWidgets.QHBoxLayout()
        tar_btn_lay = QtWidgets.QHBoxLayout()

        self.load_scr_btn = QtWidgets.QPushButton("load source")
        self.load_scr_btn.setProperty("green", True)

        self.remove_scr_btn = QtWidgets.QPushButton("remove")
        self.remove_scr_btn.setProperty("danger", True)

        self.load_tar_btn = QtWidgets.QPushButton("load target")
        self.load_tar_btn.setProperty("green", True)

        self.remove_tar_btn = QtWidgets.QPushButton("remove")
        self.remove_tar_btn.setProperty("danger", True)

        scr_btn_lay.addWidget(self.load_scr_btn)
        scr_btn_lay.addWidget(self.remove_scr_btn)

        tar_btn_lay.addWidget(self.load_tar_btn)
        tar_btn_lay.addWidget(self.remove_tar_btn)

        source_deform_layout.addLayout(scr_btn_lay)
        target_deform_layout.addLayout(tar_btn_lay)

        self.cls_layout.addLayout(source_deform_layout)
        self.cls_layout.addLayout(target_deform_layout)

        layout.addLayout(self.cls_layout)
        parent.addLayout(layout)

    def create_connections(self):
        self.source_deform_scroll_list.itemSelectionChanged.connect(
            lambda: _obj.list_widget_seleted_item(self.source_deform_scroll_list))
        self.load_scr_btn.clicked.connect(lambda: self.load_items(self.source_deform_scroll_list, False))
        self.remove_scr_btn.clicked.connect(lambda: _obj.remove_seleted_items(self.source_deform_scroll_list))
        self.target_deform_scroll_list.itemSelectionChanged.connect(
            lambda: _obj.list_widget_seleted_item(self.target_deform_scroll_list))
        self.load_tar_btn.clicked.connect(lambda: self.load_items(self.target_deform_scroll_list, False, True))
        self.remove_tar_btn.clicked.connect(lambda: _obj.remove_seleted_items(self.target_deform_scroll_list))

        self.apply_btn.clicked.connect(self.apply)
        self.help_btn.clicked.connect(lambda: Help.HelpImage("", "copy_deform_weight_tool"))

    def load_items(self, list_widget, clear=True, tar_type=False):
        '''
        :param list_widget: QtWidgets.QListWidget()
        :param clear:
        :return:
        '''
        if clear:
            list_widget.clear()

        sel = pm.ls(sl=True) or []
        if sel:
            sel = [obj.name() for obj in sel]
            if tar_type:
                if self.type_group.checkedId() == 1:
                    list_widget.addItems(sel)

                else:
                    if len(sel) < 2:
                        mayaPrint.warning(u"Check if the deformation node is selected")
                        return

                    input_info = "{}.{}".format(sel[1], sel[0])
                    list_widget.addItems([input_info])

            else:
                if len(sel) < 2:
                    mayaPrint.warning(u"Check if the deformation node is selected")
                    return

                input_info = "{}.{}".format(sel[1], sel[0])
                list_widget.addItems([input_info])

    def apply(self, *args):
        deform_edit = DeformersWeightsEditor()
        pm.undoInfo(openChunk=True)
        try:

            sources = list(
                _obj.get_list_widget_items(
                    self.source_deform_scroll_list
                )
            )

            targets = list(
                _obj.get_list_widget_items(
                    self.target_deform_scroll_list
                )
            )

            source_data = []

            for item in sources:

                if "." not in item:
                    mayaPrint.error(
                        "Please load the source deformation node."
                    )
                    return

                source_data.append(
                    tuple(item.split(".", 1))
                )

            target_data = [
                tuple(item.split(".", 1))
                if "." in item
                else (item, None)
                for item in targets
            ]

            if len(source_data) == len(target_data):

                pairs = zip(
                    source_data,
                    target_data
                )

            elif len(source_data) == 1:

                pairs = [
                    (
                        source_data[0],
                        tar
                    )
                    for tar in target_data
                ]

            else:

                mayaPrint.warning(
                    u"Only supports one-to-one and one-to-many."
                )
                return

            for (scr, scr_def), (tar, tar_def) in pairs:
                deform_edit.copy_deform_node_weight(
                    scr,
                    scr_def,
                    tar,
                    tar_def
                )

                print(
                    "{}.{} -> {}.{}".format(
                        scr,
                        scr_def,
                        tar,
                        tar_def or scr_def
                    )
                )

            mayaPrint.log(
                "Copy completed."
            )

        finally:
            if pm.objExists("def_temp_grp"):
                pm.delete("def_temp_grp")
            pm.undoInfo(closeChunk=True)

def main():
    global pyDeform_editor

    try:
        pyDeform_editor.close()  # pylint: disable=E0601
        pyDeform_editor.deleteLater()
    except:
        pass

    pyDeform_editor = CopyDeformWeightUI(parent=_widgest.maya_main_window())
    pyDeform_editor.show()
    return


if __name__ == "__main__":
    main()