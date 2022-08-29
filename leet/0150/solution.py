#!/usr/bin/env python3

from operator import add, mul, sub, truediv
from math import trunc


class Solution:

    def evalRPN(self, tokens) -> int:
        operators = {
            '+': add,
            '*': mul,
            '-': sub,
            '/': lambda a, b: trunc(truediv(a, b))
        }
        stack = []
        for token in tokens:
            if token in "+*-/":
                top = stack.pop()
                subtop = stack.pop()
                stack.append(operators[token](subtop, top))

            else:
                stack.append(int(token))

        return stack[0]
