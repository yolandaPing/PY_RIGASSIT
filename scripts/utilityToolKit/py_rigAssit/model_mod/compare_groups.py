# -*- coding: utf-8 -*-

# .FileName:compare_groups.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/8/15 15:15
# .Finish time:

"""
Maya 层级结构对比工具
"""
from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
import maya.cmds as cmds

_widgest = Widgets()


def get_tree(long_path, ignore_namespace=True):
    """递归获取变换层级树，使用完整路径"""
    short_name = long_path.split('|')[-1]
    if ignore_namespace and ':' in short_name:
        short_name = short_name.split(':')[-1]

    children = cmds.listRelatives(long_path, children=True, type='transform', fullPath=True) or []
    child_trees = []
    for ch in children:
        child_trees.append(get_tree(ch, ignore_namespace))

    return {'name': short_name, 'long': long_path, 'children': child_trees}


def compare_trees(tree1, tree2, path=""):
    """
    递归比较两棵树，返回差异列表和状态映射。
    """
    diffs = []
    status_map = {}

    current_path = "{}/{}".format(path, tree1['name']) if path else tree1['name']

    # 比较名称
    name_match = (tree1['name'] == tree2['name'])
    if not name_match:
        diffs.append("名称不匹配: 位置 {}，期望 '{}'，实际 '{}'".format(
            path or '根', tree1['name'], tree2['name']))
        status_map[tree1['long']] = 'name_mismatch'
        status_map[tree2['long']] = 'name_mismatch'

    # 子节点数量
    len1, len2 = len(tree1['children']), len(tree2['children'])
    child_count_match = (len1 == len2)
    if not child_count_match:
        diffs.append("子节点数量不同: 位置 {}，{} vs {}".format(current_path, len1, len2))
        if tree1['long'] not in status_map:
            status_map[tree1['long']] = 'child_count_mismatch'
        if tree2['long'] not in status_map:
            status_map[tree2['long']] = 'child_count_mismatch'

    # 递归比较共同子节点
    for i in range(min(len1, len2)):
        sub_diffs, sub_status = compare_trees(tree1['children'][i], tree2['children'][i], current_path)
        diffs.extend(sub_diffs)
        status_map.update(sub_status)

    # 多余或缺少
    if len1 > len2:
        for extra in tree1['children'][len2:]:
            diffs.append("多余节点: '{}'，位置 {}".format(extra['name'], current_path))
            status_map[extra['long']] = 'extra'
    elif len2 > len1:
        for missing in tree2['children'][len1:]:
            diffs.append("缺少节点: '{}'，位置 {}".format(missing['name'], current_path))
            status_map[missing['long']] = 'missing'

    # 如果当前节点完全匹配，标记为 match（但子节点可能不匹配）
    if name_match and child_count_match and len1 == len2:
        has_child_diff = any(st != 'match' for st in status_map.values() if st in ('name_mismatch', 'child_count_mismatch', 'extra', 'missing'))
        if not has_child_diff:
            status_map[tree1['long']] = 'match'
            status_map[tree2['long']] = 'match'

    return diffs, status_map


