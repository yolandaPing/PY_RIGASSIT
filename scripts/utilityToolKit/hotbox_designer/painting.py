# -*- coding: utf-8 -*-
'''新增四种shapes'''
import math
try:
    from ui_framework.core.qtCompat import *

except ImportError:
    from CommonUse.qtCompat import *

from hotbox_designer.qtutils import VALIGNS, HALIGNS
from hotbox_designer.geometry import grow_rect


MANIPULATOR_BORDER = 5
SELECTION_COLOR = '#3388FF'


def _draw_line(painter, rect, bordersize, bordercolor):

    start = QtCore.QPointF(rect.left(), rect.center().y())
    end = QtCore.QPointF(rect.right(), rect.center().y())

    pen = painter.pen()
    pen.setWidthF(bordersize)
    pen.setColor(bordercolor)
    painter.setPen(pen)

    painter.drawLine(start, end)
    return


def _draw_triangle(painter, rect):
    center_x = rect.center().x()
    top = rect.top()
    bottom = rect.bottom()
    left = rect.left()
    right = rect.right()
    # 顶点坐标 (center_x, top)
    # 左下角 (left, bottom)
    # 右下角 (right, bottom)
    triangle = QtGui.QPolygonF([
        QtCore.QPointF(center_x, top),
        QtCore.QPointF(left, bottom),
        QtCore.QPointF(right, bottom)
    ])
    painter.drawPolygon(triangle)


def _draw_diamond(painter, rect):
    center = rect.center()
    top = QtCore.QPointF(center.x(), rect.top())
    right = QtCore.QPointF(rect.right(), center.y())
    bottom = QtCore.QPointF(center.x(), rect.bottom())
    left = QtCore.QPointF(rect.left(), center.y())
    diamond = QtGui.QPolygonF([top, right, bottom, left])
    painter.drawPolygon(diamond)


def _draw_hexagon(painter, rect):
    center = rect.center()
    width = rect.width()
    height = rect.height()
    radius = min(width, height) / 2.0
    points = []
    for i in range(6):
        # 角度：0度开始（朝右），每60度一个顶点
        angle = (i * 60.0) * math.pi / 180.0
        x = center.x() + radius * math.cos(angle)
        y = center.y() + radius * math.sin(angle)
        points.append(QtCore.QPointF(x, y))
    hexagon_polygon = QtGui.QPolygonF(points)
    painter.drawPolygon(hexagon_polygon)


def _draw_star(painter, rect):
    center = rect.center()
    outer = min(rect.width(), rect.height()) / 2.0
    inner = outer * 0.382
    points = []
    for i in range(10):
        angle = math.radians(i * 36.0 - 90.0)
        r = outer if i % 2 == 0 else inner
        x = center.x() + r * math.cos(angle)
        y = center.y() + r * math.sin(angle)
        points.append(QtCore.QPointF(x, y))
    painter.drawPolygon(QtGui.QPolygonF(points))


def draw_editor(painter, rect, snap=None):
    # draw border
    pen = QtGui.QPen(QtGui.QColor('#333333'))
    pen.setStyle(QtPenStyle('DashDotLine'))
    pen.setWidth(3)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 25))
    painter.setPen(pen)
    painter.setBrush(brush)
    painter.drawRect(rect)

    if snap is None:
        return

    # draw snap grid
    pen = QtGui.QPen(QtGui.QColor('red'))
    painter.setPen(pen)

    x = 0
    y = 0
    while y < rect.bottom():
        painter.drawPoint(x, y)
        x += snap[0]
        if x > rect.right():
            x = 0
            y += snap[1]


def draw_editor_center(painter, rect, point):
    color = QtGui.QColor(200, 200, 200, 125)
    painter.setPen(QtGui.QPen(color))
    painter.setBrush(QtGui.QBrush(color))
    painter.drawRect(rect)

    path = get_center_path(QtCore.QPoint(*point))
    pen = QtGui.QPen(QtGui.QColor(50, 125, 255))
    pen.setWidth(2)
    painter.setPen(pen)
    painter.drawPath(path)


def get_center_path(point):
    ext = 12
    int_ = 5
    path = QtGui.QPainterPath(point)

    path.moveTo(QtCore.QPoint(point.x() - ext, point.y()))
    path.lineTo(QtCore.QPoint(point.x() - int_, point.y()))

    path.moveTo(QtCore.QPoint(point.x() + int_, point.y()))
    path.lineTo(QtCore.QPoint(point.x() + ext, point.y()))

    path.moveTo(QtCore.QPoint(point.x(), point.y() - ext))
    path.lineTo(QtCore.QPoint(point.x(), point.y() - int_))

    path.moveTo(QtCore.QPoint(point.x(), point.y() + int_))
    path.lineTo(QtCore.QPoint(point.x(), point.y() + ext))

    path.addEllipse(point, 1, 1)
    return path


