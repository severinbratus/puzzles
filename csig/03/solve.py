#!/usr/bin/env python3

from collections import defaultdict

def get_digit_set(x):
    return tuple(sorted(str(x)))

def solution(a):
    s = defaultdict(int)
    ans = 0
    for x in a:
        key = get_digit_set(x)
        if key in s:
            ans += s[key]
        s[key] += 1
    return ans
