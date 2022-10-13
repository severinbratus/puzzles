#include <bits/stdc++.h>
#include <unordered_map>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"

using namespace std;

class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        int fast = 0;
        int slow = 0;
        while (1) {
            fast = nums[fast];
            fast = nums[fast];
            slow = nums[slow];
            if (fast == slow) {
                break;
            }
        }
        fast = 0;
        while (1) {
            fast = nums[fast];
            slow = nums[slow];
            if (fast == slow)
                break;
        }
        return fast;
    }

    int findDuplicateNaive(vector<int>& nums) {
        unordered_set<int> seen {};
        for (const int & x : nums) {
            if (seen.count(x))
                return x;
            seen.insert(x);
        }
        return 0;
    }
};
