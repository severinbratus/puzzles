#!/usr/bin/env python3

import pytest

from collections import Counter
from math import inf

def solution(A):
    counter = Counter(A)

    # Discard unmatchable side lengths
    keys = sorted(key for key in counter.keys() if counter[key] >= 2)
    if not keys:
        return -1

    # Case #1: square
    for key in keys:
        if counter[key] >= 4:
            return 0

    if len(keys) == 1:
        return -1

    # Case #2: rectangle
    result = inf
    for key, next_key in zip(keys, keys[1:]):
        result = min(result, next_key - key)

    return result


@pytest.mark.parametrize("expected, args", [
    [0, [1, 1, 1, 1]],
    [0, [1, 3, 5, 2, 2, 1, 5, 1, 4, 1]],
    [1, [3, 5, 2, 2, 1, 5, 1, 4, 1]],
    [2, [3, 5, 3, 2, 1, 5, 1, 4, 1]],
    [2, [3, 5, 3, 2, 1, 5, 1, 4, 1]],
])
def test_main(expected, args):
    assert expected == solution(args)
