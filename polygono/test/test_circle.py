from polygono.polygon import Circle, Point
import math

def test_simple_creation():
    circle = Circle(Point(0, 0), 1)

def test_self_intersecting():
    circle = Circle(Point(0, 0), 1)
    assert circle.intersects(circle)

def test_simple_intersection():
    # Point of one is within the radius of another
    c1 = Circle(Point(0, 0), 2)
    c2 = Circle(Point(1, 0), 1)
    assert c1.intersects(c2)

def test_simple_intersection2():
    c1 = Circle(Point(0, 0), 2)
    c2 = Circle(Point(3, 0), 2)
    assert c1.intersects(c2)

def test_touching_intersection():
    c1 = Circle(Point(0, 0), 1)
    c2 = Circle(Point(2, 0), 1)
    assert c1.intersects(c2)
