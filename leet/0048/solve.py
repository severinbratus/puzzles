from collections.abc import Iterable
from itertools import product


class Solution:
    def rotate(self, matrix: list[list[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)
        mid = n // 2
        mid_point = (mid, mid)
        sector = product(range(mid), range(mid + 1)) if n % 2 else product(range(mid), repeat=2)
        rotate_normed = rotate_normed_odd if n % 2 else rotate_normed_even
        for point in sector:
            series = [point]
            for _ in range(3):
                point_normed = subv(point, mid_point)
                point_normed_rotated = rotate_normed(point_normed)
                point_rotated = addv(point_normed_rotated, mid_point)
                series.append(point_rotated)
                point = point_rotated
            rotate_quad(matrix, series)


def rotate_quad(matrix : list[list[int]], quad : list[tuple[int, int]]) -> None:
    reading = [matrix[point[0]][point[1]] for point in quad]
    for index in range(4):
        next_point = quad[(index + 1) % 4]
        matrix[next_point[0]][next_point[1]] = reading[index]


def rotate_normed_odd(point : tuple[int, int]):
    x, y = point
    return y, -x


def rotate_normed_even(point : tuple[int, int]):
    point_nudged = addv(point, (0.5, 0.5))
    point_nudged_rotated = rotate_normed_odd(point_nudged)
    point_rotated = tuple(map(int, subv(point_nudged_rotated, (0.5, 0.5))))
    return point_rotated


def subv(a : Iterable[int | float], b : Iterable[int | float]) -> tuple:
    return tuple(x - y for x, y in zip(a, b))


def addv(a : Iterable[int | float], b : Iterable[int | float]) -> tuple:
    return tuple(x + y for x, y in zip(a, b))


import pytest


@pytest.mark.parametrize("expected, arg", [
    (
        [[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]],
        [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]],
    ),
    (
        [[7,4,1],[8,5,2],[9,6,3]],
        [[1,2,3],[4,5,6],[7,8,9]],
    ),
    (
        [[3, 1], [4, 2]],
        [[1, 2], [3, 4]],
    ),
    (
        [1],
        [1]
    ),
])
def test_main(expected, arg):
    Solution().rotate(arg)
    assert expected == arg
