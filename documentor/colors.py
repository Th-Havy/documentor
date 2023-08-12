"""Module defining the colors, pens and brushes for the drawing area."""


from enum import Enum
from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QBrush, QPen, QIcon


class Color(Enum):
    BLACK = Qt.GlobalColor.black
    WHITE = Qt.GlobalColor.white
    RED = Qt.GlobalColor.red
    GREEN = Qt.GlobalColor.green
    BLUE = Qt.GlobalColor.blue
    YELLOW = Qt.GlobalColor.yellow

# Create brushes
BRUSHES = {c: QBrush(c.value) for c in Color}
PENS = {c: QPen(c.value) for c in Color}

# Create icons for background and border colors.
_color_files = [
    "black.png",
    "white.png",
    "red.png",
    "green.png",
    "blue.png",
    "yellow.png",
]

def create_border_icons():
    """Create the border icons.

    Needs to be called after creating a QGuiApplication, otherwise an error is
    raised: `QPixmap: Must construct a QGuiApplication before a QPixmap`.
    """

    current_dir = Path(__file__).resolve().parent
    border_icons = {}

    for c, file in zip(Color, _color_files):
        border_icons[c] = QIcon(str(current_dir / "images" / "border" / file))

    return border_icons

def create_background_icons():
    """Create the background icons.

    Needs to be called after creating a QGuiApplication, otherwise an error is
    raised: `QPixmap: Must construct a QGuiApplication before a QPixmap`.
    """

    current_dir = Path(__file__).resolve().parent
    background_icons = {}

    for c, file in zip(Color, _color_files):
        background_icons[c] = QIcon(str(current_dir / "images" / "background" / file))

    return background_icons
