#include <bits/stdc++.h>
#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"


using namespace std;

class Solution {
public:
int trap(vector<int>& height) {
        int n = height.size();
        vector<int> max_left(n);
        vector<int> max_right(n);

        max_left[0] = height[0];
        for (int i = 1; i < n; i++) {
            max_left[i] = max(height[i], max_left[i - 1]);
        }

        max_right[n - 1] = height[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            max_right[i] = max(height[i], max_right[i + 1]);
        }

        // cout << height << '\n';
        // cout << max_left << '\n';
        // cout << max_right << '\n';
        // cout << '\n';

        // ^ O(N) in time & space

        int sum = 0;
        for (int i = 0; i < n; i++) {
            int min_max = min(max_left[i], max_right[i]);
            sum += min_max - height[i];
        }

        return sum;
    }
};


TEST_CASE("Examples", "[twoSum]") {
    auto data = GENERATE(table<int, std::vector<int>>({
            {9, {4,2,0,3,2,5}},
            {0, {5,4,3,2,1}},
            {1, {2, 1, 2}},
            {2, {2, 0, 2}},
    }));

    Solution *solution = new Solution();
    REQUIRE(std::get<0>(data) == solution->trap(std::get<1>(data)));
}
