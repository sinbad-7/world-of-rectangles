"""
Configuration constants used in application
"""
from typing import List

from PyQt6.QtGui import QColor

START_COORDINATES: List[int] = [200, 200]
SCREEN_SIZE_MAX_PX: List[int] = [1024, 768]
SCREEN_SIZE_MIN_PX: List[int] = [200, 200]

RECTANGLE_COLORS: List[str] = ['cyan', 'darkCyan', 'darkRed', 'magenta',
                               'darkMagenta', 'darkGreen', 'yellow', 'darkBlue', 'gray']
BLACK_COLOR: QColor = QColor('black')
WHITE_COLOR: QColor = QColor('white')
GREEN_COLOR: QColor = QColor('green')
RED_COLOR: QColor = QColor('red')
BLUE_COLOR: QColor = QColor('blue')

SCREEN_COLOR: QColor = QColor(BLACK_COLOR)
BORDER_COLOR: QColor = QColor(BLACK_COLOR)
LINK_COLOR: QColor = QColor(WHITE_COLOR)
PORT_COLOR: QColor = QColor(WHITE_COLOR)
SELECTED_RECTANGLE_BORDER_COLOR: QColor = QColor(WHITE_COLOR)
SELECTED_ELEMENT_COLOR: QColor = QColor(BLUE_COLOR)
AVAILABLE_COLOR: QColor = QColor(GREEN_COLOR)
UNAVAILABLE_COLOR: QColor = QColor(RED_COLOR)
DELETE_COLOR: QColor = QColor(RED_COLOR)

RECTANGLE_WIDTH_PX: int = 100
RECTANGLE_HEIGHT_PX: int = int(RECTANGLE_WIDTH_PX / 2)
CIRCLE_RADIUS_PX: int = 10
CIRCLE_RADIUS_SQUARED_PX: int = CIRCLE_RADIUS_PX ** 2
LINK_WIDTH_PX: int = 4
