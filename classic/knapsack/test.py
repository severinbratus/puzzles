#!/usr/bin/env python3

import pytest

from solve import solve_knapsack_top_down

@pytest.mark.parametrize('expected, max_weight, weights, values', [
    (21, 10, [5, 3, 1, 2, 6, 4, 7, 8],
             [7, 9, 5, 2, 4, 5, 8, 9])
])
def test_main(expected, max_weight, weights, values):
    assert expected == solve_knapsack_top_down(max_weight, weights, values)[0]
