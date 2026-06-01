# -*- coding: utf-8 -*-

# .FileName:build_menu_bar.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/26 16:52
# .Finish time:
import xml.etree.ElementTree as ET
import webbrowser
import sys
import ud

class PYdlg:


    def build_menu_bar(self, xml_path="menu_config.xml"):
        """从 XML 文件动态构建菜单栏"""
        self.menu_bar = QtWidgets.QMenuBar()
        command_map = self._get_command_map()

        def add_action_from_element(menu, elem):
            label = elem.get("label")
            if not label:
                return

            command = elem.get("command")
            bold = elem.get("bold", "false").lower() == "true"
            checkable = elem.get("checkable", "false").lower() == "true"
            enabled = elem.get("enabled", "true").lower() == "true"
            item_id = elem.get("item_id")
      
            checked = False
            if checkable and item_id:
                checked_from = elem.get("checked_from")
                if checked_from:
         
                    try:
                        parts = checked_from.split('.')
                        obj = sys.modules.get(parts[0]) if '.' in checked_from else None
                        if obj is None:
                            # 尝试从当前实例或全局命名空间获取
                            obj = self if parts[0] == 'self' else globals().get(parts[0])
                        for part in parts[1:]:
                            obj = getattr(obj, part)
                        checked = bool(obj)
                    except Exception:
                        checked = False
                else:
                    # 若未指定 checked_from，则假设 item_id 为 ud 模块的属性名
                    checked = getattr(ud, item_id, False)

            # 创建 QAction
            action = QAction(label, self)
            if bold:
                font = action.font()
                font.setBold(True)
                action.setFont(font)
            action.setEnabled(enabled)

            # 设置复选框属性
            if checkable:
                action.setCheckable(True)
                action.setChecked(checked)

                action.triggered.connect(
                    lambda name=(item_id or label), act=action:
                    return_checkBox(name, act.isChecked())
                )

            # 设置普通命令回调
            if command and command in command_map:
                action.triggered.connect(command_map[command])

            menu.addAction(action)
            return action

        # 解析 XML 文件
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
        except Exception as e:
            print(f"加载菜单配置失败: {e}")
            return

        # 遍历所有 <menu> 节点
        for menu_elem in root.findall("menu"):
            menu_name = menu_elem.get("name", "Unnamed")
            qmenu = self.menu_bar.addMenu(menu_name)

            # 遍历菜单内的子元素
            for child in menu_elem:
                if child.tag == "separator":
                    qmenu.addSeparator()
                elif child.tag == "action":
                    add_action_from_element(qmenu, child)

        self.main_layout.setMenuBar(self.menu_bar)

    def _get_command_map(self):
        """返回命令字符串到实际回调函数的映射字典"""
        return {
            "open_bilibili": lambda: webbrowser.open("https://space.bilibili.com/3493142019967757"),
            "open_updata": lambda: webbrowser.open(self._info[-2]),
            "open_kuake": lambda: webbrowser.open(self._info[-1]),
            "open_charcoal": lambda: webbrowser.open("https://space.bilibili.com/3493142019967757"),
            "open_skinner": lambda: webbrowser.open(self._info[-2]),
            "open_br_smooth": lambda: webbrowser.open(self._info[-1]),

            "clean_namespace": lambda: self.dispatcher.execute("Clean NameSpace"),
            "optimize_scene": lambda: self.dispatcher.execute("Optimize Scene"),
            "check_scene_name": lambda: self.dispatcher.execute("Check Scene Name"),
            "delete_unused_nodes": lambda: self.dispatcher.execute("Delete Unused Nodes"),
            "delete_unknown_node": lambda: self.dispatcher.execute("Delete unknown Node"),
            "delete_unused_orig": lambda: self.dispatcher.execute("Delete unUsedOrig"),
            "delete_undisplay_point": lambda: self.dispatcher.execute("Delete unDisplayPoint"),
            "delete_unused_plug": lambda: self.dispatcher.execute("Delete unUsedPlug"),
            "delete_unused_dagpose": lambda: self.dispatcher.execute("Delete unUsedDagPose"),
            "unlock_node_selected": lambda: self.dispatcher.execute("UnLockNode selected"),
            "unlock_node_scene": lambda: self.dispatcher.execute("UnLockNode Scene"),
            "unlock_initial_shading": lambda: self.dispatcher.execute("UnLock initialShading"),
            "set_historically_interesting": lambda: self.dispatcher.execute("setIsHistoricallyInteresting"),

            "toggle_dock_mode": self.to_dock_mode,
            "reload_theme": self.reload_theme,
        }


  