#include <set>
using namespace std;

class Solution {
public:
    bool isHappy(int n) {
        set<int> visited {};
        while (true) {
            if (n == 1)
                return true;
            if (visited.count(n))
                return false;
            visited.insert(n);
            int new_n = 0;
            while (n) {
                int dig = n % 10;
                new_n += dig * dig;
                n /= 10;
            }
            n = new_n;
        }
    }
};
