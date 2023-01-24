#!/usr/bin/env python3

from collections import defaultdict

def solution(a, k):
    b = [x % k for x in a]
    # now want two i, j; i < j, s.t. b[i] + b[j] = k
    c = defaultdict(int)
    ans = 0
    for i, x in enumerate(b):
        ans += c[(k - x) % k]
        c[x] += 1
    return ans
