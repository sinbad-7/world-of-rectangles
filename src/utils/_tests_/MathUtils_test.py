from src.components.MoveableRectangle import MoveableRectangle
from src.utils import MathUtils


class TestMathUtils:
    def test_is_point_in_circle_(self):
        x_center = 10
        y_center = 10

        x1 = 3
        y1 = 3
        assert MathUtils.is_point_in_circle(x_center, y_center, x1, y1) is True

        x2 = 10
        y2 = 10
        assert MathUtils.is_point_in_circle(x_center, y_center, x2, y2) is True

        x3 = 10
        y3 = 20
        assert MathUtils.is_point_in_circle(x_center, y_center, x3, y3) is True

        x4 = 100
        y4 = 100
        assert MathUtils.is_point_in_circle(x_center, y_center, x4, y4) is False

    def test_has_border_collision(self):
        screen_width = 1000
        screen_height = 1000

        left1 = -1
        top1 = -1
        right1 = 100
        bottom1 = 50
        assert MathUtils.has_border_collision(left1, top1, right1, bottom1, screen_width, screen_height) is True

        left2 = 20
        top2 = 20
        right2 = 120
        bottom2 = 70
        assert MathUtils.has_border_collision(left2, top2, right2, bottom2, screen_width, screen_height) is False

        left3 = 0
        top3 = 0
        right3 = 100
        bottom3 = 50
        x_offset = -1
        y_offset = -1
        assert MathUtils.has_border_collision(
            left3, top3, right3, bottom3, screen_width, screen_height, x_offset, y_offset) is True

    def test_has_rectangle_overlap(self):
        left1 = 0
        top1 = 0
        right1 = 100
        bottom1 = 50

        left2 = 100
        top2 = 0
        right2 = 200
        bottom2 = 100

        left3 = 200
        top3 = 200
        right3 = 300
        bottom3 = 250

        x_offset = 250
        y_offset = 225

        assert MathUtils.has_rectangle_overlap(
            left1, right1, top1, bottom1, left2, right2, top2, bottom2) is False
        assert MathUtils.has_rectangle_overlap(
            left1, right1, top1, bottom1, left3, right3, top3, bottom3) is False
        assert MathUtils.has_rectangle_overlap(
            left1, right1, top1, bottom1, left3, right3, top3, bottom3, x_offset, y_offset) is True

    def test_has_collision(self):
        screen_width = 1000
        screen_height = 1000

        rectangles = [
            MoveableRectangle(50, 50, 100, 50),
            MoveableRectangle(500, 500, 100, 50)
        ]

        rectangle1 = MoveableRectangle(50, 50, 100, 50)
        rectangle2 = MoveableRectangle(55, 55, 100, 50)

        x_offset = -100
        y_offset = -100

        assert MathUtils.has_collision(rectangle1, rectangles, screen_width, screen_height) is False
        assert MathUtils.has_collision(rectangle2, rectangles, screen_width, screen_height) is True
        assert MathUtils.has_collision(rectangle1, rectangles, screen_width, screen_height, x_offset, y_offset) is True
