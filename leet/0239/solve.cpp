#include <bits/stdc++.h>
#include <cstddef>
#include <queue>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"

using namespace std;

void print() {
    cout << '\n';
}

template<typename T, typename ...TAIL>
void print(const T &t, TAIL... tail)
{
    cout << t << ' ';
    print(tail...);
}

class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        // heap to hold the maximum element
        priority_queue<int> heap {};

        vector<int> maxes {};
        unordered_map<int, int> counts {};

        int left_ptr = 0, right_ptr = k;

        // add initial window
        for (int i = left_ptr; i < right_ptr; i++) {
            heap.push(nums[i]);
            counts[nums[i]] = counts.count(nums[i]) ? counts[nums[i]] + 1 : 1;
        }

        // window is [left_ptr : right_ptr)
        for (; right_ptr <= nums.size(); left_ptr++, right_ptr++) {
            // find top of the heap that is actually in the window
            // as we cannot find & delete elements from the heap, we simply discard invalid heap-tops until finding a valid one.
            while (!counts.count(heap.top()) || counts[heap.top()] == 0) {
                heap.pop();
            }
            int new_max = heap.top();
            maxes.push_back(new_max);
            if (right_ptr != nums.size()) {
                // slide elements
                // one num left behind
                int left_num = nums[left_ptr];
                counts[left_num] = max(0, counts[left_num] - 1);
                // here we would remove one instance of `left_num` from `heap`, but that is impossible
                // one new num on the right
                int new_num = nums[right_ptr];
                counts[new_num] = counts.count(new_num) ? counts[new_num] + 1 : 1;
                heap.push(new_num);
            }
        }

        return maxes;
    }
};

TEST_CASE("Examples") {
    auto data = GENERATE(table<vector<int>, vector<int>, int>({
            {{1}, {1}, 1},
            {{3,3,5,5,6,7}, {1,3,-1,-3,5,3,6,7}, 3},
    }));

    Solution *solution = new Solution();
    REQUIRE(get<0>(data) == solution->maxSlidingWindow(get<1>(data), get<2>(data)));
}

// Example 1:

// Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
// Output: [3,3,5,5,6,7]
// Explanation:
// Window position                Max
// ---------------               -----
// [1  3  -1] -3  5  3  6  7       3
//  1 [3  -1  -3] 5  3  6  7       3
//  1  3 [-1  -3  5] 3  6  7       5
//  1  3  -1 [-3  5  3] 6  7       5
//  1  3  -1  -3 [5  3  6] 7       6
//  1  3  -1  -3  5 [3  6  7]      7
// Example 2:

// Input: nums = [1], k = 1
// Output: [1]
