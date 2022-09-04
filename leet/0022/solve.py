#!/usr/bin/env python3

from typing import List
from functools import cache
from itertools import product

from sys import argv
import pytest

class Solution:
    @cache
    def generateParenthesis(self, n: int) -> List[str]:
        print(f"{n=}")
        # We put one pair down, and proceed with the other ones.
        # They can either be inside or right to this pair
        if n == 0:
            return ['']
        if n == 1:
            return ['()']
        result = []
        for size_inner in range(0, n): # from 1 to n - 1
            size_outer = (n - 1) - size_inner
            print(f"{size_inner=}, {size_outer=}")
            result += ["(%s)%s" % (inner_parens, outer_parens) for inner_parens, outer_parens in product(self.generateParenthesis(size_inner), self.generateParenthesis(size_outer))]
        return result


catalan_numbers = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786]

@pytest.mark.parametrize('n', list(range(0, len(catalan_numbers))))
def test_gen_parens(n):
    assert len(Solution().generateParenthesis(n)) == catalan_numbers[n]
