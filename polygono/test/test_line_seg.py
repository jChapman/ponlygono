import pytest
from polygono.polygon import LineSeg, Point

def test_create_line():
    l = LineSeg(Point(0, 0), Point(0, 10))
    assert l.p1 == Point(0, 0)
    assert l.p2 == Point(0, 10)

def test_line_intersects_self():
    l = LineSeg(Point(0, 0), Point(0, 10))
    l2 = LineSeg(Point(0, 0), Point(0, 10))
    assert l.intersects(l2)

def test_lines_sharing_point_does_not_intersect():
    p1 = Point(0,0)
    l = LineSeg(p1, Point(0, 10))
    l2 = LineSeg(p1, Point(10, 0))
    assert not l.intersects(l2)

def test_lines_intersect_at_a_point():
    l = LineSeg(Point(0, 0), Point(0, 10))
    l2 = LineSeg(Point(0, 5), Point(5, 5))
    assert l.intersects(l2)

def test_point_along_zero_is_p1():
    p1 = Point(0,0)
    p2 = Point(0, 10)
    l = LineSeg(p1, p2)
    assert p1 == l.point_along(0)

def test_point_along_one_is_p2():
    p1 = Point(0,0)
    p2 = Point(0, 10)
    l = LineSeg(p1, p2)
    assert p2 == l.point_along(1)

def test_point_along_raises_on_gt_one():
    l = LineSeg(Point(0, 0), Point(0, 10))
    with pytest.raises(ValueError):
        l.point_along(1.1)

def test_point_along_raises_on_lt_zero():
    l = LineSeg(Point(0, 0), Point(0, 10))
    with pytest.raises(ValueError):
        l.point_along(-.1)

def test_half_along_is_half_x_axis():
    l = LineSeg(Point(0, 0), Point(0, 10))
    assert Point(0, 5) == l.point_along(.5)

    l = LineSeg(Point(0, 1), Point(0, 11))
    assert Point(0, 6) == l.point_along(.5)

def test_half_along_is_half_y_axis():
    l = LineSeg(Point(0, 0), Point(100, 0))
    assert Point(50, 0) == l.point_along(.5)

    l = LineSeg(Point(25, 0), Point(75, 0))
    assert Point(50, 0) == l.point_along(.5)

def test_line_length_hor():
    l = LineSeg(Point(0, 0), Point(100, 0))
    assert l.length == 100

def test_line_length_vert():
    l = LineSeg(Point(0, 0), Point(0, 50))
    assert l.length == 50

def test_step_too_far_is_none():
    l = LineSeg(Point(0, 0), Point(0, 50))
    assert l.step_along(51) is None

def test_step_for_dist_is_second_point():
    p2 = Point(0, 50)
    l = LineSeg(Point(0, 0), p2)
    assert l.step_along(l.length) is p2

def test_step_along():
    l = LineSeg(Point(0, 0), Point(0, 50))
    assert l.step_along(10) == Point(0, 10)