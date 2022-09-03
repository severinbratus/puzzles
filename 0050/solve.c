#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

double myPow(double x, int n){
    if (n == 0) {
        return 1;
    } else if (n < 0) {
        return 1.0 / myPow(x, n == INT32_MIN ? INT32_MAX - 1 : -n);
    }

    double y = myPow(x, n / 2);
    if (n % 2 == 0) {
        return y * y;
    } else {
        return y * y * x;
    }
}

/**
 * Attempted an iterative solution based on the one I have written in Scheme for a SICP exercise.
 * Prone to approximation errors, and hence does not pass on LC.
 */
double myPowIter(double x, int n) {
    if (n == 0) {
        return 1;
    } else if (n < 0) {
        return 1.0 / myPowIter(x, n == INT32_MIN ? INT32_MAX - 1 : -n);
    }

    float acc = 1;
    while (n) {
        if (n % 2 == 0) {
            x *= x;
            n /= 2;
        } else {
            acc *= x;
            n--;
        }
    }

    return acc;
}

int main(int argc, char *argv[]) {
    if (argc == 3)
        printf("%f\n", myPowIter(atof(argv[1]), atof(argv[2])));
    else
        printf("uhm...\n");
}
