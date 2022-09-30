#include <stdlib.h>
#include <stdio.h>

/* Good ol' Fibbonacci */
int climbStairs(int n){
    int dp[n + 1];
    dp[0] = 1; // ???
    dp[1] = 1;
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    return dp[n];
}

int climbStairsV2(int n) {
    if (n == 0 || n == 1)
        return 1;
    int a = 1;
    int b = 1;
    int tmp;
    for (int i = 2; i <= n; i++) {
        tmp = a + b;
        a = b;
        b = tmp;
    }
    return b;
}


int main(int argc, char *argv[]) {
    printf("%d\n", climbStairsV2(atoi(argv[1])));
}
