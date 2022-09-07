#include <stdbool.h>

/* A rather unsophisticated approach - act as if the matrix were flat, and do plain bin-search on it.
 * O(log(n * m)) = O(log(n) + log(m))
 */
bool searchMatrix(int** matrix, int matrixSize, int* matrixColSize, int target){
    int numsSize = *matrixColSize * matrixSize;
    int left = 0;
    int right = numsSize - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        int value = matrix[mid / *matrixColSize][mid % *matrixColSize];
        if (value == target) {
            return true;
        } else if (value < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return false;
}
