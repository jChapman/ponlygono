from polygono.polygon import Circle, Polygon, Point, Rect


def test_point_inside():
    p = Polygon([Point(0, 0), Point(0, 10), Point(10, 10), Point(10, 0)])
    assert p.point_inside(Point(5, 5))


def test_point_outside():
    p = Polygon([Point(0, 0), Point(0, 10), Point(10, 10), Point(10, 0)])
    assert not p.point_inside(Point(-1, -1))


def test_point_on_poly():
    p = Polygon([Point(0, 0), Point(0, 10), Point(10, 10), Point(10, 0)])
    assert p.point_inside(Point(0, 0))


def test_rect_inside():
    r = Rect(Point(0, 0), width=10, height=10)
    assert r.point_inside(Point(5, 5))


def test_rect_outside():
    r = Rect(Point(0, 0), width=10, height=10)
    assert not r.point_inside(Point(-1, 0))


def test_circle_inside_at_center():
    c = Circle(Point(0, 0), 10)
    assert c.point_inside(Point(0, 0))


def test_circle_inside():
    c = Circle(Point(0, 0), 10)
    assert c.point_inside(Point(3, 4))


def test_circle_outside():
    c = Circle(Point(0, 0), 10)
    assert not c.point_inside(Point(11, 0))
