from itertools import *
from functools import *

phi = (1 + 5 ** 0.5) / 2

# Model a regular icosahedron

@cache
def possible_signs(n):
    return list(product((1, -1), repeat=n))

assert(len(possible_signs(2)) == 4)

ico_vertices = set(chain([(0, signs[0], signs[1] * phi) for signs in possible_signs(2)],
                         [(signs[0], signs[1] * phi, 0) for signs in possible_signs(2)],
                         [(signs[0] * phi, 0, signs[1]) for signs in possible_signs(2)]))

# However, the vertices of our desired soccer ball graph correspond to the faces of a icosohedron,
# so we model a regular dodecahedron, the dual polyhedron of the icosahedron

dode_vertices = list(chain([signs for signs in possible_signs(3)],
                           [(0, signs[0] * phi, signs[1] / phi) for signs in possible_signs(2)],
                           [(signs[0] / phi, 0, signs[1] * phi) for signs in possible_signs(2)],
                           [(signs[0] * phi, signs[1] / phi, 0) for signs in possible_signs(2)]))

# 20 white hexagons
assert(len(dode_vertices) == 20)

# Then construct the ball graph

dode_edge_length = 2 / phi

EPSILON = 1 / 10**10

def approx(x, y):
    return abs(x - y) < EPSILON

ball = {index: [] for index in range(20)}

from scipy.spatial import distance

dist = distance.euclidean

for a, b in combinations(range(20), r=2):
    if approx(dist(dode_vertices[a], dode_vertices[b]), dode_edge_length):
        ball[a].append(b)
        ball[b].append(a)

assert(all(len(ball[node]) == 3 for node in range(20)))

# 20x21 matrix corresponding to a set of linear equations.

import numpy as np

npmtx = np.zeros((20, 21))

# e(0) == 0
npmtx[0][0] = 1

for idx in ball:
    if idx != 0:
        npmtx[idx][idx] = 1
        for adj_idx in ball[idx]:
            npmtx[idx][adj_idx] = -1/3
        npmtx[idx][-1] = 1

import sympy as sp

spmtx = sp.Matrix(npmtx)

rref = spmtx.rref()

assert(len(rref[1]) == 20)

exp_num_steps = [round(rref[0].row(idx)[-1]) for idx in range(20)]

for idx in ball:
    if idx != 0:
        assert(exp_num_steps[idx] == round(1 + (1/3) * sum(exp_num_steps[adj_idx] for adj_idx in ball[idx])))

idx = 0
print(1 + (1/3) * sum(exp_num_steps[adj_idx] for adj_idx in ball[idx]))
# 20
