#include <bits/stdc++.h>
#include <vector>

#define CATCH_CONFIG_MAIN
#include "../hpp/catch.hpp"
#include "../hpp/prettyprint.hpp"

using namespace std;


class Solution {
public:
    // vvv A clear case of over-thinking (or is it under-thinking?)
    int maxProfitSlow(vector<int>& prices) {
        int n = prices.size();
        if (n == 1)
            return 0;
        vector<int> max_right(n);
        max_right[n - 1] = prices[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            max_right[i] = max(prices[i], max_right[i + 1]);
        }
        // ^^^ O(n) memory
        int max_profit = 0;
        assert(max_profit == 0);
        // from 0 to n - 1 incl.
        for (int i = 0; i < n - 1; i++) {
            int profit = max_right[i + 1] - prices[i];
            if (profit > max_profit)
                max_profit = profit;
        }
        return max_profit;
    }

    int maxProfit(vector<int>& prices) {
        int n = prices.size();
        if (n == 1)
            return 0;
        int max_profit = 0;
        int min_price = prices[0];
        for (int i = 0; i < n - 1; i++) {
            if (prices[i] < min_price)
                min_price = prices[i];
            // As if we sell at `i + 1`, having bought at some point in `0...i`.
            int profit = prices[i + 1] - min_price;
            if (profit > max_profit)
                max_profit = profit;
        }
        return max_profit;
    }
};

TEST_CASE("Examples", "[maxProfit]") {
    auto data = GENERATE(table<int, std::vector<int>>({
                {0, {1}},
                {0, {1,1}},
                {2, {1,1,3}},
                {2, {1,3,1}},
                {5, {7,1,5,3,6,4}},
                {0, {7,6,4,3,1}},
    }));

    Solution *solution = new Solution();
    REQUIRE(std::get<0>(data) == solution->maxProfit(std::get<1>(data)));
}
