#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>

/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* plusOne(int* digits, int digits_size, int* return_size) {
    int * result = (int *) malloc((digits_size + 1) * sizeof(int));
    *return_size = digits_size;
    int carry = 1;
    for (int idx = digits_size - 1; idx >= 0; idx--) {
        carry += digits[idx];
        result[idx + 1] = carry % 10;
        carry /= 10;
    }
    if (carry) {
        result[0] = 1;
        (*return_size)++;
        return result;
    }
    else {
        return result + 1;
    }
}
