#!/usr/bin/env python3

from collections import defaultdict
from functools import reduce
from operator import mul, add
from itertools import product

import mip

Point = tuple[int, int]
Bridge = tuple[Point, Point]
Cross = tuple[Bridge, Bridge]

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


def render(values : dict[Point, int], c_vars : dict[Point, mip.Var], b_vars : dict[Bridge, mip.Var], d : int, size : Point):
    view = dict()

    for i in range(size[0]):
        for j in range(size[1]):
            if (i, j) in values:
                view[i, j] = str(values[i, j] + c_vars[i, j].x * d)[0] # type: ignore
            else:
                view[i, j] = '.'

    for b_key in b_vars:
        source, dest = b_key
        b = b_vars[b_key].x
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



# second field
maxg = [[4, 0, 4, 0, 4, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 0, 1],
	    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	    [0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
	    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	    [3, 0, 2, 0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 5, 0, 3],
	    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	    [5, 0, 4, 0, 4, 0, 3, 0, 0, 0, 5, 0, 1, 0, 0, 0, 0],
	    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 4, 0, 5, 0, 4],
	    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	    [6, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	    [3, 0, 4, 0, 5, 0, 0, 0, 2, 0, 4, 0, 2, 0, 2, 0, 4]]

def solve(field: int):

    with open(f'field_{field}.txt') as fin:
        grid = [[int(char) if char != '.' else 0 for char in line.strip()] for line in fin.readlines()]
    if grid == 2:
        assert grid == maxg

    n = len(grid)
    m = len(grid[0])
    size = (n, m)

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
    # print(reduce(add, [len(_) for _ in graph.values()]))
    b_keys : set[Bridge] = {(source, dest) for source in graph for dest in graph[source] if source < dest}
    visits : dict[Point, set[Bridge]] = defaultdict(set)

    for b_key in b_keys:
        source, dest = b_key
        min_pt = min(source, dest)
        max_pt = max(source, dest)
        diff = subv(max_pt, min_pt)
        if diff[0]:
            step = (1, 0)
            dist = diff[0]
        else:
            assert(diff[1])
            step = (0, 1)
            dist = diff[1]

        assert(not (diff[0] and diff[1])), diff
        assert(not (not diff[0] and not diff[1])), diff

        for t in range(1, dist):
            pt = addv(min_pt, scale(step, t))
            visits[pt].add(b_key)

    crosses : set[Cross] = set()
    for pt in visits:
        assert len(visits[pt]) <= 2
        if len(visits[pt]) == 2:
            crosses.add(tuple(sorted(visits[pt])))

    # print(*crosses, sep='\n')
    # print()

    good_ds = list()

    # d for displacement
    for d in (_ for _ in range(-7, 7+1) if _ != 0):

        m = mip.Model()
        m.verbose = 0

        # add constraints for binary coefficients
        c_vars : dict[Point, mip.Var] = {key: m.add_var(var_type=mip.BINARY, name=f"c_{key}") for key in values}
        m += (mip.xsum(c_vars.values()) == 1)

        # track all bridges
        b_vars : dict[Bridge, mip.Var | None] = {b_key: None for b_key in b_keys}
        for b_key in b_vars:
            b_vars[b_key] = m.add_var(var_type=mip.INTEGER, name=f"b_{b_key}", lb=0, ub=2) # type: ignore

        def get_b_vars_of(key):
            return [(b_vars[key, okey] if key < okey else b_vars[okey, key]) for okey in graph[key]]

        # the meat of it
        for key in values:
            m += (values[key] + d * c_vars[key] == mip.xsum(get_b_vars_of(key))) # type: ignore

        # disallow line crossings

        # decompose each b into p_0 + p_1
        p_vars = dict()
        for b_key in b_vars:
            p_0 = m.add_var(var_type=mip.BINARY, name=f"p_{b_key}_0")
            p_1 = m.add_var(var_type=mip.BINARY, name=f"p_{b_key}_1")
            p_vars[b_key] = (p_0, p_1)
            m += (b_vars[b_key] == p_0 + p_1)

        # on possibly crossing bridges, at most one of the perpendiculars may have bridges
        for cross in crosses:
            b_key_0, b_key_1 = cross
            for i, j in product((0, 1), repeat=2):
                m += (p_vars[b_key_0][i] + p_vars[b_key_1][j] <= 1)

        status = m.optimize()
        if status not in (mip.OptimizationStatus.INFEASIBLE, mip.OptimizationStatus.ERROR):
            # print()
            # print()
            print(f"** D = {d} **")
            print(f"{status=}")
            for key in c_vars:
                c_var = c_vars[key]
                if c_var.x == 1:
                    print(key, values[key], '-->>', values[key] + d)
            print(f"{m.num_solutions=}")

            render(values, c_vars, b_vars, d, size) # type: ignore
            print()
            good_ds.append(d)

    # print()
    print(f"{good_ds=}")

for field in range(1, 4+1):
    print(f"*** FIELD = {field} ***")
    solve(field)
    print()
    print()
