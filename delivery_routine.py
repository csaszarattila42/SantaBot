from collections import namedtuple, deque
from functools import cached_property
import math

Point = namedtuple("Point", "x y")


class Edge:
    def __init__(self, start_point: Point, end_point: Point):
        self._start_point = start_point
        self._end_point = end_point

    @property
    def start_point(self) -> Point:
        return self._start_point

    @property
    def end_point(self) -> Point:
        return self._end_point

    # please do not consider this as a writable property, thank you!
    @cached_property
    def distance(self) -> float:
        return math.dist(self.start_point, self.end_point)

    def __iter__(self):
        return iter((self.start_point, self.end_point))

    # def flip(self):
    #    return Edge(self.end_point, self.start_point)

    def __eq__(self, other) -> bool:
        return (
            (
                self.start_point == other.start_point and
                self.end_point == other.end_point
            ) or
            (
                self.start_point == other.end_point and
                self.end_point == other.start_point
            )
        )

    def get_connecting_point(self, other) -> Point:
        if not self == other:
            for point in self:
                if point in other:
                    return point

    def is_connecting_to(self, other) -> bool:
        return self.get_connecting_point(other) is not None


class Path:
    def __init__(self, edges):
        try:
            iter(edges)
        except TypeError:
            raise TypeError("edges argument must be an iterable") from None
        self._edges = deque(edges[:1])

        is_connecting_to_path = lambda e: e.is_connecting_to(self._edges[0]) or e.is_connecting_to(self._edges[-1])
        input_edges = edges[:]
        edge = next(filter(is_connecting_to_path, input_edges), None)

        while edge is not None:
            if edge.is_connecting_to(self._edges[0]):
                self._edges.appendleft(edge)
            else:
                self._edges.append(edge)
            input_edges.remove(edge)
            edge = next(filter(is_connecting_to_path, input_edges), None)

        if not input_edges.empty():
            raise ValueError("The edges arent a path")

    @cached_property
    def get_distance(self) -> float:
        return sum(e.distance for e in self._edges)

    def __iadd__(self, other):
        self._edges.extend(other._edges)
        self.get_distance.cache_clear()
        return self

    def __add__(self, other):
        new_path = Path(self._edges)
        new_path += other
        return new_path