def draw_shape(painter, shape):
    options = shape.options
    content_rect = shape.content_rect()

    if shape.clicked:
        bordercolor = QtGui.QColor(options['bordercolor.clicked'])
        backgroundcolor = QtGui.QColor(options['bgcolor.clicked'])
        bordersize = options['borderwidth.clicked']
    elif shape.hovered:
        bordercolor = QtGui.QColor(options['bordercolor.hovered'])
        backgroundcolor = QtGui.QColor(options['bgcolor.hovered'])
        bordersize = options['borderwidth.hovered']
    else:
        bordercolor = QtGui.QColor(options['bordercolor.normal'])
        backgroundcolor = QtGui.QColor(options['bgcolor.normal'])
        bordersize = options['borderwidth.normal']

    textcolor = QtGui.QColor(options['text.color'])

    alpha = options['bordercolor.transparency'] if options['border'] else 255
    bordercolor.setAlpha(255 - alpha)
    backgroundcolor.setAlpha(255 - options['bgcolor.transparency'])

    pen = QtGui.QPen(bordercolor)
    pen.setStyle(QtPenStyle('SolidLine'))
    pen.setWidthF(bordersize)

    painter.setPen(pen)
    painter.setBrush(QtGui.QBrush(backgroundcolor))

    if options['shape'] == 'square':
        painter.drawRect(shape.rect)
    elif options['shape'] == 'round':
        painter.drawEllipse(shape.rect)
    elif options['shape'] == 'triangle':
        _draw_triangle(painter, shape.rect)
    elif options['shape'] == 'diamond':
        _draw_diamond(painter, shape.rect)
    elif options['shape'] == 'hexagon':
        _draw_hexagon(painter, shape.rect)
    elif options['shape'] == 'star':
        _draw_star(painter, shape.rect)
    elif options['shape'] == 'line':
        _draw_line(painter, shape.rect, bordersize, bordercolor)
    else:
        painter.drawEllipse(shape.rect)

    if shape.pixmap is not None:
        rect = shape.image_rect or content_rect
        painter.drawPixmap(rect, shape.pixmap)

    painter.setPen(QtGui.QPen(textcolor))
    painter.setBrush(QtGui.QBrush(textcolor))

    flags = VALIGNS[options['text.valign']] | HALIGNS[options['text.halign']]

    font = QtGui.QFont()
    font.setBold(options['text.bold'])
    font.setItalic(options['text.italic'])
    font.setPixelSize(options['text.size'])

    painter.setFont(font)

    text = options['text.content']

    # Qt6 有时需要 int(flags)
    painter.drawText(QtCore.QRectF(content_rect), int(flags), text)


def draw_selection_square(painter, rect):
    bordercolor = QtGui.QColor(SELECTION_COLOR)
    backgroundcolor = QtGui.QColor(SELECTION_COLOR)
    backgroundcolor.setAlpha(85)

    painter.setPen(QtGui.QPen(bordercolor))
    painter.setBrush(QtGui.QBrush(backgroundcolor))
    painter.drawRect(rect)


def draw_manipulator(painter, manipulator, cursor):
    hovered = manipulator.hovered_rects(cursor)

    if manipulator.rect in hovered:
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
        brush = QtGui.QBrush(QtGui.QColor(125, 125, 125))
        brush.setStyle(QtBrushStyle('FDiagPattern'))

        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawPath(manipulator.hovered_path)

    pen = QtGui.QPen(QtGui.QColor('black'))
    brush = QtGui.QBrush(QtGui.QColor('white'))
    painter.setBrush(brush)

    for rect in manipulator.handler_rects():
        pen.setWidth(3 if rect in hovered else 1)
        painter.setPen(pen)
        painter.drawEllipse(rect)

    pen.setWidth(1)
    pen.setStyle(QtPenStyle('DashLine'))

    painter.setPen(pen)
    painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 0)))
    painter.drawRect(manipulator.rect)


def draw_aiming_background(painter, rect):
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 1))

    painter.setPen(pen)
    painter.setBrush(brush)
    painter.drawRect(rect)


def draw_aiming(painter, center, target):
    pen = QtGui.QPen(QtGui.QColor(35, 35, 35))
    pen.setWidth(3)

    painter.setPen(pen)
    painter.setBrush(QtGui.QColor(0, 0, 0, 0))
    painter.drawLine(center, target)


def get_hovered_path(rect):
    path = QtGui.QPainterPath()
    path.addRect(rect)
    path.addRect(grow_rect(rect, MANIPULATOR_BORDER))
    return path