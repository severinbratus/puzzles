#!/usr/bin/env python3

from functools import cache
from math import inf


def solve_knapsack_top_down(capacity : int, weights : list[int], values : list[int]) -> tuple[int, list[int]]:
    '''Return the value of items to take to maximize total value, under the max. weight constraint, and the item weights.

    A top-down dynamic programming approach w/ a cached recursive function.
    TODO: Make path tracking more efficient
    '''
    @cache
    def get_best_value(capacity, index) -> tuple[int, list[int]]:
        '''At each call, we `decide` if item under `index` should be taken or not to maximize total value'''
        if index < 0: return 0, []
        # Take the item, if weight capacity permits
        value_if_taken, values_if_taken = get_best_value(capacity - weights[index], index - 1) if weights[index] < capacity else [-inf, []]
        value_if_taken += values[index]
        values_if_taken += [values[index]]
        # Leave it be
        value_if_left, values_if_left  = get_best_value(capacity, index - 1)
        best_value = max(value_if_taken, value_if_left)
        best_values = (values_if_taken if best_value == value_if_taken else values_if_left)
        return best_value, best_values

    return get_best_value(capacity, len(weights) - 1)


def scenario():
    '''A intern has a lunch allowance of N euros (represented as N * 100 cents), and a collection of checks from LIDL.
    Decide which checks they should include in the declaration.
    '''
    check_values = [1424, 147, 916, 1129]
    allowance_value = 2150
    return solve_knapsack_top_down(allowance_value, check_values, check_values)


print(scenario())
