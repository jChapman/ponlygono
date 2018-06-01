from polygono.polygon import Polygon, Point


def test_point_inside():
    p = Polygon([Point(0, 0), Point(0, 10), Point(10, 10), Point(10, 0)])
    assert p.point_inside(Point(5, 5))


def test_point_outside():
    p = Polygon([Point(0, 0), Point(0, 10), Point(10, 10), Point(10, 0)])
    assert not p.point_inside(Point(-1, -1))


def test_point_on_poly():
    p = Polygon([Point(0, 0), Point(0, 10), Point(10, 10), Point(10, 0)])
    assert p.point_inside(Point(0, 0))
