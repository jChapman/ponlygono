from polygono.polygon import Line, Point
import math
import pytest

def test_creation():
    assert Line(Point(0,0), 1)
    assert Line(Point(0,0), 0)
    assert Line(Point(0,0), -1)
    assert Line(Point(0,0), math.inf)

def test_simple_y_intercept():
    assert Line(Point(0, 0), 1).y_intercept is 0

def test_y_intercept():
    assert Line(Point(2, 2), 1).y_intercept is 0
    assert Line(Point(2, 1), 1).y_intercept is -1

def test_y_intercept_vertical():
    assert Line(Point(1, 0), math.inf).y_intercept == None
    assert Line(Point(0, 0), math.inf).y_intercept == math.inf

def test_y_intercept_horr():
    assert Line(Point(1, 0), 0).y_intercept == 0
    assert Line(Point(0, 10), 0).y_intercept == 10

def test_point_is_on_same_as_point_created():
    assert Line(Point(0,0), 1).point_is_on(Point(0,0))
    assert Line(Point(3,100), 0).point_is_on(Point(3, 100))
    assert Line(Point(1,30), math.inf).point_is_on(Point(1, 30))

def test_point_is_on_true():
    assert Line(Point(0,0), 1).point_is_on(Point(1,1))
    assert Line(Point(3,100), 0).point_is_on(Point(0, 100))
    assert Line(Point(1,30), math.inf).point_is_on(Point(1, 300))

def test_point_is_not_on():
    assert not Line(Point(0,0), 1).point_is_on(Point(1,2))
    assert not Line(Point(3,100), 0).point_is_on(Point(0, 0))
    assert not Line(Point(1,30), math.inf).point_is_on(Point(2, 0))

def test_not_parallel_simple():
    assert Line(Point(0,0), 1).is_parallel_to(Line(Point(0,0), 2)) is False

def test_same_line_is_parallel():
    l = Line(Point(0,0), 1)
    l2 = Line(Point(1,100), 0)
    l3 = Line(Point(2,-23), math.inf)
    assert l.is_parallel_to(l)
    assert l2.is_parallel_to(l2)
    assert l3.is_parallel_to(l3)

def test_parallel_lines_are_parallel():
    l = Line(Point(0,0), 1)
    l2 = Line(Point(1,100), 1)
    assert l.is_parallel_to(l2)

    l.slope = math.inf
    l2.slope = math.inf
    assert l.is_parallel_to(l2)

    l.slope = 0
    l2.slope = 0
    assert l.is_parallel_to(l2)

def test_simple_intersection():
    assert Line(Point(0,0), 1).intersection_point(Line(Point(0,0), 2)) == Point(0,0)

def test_no_intersection():
    l = Line(Point(0,0), 1)
    assert l.intersection_point(Line(Point(1,100), 1)) is None
    # Not sure about the behavior of the following case...
    assert l.intersection_point(l) is None

def test_parallel_creation_has_same_slope():
    slope = 100
    l = Line(Point(0,0), slope)
    assert l.create_parallel_line(Point(100, 9)).slope == slope

def test_create_line_seg():
    l = Line(Point(0,0), 3/4)
    length = 10
    seg = l.create_line_segment_of_length(length)
    assert seg.length == length
    points = (Point(4, 3), Point(-4, -3))
    assert seg.p1 in points
    assert seg.p2 in points

def test_create_line_seg_vert_horr():
    l = Line(Point(0,0), 0)
    length = 10
    seg = l.create_line_segment_of_length(length)
    assert seg.length == length
    points = (Point(5, 0), Point(-5, 0))
    assert seg.p1 in points
    assert seg.p2 in points

    l.slope = math.inf
    length = 10
    seg = l.create_line_segment_of_length(length)
    assert seg.length == length
    points = (Point(0, 5), Point(0, -5))
    assert seg.p1 in points
    assert seg.p2 in points

def test_cant_make_perpendicular_if_co_linear():
    l = Line(Point(0,0), 0)
    assert l.create_line_perpendicular(Point(10, 0)) is None

def test_make_perpendicular():
    l = Line(Point(0,0), 0)
    perp_point = Point(0, 10)
    perp = l.create_line_perpendicular(perp_point)
    assert perp.slope == math.inf
    assert perp.p == perp_point

    l.slope = math.inf
    perp_point = Point(10, 0)
    perp = l.create_line_perpendicular(perp_point)
    assert perp.slope == 0
    assert perp.p == perp_point

    l.slope = 1
    perp_point = Point(-10, 10)
    perp = l.create_line_perpendicular(perp_point)
    assert perp.slope == -1
    assert perp.p == perp_point