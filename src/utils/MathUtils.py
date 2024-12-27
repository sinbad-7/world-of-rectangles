"""
Utility functions related to general calculations
"""
from typing import Optional, List
from functools import lru_cache

from components.MoveableRectangle import MoveableRectangle
from utils import Constants


@lru_cache(maxsize=128)
def has_border_collision(left: int, right: int, top: int, bottom: int,
                         screen_width: int, screen_height: int,
                         x_offset: int = 0, y_offset: int = 0) -> bool:
    """
    Checks if the rectangle with given bounds has a collision with given game field

    Args:
        left (int): left side of the moved rectangle
        right (int): right side of the moved rectangle
        top (int): top side of the moved rectangle
        bottom (int): bottom side of the moved rectangle
        screen_width (int): width of the screen
        screen_height (int): height of the screen
        x_offset (int): x offset of the moved rectangle. Default: 0
        y_offset (int): y offset of the moved rectangle. Default: 0

    Returns:
        (bool): True if rectangle with given bounds have collision with given game field. False otherwise
    """
    return (left + x_offset < 0
            or top + y_offset < 0
            or right + x_offset > screen_width
            or bottom + y_offset > screen_height)

@lru_cache(maxsize=128)
def has_rectangle_overlap(left_1: int, right_1: int, top_1: int, bottom_1: int,
                          left_2: int, right_2: int, top_2: int, bottom_2: int,
                          x_offset: int=0, y_offset: int=0) -> bool:
    """
    Checks if rectangles with given bounds and offset overlap

    Args:
        left_1 (int): left side of the moved rectangle
        right_1 (int): right side of the moved rectangle
        top_1 (int): top side of the moved rectangle
        bottom_1 (int): bottom side of the moved rectangle
        left_2 (int): left side of the other rectangle
        right_2 (int): right side of the other rectangle
        top_2 (int): top side of the other rectangle
        bottom_2 (int): bottom side of the other rectangle
        x_offset (int): x offset of the moved rectangle. Default: 0
        y_offset (int): y offset of the moved rectangle. Default: 0

    Returns:
        (bool): True if rectangles with given bounds overlap. False otherwise
    """
    moveable_left_1 = left_1 + x_offset
    moveable_top_1 = top_1 + y_offset
    moveable_right_1 = right_1 + x_offset
    moveable_bottom_1 = bottom_1 + y_offset

    no_overlap = (moveable_left_1 >= right_2
                  or left_2 >= moveable_right_1
                  or moveable_top_1 >= bottom_2
                  or top_2 >= moveable_bottom_1)

    return not no_overlap

def has_collision(moveable_rectangle: Optional[MoveableRectangle],
                  rectangles: List[Optional[MoveableRectangle]],
                  screen_width: int, screen_height: int,
                  x_offset: int=0, y_offset: int=0) -> bool:
    """
    Checks if moveable rectangle has collision with given game field or other rectangles

    Args:
        moveable_rectangle (Optional[MoveableRectangle]): moveable rectangle to check
        rectangles (List[Optional[MoveableRectangle]]): list of rectangles
        screen_width (int): width of the screen
        screen_height (int): height of the screen
        x_offset (int): x offset of moveable rectangle. Default: 0
        y_offset (int): y offset of moveable rectangle. Default: 0

    Returns:
        (bool): True if moveable rectangle has collisions with game field or other rectangles. False otherwise
    """
    if (moveable_rectangle and has_border_collision(
            *moveable_rectangle.get_bound_coordinates(), screen_width, screen_height, x_offset, y_offset)):
        return True

    for rectangle in rectangles:
        if moveable_rectangle and rectangle and moveable_rectangle != rectangle:
            has_overlap = has_rectangle_overlap(
                *moveable_rectangle.get_bound_coordinates(),
                *rectangle.get_bound_coordinates(),
                x_offset,
                y_offset
            )

            if has_overlap:
                return has_overlap

    return False

@lru_cache(maxsize=128)
def is_point_in_circle(x_center: int, y_center: int, x_coord: int, y_coord: int) -> bool:
    """
    Checks if point with given coordinates is inside the given circle

    Args:
        x_center (int): x coordinate of the circle center
        y_center (int): y coordinate of the circle center
        x_coord (int): x coordinate of the point
        y_coord (int): y coordinate of the point

    Returns:
        (bool): True if point is inside the circle, False otherwise
    """
    return ((x_coord - x_center) ** 2 + (y_coord - y_center) ** 2
            <= Constants.CIRCLE_RADIUS_SQUARED_PX)
