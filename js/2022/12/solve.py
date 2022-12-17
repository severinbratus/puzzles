#!/usr/bin/env python3

from typing import NamedTuple
from itertools import product


grid = [
    [57, 33, 132, 268, 492, 732],
    [81, 123, 240, 443, 353, 508],
    [186, 42, 195, 704, 452, 228],
    [-7, 2, 357, 452, 317, 395],
    [5, 23, -4, 592, 445, 620],
    [0, 77, 32, 403, 337, 452],
]


class Node(NamedTuple):

    path : list[tuple[int, int]] = [(5, 0)]
    values : list[int | None] = [None] * 6
    score : int = 0
    move : int = 1


def reorder(seq : list, order : list[int]):
    # return [seq[i] for i in order]
    n = len(seq)
    res = [None] * n
    for was, willb in enumerate(order):
        res[willb] = seq[was]
    return res


stack : list[Node] = list()

init = Node([(5, 0)])
term_f = lambda node: node.path[-1] == (0, 5)


class Direction(NamedTuple):

    order : list[int]
    vector : tuple[int, int]


north = Direction([1, 3, 2, 4, 0, 5], (-1, 0))
south = Direction([4, 0, 2, 1, 3, 5], (1, 0))
east = Direction([2, 1, 3, 5, 4, 0], (0, 1))
west = Direction([5, 1, 0, 2, 4, 3], (0, -1))

directions = [north, south, east, west]


# The die starts with a “score” of 0.
# On the Nth move, its score increases by N times the value of the die facing up after the move.
# However, the die is only allowed to move into a square if its score after the move matches the value in the square.
# Also, the die cannot be translated or rotated in place in addition to these moves.


def addv(a, b):
    return tuple(x + y for x, y in zip(a, b))


def inrange(a, b):
    return all(0 <= x < y for x, y in zip(a, b))


def loc(d, p):
    return d[p[0]][p[1]]


def adj(u):
    # the cube is u.path[-1]
    # and the values are in u.values.
    # so try out the four dir-s,
    # see if we can move the cube there.
    # if we can't, ignore.
    # if we can, make a node with values reordered,
    # with the new value inferred.
    # the face up is in u.values[0]
    for direction in directions:
        point = addv(direction.vector, u.path[-1])
        if inrange(point, (6, 6)):
            expected_score = loc(grid, point)
            values = reorder(u.values, direction.order)
            path = u.path + [point]
            # if the value is already assigned
            if values[0] is not None:
                actual_score = u.score + u.move * values[0]
                if actual_score == expected_score:
                    yield Node(path, values, expected_score, u.move + 1)
            # value unassigned
            else:
                # assign a value to the top
                if (expected_score - u.score) % u.move == 0:
                    values[0] = (expected_score - u.score) // u.move
                    yield Node(path, values, expected_score, u.move + 1)


def solve():
    stack = [init]
    while stack:
        u = stack.pop()
        for v in adj(u):
            if term_f(v):
                return v
            stack.append(v)

v = solve()
print(v)

for pt in product(range(6), repeat=2):
    if pt[1] == 0: print()
    c = '-' if pt not in v.path else '.'
    print(c, end='')
# print(list(adj(init)))
