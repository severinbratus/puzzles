#include <bits/stdc++.h>
#include <vector>
// #include "prettyprint.hpp"

class Solution {
public:
    std::vector<int> twoSum(std::vector<int>& nums, int target) {
        std::unordered_map<int, int> lookup;
        int n = nums.size();

        for (int i = 0; i < n; i++) {
            lookup[nums[i]] = i;
        }

        for (int i = 0; i < n; i++) {
            if (lookup.count(target - nums[i]) && lookup[target - nums[i]] != i) {
                std::vector<int> ret { i, lookup[target - nums[i]] };
                return ret;
            }
        }

        std::vector<int> ret;
        return ret;

    }
};
