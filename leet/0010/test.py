#!/usr/bin/env python3

# Input: s = "aa", p = "a"
# Output: false
# Explanation: "a" does not match the entire string "aa".

# Input: s = "aa", p = "a*"
# Output: true
# Explanation: '*' means zero or more of the preceding element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".

# Input: s = "ab", p = ".*"
# Output: true
# Explanation: ".*" means "zero or more (*) of any character (.)".

import pytest
from solve import Solution, Atom


@pytest.mark.parametrize('expected, s, p', [
    (False, "aa", "a"),
    (True, "aa", "a*"),
    (True, "ab", ".*"),
    (True, "a", "."),
    (True, "", ".*"),
    (False, "a", "b"),
    (True, "ab", "ab*"),
    (True, "abraaxas", "abr*a*x.*m*"),
    (True, "abraaxas", ".*.*.*"),
    (False, "abraaxas", "abraaxas."),
    (True, "bible", "....."),
    (False, "bible", "...."),
    (False, "hellothere", ".*s"),
    (False, "a", "ab*a"),
    (True, "aa", "ab*a"),
    (False, "b", "b.b"),
    (False, "b", "b.."),
])
def test_main(expected, s, p):
    assert expected == Solution().isMatch(s, p)


@pytest.mark.parametrize('expected, arg', [
    ([], ''),
    ([Atom('a')], 'a'),
    ([Atom('.')], '.'),
    ([Atom('.*')], '.*'),
    ([Atom('a'), Atom('b')], 'ab'),
])
def test_atomize(expected, arg):
    assert expected == Solution.atomize(arg)


@pytest.mark.parametrize('expected, args', [
    ([0], ("abc", 0, "x")),
    ([0, 1], ("abc", 0, "a")),
    ([0, 1, 2], ("baab", 1, "a")),
])
def test_lengths(expected, args):
    assert expected == list(Solution.get_possible_lengths(*args))


# My learned friend has told me that what I called atomizing is actually called `lexing`...
