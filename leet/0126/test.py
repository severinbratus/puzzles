#!/usr/bin/env python3

import pytest
from solution import Solution

# Example 1:

@pytest.mark.parametrize('expected, args', [
    (
        [
            ["hit","hot","dot","dog","cog"],
            ["hit","hot","lot","log","cog"]
        ],
        (
            "hit",
            "cog",
            ["hot","dot","dog","lot","log","cog"],
        ),
    ),
    (
        [],
        (
            "hit",
            "cog",
            ["hot","dot","dog","lot","log"],
        )
    )
])
def test_main(expected, args):
    assert Solution().findLadders(*args) == expected


@pytest.mark.parametrize("expected, args", [
    (
        True,
        ("hit", "hot"),
    ),
    (
        False,
        ("hat", "hog"),
    ),
])
def test_is_step(expected, args):
    assert Solution.is_step(*args) == expected
