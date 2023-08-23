from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsTextItem


class EditableTextItem(QGraphicsTextItem):
    """Text that can be edited by double clicking."""

    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text
        self.setPlainText(text)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)

    def focusOutEvent(self, event):
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        super().focusOutEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.textInteractionFlags() == Qt.NoTextInteraction:
            self.setTextInteractionFlags(Qt.TextEditorInteraction)
        super().mouseDoubleClickEvent(event)
