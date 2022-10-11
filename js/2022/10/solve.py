#!/usr/bin/env python3

from collections import defaultdict
from functools import reduce
from operator import mul, add

import mip

Point = tuple[int, int]

with open('data.txt') as fin:
    grid = [[int(char) if char != '.' else 0 for char in line.strip()] for line in fin.readlines()]

# print(*grid, sep='\n')

# qto dal'we?

n = len(grid)
m = len(grid[0])
size = (n, m)

diffs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def addv(a, b) -> tuple[int, ...]:
    return tuple(x + y for x, y in zip(a, b))

def subv(a, b) -> tuple[int, ...]:
    return tuple(x - y for x, y in zip(a, b))

def scale(a, k) -> tuple[int, ...]:
    return tuple(x * k for x in a)

def getv(mtx, idx):
    i, j = idx
    return mtx[i][j]

def in_range(idx, size) -> bool:
    return all(0 <= i < m for i, m in zip(idx, size))

graph : dict[Point, list[Point]] = defaultdict(list)
values : dict[Point, int] = dict()

for i in range(n):
    for j in range(m):
        # record grid values in a map
        value = getv(grid, (i, j))
        if value:
            values[i, j] = value

            # reach adjacent nodes
            for diff in diffs:
                s = 1
                while 1:
                    idx = addv((i, j), scale(diff, s))
                    if not in_range(idx, size):
                        break
                    if getv(grid, idx):
                        graph[i, j].append(idx)
                        break
                    s += 1

# print('graph', len(graph))
# print(*graph.items(), sep='\n')
# print('values', len(values))
# print(*values.items(), sep='\n')
#
# print(reduce(add, [len(_) for _ in graph.values()]))

def render(values : dict[Point, int], c_vars : dict[Point, mip.Var], b_vars : dict[tuple[Point, Point], mip.Var], d : int, size : Point):
    view = dict()

    for i in range(size[0]):
        for j in range(size[1]):
            if (i, j) in values:
                view[i, j] = str(values[i, j] + c_vars[i, j].x * d)[0] # type: ignore
            else:
                view[i, j] = '.'

    for bkey in b_vars:
        source, dest = bkey
        b = b_vars[bkey].x
        if b:
            draw_line(view, source, dest, b)

    for i in range(size[0]):
        for j in range(size[1]):
            print(view[i, j], end='')
        print()


def draw_line(view, source, dest, thickness):
    min_pt = min(source, dest)
    max_pt = max(source, dest)
    horiz = {1: '-', 2: '='}
    vert = {1: '|', 2: 'ǁ'}
    diff = subv(max_pt, min_pt)

    if diff[0]:
        step = (1, 0)
        chars = vert
        dist = diff[0]
    else:
        # elif diff[1]:
        assert(diff[1])
        step = (0, 1)
        chars = horiz
        dist = diff[1]

    assert(not (diff[0] and diff[1])), diff
    assert(not (not diff[0] and not diff[1])), diff

    for t in range(1, dist):
        pt = addv(min_pt, scale(step, t))
        if pt not in view or view[pt] == '.':
            view[pt] = chars[thickness]
        else:
            view[pt] = '+'

good_ds = list()

# d for displacement
for d in (_ for _ in range(-7, 7+1) if _ != 0):

    m = mip.Model()
    m.verbose = 0

    # add constraints for binary coefficients
    c_vars : dict[Point, mip.Var] = {key: m.add_var(var_type=mip.BINARY, name=f"c_{key}") for key in values}
    m += (mip.xsum(c_vars.values()) == 1)

    # track all bridges
    b_vars : dict[tuple[Point, Point], mip.Var | None] = {(source, dest): None for source in graph for dest in graph[source] if source < dest}
    for bkey in b_vars:
        b_vars[bkey] = m.add_var(var_type=mip.INTEGER, name=f"b_{bkey}", lb=0, ub=2) # type: ignore

    def get_b_vars_of(key):
        return [(b_vars[key, okey] if key < okey else b_vars[okey, key]) for okey in graph[key]]

    # the meat of it
    for key in values:
        m += (values[key] + d * c_vars[key] == mip.xsum(get_b_vars_of(key))) # type: ignore

    status = m.optimize()
    if status != mip.OptimizationStatus.INFEASIBLE:
        print()
        print()
        print(f"** D = {d} **")
        print(f"{status=}")
        for key in c_vars:
            c_var = c_vars[key]
            if c_var.x == 1:
                print(key, values[key], '-->>', values[key] + d)

        render(values, c_vars, b_vars, d, size) # type: ignore
        print()
        good_ds.append(d)

print()
print(f"{good_ds=}")
