#include <bits/stdc++.h>
#include <vector>
// #include "../hpp/prettyprint.hpp"

class Solution {
public:
    std::vector<int> twoSum(std::vector<int>& nums, int target) {

        // first, sort the indeces, and the vector

        std::vector<int> indexes(nums.size());
        std::iota(indexes.begin(), indexes.end(), 0);

        // std::cout << indexes << '\n';

        std::sort(indexes.begin(), indexes.end(),
                  [nums](const int a, const int b){ return nums[a] < nums[b]; });

        std::sort(nums.begin(), nums.end());

        // std::cout << nums << '\n';

        int i {0};
        int j {(int) nums.size() - 1};

        while (i < j) {
            int sum {nums[i] + nums[j]};
            if (sum == target) {
                std::vector<int> ret {indexes[i], indexes[j]};
                return ret;
            } else if (sum > target) {
                // decrease sum by decreasing j
                j--;
            } else {
                // sum < target
                // increase sum by increasing i
                i++;
            }
        }
        std::vector<int> ret;
        return ret;
    }
};
