"""
Implementation of the MoveableRectangle component
"""
import random
import uuid
from typing import List

from PyQt6.QtCore import QRect
from PyQt6.QtGui import QColor

from src.components.Port import Port
from src.utils import Constants


class MoveableRectangle(QRect):
    """
    The MoveableRectangle, child of QRect class, that stores all additional data required for the game

    Args:
        x_center_coord (int): x coordinate of the center of current object
        y_center_coord (int): y coordinate of the center of current object
        width (int): width of the rectangle
        height (int): height of the rectangle

    Attributes:
        id (str): id of this MoveableRectangle object
        color (QColor): color of the rectangle
        ports (List[Port]): list of ports
    """
    def __init__(self, x_center_coord: int, y_center_coord: int, width: int, height: int):
        super().__init__(int(x_center_coord - width / 2), int(y_center_coord - height / 2), width, height)

        self.id = str(uuid.uuid4())
        self.color: QColor = QColor(random.choice(Constants.RECTANGLE_COLORS))
        self.ports: List[Port] = []

        self.add_new_port(
            self.id,
            int(self.x() + self.width() / 2 - Constants.CIRCLE_RADIUS_PX / 2),
            int(self.y() - Constants.CIRCLE_RADIUS_PX / 2)
        )

        self.add_new_port(
            self.id,
            int(self.x() + self.width() - Constants.CIRCLE_RADIUS_PX / 2),
            int(self.y() + self.height() / 2 - Constants.CIRCLE_RADIUS_PX / 2)
        )

        self.add_new_port(
            self.id,
            int(self.x() + self.width() / 2 - Constants.CIRCLE_RADIUS_PX / 2),
            int(self.y() + self.height() - Constants.CIRCLE_RADIUS_PX / 2)
        )

        self.add_new_port(
            self.id,
            int(self.x() - Constants.CIRCLE_RADIUS_PX / 2),
            int(self.y() + self.height() / 2 - Constants.CIRCLE_RADIUS_PX / 2)
        )

    @classmethod
    def from_clone(cls, clone):
        """
        Creates a new instance of the MoveableRectangle from clone

        Args:
            clone (MoveableRectangle): other MoveableRectangle object

        Returns: new MoveableRectangle object with cloned fields
        """
        if not clone:
            return None

        return cls(clone.center().x(), clone.center().y(), clone.width(), clone.height())

    def update_ports_offset(self, x_offset: int, y_offset: int) -> None:
        """
        Updates the coordinates of ports using new offset values

        Args:
            x_offset (int): new x coordinate offset
            y_offset (int): new y coordinate offset

        Returns:
            None
        """
        for port in self.ports:
            port.setX(port.x() + x_offset)
            port.setY(port.y() + y_offset)

    def get_bound_coordinates(self) -> List[int]:
        """
        Gets the coordinates of rectangle bounds and returns them as a list

        Returns:
            List[int]: list of rectangle bounds as follows: [left, right, top, bottom]
        """
        return [
            self.x(),
            self.x() + self.width(),
            self.y(),
            self.y() + self.height()
        ]

    def add_new_port(self, parent_id:str, port_x: int, port_y: int, port_radius:int=Constants.CIRCLE_RADIUS_PX,
                     port_color:QColor=Constants.PORT_COLOR) -> None:
        """
        Updates the coordinates of links that were moved using new offset values

        Args:
            parent_id (str): parent rectangle id
            port_x (int): x coordinate of the port center
            port_y (int): y coordinate of the port center
            port_radius (int): radius of the port. Default: Constants.CIRCLE_RADIUS_PX
            port_color (QColor): color of the port. Default: Constants.PORT_COLOR

        Returns:
            None
        """
        self.ports.append(Port(parent_id, port_x, port_y, port_radius, port_color))
