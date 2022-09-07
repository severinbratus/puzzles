#define CATCH_CONFIG_FAST_COMPILE
#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
// #include "../hpp/prettyprint.hpp"
#include "solve.c"

using namespace std;

TEST_CASE("Examples") {
    auto data = GENERATE(table<int, vector<int>, int>({
                {0, {1}, 1},
                {-1, {1}, 0},
                {1, {1, 2}, 2},
                {1, {2, 1}, 1},
                {4, {4,5,6,7,0,1,2}, 0},
                {-1, {4,5,6,7,0,1,2}, 3},
                {-1, {4, 5, 6, 0, 2, 3}, 7},
                {5, {4, 5, 6, 0, 2, 3}, 3},
                {0, {6, 0, 2, 3}, 6},
    }));

    int expected = get<0>(data);
    int *nums = &get<1>(data)[0];
    int nums_size = get<1>(data).size();
    int target = get<2>(data);

    REQUIRE(expected == search(nums, nums_size, target));
}

// Example 1:
// Input: nums = [4,5,6,7,0,1,2], target = 0
// Output: 4
//
// Example 2:
// Input: nums = [4,5,6,7,0,1,2], target = 3
// Output: -1
//
// Example 3:
// Input: nums = [1], target = 0
// Output: -1
