#include <bits/stdc++.h>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"

using namespace std;


class Solution {
public:
    bool isValid(string s) {
        map<char, char> close_to_open {
            {'}', '{'},
            {']', '['},
            {')', '('},
        };
        stack<int> lifo {};
        for (const char & c : s) {
            if (c == '}' or c ==']' or c == ')') {
                if (lifo.empty() or close_to_open[c] != lifo.top())
                    return false;
                lifo.pop();
            } else {
                lifo.push(c);
            }
        }
        return lifo.empty();
    }
};


TEST_CASE("Examples") {
    auto data = GENERATE(table<bool, string>({
                {true, "()"},
                {true, "([])"},
                {true, "([{}])"},
                {false, "(()"},
                {false, "([)]"},
                {false, "[]]"},
    }));

    Solution *solution = new Solution();
    REQUIRE(std::get<0>(data) == solution->isValid(std::get<1>(data)));
}
