from typing import List, Tuple, Iterator
from dataclasses import dataclass
from itertools import combinations
import math

@dataclass
class Point:
    x: int
    y: int

    __epsilon = 0.00001

    def __eq__(self, other: 'Point') -> bool:
        if other is None:
            return False
        x_diff = self.x - other.x
        y_diff = self.y - other.y
        x_diff *= x_diff
        y_diff *= y_diff

        return x_diff < self.__epsilon and y_diff < self.__epsilon

    def __neq__(self, other: 'Point') -> bool:
        return not self.__eq__(other)
    
    def distance_to(self, other: 'Point') -> float:
        x_diff = self.x - other.x
        y_diff = self.y - other.y
        return math.sqrt(x_diff*x_diff + y_diff*y_diff)

@dataclass
class Line:
    p: Point
    slope: float

    @property
    def y_intercept(self) -> float:
        if self.slope == math.inf or self.slope == -math.inf:
            if self.p.x == 0:
                return math.inf
            return None
        return self.p.y - self.slope * self.p.x

@dataclass
class LineSeg:
    p1: Point
    p2: Point

    # https://stackoverflow.com/a/39592579
    def intersects(self, other: 'LineSeg') -> bool:
        if self == other:
            return True

        denom = (other.p2.y - other.p1.y) * (self.p2.x - self.p1.x) - (other.p2.x - other.p1.x) * (self.p2.y - self.p1.y)
        if denom == 0:
            return False

        n_a = (other.p2.x - other.p1.x) * (self.p1.y - other.p1.y) - (other.p2.y - other.p1.y) * (self.p1.x - other.p1.x)
        n_b = (self.p2.x - self.p1.x) * (self.p1.y - other.p1.y) - (self.p2.y - self.p1.y) * (self.p1.x - other.p1.x)
        ua = n_a / denom
        ub = n_b / denom

        if ua >= 0.0 and ua <= 1.0 and ub >= 0.0 and ub <= 1.0:
            intersection = Point(self.p1.x + (ua * (self.p2.x - self.p1.x)), self.p1.y + (ua * (self.p2.y - self.p1.y)))
            # If they share a point and intersect at that point then everything's cool
            if intersection in [self.p1, self.p2] and intersection in [other.p1, other.p2]:
                return False
            return True
        return False
    
    def point_along(self, percent_along: float) -> Point:
        if percent_along < 0 or percent_along > 1:
            raise ValueError('Invalid percent_along (must be between 0 and 1 inclusive)')
        
        x_total = (self.p2.x - self.p1.x) * percent_along 
        y_total = (self.p2.y - self.p1.y) * percent_along 

        return Point(self.p1.x + x_total, self.p1.y + y_total)

    def length(self) -> float:
        return self.p1.distance_to(self.p2)

class Polygon:
    verts: List[Point]

    def __init__(self, points:List[Tuple[int, int]]) -> None:
        if len(points) < 3 or len(points) != len(set(points)):
            raise ValueError('Invalid points! Polygon will close the polygon for you (no need to repeat first point as last')

        self.verts = [Point(p[0], p[1]) for p in points]

    def outline(self) -> Iterator[LineSeg]:
        itr = iter(self.verts)
        first = prev = item = next(itr)
        for item in itr:
            yield LineSeg(prev, item)
            prev = item
        yield LineSeg(item, first)

    def is_self_intersecting(self) -> bool:
        for line, other_line in combinations(self.outline(), 2):
            if line.intersects(other_line):
                #print('Intersection found between {} and {}'.format(line, other_line))
                return True

        return False

    # https://wrf.ecse.rpi.edu//Research/Short_Notes/pnpoly.html
    def point_inside(self, point: Tuple[int, int]) -> bool:
        x, y = point
        num_verts = len(self.verts)
        i = 0
        j = num_verts - 1
        contains = False
        while i < num_verts:
            if (self.verts[i].y > y) != (self.verts[j].y > y) and (x  < (self.verts[j].x - self.verts[i].x) * (y - self.verts[i].y) / (self.verts[j].y - self.verts[i].y) + self.verts[i].x):
                contains = not contains
            j = i
            i += 1

        return contains


