#include <bits/stdc++.h>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"

using namespace std;

class Solution {
public:
    int maxArea(vector<int>& height) {
        int l = 0;
        int r = height.size() - 1;
        int max_area = 0;
        while (l < r) {
            int area = min(height[l], height[r]) * (r - l);
            if (area > max_area)
                max_area = area;
            // move the pointers greedily (?)
            // reasoning:
            // we will move one of the pointers,
            // so we will move the less promising one.
            if (height[l] > height[r]) {
                r--;
            } else {
                l++;
            }
        }
        return max_area;
    }
};

TEST_CASE("Examples", "[maxArea]") {
    auto data = GENERATE(table<int, std::vector<int>>({
                {49, {1,8,6,2,5,4,8,3,7}},
                {1, {1,1}}
    }));

    Solution *solution = new Solution();
    REQUIRE(std::get<0>(data) == solution->maxArea(std::get<1>(data)));
}
