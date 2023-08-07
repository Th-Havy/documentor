from pathlib import Path
from enum import Enum

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (QMainWindow, QMenuBar, QToolBar, QGraphicsView,
    QGraphicsScene, QToolButton, QMenu)
from PySide6.QtGui import QBrush, QPen, QPixmap, QAction, QIcon


class MainWindow(QMainWindow):
    """Main windows of the application."""

    class Colors(Enum):
        BLACK = Qt.GlobalColor.black
        WHITE = Qt.GlobalColor.white
        RED = Qt.GlobalColor.red
        GREEN = Qt.GlobalColor.green
        BLUE = Qt.GlobalColor.blue
        YELLOW = Qt.GlobalColor.yellow

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Documentor")

        # Create menu bar
        self.create_image_menu()
        self.create_edit_menu()

        self.create_color_icons()
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
        self.toolbar = QToolBar("toolbar")
        self.toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(self.toolbar)

        current_dir = Path(__file__).resolve().parent

        circle_path = current_dir / "images" / "circle.png"
        ellipse_action = QAction(QIcon(str(circle_path)), "Ellipse", self)
        ellipse_action.setStatusTip("Draw an ellipse")
        ellipse_action.triggered.connect(lambda : print("ellipse"))
        self.toolbar.addAction(ellipse_action)

        square_path = current_dir / "images" / "square.png"
        rectangle_action = QAction(QIcon(str(square_path)), "Rectangle", self)
        rectangle_action.setStatusTip("Draw a rectangle")
        rectangle_action.triggered.connect(lambda : print("rectangle"))
        self.toolbar.addAction(rectangle_action)

        text_path = current_dir / "images" / "text.png"
        text_action = QAction(QIcon(str(text_path)), "Text", self)
        text_action.setStatusTip("Draw some text")
        text_action.triggered.connect(lambda : print("text"))
        self.toolbar.addAction(text_action)

        self.toolbar.addSeparator()

        self.create_border_menu()

        background_path = current_dir / "images" / "background" / "transparent.png"
        background_action = QAction(QIcon(str(background_path)), "Background", self)
        background_action.setStatusTip("Change background color")
        background_action.triggered.connect(lambda : print("background"))
        self.toolbar.addAction(background_action)


    def create_border_menu(self):

        border_menu = QMenu(self.toolbar)
        self.border_actions = {}

        for color, icon in self.border_icons.items():
            action = QAction(icon, f"Border: {color.name}", self)
            action.triggered.connect(lambda checked=False, c=color: self.set_border_color(c))
            border_menu.addAction(action)
            self.border_actions[color] = action

        self.border_button = QToolButton()
        self.border_button.setPopupMode(QToolButton.MenuButtonPopup)
        self.border_button.setMenu(border_menu)

        self.border_button.setDefaultAction(self.border_actions[self.Colors.BLUE])
        # We need to connect the triggered signal to change the default action
        # of the toolbar, otherwise it will stay with the initial default value
        self.border_button.triggered.connect(self.border_button.setDefaultAction)

        self.toolbar.addWidget(self.border_button)

    def set_border_color(self, color):
        print(color)
        self.border_color = color

    def create_pens_and_brushes(self):
        """Create brushes and pens to draw on images."""

        self.brushes = [QBrush(c.value) for c in self.Colors]
        self.pens = [QPen(c.value) for c in self.Colors]

    def create_color_icons(self):
        """Create icons for background and border colors."""

        color_files = [
            "black.png",
            "white.png",
            "red.png",
            "green.png",
            "blue.png",
            "yellow.png",
        ]

        current_dir = Path(__file__).resolve().parent

        self.border_icons = {}
        self.background_icons = {}

        for c, file in zip(self.Colors, color_files):
            self.border_icons[c] = QIcon(str(current_dir / "images" / "border" / file))
            self.background_icons[c] = QIcon(str(current_dir / "images" / "background" / file))

    def create_graphic_view(self):
        """Create graphic view to show and edit objects."""

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        ellipse = self.scene.addEllipse(10, 10, 100, 200, self.pens[2])
        pixmap = QPixmap("C:/Users/Thomas/Desktop/plan.png")
        image = self.scene.addPixmap(pixmap)
