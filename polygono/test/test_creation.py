import pytest
from polygono.polygon import Polygon, Point


def test_empty_points():
    with pytest.raises(ValueError):
        Polygon(())


def test_less_than_three_points():
    with pytest.raises(ValueError):
        Polygon([Point(0, 0), Point(1, 0)])


def test_three_unique_points():
    Polygon([Point(0, 0), Point(0, 1), Point(1, 0)])


def test_non_unique_point():
    with pytest.raises(ValueError):
        Polygon([Point(0, 0), Point(0, 1), Point(0, 0)])


def test_float_points():
    # Should this fail? Not checking right now
    Polygon([Point(0.001, 0), Point(0, 1.1), Point(0, 0)])


