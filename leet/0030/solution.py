#!/usr/bin/env python3

from collections import Counter
# from copy import deepcopy

class Solution:

    def findSubstring(self, s, words):
        """
        :type s: str
        :type words: List[str]
        :rtype: List[int]
        """

        len_word = len(words[0])
        num_words = len(words)

        len_substr = num_words * len_word

        substr_indxs = []

        words_counter = Counter(words)

        for offset in range(0, len_word):

            # initialise counter
            counter = Counter()
            for start_word in range(offset, len_substr, len_word):
                new_word = s[start_word:start_word + len_word]
                counter[new_word] += 1

            for start_substr in range(offset, (len(s) - len_substr) + 1, len_word):

                end_substr = start_substr + len_substr

                # test the substr [i, j)
                # does it contain every word?
                # does it contain every word exactly the number of times as in `words`?

                # loop invariant:
                # at the start of the iteration, `counter` correctly counts the words in s[i:j]

                # if `counter` contains all the words required by `words_counter` in sufficient quantity
                if counter == words_counter:

                    substr_indxs.append(start_substr)

                # we are leaving one word behind as the window slides further
                # this word is at the beginning of the current window
                last_word = s[start_substr:start_substr + len_word]
                counter[last_word] = max(0, counter[last_word] - 1)

                # we enter a new word into our window
                # this new word is after the the end of the current window
                new_word = s[end_substr:end_substr + len_word]
                if len(new_word) == len_word:
                    counter[new_word] += 1

        return sorted(substr_indxs)
