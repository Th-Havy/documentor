from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsTextItem
from PySide6.QtGui import QUndoCommand


class ChangeTextCommand(QUndoCommand):

    def __init__(self, item:"EditableTextItem", old_text:str, parent:QUndoCommand=None):
        super().__init__(parent)

        self.item = item
        self.text = item.toPlainText()
        self.old_text = old_text

    def undo(self):
        self.item.setPlainText(self.old_text)
        self.setText("Change back text")

    def redo(self):
        self.item.setPlainText(self.text)
        self.setText("Set text")


class EditableTextItem(QGraphicsTextItem):
    """Text that can be edited by double clicking."""

    def __init__(self, text, undo_stack, parent=None):
        super().__init__(parent)
        self.setPlainText(text)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self._old_text = ""
        self.undo_stack = undo_stack

    def focusOutEvent(self, event):
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        change_text_command = ChangeTextCommand(self, self._old_text)
        self.undo_stack.push(change_text_command)
        super().focusOutEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.textInteractionFlags() == Qt.NoTextInteraction:
            self.setTextInteractionFlags(Qt.TextEditorInteraction)
            self._old_text = self.toPlainText()
        super().mouseDoubleClickEvent(event)
