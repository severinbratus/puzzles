#include <bits/stdc++.h>
#include <unordered_set>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"

using namespace std;

class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        int max_size = 0;
        // char to last appereance
        unordered_map<char, int> appereances {};
        int size = 0;

        for (int end = 0; end < s.size(); end++) {
            char new_char = s[end];
            if (appereances.count(new_char) && appereances[new_char] >= end - size) {
                // Take the distance between this appearance and the previous one as the new size.
                max_size = max(size, max_size);
                size = end - appereances[new_char];
            } else {
                // Simply increase the window size
                size++;
            }
            appereances[new_char] = end;
        }

        max_size = max(size, max_size);
        return max_size;
    }
};

TEST_CASE("Examples") {
    auto data = GENERATE(table<int, string>({
                {1, "a"},
                {2, "ab"},
                {3, "abcabcbb"},
                {1, "bbbbb"},
                {3, "pwwkew"},
                {4, "aaaabcd"},
                {4, "xyzzyxwwb"},
                {0, ""},
    }));

    Solution *solution = new Solution();
    REQUIRE(std::get<0>(data) == solution->lengthOfLongestSubstring(std::get<1>(data)));
}


// Example 1:
// Input: s = "abcabcbb"
// Output: 3
// Explanation: The answer is "abc", with the length of 3.
//
// Example 2:
// Input: s = "bbbbb"
// Output: 1
// Explanation: The answer is "b", with the length of 1.
//
// Example 3:
// Input: s = "pwwkew"
// Output: 3
// Explanation: The answer is "wke", with the length of 3.
// Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
