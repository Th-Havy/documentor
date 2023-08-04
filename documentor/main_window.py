from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QMenuBar, QToolBar

class MainWindow(QMainWindow):
    """Main windows of the application."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Documentor")

        # Create menu bar
        menu_bar = self.menuBar()
        image_menu = menu_bar.addMenu("image")
        edit_menu = menu_bar.addMenu("edit")
        edit_menu.addAction("undo")
        edit_menu.addAction("redo")

        # Create toolbar
        toolbar = QToolBar("toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
