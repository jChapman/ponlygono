from polygono.polygon import Point
import math


def test_rotation_about_origin():
    origin = Point(0, 0)
    point = Point(1, 1)

    assert point.rotate_about(origin, 90) == Point(-1, 1)
    assert point.rotate_about(origin, 45) == Point(0, math.sqrt(2))
    assert point.rotate_about(origin, 180) == Point(-1, -1)


def test_rotation_about_simple():
    about = Point(1, 1)
    point = Point(1, 2)

    assert point.rotate_about(about, 90) == Point(0, 1)
    assert point.rotate_about(about, 180) == Point(1, 0)
