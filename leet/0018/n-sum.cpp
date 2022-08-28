#include <bits/stdc++.h>
#include "../hpp/prettyprint.hpp"


using namespace std;


class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        return n_sum_sorted(3, nums, 0, nums.size(), 0);
    }


    vector<vector<int>> fourSum(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());
        return n_sum_sorted(4, nums, 0, nums.size(), target);
    }


    size_t hashem(int i, int j) {
        hash<int> hasher {};
        size_t seed = 2;
        seed ^= hasher(i) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        seed ^= hasher(j) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        return seed;
    }


    /**
     * Return unique n-tuple with numbers from `nums` that sum up to `target`
     */
    vector<vector<int>> n_sum_sorted(int n, vector<int>& nums, int begin, int end, long long target) {
        if (n == 0) {
            return {};
        } else if (n == 1) {
            for (int i = begin; i < end; i++) {
                if (nums[i] == target)
                    return {{(int) target}};
            }
            return {};
        } else if (n == 2) {
            int i = begin;
            int j = end - 1;
            vector<vector<int>> result {};
            unordered_set<int> visited {};
            while (i < j) {
                int sum = nums[i] + nums[j];
                if (sum < target) {
                    // sum too small
                    i++;
                } else if (sum > target) {
                    // sum too large
                    j--;
                } else {
                    // sum fits
                    if (!visited.count(hashem(nums[i], nums[j]))) {
                        visited.insert(hashem(nums[i], nums[j]));
                        result.push_back({nums[i], nums[j]});
                    }
                    // still move one of the pointers
                    i++;
                }
            }
            return result;
        } else {
            vector<vector<int>> result {};
            unordered_set<int> visited {};
            for (int k = begin; k < end; k++) {
                if (!visited.count(nums[k])) {
                    visited.insert(nums[k]);
                    vector<vector<int>> subresult = n_sum_sorted(n - 1, nums, k + 1, end, target - nums[k]);
                    for (const auto values : subresult) {
                        vector<int>* full_values = new vector<int>();
                        full_values->insert(full_values->end(), nums[k]);
                        full_values->insert(full_values->end(), values.begin(), values.end());
                        result.push_back(*full_values);
                    }
                }
            }
            return result;
        }
    }
};
