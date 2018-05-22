from typing import List, Tuple, Iterator
from dataclasses import dataclass

@dataclass
class Point: 
    x: int
    y: int

@dataclass
class Line: 
    first_point: Point
    second_point: Point

class Polygon: 
    verts: List[Point]

    def __init__(self, points:List[Tuple[int, int]]) -> None:
        if len(points) < 3 or len(points) != len(set(points)):
            raise ValueError('Invalid points!')
        
        self.verts = [Point(p[0], p[1]) for p in points]
    
    def outline(self) -> Iterator[Line]:
        itr = iter(self.verts)
        first = prev = item = next(itr)
        for item in itr:
            yield Line(prev, item)
            prev = item
        yield Line(item, first)
    
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

    