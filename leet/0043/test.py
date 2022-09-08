#!/usr/bin/env python3

import pytest

from solve import *


@pytest.mark.parametrize('expected, a, b', [
    (
        [2],
        [1], [1],
    ),
    (
        [9],
        [4], [5]
    ),
    (
        [0, 1],
        [9], [1]
    ),
    (
        [7, 1],
        [8], [9]
    ),
    (
        [3, 7, 1],
        [5, 7], [8, 9]
    ),
    (
        [0, 0, 0, 1],
        [9, 9, 9], [1]
    ),
    (
        [0, 0, 0, 1],
        [1], [9, 9, 9]
    ),
])
def test_add(expected, a, b):
    add(a, b)
    assert expected == a


@pytest.mark.parametrize('expected, args', [
    (
        [1],
        ([1], 1),
    ),
    (
        [6],
        ([2], 3),
    ),
    (
        [8, 1],
        ([9], 2),
    ),
    (
        [9, 4, 5],
        ([1, 6], 9),
    ),
    (
        [8, 3, 7],
        ([3, 2, 1], 6),
    )
])
def test_digit_multiply(expected, args):
    assert expected == digit_multiply(*args)


@pytest.mark.parametrize('expected, args', [
    (
        "6",
        ("3", "2"),
    ),
    (
        "16",
        ("8", "2"),
    ),
    (
        "123",
        ("41", "3"),
    ),
    (
        "123",
        ("123", "1"),
    ),
    (
        "24",
        ("12", "2"),
    ),
    (
        "24",
        ("2", "12"),
    ),
    (
        "56088",
        ("123", "456"),
    ),
    (
        "0",
        ("987", "0"),
    ),
])
def test_main(expected, args):
    assert expected == Solution().multiply(*args)
