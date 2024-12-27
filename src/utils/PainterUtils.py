"""
Utility functions to set various QPainter styles
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen

from utils import Constants


def enable_game_field_painter_style(qp: QPainter) -> None:
    """
    Sets correct style for drawing game field

    Args:
        qp (QPainter): QPainter instance

    Returns:
        None
    """
    qp.setBrush(Constants.SCREEN_COLOR)

def enable_rectangle_painter_style(qp: QPainter, color: QColor, is_selected: bool=False) -> None:
    """
    Sets correct style for drawing moveable rectangles

    Args:
        qp (QPainter): QPainter instance
        color (QColor): color of the rectangle
        is_selected (bool): flag to check if rectangle is selected

    Returns:
        None
    """
    qp.setBrush(color)
    qp.setPen(Constants.SELECTED_RECTANGLE_BORDER_COLOR if is_selected else color)

def enable_port_painter_style(qp: QPainter, color: QColor, is_selected: bool=False,
                              is_hovered: bool=False, is_unavailable: bool=False) -> None:
    """
    Sets correct style for drawing ports

    Args:
        qp (QPainter): QPainter instance
        color (QColor): color of the rectangle
        is_selected (bool): flag to check if rectangle is selected
        is_hovered (bool): flag to check if port is hovered
        is_unavailable (bool): flag to check if port is unavailable

    Returns:
        None
    """
    brush_color = color

    if is_selected:
        brush_color = Constants.SELECTED_ELEMENT_COLOR
    if is_hovered:
        brush_color = Constants.AVAILABLE_COLOR
    if is_unavailable:
        brush_color = Constants.UNAVAILABLE_COLOR

    qp.setBrush(brush_color)
    qp.setPen(Constants.SELECTED_ELEMENT_COLOR)

def enable_link_painter_style(qp: QPainter, is_selected: bool=False) -> None:
    """
    Sets correct style for drawing links

    Args:
        qp (QPainter): QPainter instance
        is_selected (bool): flag to check if link is selected

    Returns:
        None
    """
    pen = QPen()
    pen.setWidth(Constants.LINK_WIDTH_PX)
    pen.setColor(Constants.SELECTED_ELEMENT_COLOR if is_selected else Constants.LINK_COLOR)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    qp.setPen(pen)

def enable_button_painter_style(qp: QPainter, color: QColor) -> None:
    """
    Sets correct style for drawing buttons

    Args:
        qp (QPainter): QPainter instance
        color (QColor): color of the button

    Returns:
        None
    """
    qp.setPen(color)
    qp.setBrush(color)
