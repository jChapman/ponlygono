from polygono.polygon import Line, Point
import math

def test_creation():
    assert Line(Point(0,0), 1)
    assert Line(Point(0,0), 0)
    assert Line(Point(0,0), -1)
    assert Line(Point(0,0), math.inf)

def test_not_parallel_simple():
    assert Line(Point(0,0), 1).is_parallel_to(Line(Point(0,0), 2)) is False

#def test_simple_intersection():
    #assert Line(Point(0,0), 1).intersection_point(Line(Point(0,0), 2)) == Point(0,0)

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