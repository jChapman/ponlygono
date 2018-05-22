import pytest
from polygono.polygon import Polygon

def test_point_inside():
    p = Polygon([(0, 0), (0, 10), (10, 10), (10, 0)])
    assert p.point_inside((5, 5)) == True

def test_point_outside():
    p = Polygon([(0, 0), (0, 10), (10, 10), (10, 0)])
    assert p.point_inside((-1, -1)) == False

def test_point_on_poly():
    p = Polygon([(0, 0), (0, 10), (10, 10), (10, 0)])
    assert p.point_inside((0, 0)) == True