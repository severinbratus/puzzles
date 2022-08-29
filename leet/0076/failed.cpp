
#include <bits/stdc++.h>

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
     *
     * This method was an (unsuccessful) experiment in which I have tried to solve the problem with a sort of dynamic hash.
     * This is the test case that breaks it:
     *
     * {
     *   s: "aaaaaaaaaaaabbbbbcdd",
     *   t: "abcdd"
     *   expected: "abbbbbcdd",
     * }
     *
     * The method assumes that the letters that have appeared in `t` must appear in `s` *exactly* the same amount of times as in `t`.
     */
    string minWindow(string s, string t) {
        if (t.size() > s.size()) {
            return "";
        }

        size_t required_hash = 0;
        unordered_set<char> t_char_set;

        for (const char & c : t) {
            required_hash += char_hasher(c);
            t_char_set.insert(c);
        }

        // minimal size of the subsequence
        int min_size = t.size();

        // window is [left:right)
        int left = 0;
        int right = min_size;

        int current_hash = 0;
        for (int i = 0; i < right; i++) {
            if (t_char_set.count(s[i])) {
                current_hash += char_hasher(s[i]);
            }
        }

        // in format (size, left)
        // vector<pair<int, int>> results {};
        pair<int, int> result {INT_MAX, INT_MAX};
        for (; right <= s.size(); right++) {
            if (current_hash == required_hash) {
                int current_size = right - left;
                // results.push_back({current_size, left});
                if (current_size < result.first) {
                    result = {current_size, left};
                }
            }

            // Slide the right pointer, adding a new char
            if (right != s.size()) {

                char new_char = s[right];
                if (t_char_set.count(new_char)) {
                    current_hash += char_hasher(new_char);
                }
            }

            // Only slide the left pointer when we have too many characters in the window
            // There is too many characters in the window iff the current hash is greater than the required hash.
            // Also, keep the window trimmed from the left-side: cut off characters that do not belong to `t`.
            while (left < s.size() && (current_hash > required_hash || !t_char_set.count(s[left]))) {
                char left_char = s[left]; // pun alert: left character is being left
                if (t_char_set.count(left_char)) {
                    current_hash -= char_hasher(left_char);
                }
                left++;
            }
        }

        if (result != make_pair(INT_MAX, INT_MAX)) {
            int found_size = result.first;
            int found_left = result.second;
            return string(s.begin() + found_left, s.begin() + found_left + found_size);
        } else {
            return "";
        }
    }

    size_t char_hasher(char x) {
        return (x * x) ^ 0x01b3;
    }
};
