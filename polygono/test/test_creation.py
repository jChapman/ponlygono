import pytest
from polygono.polygon import Polygon

def test_empty_points():
    with pytest.raises(ValueError):
        Polygon(())

def test_less_than_three_points():
    with pytest.raises(ValueError):
        Polygon([(0, 0), (1, 0)])

def test_three_unique_points():
    Polygon([(0, 0), (0, 1), (1, 0)])

def test_non_unique_point():
    with pytest.raises(ValueError):
        Polygon([(0, 0), (0, 1), (0, 0)])

def test_float_points():
    # Should this fail? Not checking right now
    #with pytest.raises(ValueError):
    Polygon([(0.001, 0), (0, 1.1), (0, 0)])


