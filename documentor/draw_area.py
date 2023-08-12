from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPixmap

from . import colors


class DrawArea(QGraphicsView):
    """Main view to display and draw items."""

    def __init__(self, scene:QGraphicsScene):
        super().__init__(scene)

        self.scene = scene
        self.view = QGraphicsView(self.scene)

        ellipse = self.scene.addEllipse(10, 10, 100, 200, colors.pens[colors.Color.GREEN])
        ellipse = self.scene.addEllipse(10, 10, 200, 200, colors.pens[colors.Color.RED])
        pixmap = QPixmap("C:/Users/Thomas/Desktop/plan.png")
        image = self.scene.addPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            print("Pressed")

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            print("Move")

    def mouseReleaseEvent(self, event):
        if event.button() & Qt.MouseButton.LeftButton:
            print("Released")
