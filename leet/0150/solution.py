#!/usr/bin/env python3

from operator import add, mul, sub, truediv
from math import trunc


class Solution:

    operators = {
        '+': add,
        '*': mul,
        '-': sub,
        '/': lambda a, b: trunc(truediv(a, b))
    }

    def evalRPN(self, tokens) -> int:

        stack = []

        for token in tokens:

            if Solution.is_operator(token):

                top = stack.pop()
                subtop = stack.pop()

                stack.append(Solution.operators[token](subtop, top))

            else:
                stack.append(int(token))

        return stack[0]

    def is_operator(token: str):
        return token in Solution.operators
