#!/usr/bin/env python3

# Task: find maximum integer L that satisfies predicate P

def solution(a, k):
    l = 1
    r = sum(a)

    def P(L):
        return k <= sum(x // L for x in a)

    while l <= r:
        L = mid = (l + r) // 2
        p, q = P(L), P(L + 1)
        if p and q:
            l = mid + 1
        elif (not p) and (not q):
            r = mid - 1
        else:
            assert p and not q
            return L
