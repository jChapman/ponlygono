import pytest
from polygono.polygon import Polygon, Point

def test_outline():
    p = Polygon([Point(0, 0), Point(0, 1), Point(1, 0)])
    assert 3 == len(list(p.outline()))