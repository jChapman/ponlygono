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
        if math.isinf(self.slope):
            if self.p.x == 0:
                return math.inf
            return None
        return self.p.y - self.slope * self.p.x

    def point_is_on(self, point: Point) -> bool:
        if point == self.p: 
            return True
        x_diff = point.x - self.p.x
        if x_diff == 0:
            return math.isinf(self.slope)
        return self.slope == (point.y - self.p.y) / x_diff

    def intersection_point(self, other: 'Line') -> Point:
        if self.is_parallel_to(other):
            # TODO this will return None if they are the same line, what is the correct value to return there? 
            return None
        x = (self.y_intercept - other.y_intercept) / (self.slope - other.slope) 
        return Point(x, self.slope * x + self.y_intercept)
    
    def is_parallel_to(self, other: 'Line') -> bool:
        if math.isinf(self.slope):
            return math.isinf(other.slope)
        return other.slope == self.slope
    
    def create_parallel_line(self, point: Point) -> 'Line':
        return Line(point, self.slope)
    
    def create_line_segment_of_length(self, length:float, point:Point = None) -> 'LineSeg':
        if point is None:
            point = self.p
        if not self.point_is_on(point):
            raise ValueError('Point must be on the line!')

        half_distance = length/2

        if math.isinf(self.slope):
            return LineSeg(Point(point.x, point.y + half_distance), Point(point.x, point.y-half_distance))
        
        #x_part = math.sqrt(half_distance*half_distance * (self.slope * self.slope + 1)) 
        #x1 = (x_part + self.slope * self.slope * point.x + point.x) / (self.slope * self.slope + 1)
        #x2 = (-x_part + self.slope * self.slope * point.x + point.x) / (self.slope * self.slope + 1)
        
        x_part = half_distance / math.sqrt(1 + self.slope*self.slope)
        x1 = point.x - x_part
        x2 = point.x + x_part
        return LineSeg(Point(x1, self.slope*x1 + self.y_intercept), Point(x2, self.slope*x2 + self.y_intercept))
    
    def create_line_perpendicular(self, point:Point) -> 'Line':
        if self.point_is_on(point):
            return None
        slope = self.slope
        if math.isinf(self.slope):
            slope = 0
        elif self.slope == 0:
            slope = math.inf
        else:
            slope = -1/self.slope

        return Line(point, slope)


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


