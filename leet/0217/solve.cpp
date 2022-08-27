#include <bits/stdc++.h>

class Solution {
public:
    bool containsDuplicate(std::vector<int>& nums) {
        std::unordered_set<int> lookup {};
        for (const int num : nums) {
            if (lookup.count(num))
                return true;
            lookup.insert(num);
        }
        return false;
    }
};
