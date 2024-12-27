"""
Implementation of the Link component
"""
import uuid

from PyQt6.QtCore import QLine
from PyQt6.QtGui import QColor

from utils import Constants
from components.Port import Port


class Link(QLine):
    """
    The Link, child of QLine class, that stores all additional data required for the game

    Args:
        x1_coord (int): x coordinate of the source port
        y1_coord (int): y coordinate of the source port
        x2_coord (int): x coordinate of the destination port
        y2_coord (int): y coordinate of the destination port
        src_id (str): id of the source port object
        dst_id (str): id of the destination port object
        width (int): width of the link
        color (QColor): color of the link

    Attributes:
        id (str): id of this Link object
        src_id (str): id of the source Port object
        dst_id (str): id of the destination Port object
        width (int): width of the link
        color (QColor): color of the link
    """
    def __init__(self, x1_coord: int, y1_coord: int, x2_coord: int, y2_coord: int, src_id: str,
                 dst_id: str, width: int, color: QColor):
        super().__init__(x1_coord, y1_coord, x2_coord, y2_coord)

        self.id = src_id + ';;' + dst_id + ';;' + str(uuid.uuid4())
        self.src_id = src_id
        self.dst_id = dst_id
        self.width = width
        self.color = color

    @classmethod
    def from_clone(cls, clone, src_id, dst_id):
        """
        Creates a new instance of the Link from clone

        Args:
            clone (Link): other Link object
            src_id (str): y coordinate of the click position
            dst_id (str): y coordinate of the click position

        Returns: new Link object with cloned fields
        """
        if not clone:
            return None

        return cls(clone.x1(), clone.y1(), clone.x2(), clone.y2(),
                   src_id, dst_id, clone.width, clone.color)

    @classmethod
    def from_ports(cls, src: Port, dst: Port, width: int, color: QColor):
        """
        Creates a new instance of the Link using source and destination ports with specified parameters

        Args:
            src (Port): source port object
            dst (Port): destination port object
            width (int): width of the link
            color (QColor): color of the link

        Returns: new Link object
        """
        x1 = int(src.x() + Constants.CIRCLE_RADIUS_PX / 2)
        y1 = int(src.y() + Constants.CIRCLE_RADIUS_PX / 2)
        x2 = int(dst.x() + Constants.CIRCLE_RADIUS_PX / 2)
        y2 = int(dst.y() + Constants.CIRCLE_RADIUS_PX / 2)

        return cls(x1, y1, x2, y2, src.id, dst.id, width, color)
