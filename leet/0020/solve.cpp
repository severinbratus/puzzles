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
        stack<int> fifo {};
        for (const char & c : s) {
            if (c == '}' or c ==']' or c == ')') {
                if (fifo.empty() or close_to_open[c] != fifo.top())
                    return false;
                fifo.pop();
            } else {
                fifo.push(c);
            }
        }
        return fifo.empty();
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