class CompareGroupsUI(PyouPersistentWindow):

    def __init__(self, parent=_widgest.maya_main_window()):
        super(CompareGroupsUI, self).__init__("CompareGroupsUI", "CompareGroupsUI", parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.setWindowTitle("层级结构对比工具")
        self.tree1 = None
        self.tree2 = None
        self.status_map = {}
        self.init_ui()
        self.loadWindowSettings()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(_widgest.create_title("层级结构对比工具", 15, 30))
        select_layout = QtWidgets.QHBoxLayout()

        old_layout = QtWidgets.QHBoxLayout()
        self.old_group_edit = QtWidgets.QLineEdit()
        self.old_group_edit.setReadOnly(True)
        self.old_group_edit.setPlaceholderText("请选择旧组")
        old_btn = QtWidgets.QPushButton("<<<")
        old_btn.clicked.connect(lambda: self.select_group(self.old_group_edit))

        old_layout.addWidget(_widgest.create_text(" 旧组: ", 20))
        old_layout.addWidget(self.old_group_edit, 1)
        old_layout.addWidget(old_btn)

        new_layout = QtWidgets.QHBoxLayout()
        self.new_group_edit = QtWidgets.QLineEdit()
        self.new_group_edit.setReadOnly(True)
        self.new_group_edit.setPlaceholderText("请选择新组")
        new_btn = QtWidgets.QPushButton("<<<")
        new_btn.clicked.connect(lambda: self.select_group(self.new_group_edit))

        new_layout.addWidget(_widgest.create_text(" 新组: ", 20))
        new_layout.addWidget(self.new_group_edit, 1)
        new_layout.addWidget(new_btn)

        select_layout.addLayout(old_layout, 1)
        select_layout.addLayout(new_layout, 1)
        main_layout.addLayout(select_layout)

        tree_layout = QtWidgets.QHBoxLayout()
        self.old_tree = QtWidgets.QTreeWidget()
        self.old_tree.setHeaderLabel("> 旧组层级")
        self.old_tree.setIndentation(20)
        self.old_tree.setAlternatingRowColors(True)

        self.new_tree = QtWidgets.QTreeWidget()
        self.new_tree.setHeaderLabel("> 新组层级")
        self.new_tree.setIndentation(20)
        self.new_tree.setAlternatingRowColors(True)

        self.old_tree.itemClicked.connect(self.on_tree_item_clicked)
        self.new_tree.itemClicked.connect(self.on_tree_item_clicked)

        run_btn = QtWidgets.QPushButton("▶ 运行检查")
        run_btn.setProperty("main", True)
        run_btn.clicked.connect(self.run_comparison)

        tree_layout.addWidget(self.old_tree)
        tree_layout.addWidget(self.new_tree)
        main_layout.addLayout(tree_layout)
        _widgest.separator(main_layout, True)
        main_layout.addWidget(run_btn)

        self.diff_text = QtWidgets.QTextEdit()
        self.diff_text.setReadOnly(True)
        self.diff_text.setMaximumHeight(180)
        self.diff_text.setProperty("isInfos", True)
        self.diff_text.setPlaceholderText("差异信息将显示在此...")
        main_layout.addWidget(self.diff_text)

        _widgest.create_copyrightText(main_layout, "2026")

    def select_group(self, line_edit):
        sel = cmds.ls(selection=True, long=True)
        if not sel:
            cmds.warning("请先选中一个组节点")
            return
        node = sel[0]
        if not cmds.objectType(node, isAType='transform'):
            cmds.warning("所选不是 transform 节点")
            return
        if cmds.listRelatives(node, shapes=True):
            cmds.warning("所选节点包含形状，可能不是纯组。建议选择仅包含子变换的组。")
        line_edit.setText(node)
        line_edit.setToolTip(node)

    def run_comparison(self):
        old_path = self.old_group_edit.text()
        new_path = self.new_group_edit.text()
        if not old_path or not new_path:
            cmds.warning("请先选择两个组")
            return

        if not cmds.objExists(old_path):
            cmds.warning("旧组 '{}' 不存在".format(old_path))
            return
        if not cmds.objExists(new_path):
            cmds.warning("新组 '{}' 不存在".format(new_path))
            return

        try:
            self.tree1 = get_tree(old_path)
            self.tree2 = get_tree(new_path)
        except Exception as e:
            cmds.warning("获取层级树失败: {}".format(e))
            return

        summary_lines = [
            "旧组子节点数: {}，新组子节点数: {}".format(len(self.tree1['children']), len(self.tree2['children'])),
            "旧组顶层子节点: {}".format([c['name'] for c in self.tree1['children']]),
            "新组顶层子节点: {}".format([c['name'] for c in self.tree2['children']])
        ]
        summary = "\n".join(summary_lines)

        diffs, self.status_map = compare_trees(self.tree1, self.tree2)

        self.diff_text.clear()
        self.diff_text.append("【树结构摘要】")
        self.diff_text.append(summary)
        self.diff_text.append("")

        if diffs:
            self.diff_text.append("【差异列表】")
            for d in diffs:
                self.diff_text.append("  " + d)
        else:
            self.diff_text.append("✓ 两个组的层级结构和名称完全一致！")

        self.populate_tree(self.old_tree, self.tree1, side='old')
        self.populate_tree(self.new_tree, self.tree2, side='new')
        self.old_tree.expandAll()
        self.new_tree.expandAll()

    def populate_tree(self, tree_widget, tree_data, side):
        tree_widget.clear()
        root_item = QtWidgets.QTreeWidgetItem(tree_widget)
        self._add_tree_items(root_item, tree_data, side)
        root_item.setExpanded(True)

    def _add_tree_items(self, parent_item, tree_data, side):
        long_name = tree_data['long']
        display_name = tree_data['name']
        status = self.status_map.get(long_name, 'match')

        item = QtWidgets.QTreeWidgetItem(parent_item)
        item.setText(0, display_name)
        item.setToolTip(0, long_name)

        color = QtGui.QColor(255, 255, 255)  # 默认白色
        if status == 'match':
            color = QtGui.QColor(0, 255, 0)      # 绿色
        elif status == 'name_mismatch':
            color = QtGui.QColor(255, 165, 0)    # 橙色
        elif status == 'child_count_mismatch':
            color = QtGui.QColor(255, 165, 0)    # 橙色
        elif status == 'extra':
            color = QtGui.QColor(255, 0, 0)      # 红色
        elif status == 'missing':
            color = QtGui.QColor(100, 149, 237)  # 蓝色
        item.setForeground(0, QtGui.QBrush(color))

        for child in tree_data['children']:
            self._add_tree_items(item, child, side)

    def on_tree_item_clicked(self, item, column):
        """点击树节点时在 Maya 中选中该对象"""
        long_path = item.toolTip(0)
        if long_path and cmds.objExists(long_path):
            cmds.select(long_path, replace=True)
        else:
            cmds.warning("对象 '{}' 不存在或无效".format(long_path))


def show_ui():
    global py_compare_grps

    try:
        py_compare_grps.close()
        py_compare_grps.deleteLater()
    except:
        pass

    py_compare_grps = CompareGroupsUI()
    py_compare_grps.show()

    return


if __name__ == "__main__":
    show_ui()