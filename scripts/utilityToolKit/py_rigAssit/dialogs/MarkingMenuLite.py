# -*- coding: utf-8 -*-
# FileName: MarkingMenuLite.py
import math
from py_rigAssit import QtWidgets, QtCore, QtGui


class PYMarkingMenuLite(QtWidgets.QWidget):
    RADIUS = 200
    VERTICAL_SCALE = 0.6  # 垂直压缩比例

    def __init__(self, items, parent=None):
        super(PYMarkingMenuLite, self).__init__(parent)

        self.items = items
        self.buttons = []
        self.hovered_button = None

        # Maya风格方向线
        self.center_pos = QtCore.QPoint()
        self.mouse_pos = QtCore.QPoint()

        self.setWindowFlags(
            QtCore.Qt.Popup |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.NoDropShadowWindowHint  # 关键：去除系统阴影
        )
        # 透明背景关键属性
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)  # 避免系统背景绘制
        self.setAutoFillBackground(False)
        # 全局样式表强制透明无边框
        self.setStyleSheet("QWidget { background: transparent; border: none; }")

        self.setMouseTracking(True)
        self._build_ui()

    def _build_ui(self):
        for label, cb in self.items:
            btn = QtWidgets.QPushButton(label, self)
            # btn.setFixedSize(80, 25)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                           QPushButton {
                               background: rgb(70, 70, 70);    
                               border: 1px solid black;        
                               border-radius: 0px;
                               color: white;

                           }
                           QPushButton:checked {
                               background: rgb(0, 204, 204);  
                               border: 1px solid black;
                           }
                           QPushButton:hover {
                               background: rgb(0, 204, 204);  
                               color: black;
                           }
                       """)

            self.buttons.append(btn)

    def _layout_buttons(self):
        center = QtCore.QPoint(self.RADIUS, self.RADIUS)
        angles = [90, 45, 0, 315, 270, 225, 180, 135]
        h_distance = self.RADIUS * 0.7
        v_distance = h_distance * self.VERTICAL_SCALE

        for i, btn in enumerate(self.buttons):
            angle = math.radians(angles[i % len(angles)])
            x = center.x() + math.cos(angle) * h_distance
            y = center.y() - math.sin(angle) * v_distance
            btn.move(
                int(x - btn.width() / 2),
                int(y - btn.height() / 4)   # 垂直偏移保持原逻辑
            )

    def start(self, global_pos):

        self.center_pos = QtCore.QPoint(self.RADIUS, self.RADIUS)
        self.mouse_pos = self.center_pos

        self.setGeometry(
            global_pos.x() - self.RADIUS,
            global_pos.y() - self.RADIUS,
            self.RADIUS * 2,
            self.RADIUS * 2
        )
        self._layout_buttons()
        self.show()

        self._update_hover(QtGui.QCursor.pos())
        self.update()

    def _update_hover(self, global_pos):
        """根据鼠标全局坐标，高亮命中的按钮，清除其他按钮的高亮"""
        pos = self.mapFromGlobal(global_pos)
        hit_button = None
        for btn in self.buttons:
            if btn.geometry().contains(pos):
                hit_button = btn
                break

        if hit_button != self.hovered_button:
            # 清除旧高亮
            if self.hovered_button:
                self.hovered_button.setChecked(False)
            # 设置新高亮
            if hit_button:
                hit_button.setChecked(True)
            self.hovered_button = hit_button

    def mouseMoveEvent(self, event):
        # 实时更新高亮 + Maya方向线
        self.mouse_pos = event.pos()

        self._update_hover(event.globalPos())
        self.update()

        super(PYMarkingMenuLite, self).mouseMoveEvent(event)


    def paintEvent(self, event):

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # 方向线
        pen = QtGui.QPen(
            QtGui.QColor(0, 220, 220, 220),
            2
        )
        painter.setPen(pen)

        painter.drawLine(
            self.center_pos,
            self.mouse_pos
        )

        # 中心点
        painter.setBrush(QtGui.QColor(0, 220, 220))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawEllipse(self.center_pos, 4, 4)

        painter.end()

    def mouseReleaseEvent(self, event):
        # 执行当前高亮按钮的命令
        if self.hovered_button:
            # 找到对应的回调函数
            idx = self.buttons.index(self.hovered_button)
            _, cb = self.items[idx]
            if cb:
                cb()
        self.close()   # 无论是否有高亮，释放后关闭菜单

    def mousePressEvent(self, event):
        # 点击菜单外部区域时关闭菜单（不执行命令）
        if not self.rect().contains(event.pos()):
            self.close()



