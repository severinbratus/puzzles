#!/usr/bin/env python3

from collections import defaultdict

def solution(numbers):
    # for power in powers(10 ** 6):
    return sum(solve(numbers, power) for power in powers(2 * 10 ** 6))

def powers(limit):
    power = 1;
    while power <= limit:
        yield power
        power *= 2

def solve(numbers, k):
    hashmap = defaultdict(int)
    ans = 0
    for x in numbers:
        hashmap[x] += 1
        if hashmap[k -x ]:
            ans += hashmap[k - x]
    return ans
