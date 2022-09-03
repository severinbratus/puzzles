#include <stdio.h>
#include <stdlib.h>

int missingNumber(int* nums, int nums_size){
    // I tried to be all clever and fancy by traversing the array only once,
    // but the simple boolean-array solutions are much faster.
    long expected_sum = nums_size * (nums_size + 1) / 2;
    long observed_sum = 0;
    for (int i = 0; i < nums_size; i++) {
        observed_sum += nums[i];
    }
    return expected_sum - observed_sum;
}

int main(int argc, char *argv[]) {
    int num_size = argc - 1;
    int *nums = malloc(sizeof(int) * num_size);
    int *ptr = &nums[0];
    for (int argi = 1; argi < argc; argi++) {
        *ptr = atoi(argv[argi]);
        ptr++;
    }
    printf("%d", missingNumber(nums, num_size));
    free(nums);
}
