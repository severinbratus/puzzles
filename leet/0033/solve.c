#include <assert.h>
#include <stdint.h>

#define mod(x, n) (n + (x) % n) % (n)

int offset_search(int* nums, int nums_size, int target, int offset);

int search(int* nums, int nums_size, int target){

    if (nums[0] <= nums[nums_size - 1]) {
        return offset_search(nums, nums_size, target, 0);
    }

    // nums are rotated, the sorted sequence wrapping around the edge.
    // first step: find the break:
    // find the maximum index i such that nums[i] > right_peak
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
    /* int ans = max_index; */
    /* assert(nums[mod(max_index + 1, nums_size)] <= right_peak); */
    /* assert(nums[max_index] > right_peak); */

    // run basic search with offset of max_index + 1 mod nums_size
    int offset = mod(max_index + 1, nums_size);
    return offset_search(nums, nums_size, target, offset);
}

// this `inline` makes a lot of difference in mem usage, since LC compiles with the lowest optimization setting.
inline int offset_search(int* nums, int nums_size, int target, int offset){
    int left = 0;
    int right = nums_size - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        int value = nums[mod(offset + mid, nums_size)];
        if (value == target) {
            return mod(offset + mid, nums_size);
        } else if (value < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1;
}
