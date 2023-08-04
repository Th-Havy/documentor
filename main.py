"""Main script to run the application."""

import sys
from PySide6.QtWidgets import QApplication

from documentor.main_window import MainWindow


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
