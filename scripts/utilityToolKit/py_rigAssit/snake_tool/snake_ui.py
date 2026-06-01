# -*- coding: utf-8 -*-

# .FileName:snake_ui.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2025/12/28 21:08
# .Finish time:
# -*- coding: utf-8 -*-

import inspect,os
import maya.cmds as mc
from py_rigAssit import QtWidgets, QtCore, QtGui, QAction, Widgets, PyouPersistentWindow
from SnakeTools.core import guide
from SnakeTools.core import body_rigging
from SnakeTools.core import anim_effects
from SnakeTools.core import bind_skin

def get_current_dir():
    return os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe()))
    )

_widgest = Widgets()


class SNAKEDialog(PyouPersistentWindow):
    version = 'SnakeTools v 01.0.0'


    def __init__(self, parent=_widgest.maya_main_window()):
        super(SNAKEDialog, self).__init__("SNAKEDialogApp", "SNAKEDialog", parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.WINDOW_NAME = 'Snake Tool '
        self.timeStamp = "2025-2026"
        self.name = "None"
        self._text_font = "font: bold 12px"

        self.setWindowTitle(self.WINDOW_NAME)
        self.setMinimumWidth(260)
        self.loadWindowSettings()

        self.init_ui()
        self.create_connections()


    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        self.create_menu_bar(main_layout)
        # main_layout.addWidget(_widgest.create_title(self.WINDOW_NAME, 15, 30))

        # 创建logo区域
        self.create_logo_section(main_layout)

        tab_widget = QtWidgets.QTabWidget()

        rigging_tab = QtWidgets.QWidget()
        skin_tab = QtWidgets.QWidget()

        rigging_layout = QtWidgets.QVBoxLayout(rigging_tab)
        skin_layout = QtWidgets.QVBoxLayout(skin_tab)

        rigging_scroll = QtWidgets.QScrollArea()
        rigging_scroll.setWidgetResizable(True)
        rigging_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        rigging_content = QtWidgets.QWidget()
        self.rigging_content_layout = QtWidgets.QVBoxLayout(rigging_content)
        self.rigging_content_layout.setSpacing(10)
        self.rigging_content_layout.setAlignment(QtCore.Qt.AlignTop)

        self.create_guide_section()
        self.create_rig_section()

        rigging_scroll.setWidget(rigging_content)
        rigging_layout.addWidget(rigging_scroll)

        skin_scroll = QtWidgets.QScrollArea()
        skin_scroll.setWidgetResizable(True)
        skin_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        skin_content = QtWidgets.QWidget()
        self.skin_content_layout = QtWidgets.QVBoxLayout(skin_content)
        self.skin_content_layout.setSpacing(10)
        self.skin_content_layout.setAlignment(QtCore.Qt.AlignTop)

        self.create_skin_section()

        skin_scroll.setWidget(skin_content)
        skin_layout.addWidget(skin_scroll)

        tab_widget.addTab(rigging_tab, "Rigging")
        tab_widget.addTab(skin_tab, "Bind Skin")

        main_layout.addWidget(tab_widget)

        _widgest.create_copyrightText(main_layout, self.timeStamp)

        self.update_button_states()

    def create_menu_bar(self, parent_layout):
        """创建菜单栏"""
        menu_bar = QtWidgets.QMenuBar()

        help_menu = menu_bar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self._about)
        help_menu.addAction(about_action)

        parent_layout.addWidget(menu_bar)

    def create_logo_section(self, parent_layout):
        logo_layout = QtWidgets.QVBoxLayout()
        logo_layout.setAlignment(QtCore.Qt.AlignCenter)

        logo_widget = QtWidgets.QWidget()
        v = QtWidgets.QVBoxLayout(logo_widget)
        v.setAlignment(QtCore.Qt.AlignCenter)

        logo_img = QtWidgets.QLabel()
        logo_img.setFixedHeight(60)

        base_dir = get_current_dir()
        icon_path = os.path.join(base_dir, "icons", "snake_logo.png")

        pix = QtGui.QPixmap(icon_path)
        if pix.isNull():
            print("SnakeTools logo load failed:", icon_path)
        else:
            logo_img.setPixmap(
                pix.scaled(180, 60, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            )

        logo_img.setAlignment(QtCore.Qt.AlignCenter)

        logo_text = QtWidgets.QLabel(self.version)
        logo_text.setAlignment(QtCore.Qt.AlignCenter)
        logo_text.setStyleSheet("font-size:12px;font-weight:bold;color:#DDDDDD;")

        v.addWidget(logo_img)
        v.addWidget(logo_text)

        logo_layout.addWidget(logo_widget)
        parent_layout.addLayout(logo_layout)

        _widgest.separator(parent_layout, True)

    def create_guide_section(self):
        """创建引导定位器区域"""
        guide_frame = QtWidgets.QGroupBox("Import body Guides")

        guide_layout = QtWidgets.QVBoxLayout(guide_frame)
        guide_layout.setSpacing(10)

        # 标题
        title_label = QtWidgets.QLabel("Guide")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #FFFFFF;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        guide_layout.addWidget(title_label)

        # 关节数量说明
        guide_text2 = _widgest.create_text(">> 设置关节数量，总数是您设置的数量 2n +1", 15)

        guide_layout.addWidget(guide_text2)

        # 头部关节数量输入
        head_layout = QtWidgets.QHBoxLayout()
        head_label = QtWidgets.QLabel("Head joints:")
        self.head_count_input = QtWidgets.QSpinBox()
        self.head_count_input.setRange(1, 1)
        self.head_count_input.setValue(1)
        self.head_count_input.setEnabled(False)
        head_layout.addWidget(head_label)
        head_layout.addWidget(self.head_count_input)
        head_layout.addStretch()
        guide_layout.addLayout(head_layout)

        # 身体关节数量输入
        body_layout = QtWidgets.QHBoxLayout()
        body_label = QtWidgets.QLabel("Body joints:")
        body_label2 = _widgest.create_text("* 2 + 1", 15)
        self.body_count_input = QtWidgets.QSpinBox()
        self.body_count_input.setRange(15, 100)
        self.body_count_input.setValue(21)
        self.body_count_input.setMinimumWidth(60)
        body_layout.addWidget(body_label)
        body_layout.addWidget(self.body_count_input)
        body_layout.addWidget(body_label2)
        body_layout.addStretch()
        guide_layout.addLayout(body_layout)

        guide_text1 = _widgest.create_text(">> 根据身体确定位置.", 15)
        guide_layout.addWidget(guide_text1)

        self.btn_CreateGuide = QtWidgets.QPushButton("Create Guide")
        self.btn_CreateGuide.setProperty("main", True)

        guide_layout.addWidget(self.btn_CreateGuide)
        self.rigging_content_layout.addWidget(guide_frame)


    def create_rig_section(self):
        """创建绑定系统区域"""
        rig_frame = QtWidgets.QGroupBox("Rig System")

        rig_layout = QtWidgets.QVBoxLayout(rig_frame)
        rig_layout.setSpacing(10)

        title_label = QtWidgets.QLabel("Build System")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #FFFFFF;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        rig_layout.addWidget(title_label)

        self.btn_RigBody = QtWidgets.QPushButton("Build body System")
        self.btn_RigBody.setProperty("main", True)

        mid_sine_btn = QtWidgets.QPushButton("+ Mid Sine ")
        in_sine_btn = QtWidgets.QPushButton("+ In Sine ")
        bend_start_btn = QtWidgets.QPushButton("+ Start Bend ")
        bend_end_btn = QtWidgets.QPushButton("+ End Bend ")
        ball_btn = QtWidgets.QPushButton("+ Volume Ball ")
        totationl_btn = QtWidgets.QPushButton("+ Spiral")

        mid_sine_btn.clicked.connect(lambda: anim_effects._build("mid_sine"))
        in_sine_btn.clicked.connect(lambda: anim_effects._build("in_sine"))
        bend_start_btn.clicked.connect(lambda: anim_effects._build("body_bend"))
        bend_end_btn.clicked.connect(lambda: anim_effects._build("tail_bend"))
        ball_btn.clicked.connect(lambda: anim_effects._build("ball"))
        totationl_btn.clicked.connect(lambda: anim_effects._build("rotation"))

        rig_layout.addWidget(self.btn_RigBody)
        rig_layout.addWidget(_widgest.create_text("> 下面功能可选择添加", 15))
        rig_layout.addWidget(mid_sine_btn)
        rig_layout.addWidget(in_sine_btn)
        rig_layout.addWidget(bend_start_btn)
        rig_layout.addWidget(bend_end_btn)
        rig_layout.addWidget(ball_btn)
        rig_layout.addWidget(totationl_btn)

        self.rigging_content_layout.addWidget(rig_frame)


    def create_skin_section(self):
        """创建蒙皮区域"""
        skin_frame = QtWidgets.QGroupBox("Bind Skin")

        skin_layout = QtWidgets.QVBoxLayout(skin_frame)
        skin_layout.setSpacing(10)

        skin_layout.addWidget(_widgest.create_text("选择蒙皮关节."))

        skin_btn_layout = QtWidgets.QVBoxLayout()
        add_skin_btn = QtWidgets.QPushButton("+ skin joints")

        add_skin_btn.clicked.connect(bind_skin.add_bind)

        bind_skin_btn = QtWidgets.QPushButton("Bind Skin")

        bind_skin_btn.clicked.connect(bind_skin.smoothBindOptions)

        skin_btn_layout.addWidget(add_skin_btn)
        skin_btn_layout.addWidget(bind_skin_btn)
        skin_layout.addLayout(skin_btn_layout)

        _widgest.separator(skin_layout, True)

        # 自动拆分权重区域
        auto_split_frame = QtWidgets.QGroupBox("Automation Split Weight")

        auto_split_layout = QtWidgets.QVBoxLayout(auto_split_frame)
        auto_split_layout.addWidget(_widgest.create_text("", 10))
        auto_split_layout.addWidget(_widgest.create_text("> 关节需要顺序添加蒙皮", 15))
        auto_split_layout.addWidget(_widgest.create_text("* maya安装numpy计算会提速", 15))

        auto_weight_btn = QtWidgets.QPushButton("Auto Weight")
        auto_weight_btn.setProperty("main", True)
        auto_weight_btn.clicked.connect(bind_skin.auto_weights)

        auto_split_layout.addWidget(auto_weight_btn)

        skin_layout.addWidget(auto_split_frame)
        self.skin_content_layout.addWidget(skin_frame)


    def create_connections(self):
        self.btn_CreateGuide.clicked.connect(self.import_guide)
        self.btn_RigBody.clicked.connect(self.build_system)

    def update_button_states(self):
        """更新按钮状态"""
        if not mc.objExists("BodyLoc_cur") and not mc.objExists("HeadLoc_cur"):
            self.btn_CreateGuide.setText("Create Guide")
        else:
            self.btn_CreateGuide.setText("Rebuild Guide")

        if not mc.objExists("snake_rig_grp") or not mc.objExists("joints_grp"):
            self.btn_RigBody.setText("Build body System")
        else:
            self.btn_RigBody.setText("Rebuild body System")

    def _about(self):
        print("# Developers: Yolanda Ping\n#  yolandaping1224@gmail.com")

    def import_guide(self):
        """创建关节"""
        count = self.body_count_input.value()
        guide.create_body_guide((count*2)+1)
        self.btn_CreateGuide.setText("Rebuild Guide")


    def build_system(self):
        """创建身体绑定系统"""
        body_rigging._rebuild_system()
        self.btn_RigBody.setText("Rebuild body System")

def main():
    """主函数"""
    global py_snake_ui
    try:
        py_snake_ui.close()  # pylint: disable=E0601
        py_snake_ui.deleteLater()
    except:
        pass

    py_snake_ui = SNAKEDialog()
    py_snake_ui.setObjectName("pyQuickBoxIconUI")
    py_snake_ui.show()


if __name__ == '__main__':
    main()