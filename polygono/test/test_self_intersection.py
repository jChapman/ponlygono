from polygono.polygon import Polygon, Point


def test_non_intersecting():
    p = Polygon([Point(0, 0), Point(0, 10), Point(10, 10), Point(10, 0)])
    assert not p.is_self_intersecting()


def test_intersecting():
    p = Polygon([Point(0, 0), Point(10, 0), Point(5, -10), Point(5, 10)])
    assert p.is_self_intersecting()
