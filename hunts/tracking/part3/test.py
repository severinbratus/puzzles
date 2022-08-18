#!/usr/bin/env python3

import pytest

from solve import compute_capacity

@pytest.mark.parametrize("expected, arg", [
    (1, [2, 1, 2]),
    (1, [2, 0, 1]),
    (9, [7, 6, 5, 4, 4, 9]),
    (0, [18, 15, 12])
])
def test_compute_capacity(expected, arg):
    assert expected == compute_capacity(arg)
