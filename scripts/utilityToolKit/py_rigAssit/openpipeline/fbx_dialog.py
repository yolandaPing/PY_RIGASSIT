# -*- coding: utf-8 -*-

# .FileName:fbx_dialog.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2025/12/18 21:08
# .Finish time:

"""
FBX导出设置对话框模块
独立的非模态对话框，解决界面阻塞问题。
"""
try:
    from ui_framework.core.qtCompat import *
    from ui_framework.widgets.widgets import Widgets, PyouPersistentWindow
except:
    from CommonUse.qtCompat import *
    from CommonUse.widgetsUse import Widgets, PyouPersistentWindow

try:
    import maya.cmds as cmds
    IN_MAYA = True
except Exception:
    IN_MAYA = False

_widgest = Widgets()


class FBXExportDialog(QtWidgets.QDialog):
    """FBX导出设置对话框（非模态）"""

    def __init__(self, parent=None, fbx_config=None):
        super(FBXExportDialog, self).__init__(parent)
        self.fbx_config = fbx_config or ['Geo_grp', 'root_jnt']
        self.setWindowTitle(u'设置FBX导出对象')
        self.setFixedSize(400, 200)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # 几何体组设置行
        geo_layout = QtWidgets.QHBoxLayout()
        geo_label = QtWidgets.QLabel(u'几何体组名称:')
        geo_label.setFixedWidth(120)
        self.geo_name_edit = QtWidgets.QLineEdit()
        self.geo_name_edit.setText(self.fbx_config[0])
        get_geo_btn = QtWidgets.QPushButton(u'<<<')
        get_geo_btn.clicked.connect(lambda: self.get_object_from_scene(self.geo_name_edit))
        geo_layout.addWidget(geo_label)
        geo_layout.addWidget(self.geo_name_edit)
        geo_layout.addWidget(get_geo_btn)
        layout.addLayout(geo_layout)

        # 根关节设置行
        joint_layout = QtWidgets.QHBoxLayout()
        joint_label = QtWidgets.QLabel(u'根关节名称:')
        joint_label.setFixedWidth(120)
        self.joint_name_edit = QtWidgets.QLineEdit()
        self.joint_name_edit.setText(self.fbx_config[1])
        get_joint_btn = QtWidgets.QPushButton(u'<<<')
        get_joint_btn.clicked.connect(lambda: self.get_object_from_scene(self.joint_name_edit, 'joint'))
        joint_layout.addWidget(joint_label)
        joint_layout.addWidget(self.joint_name_edit)
        joint_layout.addWidget(get_joint_btn)
        layout.addLayout(joint_layout)

        # 提示信息
        info_label = QtWidgets.QLabel(u'提示：这些名称将在导出FBX时自动查找并导出')
        info_label.setStyleSheet('color: #666; font-size: 11px;')
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # 按钮行
        button_layout = QtWidgets.QHBoxLayout()
        test_btn = QtWidgets.QPushButton(u'测试对象')
        test_btn.clicked.connect(self.test_fbx_objects)
        button_layout.addWidget(test_btn)
        button_layout.addStretch()
        self.ok_btn = QtWidgets.QPushButton(u'确定')
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn = QtWidgets.QPushButton(u'取消')
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

    def get_object_from_scene(self, target_edit, obj_type='transform'):
        """从Maya场景中获取对象名称并填入文本框"""
        if not IN_MAYA:
            QtWidgets.QMessageBox.warning(self, u'错误', u'此功能只能在Maya中运行')
            return
        try:
            selected = cmds.ls(selection=True, type=obj_type)
            if selected:
                target_edit.setText(selected[0])
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, u'错误', u'获取场景对象失败:\n{}'.format(str(e)))

    def test_fbx_objects(self):
        """测试FBX导出对象是否存在于当前场景"""
        if not IN_MAYA:
            QtWidgets.QMessageBox.warning(self, u'错误', u'此功能只能在Maya中运行')
            return

        geo_name = self.geo_name_edit.text().strip()
        joint_name = self.joint_name_edit.text().strip()
        if not geo_name and not joint_name:
            QtWidgets.QMessageBox.warning(self, u'提示', u'请先设置要导出的对象名称')
            return

        try:
            missing_objects = []
            # 测试几何体组
            if geo_name:
                if not cmds.objExists(geo_name):
                    missing_objects.append(geo_name)
                elif cmds.objectType(geo_name) != 'transform':
                    missing_objects.append(u'{} (类型错误，期望transform)'.format(geo_name))
            # 测试根关节
            if joint_name:
                if not cmds.objExists(joint_name):
                    missing_objects.append(joint_name)
                elif cmds.objectType(joint_name) not in ['joint', 'transform']:
                    missing_objects.append(u'{} (类型错误，期望joint)'.format(joint_name))

            if not missing_objects:
                QtWidgets.QMessageBox.information(self, u'测试通过', u'所有设置的对象都存在于当前场景中')
            else:
                QtWidgets.QMessageBox.warning(self, u'测试失败', u'以下对象不存在或类型错误:\n\n' + '\n'.join(missing_objects))
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, u'错误', u'测试过程中发生错误:\n{}'.format(str(e)))

    def get_settings(self):
        """获取对话框中设置的FBX对象名称"""
        return [
            self.geo_name_edit.text().strip(),
            self.joint_name_edit.text().strip()
        ]