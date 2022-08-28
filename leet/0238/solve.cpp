#include <bits/stdc++.h>
#include <vector>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"


using namespace std;


class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();

        vector<int> left_prod(n);
        left_prod[0] = nums[0];
        for (int i = 1; i < n; i++) {
            left_prod[i] = nums[i] * left_prod[i - 1];
        }

        vector<int> right_prod(n);
        right_prod[n - 1] = nums[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            right_prod[i] = nums[i] * right_prod[i + 1];
        }

        vector<int> answer(n);
        for (int i = 0; i < n; i++) {
            answer[i] = 1;
            if (i != 0) {
                answer[i] *= left_prod[i - 1];
            }
            if (i != n - 1) {
                answer[i] *= right_prod[i + 1];
            }
        }

        // cout << nums << '\n';
        // cout << left_prod << '\n';
        // cout << right_prod << '\n';
        // cout << answer << '\n';

        // ^^^ Idea: it is as if we were doing dynamic programming on multiplication.

        return answer;
    }
};

TEST_CASE("Examples") {
    auto data = GENERATE(table<std::vector<int>, std::vector<int>>({
            {{24,12,8,6}, {1,2,3,4}},
            {{0,0,9,0,0}, {-1,1,0,-3,3}},
    }));

    Solution *solution = new Solution();
    REQUIRE(std::get<0>(data) == solution->productExceptSelf(std::get<1>(data)));
}

// Example 1:
// Input: nums = [1,2,3,4]
// Output: [24,12,8,6]
//
// Example 2:
// Input: nums = [-1,1,0,-3,3]
// Output: [0,0,9,0,0]
