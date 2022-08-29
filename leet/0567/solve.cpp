#include <bits/stdc++.h>
#include <cstddef>
#include <unordered_map>
#include <unordered_set>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"

using namespace std;

void print() {
    cout << '\n';
}

template<typename T, typename ...TAIL>
void print(const T &t, TAIL... tail)
{
    cout << t << ' ';
    print(tail...);
}

// Because of the hash-based map equality check, the solution might yield the wrong result
// with with some small probability. It's still deterministic though. (;p)

class Solution {
public:
    /**
     * Check if a permutation of `s1` is in `s2`
     */
    bool checkInclusion(string s1, string s2) {

        if (s1.size() > s2.size()) {
            return false;
        }

        size_t required_hash = 0;

        for (const char & c : s1) {
            required_hash += char_hasher(c);
        }

        int window_size = s1.size();

        size_t current_hash = 0;
        for (int i = 0; i < window_size; i++) {
            current_hash += char_hasher(s2[i]);
        }

        // slide a window on [left : right), incl-excl
        for (int left = 0; left <= s2.size() - window_size; left++) {
            print(left, current_hash);
            int right = left + window_size;
            if (current_hash == required_hash) {
                return true;
            }
            // character being left behind
            current_hash -= char_hasher(s2[left]);
            current_hash += char_hasher(s2[right]);
        }

        return false;
    }

    size_t char_hasher(char x) {
        return (x * x) ^ 0x01b3;
    }
};


TEST_CASE("Examples") {
    auto data = GENERATE(table<bool, string, string>({
                {true, "ab", "eidbaooo"},
                {false, "ab", "eidboaoo"},
    }));

    Solution *solution = new Solution();
    REQUIRE(get<0>(data) == solution->checkInclusion(get<1>(data), get<2>(data)));
}


// Example 1:

// Input: s1 = "ab", s2 = "eidbaooo"
// Output: true
// Explanation: s2 contains one permutation of s1 ("ba").
// Example 2:

// Input: s1 = "ab", s2 = "eidboaoo"
// Output: false
