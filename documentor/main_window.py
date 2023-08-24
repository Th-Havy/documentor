from pathlib import Path
from enum import Enum

from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QToolBar,
    QGraphicsView, QGraphicsScene, QToolButton, QMenu, QFileDialog, QSpinBox)
from PySide6.QtGui import (QPixmap, QAction, QIcon, QClipboard, QKeySequence,
    QActionGroup, QUndoStack)

from . import colors
from .draw_area import DrawArea, CurrentTool


class MainWindow(QMainWindow):
    """Main windows of the application."""


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Documentor")
        self.set_window_icon()
        self.resize(640, 480)

        # Create menu bar
        self.create_image_menu()
        self.create_edit_menu()

        self.create_toolbar()

        # Create graphic view to show and edit objects.
        self.scene = QGraphicsScene(self)
        self.draw_area = DrawArea(self.scene, self.undo_stack)
        self.setCentralWidget(self.draw_area)

    def set_window_icon(self):
        current_dir = Path(__file__).resolve().parent
        app_icon = QIcon(str(current_dir / "images" / "icon.png"))
        self.setWindowIcon(app_icon)

    def create_image_menu(self):
        image_menu = self.menuBar().addMenu("Image")

        self.import_action = image_menu.addAction("Import")
        self.import_action.triggered.connect(self.import_image)

        self.paste_action = image_menu.addAction("Paste")
        self.paste_action.triggered.connect(self.paste_image)
        self.paste_action.setShortcut(QKeySequence("Ctrl+V"))

        self.save_action = image_menu.addAction("Save")
        self.save_action.triggered.connect(self.save_image)
        self.save_action.setShortcut(QKeySequence("Ctrl+S"))

        self.save_as_action = image_menu.addAction("Save as")
        self.save_as_action.triggered.connect(lambda : print("saved as"))
        self.save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))

    def create_edit_menu(self):

        # Create undo-redo
        self.undo_stack = QUndoStack(self)

        edit_menu = self.menuBar().addMenu("edit")

        self.undo_action = self.undo_stack.createUndoAction(self, "Undo")
        edit_menu.addAction(self.undo_action)
        self.undo_action.setShortcut(QKeySequence("Ctrl+Z"))

        self.redo_action = self.undo_stack.createRedoAction(self, "Redo")
        edit_menu.addAction(self.redo_action)
        self.redo_action.setShortcut(QKeySequence("Ctrl+Y"))

    def create_toolbar(self):
        self.toolbar = QToolBar("toolbar")
        self.toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(self.toolbar)
        tool_group = QActionGroup(self)

        current_dir = Path(__file__).resolve().parent

        cursor_path = current_dir / "images" / "cursor.png"
        cursor_action = QAction(QIcon(str(cursor_path)), "Cursor", self, checkable=True)
        cursor_action.setStatusTip("Select elements")
        cursor_action.triggered.connect(lambda : self.draw_area.set_current_tool(CurrentTool.CURSOR))
        self.toolbar.addAction(cursor_action)
        tool_group.addAction(cursor_action)

        circle_path = current_dir / "images" / "circle.png"
        ellipse_action = QAction(QIcon(str(circle_path)), "Ellipse", self, checkable=True)
        ellipse_action.setStatusTip("Draw an ellipse")
        ellipse_action.triggered.connect(lambda : self.draw_area.set_current_tool(CurrentTool.ELLIPSE))
        self.toolbar.addAction(ellipse_action)
        tool_group.addAction(ellipse_action)

        square_path = current_dir / "images" / "square.png"
        rectangle_action = QAction(QIcon(str(square_path)), "Rectangle", self, checkable=True)
        rectangle_action.setStatusTip("Draw a rectangle")
        rectangle_action.triggered.connect(lambda : self.draw_area.set_current_tool(CurrentTool.RECTANGLE))
        self.toolbar.addAction(rectangle_action)
        tool_group.addAction(rectangle_action)

        text_path = current_dir / "images" / "text.png"
        text_action = QAction(QIcon(str(text_path)), "Text", self, checkable=True)
        text_action.setStatusTip("Draw some text")
        text_action.triggered.connect(lambda : self.draw_area.set_current_tool(CurrentTool.TEXT))
        self.toolbar.addAction(text_action)
        tool_group.addAction(text_action)

        self.toolbar.addSeparator()

        self.create_border_menu()
        self.create_background_menu()

        border_size_spin_box = QSpinBox(self)
        border_size_spin_box.setRange(1, 20)
        border_size_spin_box.valueChanged.connect(lambda v: self.draw_area.set_border_size(v))
        self.toolbar.addWidget(border_size_spin_box)

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

        self.border_button.setDefaultAction(self.border_actions[colors.Color.RED])
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

        self.background_button.setDefaultAction(self.background_actions[colors.Color.TRANSPARENT])
        # We need to connect the triggered signal to change the default action
        # of the toolbar, otherwise it will stay with the initial default value
        self.background_button.triggered.connect(self.background_button.setDefaultAction)

        self.toolbar.addWidget(self.background_button)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.draw_area.setSceneRect(0, 0, event.size().width(), event.size().height())


    def import_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        self.draw_area.draw_image(QPixmap(file_name))

    def paste_image(self):
        clipboard = QApplication.clipboard()
        mimeData = clipboard.mimeData()

        if (mimeData.hasImage()):
            self.draw_area.draw_image(QPixmap(mimeData.imageData()))

    def save_image(self) -> QPixmap:
        filepath, _ = QFileDialog.getSaveFileName(self, "Save image", "", "Image Files (*.png *.jpg *.bmp)")

        if filepath:
            pixmap = self.draw_area.grab(QRect(
                self.scene.sceneRect().x(),
                self.scene.sceneRect().y(),
                self.scene.sceneRect().width(),
                self.scene.sceneRect().height(),
            ))
            pixmap.save(filepath)
