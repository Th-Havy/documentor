from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPixmap

from . import colors


class DrawArea(QGraphicsView):
    """Main view to display and draw items."""

    def __init__(self, scene:QGraphicsScene):
        super().__init__(scene)

        self.scene = scene
        self.view = QGraphicsView(self.scene)

        # To keep track of shape drawing
        self.draw_begin = QPoint()
        self.draw_end = QPoint()

        self.draw_shapes()

    def draw_shapes(self):
        ellipse = self.scene.addEllipse(10, 10, 100, 200, colors.pens[colors.Color.GREEN])
        pixmap = QPixmap("C:/Users/Thomas/Desktop/plan.png")
        image = self.scene.addPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            print("Pressed")
            self.draw_begin = event.pos()
            self.draw_end = self.draw_begin
            self.rectangle = self.scene.addRect(QRect(self.draw_begin, self.draw_end), colors.pens[colors.Color.RED])

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            print("Move")
            self.draw_end = event.pos()
            self.rectangle.setRect(QRect(self.draw_begin, self.draw_end))

    def mouseReleaseEvent(self, event):
        if event.button() & Qt.MouseButton.LeftButton:
            print("Released")
