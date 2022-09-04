#include <bits/stdc++.h>
#include <cstdint>
#include <vector>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"

using namespace std;


class Solution {
public:
    int carFleet(int target, vector<int>& position, vector<int>& speed) {
        // So: we sort the cars by position.
        // We compute the expected time of arrival.
        // Now if the ETA of a car is lower than (or same as) that of a the one in front of it, they will form a fleet;
        // If not, they do not meet.
        int n = position.size();
        vector<int> indexes_by_position(position.size());
        iota(indexes_by_position.begin(), indexes_by_position.end(), 0);
        sort(indexes_by_position.begin(), indexes_by_position.end(), [&position, &speed](const int & a, const int & b) {
            return position[a] < position[b];
        });
        // vector<float> eta(position.size());
        float max_eta = INT32_MIN;
        int count_maxes = 0;
        for (int i = n - 1; i >= 0; i--) {
            int index = indexes_by_position[i];
            float eta = ((float) target - position[index]) / speed[index];
            // if (eta[index] > max_eta) {
            if (eta > max_eta) {
                max_eta = eta;
                count_maxes++;
            }
        }
        // cout << "pos: " << position << endl;
        // cout << "spd: " << speed << endl;
        // cout << "eta: " << eta << endl;
        return count_maxes;
    }
};


TEST_CASE("Examples") {
    auto data = GENERATE(table<int, int, vector<int>, vector<int>>({
            {3, 12, {10, 8, 0, 5, 3}, {2, 4, 1, 1, 3}},
            {1, 10, {3}, {3}},
            {1, 100, {0, 2, 4}, {4, 2, 1}},
            {2, 10, {6, 8}, {3, 2}},
            {1, 10, {6, 8}, {4, 2}},
    }));

    Solution *solution = new Solution();
    REQUIRE(get<0>(data) == solution->carFleet(get<1>(data), get<2>(data), get<3>(data)));
}

// Input: target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]
// Output: 3
//
// Input: target = 10, position = [3], speed = [3]
// Output: 1
//
// Input: target = 100, position = [0,2,4], speed = [4,2,1]
// Output: 1

// Input: 10, [6,8], [3,2]
// Expected: 2


// Runtime: 501 ms, faster than 18.94% of C++ online submissions for Car Fleet.
// Memory Usage: 72.5 MB, less than 99.14% of C++ online submissions for Car Fleet.
// Comment: I guess I was somehow supposed to use a stack for this?
// Time O(nlogn), Space O(n)
