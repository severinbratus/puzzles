#!/usr/bin/env python3

from collections import Counter
from itertools import chain


def solution(a):
    ch = map(int, chain(*(str(x) for x in a)))
    counter = Counter(ch)
    max_val = max(counter.values())
    max_val_keys = [key for key in counter.keys() if counter[key] == max_val]
    max_val_keys.sort()
    return max_val_keys
