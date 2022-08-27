#include <vector>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "solve.cpp"

TEST_CASE("Examples", "[twoSum]") {
    auto data = GENERATE(table<bool, std::vector<int>>({
                {true, {1, 1}},
                {false, {1}},
                {true, {1, 2, 3, 2}},
    }));

    Solution *solution = new Solution();
    REQUIRE(std::get<0>(data) == solution->containsDuplicate(std::get<1>(data)));
}
