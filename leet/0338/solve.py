#!/usr/bin/env python3

# It is very easy to come up with a solution with a runtime of O(n log n). Can you do it in linear time O(n) and possibly in a single pass?

class Solution(object):
    def countBits(self, n):
        """
        :type n: int
        :rtype: List[int]
        """
        if n == 0:
            return [0]
        result = [0] * (n + 1)
        result[1] = 1
        power_lower = 2
        power_upper = 4
        for index in range(2, n + 1):
            if index == power_upper:
                power_lower *= 2
                power_upper *= 2
            result[index] = result[index - power_lower] + 1

        return result

import pytest

@pytest.mark.parametrize('arg, expected', [
    (0, [0]),
    (1, [0,1]),
    (2, [0,1,1]),
    (5, [0,1,1,2,1,2]),
    (15, [0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4]),
])
def test_main(expected, arg):
    assert Solution().countBits(arg) == expected

# Example 1:
# Input: n = 2
# Output: [0,1,1]

# Example 2:
# Input: n = 5
# Output: [0,1,1,2,1,2]
