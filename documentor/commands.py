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

    def __init__(self, items:list[QGraphicsItem], scene: QGraphicsScene, parent:QUndoCommand=None):
        super().__init__(parent)

        self.items = items
        self.scene = scene

    def undo(self):
        for item in self.items:
            self.scene.addItem(item)
        self.setText("Undeleted items")
        self.scene.update()

    def redo(self):
        for item in self.items:
            self.scene.removeItem(item)
        self.setText("Redeleted items")
        self.scene.update()


class MoveCommand(QUndoCommand):

    def __init__(self, items:list[QGraphicsItem], scene: QGraphicsScene, old_positions:list[QPointF], parent:QUndoCommand=None):
        super().__init__(parent)

        self.scene = scene
        self.items = items
        self.old_positions = old_positions
        self.new_positions = [item.pos() for item in self.items]

    def undo(self):
        for item, pos in zip(self.items, self.old_positions):
            item.setPos(pos)
        self.scene.update()
        self.setText("Undone move")

    def redo(self):
        for item, pos in zip(self.items, self.new_positions):
            item.setPos(pos)
        self.scene.update()
        self.setText("Redone move")

    # def mergeWith(self, command: QUndoCommand) -> bool:
    #     pass
