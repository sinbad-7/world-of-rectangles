"""
Implementation of the main game model
"""
from typing import Optional, List, Dict

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPolygon

from src.components.Link import Link
from src.components.MoveableRectangle import MoveableRectangle
from src.components.Port import Port
from src.utils import Constants
from src.utils.MathUtils import has_collision, is_point_in_circle


class GameModel:
    """
    The GameModel that stores all data required for the game

    Args: # noqa
        clone (GameModel): other GameModel object to populate the game model with custom values. Default = None

    Attributes:
        window_x (int): initial x coordinate of the game window
        window_y (int): initial y coordinate of the game window
        field_width (int): width of the game field
        field_height (int): height of the game field
        min_field_width (int): min width of the game field
        min_field_height (int): min height of the game field
        is_dragging_link (bool): flag to check if any link is being dragged
        rectangles (List[MoveableRectangle]): list of moveable rectangle objects
        links (List[Link]): list of link objects
        linked_port_ids (List[str]): list of port ids that were linked
        selected_rectangle (Optional[MoveableRectangle]): selected moveable rectangle object
        selected_port (Optional[Port]): selected port object
        hovered_port (Optional[Port]): hovered port object
        selected_link (Optional[Link]): selected link object
        x1 (int): x coordinate of the initial click position
        y1 (int): y coordinate of the initial click position
        x2 (int): x coordinate of the moving mouse position
        y2 (int): y coordinate of the moving mouse position
    """
    def __init__(self, clone=None):
        self.window_x = Constants.START_COORDINATES[0] if clone is None else clone.window_x
        self.window_y = Constants.START_COORDINATES[1] if clone is None else clone.window_y

        self.field_width = Constants.SCREEN_SIZE_MAX_PX[0] if clone is None else clone.field_width
        self.field_height = Constants.SCREEN_SIZE_MAX_PX[1] if clone is None else clone.field_height

        self.min_field_width = Constants.SCREEN_SIZE_MIN_PX[0] if clone is None else clone.min_field_width
        self.min_field_height = Constants.SCREEN_SIZE_MIN_PX[1] if clone is None else clone.min_field_height

        self.is_dragging_link: bool = False if clone is None else clone.is_dragging_link

        self.rectangles: List[MoveableRectangle] = []

        ports_map: Dict[str, str] = {}

        if clone and len(clone.rectangles):
            for clone_rectangle in clone.rectangles:
                new_rectangle = MoveableRectangle.from_clone(clone_rectangle)
                self.rectangles.append(new_rectangle)
                for i in range(0, len(clone_rectangle.ports)):
                    ports_map[clone_rectangle.ports[i].id] = new_rectangle.ports[i].id

        self.links: List[Link] = []

        if clone and len(clone.links):
            for clone_link in clone.links:
                new_link = Link.from_clone(clone_link, ports_map[clone_link.src_id], ports_map[clone_link.src_id])
                self.links.append(new_link)

        self.linked_port_ids: List[str] = []

        for link in self.links:
            self.linked_port_ids.append(link.src_id)
            self.linked_port_ids.append(link.dst_id)

        self.selected_rectangle: Optional[MoveableRectangle] = \
            None if clone is None else MoveableRectangle.from_clone(clone.selected_rectangle)

        self.selected_port: Optional[Port] = \
            None if clone is None else Port.from_clone(clone.selected_port)

        self.hovered_port: Optional[Port] = \
            None if clone is None else Port.from_clone(clone.hovered_port)

        self.selected_link: Optional[Link] = None if clone is None else (
            Link.from_clone(
                clone.selected_link,
                ports_map[clone.selected_link.src_id],
                ports_map[clone.selected_link.dst_id])
        )

        self.x1 = 0 if clone is None else clone.x1
        self.x2 = 0 if clone is None else clone.x2
        self.y1 = 0 if clone is None else clone.y1
        self.y2 = 0 if clone is None else clone.y2

    def try_add_new_rectangle(self, x_coord: int, y_coord: int) -> Optional[MoveableRectangle]:
        """
        Tries to add new MoveableRectangle object to the game model with center at (x_coord, y_coord)

        Args:
            x_coord (int): x coordinate of the click position
            y_coord (int): y coordinate of the click position

        Returns:
            Optional[MoveableRectangle]: MoveableRectangle object if it was successfully added to the game model.
            None otherwise
        """
        temp_rectangle = MoveableRectangle(x_coord, y_coord, Constants.RECTANGLE_WIDTH_PX,
                                           Constants.RECTANGLE_HEIGHT_PX)

        if not self.rectangles or len(self.rectangles) == 0:
            self.rectangles.append(temp_rectangle)
            return temp_rectangle

        if not has_collision(temp_rectangle, self.rectangles, self.field_width, self.field_height):
            self.rectangles.append(temp_rectangle)
            return temp_rectangle

        return None

    def find_selected_rectangle(self, x_coord: int, y_coord: int) -> Optional[MoveableRectangle]:
        """
        Tries to find the MoveableRectangle object from the game model at coordinates (x_coord, y_coord)

        Args:
            x_coord (int): x coordinate of the click position
            y_coord (int): y coordinate of the click position

        Returns:
            Optional[MoveableRectangle]: MoveableRectangle object if rectangle was found. None otherwise
        """
        for rectangle in self.rectangles:
            if rectangle.contains(x_coord, y_coord):
                return rectangle

        return None

    def find_selected_port(self, x_coord: int, y_coord: int,
                           search_all: bool=False) -> Optional[Port]:
        """
        Tries to find the Port object from the selected rectangle at coordinates (x_coord, y_coord)
        If search_all is set to True - all ports are searched

        Args:
            x_coord (int): x coordinate of the click position
            y_coord (int): y coordinate of the click position
            search_all (bool): flag if every port should be searched.
            Default = False - only port of the selected rectangle will be searched

        Returns:
            Optional[Port]: Port object if port was found. None otherwise
        """
        if self.selected_rectangle is None:
            return None

        if search_all:
            for rect in self.rectangles:
                for port in rect.ports:
                    if is_point_in_circle(port.x(), port.y(), x_coord, y_coord):
                        return port
        else:
            for port in self.selected_rectangle.ports:
                if is_point_in_circle(port.x(), port.y(), x_coord, y_coord):
                    return port

        return None

    def find_selected_link(self, x_coord: int, y_coord: int) -> Optional[Link]:
        """
        Tries to find the Link object from the game model at coordinates (x_coord, y_coord)

        Args:
            x_coord (int): x coordinate of the click position
            y_coord (int): y coordinate of the click position

        Returns:
            Optional[Link]: Link object if link was found. None otherwise
        """
        for link in self.links:
            src_x, src_y = link.x1(), link.y1()
            dst_x, dst_y = link.x2(), link.y2()
            link_polygon = QPolygon([
                QPoint(int(src_x + Constants.LINK_WIDTH_PX), int(src_y - Constants.LINK_WIDTH_PX)),
                QPoint(int(dst_x + Constants.LINK_WIDTH_PX), int(dst_y - Constants.LINK_WIDTH_PX)),
                QPoint(int(dst_x - Constants.LINK_WIDTH_PX), int(dst_y + Constants.LINK_WIDTH_PX)),
                QPoint(int(src_x - Constants.LINK_WIDTH_PX), int(src_y + Constants.LINK_WIDTH_PX))
            ])

            if link_polygon.containsPoint(QPoint(x_coord, y_coord), Qt.FillRule.WindingFill):
                return link

        return None

    def update_links_offset(self, x_offset: int, y_offset: int) -> None:
        """
        Updates the coordinates of links that were moved using new offset values

        Args:
            x_offset (int): new x coordinate offset
            y_offset (int): new y coordinate offset

        Returns:
            None
        """
        if self.selected_rectangle is None:
            return

        for link in self.links:
            src_x_offset = 0
            src_y_offset = 0
            dst_x_offset = 0
            dst_y_offset = 0

            src_port = next((x for x in self.selected_rectangle.ports if x.id == link.src_id), None)
            dst_port = next((x for x in self.selected_rectangle.ports if x.id == link.dst_id), None)

            if src_port:
                src_x_offset = x_offset
                src_y_offset = y_offset
            if dst_port:
                dst_x_offset = x_offset
                dst_y_offset = y_offset

            link.setLine(
                link.x1() + src_x_offset,
                link.y1() + src_y_offset,
                link.x2() + dst_x_offset,
                link.y2() + dst_y_offset
            )

    def recalculate_min_field_size(self) -> (int, int):
        """
        Recalculates the min field size of the game model considering current rectangle positions

        Returns:
            (int, int): min_width and min_height values
        """
        max_width = Constants.SCREEN_SIZE_MIN_PX[0]
        max_height = Constants.SCREEN_SIZE_MIN_PX[1]

        for rectangle in self.rectangles:
            max_width = max(max_width, rectangle.x() + rectangle.width())
            max_height = max(max_height, rectangle.y() + rectangle.height())

        self.min_field_width, self.min_field_height = max_width, max_height

        return max_width, max_height
