#include <algorithm>
#include <bits/stdc++.h>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"

using namespace std;

class Solution {
public:
    // string ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    int characterReplacement(string s, int k) {
        int right, left;
        right = left = 0;
        unordered_map<int, int> counts {};
        int max_size = 0;

        int window_size = 0;
        for (right = 0; right < s.size(); right++) {
            // add new char from right
            char new_char = s[right];
            counts[new_char] = counts.count(new_char) ? counts[new_char] + 1 : 1;
            window_size++;
            // take most frequest char
            char most_frequest_char = find_most_frequent(counts);
            int top_frequency = counts[most_frequest_char];
            int changes_needed = window_size - (top_frequency);
            // validate window
            if (changes_needed > k) {
                // invalid window
                // slide the left pointer
                counts[s[left]]--;
                left++;
                window_size--;
            }
            max_size = max(window_size, max_size);
        }
        return max_size;
    }


    int find_most_frequent(unordered_map<int, int> counts) {
        auto max_pair_ptr = max_element(counts.begin(), counts.end(),
                           [](const pair<int,int> &a, const pair<int,int> &b) {
                               return a.second < b.second;
                           });
        return max_pair_ptr->first;
    }
};


TEST_CASE("Examples") {
    auto data = GENERATE(table<int, string, int>({
                {2, "AB", 1},
                {2, "AB", 2},
                {2, "ABC", 1},
                {3, "ABC", 2},
                {4, "ABAB", 2},
                {4, "AABABBA", 1},
                {5, "BYBAABA", 2},
                {7, "BYBAABABBBBO", 2},
    }));

    Solution *solution = new Solution();
    REQUIRE(get<0>(data) == solution->characterReplacement(get<1>(data), get<2>(data)));
}

// Example 1:
// Input: s = "ABAB", k = 2
// Output: 4
// Explanation: Replace the two 'A's with two 'B's or vice versa.
//
// Example 2:
// Input: s = "AABABBA", k = 1
// Output: 4
// Explanation: Replace the one 'A' in the middle with 'B' and form "AABBBBA".
// The substring "BBBB" has the longest repeating letters, which is 4.
