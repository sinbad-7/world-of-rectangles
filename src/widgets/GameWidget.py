"""
Implementation of the main game widget
"""
from typing import Optional

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QMouseEvent, QResizeEvent

from components.Link import Link
from components.MoveableRectangle import MoveableRectangle
from models.GameModel import GameModel
from utils import Constants, PainterUtils
from utils.MathUtils import has_collision, is_point_in_circle


class GameWidget(QWidget):
    """
    The GameWidget, child of QWidget class, that implements the main game logic

    Args:
        model (GameModel): GameModel object with game data

    Attributes:
        model (GameModel): GameModel object to hold game data
    """

    def __init__(self, model: GameModel):
        super().__init__()

        self.model = model
        self.init_ui()

    def init_ui(self):
        """
        Initializes the game widget object

        Returns:
            None
        """
        self.setGeometry(self.model.window_x, self.model.window_y, self.model.field_width, self.model.field_height)
        self.setMaximumSize(*Constants.SCREEN_SIZE_MAX_PX)
        self.setMinimumSize(self.model.min_field_width, self.model.min_field_height)
        self.setMouseTracking(True)
        self.setWindowTitle('World of Rectangles')

    def mouseMoveEvent(self, event: Optional[QMouseEvent]) -> None:
        """
        Handles the mouse movement logic

        Args:
            event (QMouseEvent): event data

        Returns:
            None
        """
        if not event:
            return

        if self.model.x1 > 0:
            new_x2 = event.pos().x() - self.model.x1
            new_y2 = event.pos().y() - self.model.y1

            if self.model.is_dragging_link:
                self.model.hovered_port = (
                    self.model.find_selected_port(event.pos().x(), event.pos().y(), True))

                self.model.x2 = new_x2
                self.model.y2 = new_y2
            else:
                if not has_collision(self.model.selected_rectangle, self.model.rectangles,
                                     self.model.field_width, self.model.field_height, new_x2, new_y2):
                    self.model.x2 = new_x2
                    self.model.y2 = new_y2

            self.update()

    def handle_delete_link_button_pressed(self) -> bool:
        """
        Handles the case when user pressed delete link button

        Returns:
            (bool): True if delete button was pressed and press event is handled. False otherwise
        """
        if (self.model.selected_link and is_point_in_circle(
                self.model.selected_link.center().x(),
                self.model.selected_link.center().y(),
                self.model.x1,
                self.model.y1)
        ):
            self.model.links.remove(self.model.selected_link)
            self.model.linked_port_ids.remove(self.model.selected_link.src_id)
            self.model.linked_port_ids.remove(self.model.selected_link.dst_id)
            self.model.selected_link = None
            self.update()
            return True

        return False

    def handle_link_pressed(self) -> bool:
        """
        Handles the case when user pressed link object

        Returns:
            (bool): True if link was pressed and press event is handled. False otherwise
        """
        self.model.selected_link = self.model.find_selected_link(self.model.x1, self.model.y1)

        if self.model.selected_link is not None:
            self.model.selected_port = None
            self.model.selected_rectangle = None
            self.model.is_dragging_link = False

            self.update()
            return True

        return False

    def handle_port_pressed(self) -> bool:
        """
        Handles the case when user pressed port object

        Returns:
            (bool): True if port was pressed and press event is handled. False otherwise
        """
        self.model.selected_port = self.model.find_selected_port(self.model.x1, self.model.y1)

        if (self.model.selected_port is not None
                and self.model.selected_port.id not in self.model.linked_port_ids):
            self.update()
            self.model.is_dragging_link = True
            return True

        self.model.selected_port = None
        return False

    def handle_moveable_rectangle_pressed(self) -> bool:
        """
        Handles the case when user pressed moveable rectangle object

        Returns:
            (bool): True if moveable rectangle was pressed and press event is handled. False otherwise
        """
        self.model.selected_rectangle = self.model.find_selected_rectangle(self.model.x1, self.model.y1)

        if self.model.selected_rectangle is not None:
            self.update()
            return True

        return False

    def mousePressEvent(self, event: Optional[QMouseEvent]) -> None:
        """
        Handles the mouse press logic

        Args:
            event (QMouseEvent): event data

        Returns:
            None
        """
        if event is None:
            return

        self.model.x1 = event.pos().x()
        self.model.y1 = event.pos().y()

        if self.handle_delete_link_button_pressed():
            return

        if self.handle_link_pressed():
            return

        if self.handle_port_pressed():
            return

        self.handle_moveable_rectangle_pressed()

    def mouseDoubleClickEvent(self, event) -> None:
        """
        Handles the mouse double click logic

        Args:
            event (QMouseEvent): event data

        Returns:
            None
        """
        if not event:
            return

        self.model.x1 = event.pos().x()
        self.model.y1 = event.pos().y()

        selected_link = self.model.find_selected_link(self.model.x1, self.model.y1)
        selected_port = self.model.find_selected_port(self.model.x1, self.model.y1)

        if selected_link is not None or selected_port is not None:
            return

        selected_rectangle = self.model.find_selected_rectangle(self.model.x1, self.model.y1)

        if selected_rectangle is None:
            new_rectangle = self.model.try_add_new_rectangle(self.model.x1, self.model.y1)
            self.model.x1 = self.model.y1 = 0

            if new_rectangle:
                self.model.selected_rectangle = new_rectangle
                self.update()

    def mouseReleaseEvent(self, event: Optional[QMouseEvent]) -> None:
        """
        Handles the mouse release logic

        Args:
            event (QMouseEvent): event data

        Returns:
            None
        """
        if not event:
            return

        if self.model.selected_rectangle and not self.model.is_dragging_link:
            self.model.selected_rectangle.setRect(
                self.model.selected_rectangle.x() + self.model.x2,
                self.model.selected_rectangle.y() + self.model.y2,
                self.model.selected_rectangle.width(),
                self.model.selected_rectangle.height()
            )

            self.model.selected_rectangle.update_ports_offset(self.model.x2, self.model.y2)
            self.model.update_links_offset(self.model.x2, self.model.y2)

        if (self.model.selected_port is not None
                and self.model.hovered_port is not None
                and self.model.hovered_port not in self.model.selected_rectangle.ports
        ):
            self.model.links.append(
                Link.from_ports(
                    self.model.selected_port,
                    self.model.hovered_port,
                    Constants.LINK_WIDTH_PX,
                    Constants.LINK_COLOR)
            )
            self.model.linked_port_ids.append(self.model.selected_port.id)
            self.model.linked_port_ids.append(self.model.hovered_port.id)

        self.model.x1 = self.model.x2 = self.model.y1 = self.model.y2 = 0
        self.model.is_dragging_link = False
        self.model.hovered_port = None
        self.setMinimumSize(*self.model.recalculate_min_field_size())
        self.update()

    def resizeEvent(self, event: Optional[QResizeEvent]) -> None:
        """
        Handles the window resize logic

        Args:
            event (QResizeEvent): event data

        Returns:
            None
        """
        self.model.field_width = self.width()
        self.model.field_height = self.height()

    def paintEvent(self, event) -> None:
        """
        Handles the window re-paint logic

        Returns:
            None
        """
        qp = QPainter()
        qp.begin(self)
        self.draw_game_objects(qp)
        qp.end()

    def draw_game_field(self, qp: QPainter) -> None:
        """
        Draws the game field with correct styles

        Args:
            qp (QPainter): QPainter instance

        Returns:
            None
        """
        PainterUtils.enable_game_field_painter_style(qp)
        qp.drawRect(0, 0, self.model.field_width, self.model.field_height)

    def draw_links(self, qp: QPainter) -> None:
        """
        Draws the link objects with correct styles

        Args:
            qp (QPainter): QPainter instance

        Returns:
            None
        """
        if self.model.is_dragging_link:
            PainterUtils.enable_link_painter_style(qp)
            qp.drawLine(
                self.model.x1,
                self.model.y1,
                self.model.x1 + self.model.x2,
                self.model.y1 + self.model.y2
            )

        for link in self.model.links:
            src_offset_x = 0
            src_offset_y = 0
            dst_offset_x = 0
            dst_offset_y = 0

            if self.model.selected_rectangle and not self.model.is_dragging_link:
                src_port = next((x for x in self.model.selected_rectangle.ports if x.id == link.src_id), None)
                dst_port = next((x for x in self.model.selected_rectangle.ports if x.id == link.dst_id), None)

                if src_port:
                    src_offset_x = self.model.x2
                    src_offset_y = self.model.y2
                if dst_port:
                    dst_offset_x = self.model.x2
                    dst_offset_y = self.model.y2

            PainterUtils.enable_link_painter_style(qp, self.model.selected_link == link)
            qp.drawLine(
                link.x1() + src_offset_x,
                link.y1() + src_offset_y,
                link.x2() + dst_offset_x,
                link.y2() + dst_offset_y
            )

        if self.model.selected_link is not None:
            center_x, center_y = self.model.selected_link.center().x(), self.model.selected_link.center().y()

            PainterUtils.enable_button_painter_style(qp, Constants.DELETE_COLOR)
            qp.drawEllipse(
                int(center_x - Constants.CIRCLE_RADIUS_PX / 2),
                int(center_y - Constants.CIRCLE_RADIUS_PX / 2),
                Constants.CIRCLE_RADIUS_PX,
                Constants.CIRCLE_RADIUS_PX
            )

    def draw_ports(self, qp: QPainter, rectangle: MoveableRectangle) -> None:
        """
        Draws the ports of the given moveable rectangle with correct styles

        Args:
            qp (QPainter): QPainter instance
            rectangle (MoveableRectangle): moveable rectangle object to draw ports for

        Returns:
            None
        """
        for port in rectangle.ports:
            if port.id in self.model.linked_port_ids:
                continue

            is_selected = port == self.model.selected_port
            is_hovered = port == self.model.hovered_port and self.model.selected_port != self.model.hovered_port
            is_unavailable = (
                    port == self.model.hovered_port
                    and self.model.selected_port != self.model.hovered_port
                    and self.model.hovered_port in self.model.selected_rectangle.ports
            )

            port_x = port.x() if self.model.is_dragging_link else port.x() + self.model.x2
            port_y = port.y() if self.model.is_dragging_link else port.y() + self.model.y2

            PainterUtils.enable_port_painter_style(qp, port.color, is_selected, is_hovered, is_unavailable)
            qp.drawEllipse(port_x, port_y, port.radius, port.radius)

    def draw_rectangles(self, qp: QPainter) -> None:
        """
        Draws the rectangle objects with correct styles

        Args:
            qp (QPainter): QPainter instance

        Returns:
            None
        """
        for rect in self.model.rectangles:
            if rect == self.model.selected_rectangle:
                rect_x = rect.x() if self.model.is_dragging_link else rect.x() + self.model.x2
                rect_y = rect.y() if self.model.is_dragging_link else rect.y() + self.model.y2

                PainterUtils.enable_rectangle_painter_style(qp, rect.color, rect == self.model.selected_rectangle)
                qp.drawRect(rect_x, rect_y, rect.width(), rect.height())

                self.draw_ports(qp, rect)
            else:
                PainterUtils.enable_rectangle_painter_style(qp, rect.color, rect == self.model.selected_rectangle)
                qp.drawRect(rect.x(), rect.y(), rect.width(), rect.height())

                if self.model.selected_port is not None:
                    self.draw_ports(qp, rect)

    def draw_game_objects(self, qp: QPainter) -> None:
        """
        Handles drawing of all game objects

        Args:
            qp (QPainter): QPainter instance

        Returns:
            None
        """
        self.draw_game_field(qp)
        self.draw_rectangles(qp)
        self.draw_links(qp)
