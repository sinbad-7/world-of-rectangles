"""
Implementation of the Port component
"""
import uuid

from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QColor


class Port(QPoint):
    """
    The Port, child of QPoint class, that stores all additional data required for the game

    Args:
        parent_id (str): id of the parent MoveableRectangle object
        x_coord (int): x coordinate of the center of current object
        y_coord (int): y coordinate of the center of current object
        radius (int): radius of the port
        color (QColor): color of the port

    Attributes:
        id (str): id of this Port object
        parent_id (str): id of the parent MoveableRectangle object
        radius (int): radius of the port
        color (QColor): color of the port
    """
    def __init__(self, parent_id: str, x_coord: int, y_coord: int, radius: int, color: QColor):
        super().__init__(x_coord, y_coord)

        self.id = parent_id + '_' + str(uuid.uuid4())
        self.parent_id = parent_id
        self.radius = radius
        self.color = color

    @classmethod
    def from_clone(cls, clone):
        """
        Creates a new instance of the Port from clone

        Args:
            clone (Port): other Port object

        Returns: new Port object with cloned fields
        """
        if not clone:
            return None

        return cls(clone.parent_id, clone.x(), clone.y(), clone.radius, clone.color)
