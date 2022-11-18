#!/usr/bin/env python3

from sympy import Point, Segment, Polygon, RegularPolygon, sqrt, simplify, nsimplify, pi

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import Polygon as PatchPolygon

import numpy as np

from itertools import product
from dataclasses import dataclass, field
from reprlib import recursive_repr
from random import randrange


R = sqrt((5 + sqrt(5)) / 10)
H = sqrt(5 + 2 * sqrt(5)) / 2
A = H - R


@dataclass
class Node:
    # `Canonical` polygon
    polygon : Polygon
    # Connections
    ports : list = field(default_factory=lambda: [None] * 5)

    @recursive_repr()
    def __repr__(self):
        return f"Node(polygon=Polygon@{round_point(self.polygon.centroid)}, ports={dictify_ports(self.ports)})"


def round_point(point) -> tuple[int, int]:
    return (round(point[0], 2), round(point[1], 2))


def dictify_ports(ports):
    return {i: v for i, v in enumerate(ports) if v != None}


class Polyform:
    size : int = 0
    nodes : list[Node]
    polygons : list[Polygon]

    def __init__(self):
        '''Construct the default, two pentagon polyform
        '''
        polygon_1 = RegularPolygon(c=Point(0, 0), r=R, n=5)
        polygon_2 = RegularPolygon(c=Point(-2 * A, 0), r=R, n=5)
        polygon_2.spin(pi)
        node_1 = Node(polygon_1)
        node_2 = Node(polygon_2)
        node_1.ports[0] = node_2
        node_2.ports[0] = node_1
        # print(f"{node_1=}")
        # print(f"{node_2=}")
        nodes = [node_1, node_2]
        self.nodes = nodes
        self.polygons = [node.polygon for node in nodes]

    def __len__(self):
        return self.size

    def get_children(self):
        '''Return possible extensions of the polyform
        '''
        pass

    def metric(self):
        '''Return the smallest non-zero distance between any two of the pentagons.
        '''
        return min(nonzero(polygon_distance(p, q) for p, q in product(pentagons, repeat=2) if p != q))


def nonzero(xs):
    return filter(lambda x: x != 0, xs)


def polygon_distance(p, q):
    return p.distance(q)


def recurse(polyform, cache):
    # given a polyform of pentagons,
    # recurse on the possible extended polyforms.
    # base case: polyform has 17 pentagons
    if len(polyform) == 17:
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
    poly = PatchPolygon([side.p1 for side in polygon.sides], facecolor=colors.to_rgba('w', 0.2), edgecolor='k')
    ax.add_patch(poly)


# print(f"{polygon.perimeter=}")
# print(f"{nsimplify(polygon.perimeter)=}")
# side = polygon.sides[0].length
# print(f"{side=}")
# print(f"{nsimplify(side)=}")
# draw_polygon(ax, polygon)
# draw_polygon(ax, polygon_2)
#


def plot_polyform(polyform : Polyform, show = False, save = True):
    fig, ax = plt.subplots()

    for polygon in polyform.polygons:
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


default_polyform = Polyform()
plot_polyform(default_polyform)
