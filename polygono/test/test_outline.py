import pytest
from polygono.polygon import Polygon

def test_outline():
    p = Polygon([(0, 0), (0, 1), (1, 0)])
    assert 3 == len(list(p.outline()))