#!/usr/bin/env python3

from typing import List
from collections.abc import Iterable
import pdb

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:

        turn_right = {
            (0, 1): (1, 0),
            (1, 0): (0, -1),
            (0, -1): (-1, 0),
            (-1, 0): (0, 1),
        }

        n = len(matrix)
        m = len(matrix[0])

        size = n * m
        point = (0, 0)
        vector = (0, 1)
        visited : set[tuple[int, int]] = set()
        spiral = []

        def valid(point):
            return point not in visited and in_range(point, (n, m))

        while size:
            visited.add(point)
            spiral.append(matrix[point[0]][point[1]])
            size -= 1

            # move from point by vector
            next_point = addv(point, vector)
            if not valid(next_point):
                vector = turn_right[vector]
                next_point = addv(point, vector)

            print(next_point)
            point = next_point

        return spiral


def in_range(point, bounds):
    return all(0 <= value < bound for value, bound in zip(point, bounds))


def addv(a : Iterable[int | float], b : Iterable[int | float]) -> tuple:
    return tuple(x + y for x, y in zip(a, b))


import pytest


@pytest.mark.parametrize("expected, arg", [
    (
        [1,2,3,4,8,12,11,10,9,5,6,7],
        [[1,2,3,4],[5,6,7,8],[9,10,11,12]],
    ),
    (
        [1,2,3,6,9,8,7,4,5],
        [[1,2,3],[4,5,6],[7,8,9]],
    ),
])
def test_main(expected, arg):
    assert expected == Solution().spiralOrder(arg)

# Of course, there are smarter ways to do this - without keeping a full-on hash-set of visited points.
# Since the spiral spreads in straight parallel lines, it's trajectory is predictable, though the sequence is a bit peculiar.
#   n - 1,
#   m - 1, n - 1,
#   m - 2, n - 2,
#   m - 3, n - 3,
#   m - 4, ...
