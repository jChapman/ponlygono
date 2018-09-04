from typing import List, Iterator
from dataclasses import dataclass
from itertools import combinations
import math


@dataclass(frozen=True)
class Point:
    x: float
    y: float

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
    
    def unpack(self):
        return self.x, self.y

    def rotate_about(self, about: 'Point', degrees: float) -> 'Point':
        sin_comp = math.sin(math.radians(degrees))
        cos_comp = math.cos(math.radians(degrees))
        x_diff = self.x - about.x
        y_diff = self.y - about.y
        new_x = about.x + cos_comp * x_diff - sin_comp * y_diff
        new_y = about.y + sin_comp * x_diff + cos_comp * y_diff

        return Point(new_x, new_y)


@dataclass
class Line:
    p: Point
    slope: float

    __epsilon = 0.00001

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
    
    def create_line_segment_of_length(self, length: float, point: Point = None) -> 'LineSeg':
        if point is None:
            point = self.p
        if not self.point_is_on(point):
            raise ValueError('Point must be on the line!')

        half_distance = length/2

        if math.isinf(self.slope):
            return LineSeg(Point(point.x, point.y + half_distance), Point(point.x, point.y-half_distance))
        
        x_part = half_distance / math.sqrt(1 + self.slope*self.slope)
        x1 = point.x - x_part
        x2 = point.x + x_part
        return LineSeg(Point(x1, self.slope*x1 + self.y_intercept), Point(x2, self.slope*x2 + self.y_intercept))
    
    def create_line_perpendicular(self, point: Point) -> 'Line':
        if self.point_is_on(point):
            return None
        if math.isinf(self.slope):
            slope = 0
        elif abs(self.slope) < self.__epsilon:
            slope = math.inf
        else:
            slope = -1/self.slope

        return Line(point, slope)


@dataclass
class LineSeg:
    p1: Point
    p2: Point

    # https://stackoverflow.com/a/39592579
    def intersection_point(self, other: 'LineSeg') -> Point:
        denom = (other.p2.y - other.p1.y) * (self.p2.x - self.p1.x) - (other.p2.x - other.p1.x) * (self.p2.y - self.p1.y)
        if denom == 0:
            return None

        n_a = (other.p2.x - other.p1.x) * (self.p1.y - other.p1.y) - (other.p2.y - other.p1.y) * (self.p1.x - other.p1.x)
        n_b = (self.p2.x - self.p1.x) * (self.p1.y - other.p1.y) - (self.p2.y - self.p1.y) * (self.p1.x - other.p1.x)
        ua = n_a / denom
        ub = n_b / denom

        if 0.0 <= ua <= 1.0 and 0.0 <= ub <= 1.0:
            return Point(self.p1.x + (ua * (self.p2.x - self.p1.x)), self.p1.y + (ua * (self.p2.y - self.p1.y)))
        return None

    def intersects(self, other: 'LineSeg') -> bool:
        if self == other:
            return True
        intersection = self.intersection_point(other)
        if intersection is None:
            return False
        # If they share a point and intersect at that point then everything's cool
        if intersection in [self.p1, self.p2] and intersection in [other.p1, other.p2]:
            return False
        return True

    def point_along(self, percent_along: float) -> Point:
        if percent_along < 0 or percent_along > 1:
            raise ValueError('Invalid percent_along (must be between 0 and 1 inclusive)')
        
        x_total = (self.p2.x - self.p1.x) * percent_along 
        y_total = (self.p2.y - self.p1.y) * percent_along 

        return Point(self.p1.x + x_total, self.p1.y + y_total)
    
    def step_along(self, distance: float) -> Point:
        length = self.length
        if distance > length:
            return None
        elif distance == length:
            return self.p2
        t = distance / length
        x = (1-t) * self.p1.x + t * self.p2.x
        y = (1-t) * self.p1.y + t * self.p2.y
        return Point(x, y)
        
    @property
    def length(self) -> float:
        return self.p1.distance_to(self.p2)


@dataclass
class Circle:
    point: Point
    radius: float

    def intersects(self, other: 'Circle'):
        return self.point.distance_to(other.point) <= self.radius + other.radius


class Polygon:
    verts: List[Point]

    def __init__(self, points: List[Point]) -> None:
        if len(points) < 3 or len(points) != len(set(points)):
            raise ValueError('Invalid points! Polygon will close the polygon for you (no need to repeat first point as last')

        self.verts = points

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
                # print('Intersection found between {} and {}'.format(line, other_line))
                return True

        return False

    # https://wrf.ecse.rpi.edu//Research/Short_Notes/pnpoly.html
    def point_inside(self, point: Point) -> bool:
        num_verts = len(self.verts)
        i = 0
        j = num_verts - 1
        contains = False
        while i < num_verts:
            if (self.verts[i].y > point.y) != (self.verts[j].y > point.y) and (point.x  < (self.verts[j].x - self.verts[i].x) * (point.y - self.verts[i].y) / (self.verts[j].y - self.verts[i].y) + self.verts[i].x):
                contains = not contains
            j = i
            i += 1

        return contains


class Rect(Polygon): 

    def __init__(self, upper_left: Point, lower_right: Point=None, width: float=None, height: float=None):
        if upper_left and lower_right and (width or height):
            raise ValueError('Too many params! Either pass two points or a single point with width and height')
        if upper_left and lower_right:
            super().__init__([upper_left, Point(upper_left.x, lower_right.y), lower_right, Point(lower_right.x, upper_left.y)])
            self.width = abs(upper_left.x - lower_right.x)
            self.height = abs(upper_left.y - lower_right.y)
        elif width and height:
            super().__init__([upper_left, Point(upper_left.x, upper_left.y+height), Point(upper_left.x+width, upper_left.y+height), Point(upper_left.x+width, upper_left.y)])
            self.width = width
            self.height = height

    @property
    def upper_left(self):
        return self.verts[0]

