#!/usr/bin/env python3

import pytest

from solution import Solution

# Example 1:

# Input: tokens = ["2", "1", "+", "3", "*"]
# Output: 9
# Explanation: ((2 + 1) * 3) = 9
# Example 2:

# Input: tokens = ["4", "13", "5", "/", "+"]
# Output: 6
# Explanation: (4 + (13 / 5)) = 6
# Example 3:

# Input: tokens = ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
# Output: 22
# Explanation: ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
# = ((10 * (6 / (12 * -11))) + 17) + 5
# = ((10 * (6 / -132)) + 17) + 5
# = ((10 * 0) + 17) + 5
# = (0 + 17) + 5
# = 17 + 5
# = 22


@pytest.mark.parametrize("expected, tokens",  [
    (22,  ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]),
    (6,  ["4", "13", "5", "/", "+"]),
    (9,  ["2", "1", "+", "3", "*"])
])
def test_main(expected,  tokens):
    assert expected == Solution().evalRPN(tokens)
