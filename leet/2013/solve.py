#!/usr/bin/env python3

from collections import defaultdict
from typing import List

class DetectSquares:

    def __init__(self):
        self.pos_diags : dict[int, set[tuple[int, int]]] = defaultdict(set)
        self.neg_diags : dict[int, set[tuple[int, int]]] = defaultdict(set)
        self.points : dict[tuple[int, int], int] = defaultdict(int)

    def add(self, point: List[int]) -> None:
        x, y = point
        self.pos_diags[y - x].add(tuple(point))
        self.neg_diags[y + x].add(tuple(point))
        self.points[tuple(point)] += 1

    def count(self, point: List[int]) -> int:
        total = 0
        x, y = point
        for diag in (self.pos_diags[y - x], self.neg_diags[y + x]):
            for diag_point in diag:
                if diag_point != tuple(point):
                    if (diag_point[0], point[1]) in self.points and (point[0], diag_point[1]) in self.points:
                        total += self.points[diag_point] * self.points[diag_point[0], point[1]] * self.points[point[0], diag_point[1]]
        return total
