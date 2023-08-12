from enum import Enum

from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPixmap, QFont

from . import colors


class CurrentTool(Enum):
    RECTANGLE = 0
    ELLIPSE = 1
    TEXT = 2


class DrawArea(QGraphicsView):
    """Main view to display and draw items."""

    def __init__(self, scene:QGraphicsScene):
        super().__init__(scene)

        self.scene = scene
        self.view = QGraphicsView(self.scene)

        # To keep track of shape drawing
        self.current_tool = CurrentTool.RECTANGLE
        self.draw_begin = QPoint()
        self.draw_end = QPoint()
        self.shape = None

        # Default pens and brushes
        self.border_color = colors.Color.GREEN
        self.background_color = colors.Color.GREEN
        self.pen = colors.PENS[self.border_color]
        self.brush = colors.BRUSHES[self.background_color]
        self.font = QFont("Times", 10, QFont.Bold)

        self.draw_shapes()

    def draw_shapes(self):
        ellipse = self.scene.addEllipse(10, 10, 100, 200, self.pen, self.brush)
        pixmap = QPixmap("C:/Users/Thomas/Desktop/plan.png")
        image = self.scene.addPixmap(pixmap)
        text = self.scene.addSimpleText("text", self.font)
        text.setPos(0, 50)

    def mousePressEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.begin_draw_shape(event.pos())

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.update_draw_shape(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() & Qt.MouseButton.LeftButton:
            self.end_draw_shape()

    def set_current_tool(self, tool:CurrentTool):
        self.current_tool = tool

    def set_border_color(self, border_color):
        self.border_color = border_color
        self.pen = colors.PENS[self.border_color]

    def set_background_color(self, background_color):
        self.background_color = background_color
        self.brush = colors.BRUSHES[self.background_color]

    def begin_draw_shape(self, pos):
        self.draw_begin = pos
        self.draw_end = self.draw_begin

        if self.current_tool == CurrentTool.RECTANGLE:
            self.shape = self.scene.addRect(QRect(self.draw_begin, self.draw_end), self.pen, self.brush)
        if self.current_tool == CurrentTool.ELLIPSE:
            self.shape = self.scene.addEllipse(QRect(self.draw_begin, self.draw_end), self.pen, self.brush)
        if self.current_tool == CurrentTool.TEXT:
            self.shape = self.scene.addSimpleText("Text", self.font)
            self.shape.setBrush(self.brush)
            self.shape.setPos(self.draw_begin)

    def update_draw_shape(self, pos):
        if self.current_tool != CurrentTool.TEXT:
            self.draw_end = pos
            self.shape.setRect(QRect(self.draw_begin, self.draw_end))
        else:
            self.shape.setPos(pos)

    def end_draw_shape(self):
        self.draw_begin = QPoint()
        self.draw_end = QPoint()
        self.shape = None
