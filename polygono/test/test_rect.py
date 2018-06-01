import pytest
from polygono.polygon import Rect, Point


def test_create_fails_with_too_many_params():
    with pytest.raises(ValueError):
        Rect(Point(0, 0), Point(1, 1), 10)


def test_create_with_two_points():
    assert Rect(Point(0, 0), Point(10, 10))


def test_create_with_point_and_wh():
    assert Rect(Point(0, 0), width=10, height=10)


def test_create_square():
    r = Rect(Point(0, 0), width=10, height=10)
    for p in [Point(0, 0), Point(0, 10), Point(10, 10), Point(10, 0)]:
        assert p in r.verts
    r = Rect(Point(0, 0), Point(10, 10))
    for p in [Point(0, 0), Point(0, 10), Point(10, 10), Point(10, 0)]:
        assert p in r.verts
