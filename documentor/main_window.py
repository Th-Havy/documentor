from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (QMainWindow, QMenuBar, QToolBar, QGraphicsView,
    QGraphicsScene)
from PySide6.QtGui import QBrush, QPen, QPixmap, QAction, QIcon


class MainWindow(QMainWindow):
    """Main windows of the application."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Documentor")

        # Create menu bar
        self.create_image_menu()
        self.create_edit_menu()

        self.create_toolbar()

        self.create_pens_and_brushes()
        self.create_graphic_view()

    def create_image_menu(self):
        image_menu = self.menuBar().addMenu("image")

        self.import_action = image_menu.addAction("import")
        self.import_action.triggered.connect(lambda : print("imported"))

        self.paste_action = image_menu.addAction("paste")
        self.paste_action.triggered.connect(lambda : print("pasted"))

        self.save_action = image_menu.addAction("save")
        self.save_action.triggered.connect(lambda : print("saved"))

    def create_edit_menu(self):
        edit_menu = self.menuBar().addMenu("edit")

        self.undo_action = edit_menu.addAction("undo")
        self.undo_action.triggered.connect(lambda : print("undone"))
        self.redo_action = edit_menu.addAction("redo")
        self.redo_action.triggered.connect(lambda : print("redone"))

    def create_toolbar(self):
        toolbar = QToolBar("toolbar")
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(toolbar)

        current_dir = Path(__file__).resolve().parent

        circle_path = current_dir / "images" / "circle.png"
        ellipse_action = QAction(QIcon(str(circle_path)), "Ellipse", self)
        ellipse_action.setStatusTip("Draw an ellipse")
        ellipse_action.triggered.connect(lambda : print("ellipse"))
        toolbar.addAction(ellipse_action)

        square_path = current_dir / "images" / "square.png"
        rectangle_action = QAction(QIcon(str(square_path)), "Rectangle", self)
        rectangle_action.setStatusTip("Draw a rectangle")
        rectangle_action.triggered.connect(lambda : print("rectangle"))
        toolbar.addAction(rectangle_action)

        text_path = current_dir / "images" / "text.png"
        text_action = QAction(QIcon(str(text_path)), "Text", self)
        text_action.setStatusTip("Draw some text")
        text_action.triggered.connect(lambda : print("text"))
        toolbar.addAction(text_action)

        toolbar.addSeparator()

        border_path = current_dir / "images" / "border" / "red.png"
        border_action = QAction(QIcon(str(border_path)), "Border", self)
        border_action.setStatusTip("Change border color")
        border_action.triggered.connect(lambda : print("border"))
        toolbar.addAction(border_action)

        background_path = current_dir / "images" / "background" / "transparent.png"
        background_action = QAction(QIcon(str(background_path)), "Background", self)
        background_action.setStatusTip("Change background color")
        background_action.triggered.connect(lambda : print("background"))
        toolbar.addAction(background_action)

    def create_pens_and_brushes(self):
        """Create brushes and pens to draw on images."""

        colors = [
            Qt.GlobalColor.black,
            Qt.GlobalColor.white,
            Qt.GlobalColor.red,
            Qt.GlobalColor.green,
            Qt.GlobalColor.blue,
            Qt.GlobalColor.yellow,
        ]

        self.brushes = [QBrush(c) for c in colors]
        self.pens = [QPen(c) for c in colors]

    def create_graphic_view(self):
        """Create graphic view to show and edit objects."""

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        ellipse = self.scene.addEllipse(10, 10, 100, 200, self.pens[2])
        pixmap = QPixmap("C:/Users/Thomas/Desktop/plan.png")
        image = self.scene.addPixmap(pixmap)
