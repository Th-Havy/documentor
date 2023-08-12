from pathlib import Path
from enum import Enum

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QToolBar,
    QGraphicsView, QGraphicsScene, QToolButton, QMenu, QFileDialog)
from PySide6.QtGui import QBrush, QPen, QPixmap, QAction, QIcon, QClipboard

from . import colors
from .draw_area import DrawArea, CurrentTool


class MainWindow(QMainWindow):
    """Main windows of the application."""


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Documentor")

        # Create menu bar
        self.create_image_menu()
        self.create_edit_menu()

        self.create_toolbar()

        # Create graphic view to show and edit objects.
        self.scene = QGraphicsScene(self)
        self.draw_area = DrawArea(self.scene)
        self.setCentralWidget(self.draw_area)

    def create_image_menu(self):
        image_menu = self.menuBar().addMenu("image")

        self.import_action = image_menu.addAction("import")
        # self.import_action.triggered.connect(lambda : self.draw_area.draw_image(QPixmap("C:/Users/Thomas/Desktop/plan.png")))
        self.import_action.triggered.connect(self.import_image)

        self.paste_action = image_menu.addAction("paste")
        self.paste_action.triggered.connect(self.paste_image)

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
        ellipse_action.triggered.connect(lambda : self.draw_area.set_current_tool(CurrentTool.ELLIPSE))
        self.toolbar.addAction(ellipse_action)

        square_path = current_dir / "images" / "square.png"
        rectangle_action = QAction(QIcon(str(square_path)), "Rectangle", self)
        rectangle_action.setStatusTip("Draw a rectangle")
        rectangle_action.triggered.connect(lambda : self.draw_area.set_current_tool(CurrentTool.RECTANGLE))
        self.toolbar.addAction(rectangle_action)

        text_path = current_dir / "images" / "text.png"
        text_action = QAction(QIcon(str(text_path)), "Text", self)
        text_action.setStatusTip("Draw some text")
        text_action.triggered.connect(lambda : self.draw_area.set_current_tool(CurrentTool.TEXT))
        self.toolbar.addAction(text_action)

        self.toolbar.addSeparator()

        self.create_border_menu()
        self.create_background_menu()


    def create_border_menu(self):

        border_menu = QMenu(self.toolbar)
        self.border_actions = {}

        for color, icon in colors.create_border_icons().items():
            action = QAction(icon, f"Border: {color.name}", self)
            action.triggered.connect(lambda checked=False, c=color: self.draw_area.set_border_color(c))
            border_menu.addAction(action)
            self.border_actions[color] = action

        self.border_button = QToolButton()
        self.border_button.setPopupMode(QToolButton.MenuButtonPopup)
        self.border_button.setMenu(border_menu)

        self.border_button.setDefaultAction(self.border_actions[colors.Color.BLUE])
        # We need to connect the triggered signal to change the default action
        # of the toolbar, otherwise it will stay with the initial default value
        self.border_button.triggered.connect(self.border_button.setDefaultAction)

        self.toolbar.addWidget(self.border_button)

    def create_background_menu(self):

        background_menu = QMenu(self.toolbar)
        self.background_actions = {}

        for color, icon in colors.create_background_icons().items():
            action = QAction(icon, f"Background: {color.name}", self)
            action.triggered.connect(lambda checked=False, c=color: self.draw_area.set_background_color(c))
            background_menu.addAction(action)
            self.background_actions[color] = action

        self.background_button = QToolButton()
        self.background_button.setPopupMode(QToolButton.MenuButtonPopup)
        self.background_button.setMenu(background_menu)

        self.background_button.setDefaultAction(self.background_actions[colors.Color.BLUE])
        # We need to connect the triggered signal to change the default action
        # of the toolbar, otherwise it will stay with the initial default value
        self.background_button.triggered.connect(self.background_button.setDefaultAction)

        self.toolbar.addWidget(self.background_button)

    def import_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        self.draw_area.draw_image(QPixmap(file_name))

    def paste_image(self):
        clipboard = QApplication.clipboard()
        mimeData = clipboard.mimeData()

        if (mimeData.hasImage()):
            self.draw_area.draw_image(QPixmap(mimeData.imageData()))
