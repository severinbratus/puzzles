#!/usr/bin/env python3

import pytest

import solve

@pytest.mark.parametrize("expected,arg", [
    ([(1, 10), (1, 8), (2, 9), (0, 9)], (1, 9))
])
def test_get_vicinity(expected, arg):
    assert expected == list(solve.get_vicinity(arg))


@pytest.mark.parametrize("expected,arg", [
    ('LLL', [(0, 0), (-1, 0), (-2, 0), (-3, 0)]),
    ('DL', [(1, 9), (1, 10), (0, 10)])
])
def test_symbolize(expected, arg):
    assert expected == solve.symbolize(arg)


@pytest.mark.parametrize("expected,arg", [
    ([(0, 0)], solve.Fragment((0, 0), [])),
    ([(1, 9), (1, 10)], solve.Fragment((1, 9), ['D'])),
    ([(0, 0), (-1, 0), (0, 0)], solve.Fragment((0, 0), ['L', 'R'])),
    ([(0, 0), (1, 0)], solve.Fragment((0, 0), ['R', 'R', 'X'])),
    ([(0, 0), (1, 0), (2, 0)], solve.Fragment((0, 0), ['R', 'R', 'S'])),
    ([(0, 0), (1, 0), (2, 0)], solve.Fragment((0, 0), ['R', 'R', 'F'])),
])
def test_get_points(expected, arg):
    observed = list(solve.get_points(arg))
    assert expected == list(map(lambda pair: pair[0], observed))
