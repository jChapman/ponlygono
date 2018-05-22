import pytest
from polygono.polygon import Polygon

def test_non_inersecting():
    p = Polygon([(0, 0), (0, 10), (10, 10), (10, 0)])
    assert p.is_self_intersecting() == False

def test_intersecting():
    p = Polygon([(0, 0), (10, 0), (5, -10), (5, 10)])
    assert p.is_self_intersecting() == True