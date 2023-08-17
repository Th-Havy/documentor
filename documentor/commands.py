"""This module contains the commands to implement the undo/redo system."""


from PySide6.QtCore import QPointF
from PySide6.QtGui import QUndoCommand, QBrush, QPen, QFont
from PySide6.QtWidgets import QGraphicsItem, QGraphicsScene


class AddCommand(QUndoCommand):

    def __init__(self, item:QGraphicsItem, scene: QGraphicsScene, pen:QPen=None,
                 brush:QBrush=None, font:QFont=None, parent:QUndoCommand=None):
        super().__init__(parent)

        self.item = item
        self.scene = scene

        if pen:
            self.item.setPen(pen)
        if brush:
            if font:
                self.item.setDefaultTextColor(brush.color())
            else:
                self.item.setBrush(brush)
        if font:
            self.item.setFont(font)

    def undo(self):
        self.scene.removeItem(self.item)
        self.scene.update()
        self.setText("Removed item")

    def redo(self):
        self.scene.addItem(self.item)
        self.setText("Re-added item")


class DeleteCommand(QUndoCommand):

    def __init__(self, item:QGraphicsItem, scene: QGraphicsScene, parent:QUndoCommand=None):
        super().__init__(parent)

        self.item = item
        self.scene = scene

    def undo(self):
        self.scene.addItem(self.item)
        self.setText("Undeleted item")
        self.scene.update()

    def redo(self):
        self.scene.removeItem(self.item)
        self.scene.update()
        self.setText("Redeleted item")


class MoveCommand(QUndoCommand):

    def __init__(self, item:QGraphicsItem, old_position:QPointF, parent:QUndoCommand=None):
        super().__init__(parent)

        self.item = item
        self.old_position = old_position
        self.new_position = item.pos()

    def undo(self):
        self.item.setPos(self.old_position)
        self.item.scene().update()
        self.setText("Undone move")

    def redo(self):
        self.item.setPos(self.new_position)
        self.setText("Redone move")

    def mergeWith(self, command: QUndoCommand) -> bool:
        pass

    def id(self) -> int:
        return 1234
