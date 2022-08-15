#!/usr/bin/env python3

# Example 1:

# Input: num = "123", target = 6
# Output: ["1*2*3","1+2+3"]
# Explanation: Both "1*2*3" and "1+2+3" evaluate to 6.
# Example 2:

# Input: num = "232", target = 8
# Output: ["2*3+2","2+3*2"]
# Explanation: Both "2*3+2" and "2+3*2" evaluate to 8.
# Example 3:

# Input: num = "3456237490", target = 9191
# Output: []
# Explanation: There are no expressions that can be created from "3456237490" to evaluate to 9191.

import pytest
from solution import Solution


@pytest.mark.parametrize("expected, args",  [
    (["1*2*3", "1+2+3"], ("123", 6)),
    (["2*3+2", "2+3*2"], ("232", 8)),
    ([], ("3456237490", 9191)),
    (["1*0+5", "10-5"], ("105", 5))
])
def test_main(expected, args):
    assert expected == Solution().addOperators(*args)


def test_extreme():
    num = "1000000009"
    target = 9
    print(Solution().addOperators(num, target))
