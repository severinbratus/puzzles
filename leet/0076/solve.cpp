#include <algorithm>
#include <bits/stdc++.h>
#include <cstddef>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"

using namespace std;

void print() {
    cout << endl;
}

template<typename T, typename ...TAIL>
void print(const T &t, TAIL... tail)
{
    cout << t << ' ';
    print(tail...);
}


class Solution {
public:
    /**
     * Find a subsequence derived from `t` in `s`
     * */
    string minWindow(string s, string t) {

        if (t.size() > s.size()) {
            return "";
        }

        unordered_map<char, int> required {};
        for (const char & _char : t) {
            required[_char] = required.count(_char) ? required[_char] + 1 : 1;
        }
        int unsatisfied = required.size();

        int left_ptr = 0;
        int right_ptr = t.size();

        for (int i = 0; i < right_ptr; i++) {
            if (required.count(s[i])) {
                required[s[i]]--;
                if (required[s[i]] == 0) {
                    unsatisfied--;
                }
            }
        }

        pair<int, int> result {INT_MAX, INT_MAX};

        for (; right_ptr <= s.size(); right_ptr++) {
            // if (is_satisfied(required)) {
            if (unsatisfied == 0) {
                int current_size = right_ptr - left_ptr;
                // results.push_back({current_size, left_ptr});
                if (current_size < result.first) {
                    result = {current_size, left_ptr};
                }
            }
            // add char under right pointer
            if (right_ptr != s.size()) {
                char new_char = s[right_ptr];
                if (required.count(new_char)) {
                    required[new_char]--;
                    if (required[new_char] == 0) {
                        unsatisfied--;
                    }
                }
            }
            // slide left pointer as far as possible
            while (left_ptr < right_ptr && (!required.count(s[left_ptr]) || required[s[left_ptr]] < 0)) {
                if (required.count(s[left_ptr])) {
                    required[s[left_ptr]]++;
                    assert(required[s[left_ptr]] <= 0);
                }
                left_ptr++;
            }
        }

        if (result != make_pair(INT_MAX, INT_MAX)) {
            int found_size = result.first;
            int found_left_ptr = result.second;
            return string(s.begin() + found_left_ptr, s.begin() + found_left_ptr + found_size);
        } else {
            return "";
        }
    }

    bool is_satisfied(unordered_map<char, int> required) {
        for (const pair<char, int> & kv_pair : required) {
            if (kv_pair.second > 0)
                return false;
        }
        return true;
    }

};


TEST_CASE("Examples") {
    auto data = GENERATE(table<string, string, string>({
                {"BANC", "ADOBECODEBANC", "ABC"},
                {"a", "a", "a"},
                {"", "a", "aa"},
                {"", "a", "b"},
                {"you", "if you are", "yu"},
                {"ding", "reading this", "dg"},
                {"probab", "i am probably dead", "bbp"},
                {"abbbbbcdd", "aaaaaaaaaaaabbbbbcdd", "abcdd"},
                {"xyzzz", "xyzzzzz", "zyzzx"},
    }));

    Solution *solution = new Solution();
    REQUIRE(get<0>(data) == solution->minWindow(get<1>(data), get<2>(data)));
}

// Example 1:

// Input: s = "ADOBECODEBANC", t = "ABC"
// Output: "BANC"
// Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.
// Example 2:

// Input: s = "a", t = "a"
// Output: "a"
// Explanation: The entire string s is the minimum window.
// Example 3:

// Input: s = "a", t = "aa"
// Output: ""
// Explanation: Both 'a's from t must be included in the window.
// Since the largest window of s only has one 'a', return empty string.
