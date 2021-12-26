from collections import namedtuple, deque
from functools import lru_cache
from itertools import cycle
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

    @property
    @lru_cache(maxsize=1)
    def get_distance(self) -> float:
        return math.dist(self.start_point, self.end_point)

    def flip(self):
        return Edge(self.end_point, self.start_point)

    def __eq__(self, other) -> bool:
        return set(self) == set(other)

    def __str__(self) -> str:
        return f"{self.start_point}-{self.end_point}"

    def get_connecting_point(self, other) -> Point:
        return set(self) & set(other)

    def is_connecting_to(self, other):
        return len(self.get_connecting_point(other)) == 1


class Path:
    def __init__(self, edges):
        try:
            iter(edges)
        except TypeError:
            raise TypeError("edges argument must be an iterable") from None

        self._edges = deque(edges[:1])
        input_edges = edges[:]
        edge_iter = cycle(input_edges)
        modified = True
        while modified:
            modified = False
            try:
                edge = next(edge_iter)
            except StopIteration:
                break
            if edge.is_connecting_to(self._edges[0]) or edge.is_connecting_to(self._edges[-1]):
                if edge.is_connecting_to(self._edges[0]):
                    self._edges.appendleft(edge)
                else:
                    self._edges.append(edge)
                input_edges.remove(edge)
                edge_iter = cycle(input_edges)
                modified = True

        if not input_edges.empty():
            raise ValueError("The edges arent a path")

    def get_distance(self) -> float:
        return sum(e.get_distance() for e in self._edges)

    def __iadd__(self, other):
        self._edges.extend(other._edges)
        return self
