#include <stdlib.h>
#include <stdint.h>

#define CATCH_CONFIG_FAST_COMPILE
#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"
#include "solve.c"

using namespace std;

TEST_CASE("Examples") {
    auto data = GENERATE(table<int, vector<int>, int>({
            {4, {3, 6, 7, 11}, 8},
            {30, {30, 11, 23, 4, 20}, 5},
            {23, {30, 11, 23, 4, 20}, 6},
            {1, {312884470}, 968709470},
            // ^ what is this?
            // koko has 968,709,470 hours to eat 312,884,470
            // unsigned int max limit is 2,147,483,648
            // minimal possible value of k is 1, w/ koko eating for 312M hours, and waiting the other ~600M idly.
    }));

    int expected = get<0>(data);
    int *piles = &get<1>(data)[0];
    int allowed_hours = get<2>(data);

    REQUIRE(expected == minEatingSpeed(piles, get<1>(data).size(), allowed_hours));
}

// Example 1:
// Input: piles = [3,6,7,11], h = 8
// Output: 4

// Example 2:
// Input: piles = [30,11,23,4,20], h = 5
// Output: 30

// Example 3:
// Input: piles = [30,11,23,4,20], h = 6
// Output: 23
