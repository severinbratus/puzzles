#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int get_len(uint num) {
    int len = 0;
    while (num) {
        num /= 10;
        len++;
    }
    return len;
}

int reverse(int num) {
    int sign = num > 0 ? 1 : -1;
    if (num == INT32_MIN) return 0;
    int absval = num > 0 ? num : -num;
    int length = get_len(absval);
    int index = 0;
    long result = 0;

    long powers[length + 1];
    powers[0] = 1;
    for (int i = 1; i <= length; i++) {
        powers[i] = 10 * powers[i - 1];
    }

    while (absval) {
        // i-th digit.
        long digit = absval % 10;
        result += powers[length - index - 1] * digit;
        absval /= 10;
        index++;
    }

    if (INT32_MIN <= result && result <= INT32_MAX) {
        return sign * result;
    } else {
        return 0;
    }
}

int main(int argc, char *argv[]) {
    printf("%d\n", reverse(atoi(argv[1])));
}
