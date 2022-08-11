#!/usr/bin/env python3

from functools import cache

@cache
def p(cell = (0, 0), n = 20, returning = True):
    '''Return the probability that Andy reaches the home cell (0, 0), in no more than n steps,
    starting on the given cell and walking uniform-randomly.
    '''
    if n < 0:
        # Impossible.
        return 0
    if n == 0:
        # Probability that Andy reaches home in 0 steps is either 0 or 1,
        # depending on whether Andy is already home.
        return int(cell == (0, 0) and returning)
    if cell == (0, 0) and returning:
        # Andy has already reached home.
        return 1

    return (1/3) * sum(p(adj_cell, n - 1) for adj_cell in adj(cell))

possible_diffs = [[(0, 1), (0, -1), (1, 1)],
                  [(0, 1), (0, -1), (-1, -1)]]

def sumv(a, b):
    return tuple(x + y for x, y in zip(a, b))

def adj(cell):
    return list(sumv(diffs, cell) for diffs in possible_diffs[cell[1] % 2])

for i in range(1, 21):
    _ = p(n = i, returning = False)
    print(i, round(_, 7), round(1 - _, 7))
