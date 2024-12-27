from PyQt6.QtGui import QColor

from src.components.Link import Link
from src.models.GameModel import GameModel


class TestGameModel:
    def test_attributes(self):
        model = GameModel()
        assert model is not None

        expected_attributes = {
            "window_x": 200,
            "window_y": 200,
            "field_width": 1024,
            "field_height": 768,
            "min_field_width": 200,
            "min_field_height": 200,
            "is_dragging_link": False,
            "rectangles": [],
            "links": [],
            "linked_port_ids": [],
            "selected_rectangle": None,
            "selected_port": None,
            "hovered_port": None,
            "selected_link": None,
            "x1": 0,
            "x2": 0,
            "y1": 0,
            "y2": 0
        }

        actual_attributes = vars(model)

        for attribute in actual_attributes:
            assert attribute in expected_attributes

        for attribute in actual_attributes:
            assert actual_attributes[attribute] == expected_attributes[attribute]

    def test_try_add_new_rectangle(self):
        model = GameModel()

        x1 = 10
        y1 = 10

        is_added1 = model.try_add_new_rectangle(x1, y1)

        assert is_added1

        is_added2 = model.try_add_new_rectangle(x1, y1)

        assert not is_added2

    def test_find_selected_rectangle(self):
        model = GameModel()

        x1 = 10
        y1 = 10

        is_added1 = model.try_add_new_rectangle(x1, y1)
        assert is_added1

        added_rectangle = model.rectangles[0]

        actual_rectangle = model.find_selected_rectangle(x1, y1)

        assert actual_rectangle and actual_rectangle == added_rectangle

    def test_find_selected_port(self):
        model = GameModel()

        x1 = 10
        y1 = 10

        is_added1 = model.try_add_new_rectangle(x1, y1)
        assert is_added1

        expected_port = model.rectangles[0].ports[0]
        expected_x, expected_y = expected_port.x(), expected_port.y()

        assert model.find_selected_port(x1, y1, True) is None

        model.selected_rectangle = model.rectangles[0]
        assert model.find_selected_port(expected_x, expected_y, False) is expected_port

    def test_find_selected_link(self):
        model = GameModel()

        x1 = 10
        y1 = 10

        x2 = 500
        y2 = 500

        is_added1 = model.try_add_new_rectangle(x1, y1)
        is_added2 = model.try_add_new_rectangle(x2, y2)
        assert is_added1 and is_added2

        port1 = model.rectangles[0].ports[0]
        port2 = model.rectangles[1].ports[0]
        expected_link = Link.from_ports(port1, port2, 4, QColor('white'))
        expected_x, expected_y = expected_link.center().x(), expected_link.center().y()
        model.links.append(expected_link)

        assert model.find_selected_link(expected_x, expected_y) is expected_link
        assert model.find_selected_link(1000, 1000) is None

    def test_update_links_offset(self):
        model = GameModel()

        x1 = 10
        y1 = 10

        x2 = 500
        y2 = 500

        is_added1 = model.try_add_new_rectangle(x1, y1)
        is_added2 = model.try_add_new_rectangle(x2, y2)
        assert is_added1 and is_added2

        x_offset = 15
        y_offset = 10

        port1 = model.rectangles[0].ports[0]
        port2 = model.rectangles[1].ports[0]
        expected_link = Link.from_ports(port1, port2, 4, QColor('white'))
        model.links.append(expected_link)

        model.selected_rectangle = model.rectangles[0]
        expected_x1, expected_y1, expected_x2, expected_y2 = (
            expected_link.x1() + x_offset,
            expected_link.y1() + y_offset,
            expected_link.x2(),
            expected_link.y2()
        )

        model.update_links_offset(x_offset, y_offset)

        actual_x1, actual_y1, actual_x2, actual_y2 = (
            expected_link.x1(),
            expected_link.y1(),
            expected_link.x2(),
            expected_link.y2()
        )

        assert expected_x1 == actual_x1
        assert expected_y1 == actual_y1
        assert expected_x2 == actual_x2
        assert expected_y2 == actual_y2

    def test_recalculate_min_field_size(self):
        model = GameModel()

        x1 = 500
        y1 = 500

        is_added1 = model.try_add_new_rectangle(x1, y1)

        expected_min_width, expected_min_height =\
            is_added1.left() + is_added1.width(), is_added1.top() + is_added1.height()

        actual_min_width, actual_min_height = model.recalculate_min_field_size()

        assert actual_min_width == expected_min_width
        assert actual_min_height == expected_min_height
