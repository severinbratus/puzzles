#!/usr/bin/env python3

import unittest

from solution import Solution
from pdb import set_trace

class Test(unittest.TestCase):

    # Input: s = "barfoothefoobarman", words = ["foo", "bar"]
    # Output: [0, 9]
    # Explanation: Substrings starting at index 0 and 9 are "barfoo" and "foobar" respectively.
    # The output order does not matter, returning [9, 0] is fine too.
    def test_1(self):
        s = "barfoothefoobarman"
        words = ["foo", "bar"]
        output = [0, 9]
        self.assertEqual(Solution().findSubstring(s, words), output)

    def test_2(self):
        # s = "wordgoodgoodgoodbestword", words = ["word", "good","best","word"]
        s = "wordgoodgoodgoodbestword"
        words = ["word", "good","best","word"]
        output = []
        self.assertEqual(Solution().findSubstring(s, words), output)
        # NOTE: "word" appears twice in the word list, and must appear exactly twice in the substring!

    # Input: s = "barfoofoobarthefoobarman", words = ["bar", "foo","the"]
    # Output: [6, 9,12]
    def test_3(self):
        s = "barfoofoobarthefoobarman"
        words = ["bar", "foo","the"]
        output = [6, 9,12]
        self.assertEqual(Solution().findSubstring(s, words), output)

    def test_1b(self):
        s = "xbarfoothefoobarman"
        words = ["foo", "bar"]
        output = [1, 10]
        self.assertEqual(Solution().findSubstring(s, words), output)

    def test_4(self):
        s = "baaaab"
        words = ["aaa"]
        output = [1, 2]
        self.assertEqual(Solution().findSubstring(s, words), output)

    def test_5(self):
        s = "baaaab"
        words = ["baa", "aaa"]
        output = []
        self.assertEqual(Solution().findSubstring(s, words), output)

    def test_6(self):
        s = "foobman"
        words = ["foo", "man"]
        output = []
        self.assertEqual(Solution().findSubstring(s, words), output)

    def test_7(self):
        s = "barfoothefoobarman"
        words = ["foo", "bar"]
        output = [0, 9]
        # print(Solution().findSubstring(s, words))
        # print(output)
        self.assertEqual(Solution().findSubstring(s, words), output)

    def test_8(self):
        s = "wordgoodgoodgoodbestword"
        words = ["word","good","best","good"]
        output = [8]
        self.assertEqual(Solution().findSubstring(s, words), output)

if __name__ == '__main__':
    unittest.main()
