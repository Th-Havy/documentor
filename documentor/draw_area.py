from enum import Enum

from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsItem,
    QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsTextItem)
from PySide6.QtGui import QPixmap, QFont, QUndoStack

from . import colors
from .commands import AddCommand, DeleteCommand, MoveCommand
from .editable_text_item import EditableTextItem


class CurrentTool(Enum):
    CURSOR = 0
    RECTANGLE = 1
    ELLIPSE = 2
    TEXT = 3


class DrawArea(QGraphicsView):
    """Main view to display and draw items."""

    def __init__(self, scene:QGraphicsScene, undo_stack:QUndoStack):
        super().__init__(scene)

        self.scene = scene
        self.view = QGraphicsView(self.scene)
        self.undo_stack = undo_stack
        self.move_old_positions = []

        # To keep track of shape drawing
        self.current_tool = CurrentTool.CURSOR
        self.draw_begin = QPoint()
        self.draw_end = QPoint()
        self.shape = None
        self.image = None

        # Default pens and brushes
        self.border_color = colors.Color.GREEN
        self.background_color = colors.Color.GREEN
        self.pen = colors.PENS[self.border_color]
        self.brush = colors.BRUSHES[self.background_color]
        self.font = QFont("Times", 10, QFont.Bold)

        # Allow drag&drop of image
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):

        if self.current_tool == CurrentTool.CURSOR:
            super().mousePressEvent(event)

            if self.scene.selectedItems():
                self.begin_move_items(self.scene.selectedItems())
            return

        if event.buttons() & Qt.MouseButton.LeftButton:
            self.begin_draw_shape(event.pos())

    def mouseMoveEvent(self, event):

        if self.current_tool == CurrentTool.CURSOR:
            super().mouseMoveEvent(event)
            return

        if event.buttons() & Qt.MouseButton.LeftButton:
            self.update_draw_shape(event.pos())

    def mouseReleaseEvent(self, event):

        if self.current_tool == CurrentTool.CURSOR:
            super().mouseReleaseEvent(event)

            if self.scene.selectedItems():
                self.end_move_items(self.scene.selectedItems())
            return

        if event.button() & Qt.MouseButton.LeftButton:
            self.end_draw_shape()

    def dragEnterEvent(self, event):
        """Must be overriden so that dropEvent() gets called."""
        if (event.mimeData().hasImage()):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        """Must be overriden so that dropEvent() gets called."""
        pass

    def dropEvent(self, event):
        if (event.mimeData().hasImage()):
            self.draw_image(QPixmap(event.mimeData().imageData()))

    def set_current_tool(self, tool:CurrentTool):
        self.current_tool = tool

    def set_border_color(self, border_color):
        self.border_color = border_color
        self.pen = colors.PENS[self.border_color]

    def set_background_color(self, background_color):
        self.background_color = background_color
        self.brush = colors.BRUSHES[self.background_color]

    def begin_draw_shape(self, pos):
        self.draw_begin = pos
        self.draw_end = self.draw_begin

        if self.current_tool == CurrentTool.RECTANGLE:
            self.shape = QGraphicsRectItem(QRect(self.draw_begin, self.draw_end))
            add_command = AddCommand(self.shape, self.scene, self.pen, self.brush)
            self.undo_stack.push(add_command)
        if self.current_tool == CurrentTool.ELLIPSE:
            self.shape = QGraphicsEllipseItem(QRect(self.draw_begin, self.draw_end))
            add_command = AddCommand(self.shape, self.scene, self.pen, self.brush)
            self.undo_stack.push(add_command)
        if self.current_tool == CurrentTool.TEXT:
            self.shape = EditableTextItem("Text", self.undo_stack)
            self.shape.setPos(self.draw_begin)
            add_command = AddCommand(self.shape, self.scene, brush=self.brush, font=self.font)
            self.undo_stack.push(add_command)

    def update_draw_shape(self, pos):
        if self.current_tool != CurrentTool.TEXT:
            self.draw_end = pos
            self.shape.setRect(QRect(self.draw_begin, self.draw_end))
        else:
            self.shape.setPos(pos)

    def end_draw_shape(self):
        self.draw_begin = QPoint()
        self.draw_end = QPoint()

        self.shape.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.shape.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.shape.setFlag(QGraphicsItem.ItemIsFocusable, True)

        self.shape = None

    def draw_image(self, pixmap:QPixmap):
        self.image = self.scene.addPixmap(pixmap)
        # Always place the image in the background
        self.image.setZValue(-1)

    def keyPressEvent(self, event):
        """Delete selected items when pressing Del key."""

        # Necessary to edit text
        super().keyPressEvent(event)

        if self.current_tool == CurrentTool.CURSOR:
            if event.key() == Qt.Key.Key_Delete:
                self.delete_selected_items()

    def delete_selected_items(self):
        delete_command = DeleteCommand(self.scene.selectedItems(), self.scene)
        self.undo_stack.push(delete_command)

    def begin_move_items(self, selected_items):
        self.move_old_positions = [item.pos() for item in selected_items]

    def end_move_items(self, selected_items):
        move_command = MoveCommand(selected_items, self.scene, self.move_old_positions)
        self.undo_stack.push(move_command)
