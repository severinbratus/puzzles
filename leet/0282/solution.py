#!/usr/bin/env python3

from itertools import product

import re


class Solution:

    trail_pattern = re.compile("0[0-9]")

    def addOperators(self, num: str, target: int):
        exprs = (Solution.interlace(num, signs)
                 for signs in product(["", "+", "*", "-"], repeat=len(num) - 1))
        return sorted([expr for expr in exprs
                       if not Solution.trail_pattern.search(expr) and eval(expr) == target])

    def interlace(num, signs):
        return ''.join(Solution.flatten(zip(num, signs))) + num[-1]

    def flatten(array):
        return (value for subarray in array for value in subarray)
