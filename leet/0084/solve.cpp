#include <bits/stdc++.h>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"

using namespace std;

class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        vector<int> index_stack {};
        vector<int> height_stack {};
        int max_area = 0;
        heights.push_back(0);
        for (int right_index = 0; right_index < heights.size(); right_index++) {
            int new_height = heights[right_index];
            int left_index = right_index;
            // what now???
            // we want a monotonically increasing stack.
            // when a value is greater then the top of the stack in height, we simply push it.
            // otherwise, value is less than or equal to the top,
            //   so we can extend the index of the lesser height backwards,
            //   the greater height is simply discarded from the stack.
            while (!height_stack.empty() && height_stack.back() >= new_height) {
                left_index = index_stack.back();
                int left_height = height_stack.back();
                height_stack.pop_back();
                index_stack.pop_back();
                int width = right_index - left_index;
                max_area = max(max_area, width * left_height);
            }
            height_stack.push_back(new_height);
            index_stack.push_back(left_index);
        }
        height_stack.pop_back();
        return max_area;
    }
};

TEST_CASE("Examples") {
    auto data = GENERATE(table<int, vector<int>>({
                {10, {2,1,5,6,2,3}},
                {4, {2, 4}},
                {0, {0}},
                {0, {0, 0, 0}},
                {1, {1}},
                {2, {2}},
                {2, {1, 1}},
                {4, {2, 3}},
                {4, {3, 2}},
                {4, {3, 2, 1}},
                {3, {1, 1, 0, 3}},
                {9, {1, 2, 3, 4, 5}},
    }));

    Solution *solution = new Solution();
    REQUIRE(get<0>(data) == solution->largestRectangleArea(get<1>(data)));
}

// Input: heights = [2,1,5,6,2,3]
// Output: 10
