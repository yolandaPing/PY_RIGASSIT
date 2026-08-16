# -*- coding: utf-8 -*-

# .FileName:curvesFromTubesPro.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/6/23 23:46
# .Finish time:
# -*- coding: utf-8 -*-
from __future__ import print_function, division
import sys
import time
import traceback

import maya.cmds as cmds
import maya.api.OpenMaya as om

from py_rigAssit import QtWidgets, QtCore, QtGui, QAction, Widgets, PyouPersistentWindow
from py_rigAssit.dialogs import Help, mayaPrint

from GeneralTools.curves_from_tubes_core import PYCurveTubeBuilder


PY2 = sys.version_info[0] == 2
try:
    xrange
except NameError:
    xrange = range
try:
    long
except NameError:
    long = int

PY_WIDGEST = Widgets()


def log(msg):
    mayaPrint.log("[PY_CFT] {}".format(msg))


def safe_delete(node):
    if not node:
        return
    try:
        if cmds.objExists(node):
            cmds.delete(node)
    except:
        pass


def get_dag_path(node):
    sel = om.MSelectionList()
    sel.add(node)
    try:
        return sel.getDagPath(0)
    except TypeError:
        dag, _ = sel.getDagPath(0)
        return dag


def list_mesh_transforms(selection_only=True):
    result = []
    if selection_only:
        nodes = cmds.ls(sl=True, long=True) or []
    else:
        nodes = cmds.ls(type="transform", long=True) or []

    for node in nodes:
        shapes = cmds.listRelatives(node, s=True, ni=True, fullPath=True) or []
        for s in shapes:
            if cmds.nodeType(s) == "mesh":
                result.append(node)
                break
    return list(set(result))


def create_log_widget():
    class _Log(QtWidgets.QTextEdit):
        def __init__(self):
            super(_Log, self).__init__()
            self.setReadOnly(True)

        def write_line(self, text):
            """Append text with newline."""
            self.append(text)

    return _Log()


class PYTopologyDialog(QtWidgets.QDialog):
    def __init__(self, rows, parent=None):
        super(PYTopologyDialog, self).__init__(parent)
        self.rows = rows
        self.setWindowTitle("Topology Report")
        self.resize(420, 420)

        layout = QtWidgets.QVBoxLayout(self)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Mesh", "Error"])
        self.table.setRowCount(len(rows))
        self.table.horizontalHeader().setStretchLastSection(True)

        for i, (mesh, error) in enumerate(rows):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(mesh))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(error))

        layout.addWidget(self.table)

        btn = QtWidgets.QPushButton("Copy Report")
        btn.clicked.connect(self.copy_report)
        layout.addWidget(btn)

    def copy_report(self):
        text = ["{} | {}".format(mesh, error) for mesh, error in self.rows]
        QtWidgets.QApplication.clipboard().setText("\n".join(text))


