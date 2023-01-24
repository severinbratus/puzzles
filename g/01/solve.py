#!/usr/bin/env python3

import pytest

# def solution(S):
#     numbers = [ord(c) - ord('a') for c in S]
#     result = 0
#     expected = 0
#     m = 3
#     for actual in numbers:
#         # print(f"{expected=}")
#         # print(f"{actual=}")
#         if actual < expected:
#             # go the end of the sequence
#             result += m - expected
#             # then to the actual value
#             result += actual
#         else:
#             assert actual - expected < 3
#             result += actual - expected
#         # print(f"{result=}")
#         # print()
#         expected = (actual + 1) % m
#     return result

import sys

import sys

def eprint(*args):
    sys.stderr.write(' '.join(map(str, args)) + '\n')

def solution(S):
    numbers = [ord(c) - ord('a') for c in S]
    eprint(numbers)
    result = 0
    expected = 0
    m = 3
    for actual in numbers:
        eprint(f"{expected=}")
        eprint(f"{actual=}")
        if actual < expected:
            # go the end of the sequence
            result += m - expected
            # then to the actual value
            result += actual
        else:
            assert actual - expected < 3
            result += actual - expected
        eprint(f"{result=}")
        eprint()
        expected = (actual + 1) % m
    return result





@pytest.mark.parametrize("expected, args", [
    # [50, ("aa", 26)],
    [4, ["aabcc"]],
    [0, ["abcabcabca"]],
    [0, ["a"]],
    [2, ["aa"]],
    [1, ["b"]],
    [2, ["ba"]],
    [0, ["ab"]],
    [2, ["babca"]],
])
def test_main(expected, args):
    print(expected, args, solution(*args))
    assert expected == solution(*args)
