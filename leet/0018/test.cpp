#include <vector>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "n-sum.cpp"


TEST_CASE("n_sum_sorted", "[n_sum_sorted]") {
    auto data = GENERATE(table<int, vector<vector<int>>, vector<int>>({
            {2, {{-2,2}}, {-2,2,3,4,5}},
            {3, {{-2,1,1}}, {-2,1,1,4,5}},
            {3, {{-4,0,4}, {-2,1,1}}, {-4,-2,0,1,1,4,5}},
            {4, {{-4,-2,1,5}, {-2,0,1,1}}, {-4,-2,0,1,1,4,5}},

    }));

    Solution *solution = new Solution();
    auto expected = std::get<1>(data);
    auto n = std::get<0>(data);
    auto nums = std::get<2>(data);
    REQUIRE(expected == solution->n_sum_sorted(n, nums, 0, nums.size(), 0));
}

TEST_CASE("threeSum", "[threeSum]") {
    auto data = GENERATE(table<vector<vector<int>>, vector<int>>({
            {{{-2,1,1}}, {-2,1,1,4,5}},
            {{{-4,0,4}, {-2,1,1}}, {-4,-2,0,1,1,4,5}},
            {{{-1,-1,2}, {-1,0,1}}, {-1,0,1,2,-1,-4}},
            {{{-4,-2,6}, {-4,0,4}, {-4,1,3}, {-4,2,2}, {-2,-2,4}, {-2,0,2}}, {-4,-2,-2,-2,0,1,2,2,2,3,3,4,4,6,6}},
            {{{0, 0, 0}}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}},
    }));

    Solution *solution = new Solution();
    auto expected = std::get<0>(data);
    auto nums = std::get<1>(data);
    REQUIRE(expected == solution->threeSum(nums));
}

TEST_CASE("fourSum: negative values", "[fourSum]") {
    vector<int> nums {1,0,-1,0,-2,2};
    int target {0};

    Solution *solution = new Solution();
    solution->fourSum(nums, target);
}

TEST_CASE("fourSum: extremely large values", "[fourSum]") {
    // Int limit      2147483647
    vector<int> nums {1000000000,1000000000,1000000000,1000000000};
    int target       {-294967296};
    vector<vector<int>> expected {};

    Solution *solution = new Solution();
    REQUIRE(expected == solution->fourSum(nums, target));
}
