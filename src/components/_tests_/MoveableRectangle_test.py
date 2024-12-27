from PyQt6.QtGui import QColor

from src.components.MoveableRectangle import MoveableRectangle


class TestMoveableRectangle:
    def test_update_ports_offset(self):
        x_offset = 12
        y_offset = 30
        expected_rectangle = MoveableRectangle(100, 100, 100, 50)

        expected_coordinates = []

        for port in expected_rectangle.ports:
            expected_coordinates.append((port.x() + x_offset, port.y() + y_offset))

        expected_rectangle.update_ports_offset(x_offset, y_offset)

        for i in range(len(expected_coordinates)):
            port = expected_rectangle.ports[i]
            assert expected_coordinates[i] == (port.x(), port.y())

    def test_get_bound_coordinates(self):
        expected_rectangle = MoveableRectangle(100, 100, 100, 50)

        expected_left = expected_rectangle.left()
        expected_top = expected_rectangle.top()
        expected_right = expected_rectangle.left() + expected_rectangle.width()
        expected_bottom = expected_rectangle.top() + expected_rectangle.height()

        actual_left, actual_right, actual_top, actual_bottom = expected_rectangle.get_bound_coordinates()

        assert actual_left == expected_left
        assert actual_top == expected_top
        assert actual_right == expected_right
        assert actual_bottom == expected_bottom

    def test_add_new_port(self):
        expected_parent_id = "test"
        expected_x_coord = 25
        expected_y_coord = 25
        expected_radius = 10
        expected_color = QColor('white')

        rectangle = MoveableRectangle(100, 100, 100, 50)
        default_port_length = len(rectangle.ports)

        rectangle.add_new_port(
            expected_parent_id,
            expected_x_coord,
            expected_y_coord,
            expected_radius,
            expected_color
        )

        assert len(rectangle.ports) == default_port_length + 1

        actual_port = rectangle.ports[-1]

        assert actual_port.id.startswith(expected_parent_id)
        assert actual_port.x() == expected_x_coord
        assert actual_port.y() == expected_y_coord
        assert actual_port.radius == expected_radius
        assert actual_port.color == expected_color
