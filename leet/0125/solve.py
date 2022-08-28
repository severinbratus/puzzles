#!/usr/bin/env python3

class Solution:
    def isPalindrome(self, z: str) -> bool:
        s = list(map(str.lower, filter(str.isalnum, z)))
        return all(s[i] == s[j] for i, j in zip(range(len(s)), range(len(s) - 1, -1, -1)))


def test_main():
    assert Solution().isPalindrome("")
    assert Solution().isPalindrome("a")
    assert Solution().isPalindrome("abba")
    assert Solution().isPalindrome("abcba")
    assert not Solution().isPalindrome("abcbx")
    assert not Solution().isPalindrome("xbcba")
    assert Solution().isPalindrome("A man, a plan, a canal: Panama")
    assert not Solution().isPalindrome("0P")
