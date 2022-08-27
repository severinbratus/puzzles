#!/usr/bin/env python3

from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        nums_lookup = set(nums)
        max_streak = 0
        for num in nums:
            if num - 1 not in nums_lookup:
                streak = 1
                while num + streak in nums_lookup:
                    streak += 1
                if streak > max_streak:
                    max_streak = streak

        return max_streak



import pytest


@pytest.mark.parametrize('expected, nums', [
    (9, [0,3,7,2,5,8,4,6,0,1]),
    (4, [100,4,200,1,3,2]),
    (7, [0,1,2,500,4,5,6,3]),
])
def test_main(expected, nums):
    assert Solution().longestConsecutive(nums) == expected
