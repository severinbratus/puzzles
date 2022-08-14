#include <vector>
#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "solution-2.cpp"

// TEST_CASE( "Example 1", "[twoSum]" ) {
//     std::vector<int> expected {0, 1};
//     std::vector<int> nums {2,7,11,15};
//     int target {9};
//     Solution *solution = new Solution();
//     std::vector<int> observed {solution->twoSum(nums, target)};
//     REQUIRE(observed == expected);
// }

// Example 1:
// Input: nums = [2,7,11,15], target = 9
// Output: [0,1]
// Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
//
// Example 2:
// Input: nums = [3,2,4], target = 6
// Output: [1,2]
//
// Example 3:
// Input: nums = [3,3], target = 6
// Output: [0,1]

TEST_CASE("Examples", "[twoSum]") {
    auto data = GENERATE(table<std::vector<int>, std::vector<int>, int>({
            {{0, 1}, {2, 7, 11, 15}, 9},
            {{1, 2}, {3, 2, 4}, 6},
            {{0, 1}, {3, 3}, 6}
    }));

    // REQUIRE(strlen(std::get<0>(data)) == static_cast<size_t>(std::get<1>(data)));

    Solution *solution = new Solution();
    REQUIRE(std::get<0>(data) == solution->twoSum(std::get<1>(data), std::get<2>(data)));
}
