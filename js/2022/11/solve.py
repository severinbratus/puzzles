#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import Polygon as PatchPolygon

import numpy as np
import sympy as sp

from itertools import product
from dataclasses import dataclass, field
from reprlib import recursive_repr
from random import randrange

from math import sqrt
from functools import cache


R = sqrt((5 + sqrt(5)) / 10)
H = sqrt(5 + 2 * sqrt(5)) / 2
A = H - R

print("CONSTS")
print(f"{R=}")
print(f"{H=}")
print(f"{A=}")

M = 3 # 17

Point = np.array
Segment = tuple[np.array, np.array]


'''So `sympy` takes like 30 secs to compute the intersection of two pentagons.
This ain't good.
'''
class RegularPolygon:

    center : Point
    radius : float # float64 = 16 decimal digits of precision
    n : int
    angle : float

    sides : list[Segment]
    vertices : list[Point]


    def __init__(self, c, r = R, n = 5, a = 0):
        self.center = c
        self.radius = r
        self.n = n
        self.angle = a

        b = np.pi * 2 / n

        self.vertices = [c + rotated(np.array((r, 0)), a + i * b) for i in range(n)]
        self.sides = [(self.vertices[i], self.vertices[(i + 1) % n]) for i in range(n)]


Polygon = RegularPolygon


def rotated(vector, angle) -> Point:
    # print(f"{vector=}")
    # print(f"{angle=}")
    if angle == 0:
        return vector
    cos_, sin_ = np.cos(angle), np.sin(angle)
    rotation = np.array(((cos_, -sin_), (sin_, cos_)))
    return rotation @ vector


@dataclass
class Node:
    # `Canonical` polygon
    polygon : Polygon
    # Connections
    ports : list = field(default_factory=lambda: [None] * 5)

    @recursive_repr()
    def __repr__(self):
        return f"Node(polygon=Polygon@{round_point(self.polygon.center)}, ports={dictify_ports(self.ports)})"


def round_point(point) -> tuple[int, int]:
    '''Round a real 2D point'''
    return (round(point[0], 2), round(point[1], 2))


def dictify_ports(ports):
    '''Prettify port structure
    '''
    return {i: v for i, v in enumerate(ports) if v != None}


# def concretize(polygon):
#     return Polygon(*[point.evalf() for point in polygon.vertices])


class Polyform:
    size : int = 0
    nodes : list[Node]
    polygons : list[Polygon]


    def __init__(self):
        '''Construct the default, two pentagon polyform
        '''
        # polygon_1 = concretize(RegularPolygon(c=Point(0, 0), r=R, n=n))
        polygon_1 = RegularPolygon(c=np.array((0, 0)), r=R, n=5)
        polygon_2 = RegularPolygon(c=np.array((-2 * A, 0)), r=R, n=5, a=np.pi)
        node_1 = Node(polygon_1)
        node_2 = Node(polygon_2)
        node_1.ports[2] = node_2
        node_2.ports[2] = node_1
        nodes = [node_1, node_2]
        self.nodes = nodes
        self.polygons = [node.polygon for node in nodes]


    def __len__(self):
        return self.size


    def get_children(self):
        '''Return possible extensions of the polyform
        '''
        for node in self.nodes:
            polygon = node.polygon

            # check if we can add new polygons at the free ports
            for port, x in enumerate(node.ports):
                if not x:
                    mp = np.mean(polygon.sides[port])
                    # v is the vector from the side midpoint to the centre of the new polygon
                    v = - (polygon.center - mp)
                    a = angle_between((1, 0), v)
                    c = mp + v
                    new_polygon = RegularPolygon(c=c, r=R, n=5, a=a)
                    if not any(overlap(new_polygon, some_polygon) for some_polygon in self.polygons):
                        yield new_polygon


    def metric(self):
        '''Return the smallest non-zero distance between any two of the pentagons.
        '''
        return min(nonzero(polygon_distance(p, q) for p, q in product(pentagons, repeat=2) if p != q))


    def root(self):
        return self.nodes[0]


def nonzero(xs):
    return filter(lambda x: x != 0, xs)


def angle_between(a, b):
    return np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def polygon_distance(p, q):
    # print(list(segment_distance(a, b) for a, b in product(p.sides, q.sides)))
    return min(segment_distance(a, b) for a, b in product(p.sides, q.sides))


def segment_distance(ab, cd):
    ab_ = sp.Segment(*[sp.Point(_, evaluate=False) for _ in ab])
    cd_ = sp.Segment(*[sp.Point(_, evaluate=False) for _ in cd])
    a_, b_ = ab_.points
    c_, d_ = cd_.points
    return float(min(cd_.distance(a_), cd_.distance(b_), ab_.distance(c_), ab_.distance(d_)))

# a = ((0, 0), (1, 1))
# b = ((1, 0), (2, 1))
# print(segment_distance(a, b))


def overlap(polygon_a, polygon_b):
    '''Two convex regular polygons overlap (share non-edge points) iff they have two points of intersection'''
    return False


def recurse(polyform, cache):
    # given a polyform of pentagons,
    # recurse on the possible extended polyforms.
    # base case: polyform has 17 pentagons
    if len(polyform) == M:
        return polyform.metric()
    return min(recurse(child_polyform, cache) for child_polyform in polyform.get_children())


def solve(n : int) -> int:
    # we start off w/ two pentagons
    cache = dict()
    init : Polyform = Polyform()
    return recurse(init, cache)


import pytest


@pytest.mark.parametrize("expected, args", [
    (1, [3]),
    (0.5877853, [4]),
])
def test_main(expected, args):
    assert pytest.approx(expected) == solve(*args)


def draw_polygon(ax, polygon: Polygon):
    poly = PatchPolygon([side[0] for side in polygon.sides], facecolor=colors.to_rgba('w', 0.2), edgecolor='k')
    ax.add_patch(poly)


def plot_polygons(polygons : list[Polygon], show = True, save = False):
    print('plot_polygons')
    fig, ax = plt.subplots()

    for polygon in polygons:
        draw_polygon(ax, polygon)

    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed')
    ax.xaxis.grid(color='gray', linestyle='dashed')
    ax.set_aspect('equal')
    minx = miny = -10
    maxx = maxy = +10
    ax.set_xlim((minx, maxx))
    ax.set_ylim((miny, maxy))
    ax.set_xticks(np.arange(minx, maxx + 1, 1))
    ax.set_yticks(np.arange(miny, maxy + 1, 1))

    if save: plt.savefig(f"plot-{randrange(10000):04d}.png")
    if show: plt.show()


polyform = Polyform()
# p, q = polyform.polygons
# print(polygon_distance(p, q))

children = list(polyform.get_children())
plot_polygons(children)

# polygon = RegularPolygon(c=np.array((0, 0)), r=R, n=5)
# plot_polygons([polygon])
