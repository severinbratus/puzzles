#include <stdio.h>
#include <stdlib.h>

int hammingWeightNaive(int n) {
    int m = 0;
    while (n) {
        if (n & 1)
            m++;
        n = n >> 1;
    }
    return m;
}

int hammingWeight(int n) {
    int m = 0;
    while (n) {
        n &= (n - 1);
        m++;
    }
    return m;
}

int main(int argc, char *argv[]) {
    printf("%d", hammingWeight(atoi(argv[1])));
}
