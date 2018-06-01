import pytest
from polygono.polygon import LineSeg, Point


def test_create_line():
    line = LineSeg(Point(0, 0), Point(0, 10))
    assert line.p1 == Point(0, 0)
    assert line.p2 == Point(0, 10)


def test_line_intersects_self():
    line = LineSeg(Point(0, 0), Point(0, 10))
    l2 = LineSeg(Point(0, 0), Point(0, 10))
    assert line.intersects(l2)


def test_lines_sharing_point_does_not_intersect():
    p1 = Point(0, 0)
    line = LineSeg(p1, Point(0, 10))
    l2 = LineSeg(p1, Point(10, 0))
    assert not line.intersects(l2)


def test_lines_intersect_at_a_point():
    line = LineSeg(Point(0, 0), Point(0, 10))
    l2 = LineSeg(Point(0, 5), Point(5, 5))
    assert line.intersects(l2)


def test_point_along_zero_is_p1():
    p1 = Point(0, 0)
    p2 = Point(0, 10)
    line = LineSeg(p1, p2)
    assert p1 == line.point_along(0)


def test_point_along_one_is_p2():
    p1 = Point(0, 0)
    p2 = Point(0, 10)
    line = LineSeg(p1, p2)
    assert p2 == line.point_along(1)


def test_point_along_raises_on_gt_one():
    line = LineSeg(Point(0, 0), Point(0, 10))
    with pytest.raises(ValueError):
        line.point_along(1.1)


def test_point_along_raises_on_lt_zero():
    line = LineSeg(Point(0, 0), Point(0, 10))
    with pytest.raises(ValueError):
        line.point_along(-.1)


def test_half_along_is_half_x_axis():
    line = LineSeg(Point(0, 0), Point(0, 10))
    assert Point(0, 5) == line.point_along(.5)

    line = LineSeg(Point(0, 1), Point(0, 11))
    assert Point(0, 6) == line.point_along(.5)


def test_half_along_is_half_y_axis():
    line = LineSeg(Point(0, 0), Point(100, 0))
    assert Point(50, 0) == line.point_along(.5)

    line = LineSeg(Point(25, 0), Point(75, 0))
    assert Point(50, 0) == line.point_along(.5)


def test_line_length_hor():
    line = LineSeg(Point(0, 0), Point(100, 0))
    assert line.length == 100


def test_line_length_vert():
    line = LineSeg(Point(0, 0), Point(0, 50))
    assert line.length == 50


def test_step_too_far_is_none():
    line = LineSeg(Point(0, 0), Point(0, 50))
    assert line.step_along(51) is None


def test_step_for_dist_is_second_point():
    p2 = Point(0, 50)
    line = LineSeg(Point(0, 0), p2)
    assert line.step_along(line.length) is p2


def test_step_along():
    line = LineSeg(Point(0, 0), Point(0, 50))
    assert line.step_along(10) == Point(0, 10)
