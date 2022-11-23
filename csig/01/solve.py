#!/usr/bin/env python3

from itertools import product

# Task. Given number of rows, cols, and a list of black points, count how many 2x2 subgrids have 0, 1, 2, 3, or 4 black points, as an array of size 5.

def addv(a, b):
    return tuple(x + y for x, y in zip(a, b))


def is_valid(base, rows, cols):
    min_point = base
    max_point = addv(base, (1, 1))
    return min_point[0] >= 0 and min_point[1] >= 0 and max_point[0] < rows and max_point[1] < cols


def solution(rows : int, cols : int, blacks_ : list[tuple[int, int]]):
    pos_diffs = list(product((0, +1), repeat=2))
    neg_diffs = list(product((-1, 0), repeat=2))

    # use a hash-set for easy look-up
    blacks = set(blacks_)

    result = [0] * 5

    visited = set()

    for point in blacks:
        for neg_diff in neg_diffs:
            # base point of a square that contains the black point
            base = addv(point, neg_diff)
            if base not in visited and is_valid(base, rows, cols):
                visited.add(base)
                count = 0
                for pos_diff in pos_diffs:
                    if addv(base, pos_diff) in blacks:
                        count += 1
                assert count
                result[count] += 1

    # now counting white squares is tricky
    total = (rows - 1) * (cols - 1)
    result[0] = total - sum(result)

    return result


import pytest

@pytest.mark.parametrize("expected, args", [
    ([1, 0, 0, 0, 0], (2, 2, [])),
    ([0, 1, 0, 0, 0], (2, 2, [(0, 0)])),
    ([0, 0, 1, 0, 0], (2, 2, [(0, 0), (1, 1)])),
    ([1, 2, 0, 1, 0], (3, 3, [(0, 0), (1, 0), (0, 1)])),
    ([6, 2, 0, 1, 0], (4, 4, [(0, 0), (1, 0), (0, 1)])),
    ([99 * 99, 0, 0, 0, 0], (100, 100, [])),
])
def test_main(expected, args):
    assert expected == solution(*args)
