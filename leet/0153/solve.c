#include <stdint.h>

#define mod(x, n) (n + (x) % n) % (n)

/* almost literally copied from 0033/solve.c */
int findMin(int* nums, int nums_size){
    if (nums[0] <= nums[nums_size - 1]) {
        return nums[0];
    }
    int right_peak = nums[nums_size - 1];
    int left = 0;
    int right = nums_size - 1;
    int mid;
    int max_index = INT32_MIN;
    while (left <= right) {
        mid = left + (right - left) / 2;
        if (nums[mid] <= right_peak) {
            // we are on the right division, move the window left
            right = mid - 1;
        } else {
            // we are on the left division, but this index (mid) may not be the greatest.
            if (max_index < mid)
                max_index = mid;
            left  = mid + 1;
        }
    }
    return nums[mod(max_index + 1, nums_size)];
}