class PYCurveTubeProcessor(object):
    def __init__(self, ui=None):
        self.ui = ui
        self.builder = PYCurveTubeBuilder()
        self.trash = []  # additional trash from processor
        self.bad_topology = []
        self.curves_grp = "tubes_curves_grp"
        self.joints_grp = "tubes_joints_grp"

    def info(self, text):
        log(text)
        if self.ui and hasattr(self.ui, 'log_widget'):
            self.ui.log_widget.write_line(text)

    def progress(self, value):
        if self.ui and hasattr(self.ui, 'progress'):
            self.ui.progress.setValue(value)
            # QApplication may not be imported here, but UI will handle events if needed

    def add_trash(self, node):
        if node and node not in self.trash:
            self.trash.append(node)

    def cleanup(self):
        # cleanup builder's trash and own trash
        self.builder.cleanup()
        for n in self.trash:
            safe_delete(n)
        self.trash = []

    def report_bad_mesh(self, mesh, reason):
        self.bad_topology.append((mesh, reason))
        self.info("[BAD TOPOLOGY] {} -> {}".format(mesh, reason))

    def collect_meshes(self, type_id=0):

        selection = cmds.ls(sl=True, long=True) or []
        if not selection:
            if type_id == 2:
                return self.process_visible()
            else:
                return []

        if type_id == 1:
            root = selection[0]
            return self.process_hierarchy(root)

        else:
            meshes = set()
            for node in selection:
                if not cmds.objExists(node):
                    continue
                ntype = cmds.nodeType(node)
                if ntype == "transform":
                    shapes = cmds.listRelatives(node, s=True, ni=True, fullPath=True) or []
                    for s in shapes:
                        if cmds.nodeType(s) == "mesh":
                            meshes.add(node)
                            break
                elif ntype == "mesh":
                    parent = cmds.listRelatives(node, parent=True, fullPath=True) or []
                    if parent:
                        meshes.add(parent[0])
            return sorted(list(meshes))

    def process_hierarchy(self, root):
        transforms = []
        descendants = cmds.listRelatives(root, ad=True, fullPath=True) or []

        for node in descendants:
            if cmds.nodeType(node) != "transform":
                continue
            shapes = cmds.listRelatives(node, s=True, ni=True, fullPath=True) or []
            for s in shapes:
                if cmds.nodeType(s) == "mesh":
                    transforms.append(node)
                    break
        return transforms

    def process_visible(self):
        shapes = cmds.ls(type="mesh", long=True) or []
        visible = []
        for shape in shapes:
            if cmds.getAttr(shape + ".visibility"):
                parent = cmds.listRelatives(shape, p=True, fullPath=True)
                if parent:
                    visible.append(parent[0])
        return visible

    def prepare_groups(self, mode):
        if not cmds.objExists(self.curves_grp):
            self.curves_grp = cmds.group(em=True, name=self.curves_grp)
        if mode == "joint" and not cmds.objExists(self.joints_grp):
            self.joints_grp = cmds.group(em=True, name=self.joints_grp)

    def parent_outputs(self, curve, mode):
        try:
            if curve and cmds.objExists(self.curves_grp):
                cmds.parent(curve, self.curves_grp)
        except:
            pass
        if mode == "joint":
            joints = cmds.ls("*_jnt", type="joint") or []
            roots = [j for j in joints if not cmds.listRelatives(j, p=True)]
            for root in roots:
                try:
                    cmds.parent(root, self.joints_grp)
                except:
                    try:
                        cmds.parent(root, "tubes_joints_grp")
                    except:
                        pass

    def reset_runtime_state(self):
        self.bad_topology = []
        self.trash = []
        self.builder.trash = []
        if self.ui and hasattr(self.ui, 'progress'):
            self.ui.progress.setValue(0)
        if self.ui and hasattr(self.ui, 'log_widget'):
            self.ui.log_widget.clear()

    def process_single_mesh(self, mesh, mode="default",
                            threshold=0.01, reverse=False,
                            dropoff=50.0, joint_count=10,
                            orient="zyx", secondary_axis="y"):
        """
        处理单个网格：自动预处理、提取曲线，并根据模式创建 Wire 或 Joint。
        返回生成的曲线列表（可能为空）。
        """
        dag = get_dag_path(mesh)
        error = self.builder.check_mesh(dag)
        if error:
            self.report_bad_mesh(mesh, error)
            return []

        self.info("Processing {}".format(mesh))

        curves = self.builder.extract_curves_from_mesh(mesh, threshold, reverse)
        if not curves:
            self.report_bad_mesh(mesh, u"未找到干净的管状壳体或曲线提取失败")
            return []

        created_curves = []
        for curve in curves:
            if mode == "wire":
                self.builder.create_wire_deformer(mesh, curve, dropoff)
            elif mode == "joint":
                self.builder.create_joint_chain(curve, mesh, joint_count, orient, secondary_axis)

            self.parent_outputs(curve, mode)
            created_curves.append(curve)

        if self.builder.trash:
            self.trash.extend(self.builder.trash)
            self.builder.trash = []

        return created_curves

    def create(self, mode="default", hierarchy=0):
        """
        Main entry point for UI. Reads values from self.ui if available.
        """
        # Gather UI values
        threshold = 0.01
        reverse = False
        dropoff = 50.0
        joint_count = 10
        orient = "zyx"
        secondary_axis = "y"

        if self.ui:
            try:
                threshold = float(self.ui.threshold.text())
            except:
                pass
            try:
                reverse = self.ui.reverse_curve.isChecked()
            except:
                pass
            try:
                dropoff = float(self.ui.dropoff.text())
            except:
                pass
            try:
                joint_count = int(self.ui.joint_count.text())
            except:
                pass
            try:
                orient = self.ui.orient_combo.currentText()
            except:
                pass
            try:
                secondary_axis = self.ui.axis_combo.currentText()
            except:
                pass

        self.reset_runtime_state()
        start_time = time.time()
        cmds.undoInfo(openChunk=True)
        try:
            meshes = self.collect_meshes(hierarchy)
            if not meshes:
                self.info("No mesh selected.")
                return

            self.info("=" * 50)
            self.info("CurvesFromTubes Pro Started")
            self.info("Mode: {}".format(mode))
            self.info("Mesh count: {}".format(len(meshes)))
            self.prepare_groups(mode)

            all_curves = []  # 存储所有生成的曲线
            total = float(len(meshes))
            for i, mesh in enumerate(meshes):
                progress = int((float(i) / total) * 100.0)
                self.progress(progress)
                try:
                    curves = self.process_single_mesh(
                        mesh, mode,
                        threshold=threshold,
                        reverse=reverse,
                        dropoff=dropoff,
                        joint_count=joint_count,
                        orient=orient,
                        secondary_axis=secondary_axis
                    )
                    if curves:
                        all_curves.extend(curves)
                        self.info("[OK] {} ({} curves)".format(mesh, len(curves)))
                except Exception:
                    self.report_bad_mesh(mesh, traceback.format_exc())

            self.progress(100)
            if all_curves:
                cmds.select(all_curves)
            else:
                self.info("No curves created.")

            elapsed = time.time() - start_time
            self.info("=" * 50)
            self.info("Finished in {:.3f}s".format(elapsed))
            self.info("Created curves: {}".format(len(all_curves)))
            if self.bad_topology:
                self.info("Bad topology count: {}".format(len(self.bad_topology)))

            self.cleanup()

        except Exception:
            self.info(traceback.format_exc())
        finally:
            cmds.undoInfo(closeChunk=True)

class PYAboutDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PYAboutDialog, self).__init__(parent)
        self.setWindowTitle("About")
        self.resize(200, 220)
        layout = QtWidgets.QVBoxLayout(self)
        text = QtWidgets.QTextEdit()
        text.setReadOnly(True)
        text.setText(
            "PY CurvesFromTubes Pro\n\n"
            "Supported Maya Versions:\n"
            "2018 - 2026\n\n"
            "Features:\n"
            "- Curve Extraction\n"
            "- Wire Deformer\n"
            "- Joint Chain\n"
            "- Topology Report\n"
            "- Batch Processing\n\n"
            "Rebuilt for production pipeline."
        )
        layout.addWidget(text)


class PYCurvesFromTubesPro(PyouPersistentWindow):
    WEBS = "https://www.bilibili.com/video/..."

    def __init__(self, parent=None):
        super(PYCurvesFromTubesPro, self).__init__("PYCurvesFromTubesPro", "PYCurvesFromTubesProDialog", parent)
        self.processor = PYCurveTubeProcessor(self)
        self.setWindowTitle("Curves From Tubes Pro")
        self.resize(220, 420)
        self.init_ui()
        # self.loadWindowSettings()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(6)
        self.create_menu_bar(main_layout)
        main_layout.addWidget(
            PY_WIDGEST.create_title("Curves From Tubes", 14, self.WEBS)
        )

        container = QtWidgets.QWidget()
        container.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        cld_layout = QtWidgets.QVBoxLayout(container)
        cld_layout.setContentsMargins(0, 0, 0, 0)
        cld_layout.setSpacing(2)

        tip_layout = QtWidgets.QVBoxLayout()
        tip_layout.setContentsMargins(0, 0, 0, 0)
        tip_layout.setSpacing(2)

        sec1 = PY_WIDGEST.create_section("create Curve")
        sec2 = PY_WIDGEST.create_section("curve Wire")
        sec3 = PY_WIDGEST.create_section("create Joint")
        sec4 = PY_WIDGEST.create_section("report ")
        self.threshold = PY_WIDGEST.create_floatSlider("Threshold CV:")
        self.threshold.setRange(.001, 10)
        self.threshold.setValue(0.01)

        self.reverse_curve = QtWidgets.QCheckBox("Reverse Curve")

        self.dropoff = QtWidgets.QSpinBox()
        self.dropoff.setRange(.001, 10000)
        self.dropoff.setValue(100)
        self.joint_count = QtWidgets.QSpinBox()
        self.joint_count.setValue(10)
        self.dropoff.setFixedWidth(50)
        self.joint_count.setFixedWidth(50)

        Dropoff_form = QtWidgets.QFormLayout()
        label = PY_WIDGEST.create_text('Wire Dropoff:')
        Dropoff_form.addRow(label, self.dropoff)
        sec2.addLayout(Dropoff_form)

        count_layout = QtWidgets.QVBoxLayout()
        Count_form = QtWidgets.QFormLayout()
        label = PY_WIDGEST.create_text('关节数量:')
        Count_form.addRow(label, self.joint_count)
        count_layout.addLayout(Count_form)

        orient_layout = QtWidgets.QHBoxLayout()
        orient_layout.addWidget(QtWidgets.QLabel("Orient:"))
        self.orient_combo = QtWidgets.QComboBox()
        self.orient_combo.addItems(["zyx", "xyz", "yzx", "zxy", "yxz", "xzy", "none"])

        orient_layout.addWidget(QtWidgets.QLabel("Axis:"))
        self.axis_combo = QtWidgets.QComboBox()
        self.axis_combo.addItems(["y", "x", "-x", "-y", "z", "-z", "none"])

        orient_layout.addWidget(self.orient_combo)
        orient_layout.addWidget(self.axis_combo)
        count_layout.addLayout(orient_layout)
        sec3.addLayout(count_layout)

        btn_group = QtWidgets.QGroupBox("Actions")
        btn_layout = QtWidgets.QVBoxLayout(btn_group)
        btn_layout.addLayout(tip_layout)

        self.create_type = PY_WIDGEST.create_radioSelector(["Seleted", "Hierarchy", "Visible"], columns=3)

        tip_layout.addWidget(self.create_type)
        tip_layout.addWidget(self.threshold)
        tip_layout.addWidget(self.reverse_curve)
        PY_WIDGEST.separator(tip_layout, True)
        PY_WIDGEST.separator(tip_layout, False)

        self.btn_curve = QtWidgets.QPushButton("Create Curves")
        self.btn_wire = QtWidgets.QPushButton("Create Wire Deformer")

        self.btn_joint = QtWidgets.QPushButton("Create Joint Chain")
        self.btn_report = QtWidgets.QPushButton("查看拓扑报告")

        sec1.addWidget(self.btn_curve)
        sec2.addWidget(self.btn_wire)
        sec3.addWidget(self.btn_joint)
        sec4.addWidget(self.btn_report)

        for btn in (sec1, sec2, sec3, sec4):
            btn_layout.addWidget(btn)
        cld_layout.addWidget(btn_group)

        self.progress = QtWidgets.QProgressBar()
        self.progress.setValue(0)
        cld_layout.addWidget(self.progress)

        # log
        self.log_widget = create_log_widget()
        cld_layout.addWidget(self.log_widget, 1)
        main_layout.addWidget(container)
        PY_WIDGEST.create_copyrightText(main_layout, "2026")
        self.log_widget.setVisible(False)

        self.btn_curve.clicked.connect(lambda: self.processor.create("default", self.create_type.checkedId()))
        self.btn_wire.clicked.connect(lambda: self.processor.create("wire", self.create_type.checkedId()))
        self.btn_joint.clicked.connect(lambda: self.processor.create("joint", self.create_type.checkedId()))
        self.btn_report.clicked.connect(self.show_report)

    def create_menu_bar(self, parent_layout):
        menu_bar = QtWidgets.QMenuBar()
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        e_mail = QAction("bilibili:我有一只猛犬", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        help_menu.addAction(e_mail)
        parent_layout.setMenuBar(menu_bar)

    def export_log(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export Log", "", "Text Files (*.txt)"
        )
        if path:
            with open(path, "w") as f:
                f.write(self.log_widget.toPlainText())

    def show_about(self):
        dlg = PYAboutDialog(self)
        dlg.show()

    def show_report(self):
        if not self.processor.bad_topology:
            QtWidgets.QMessageBox.information(self, "Info", u"没有拓扑问题")
            return
        dlg = PYTopologyDialog(self.processor.bad_topology, self)
        dlg.show()


def show():
    global _py_tubes_window
    try:
        _py_tubes_window.close()  # pylint: disable=E0601
        _py_tubes_window.deleteLater()
    except:
        pass

    _py_tubes_window = PYCurvesFromTubesPro(PY_WIDGEST.maya_main_window())
    _py_tubes_window.show()


if __name__ == "__main__":
    show()