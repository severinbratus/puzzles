#!/usr/bin/env python3

from math import inf
from typing import List

class Solution:
    def findMedianSortedArrays(self, A: List[int], B: List[int]) -> float:
        '''Disclaimer: I didn't come up w/ such an elegant solution on my own.
        I have watched NC's explanation vid before coding.
        '''
        if A == []:
            return self.findMedian(B)
        if B == []:
            return self.findMedian(A)

        # it is most efficient to bin-search on the shortest array
        if len(A) > len(B):
            A, B = B, A

        left_ptr = 0
        right_ptr = len(A) - 1

        # these pointers indicate where the boundary of the left partition in the first array must be.
        # the left partition is the partition where all elements are less than (or equal to) the median are.
        # it is of size (n + m) // 2

        total_size = len(A) + len(B)
        half_size = total_size // 2

        # we perform binary search w/ the two pointers,
        #   to determine the right boundary of this partition in the first array.
        while True:
            # take mid
            # ptr_a = left_ptr + (right_ptr - left_ptr) // 2
            ptr_a = (left_ptr + right_ptr) // 2
            left_part_len_a = ptr_a + 1
            left_part_len_b = half_size - left_part_len_a
            ptr_b = left_part_len_b - 1
            assert(ptr_b == half_size - ptr_a - 2)

            # edges are lazily assumed to carry infinitums

            print(ptr_a)
            a_left = A[ptr_a] if ptr_a >= 0 else -inf
            a_right = A[ptr_a + 1] if (ptr_a + 1) < len(A) else inf

            b_left = B[ptr_b] if ptr_b >= 0 else -inf
            b_right = B[ptr_b + 1] if (ptr_b + 1) < len(B) else inf

            # check if mid_ptr is fit.
            if a_left <= b_right and b_left <= a_right:
                # let's go, this is it.
                if total_size % 2 == 1:
                    # the median is an element of either A or B
                    # because the length of the left partition is really less than half the length,
                    #   we take the first element of the right partition, the min of the partitions of A and B
                    return min(b_right, a_right)
                else:
                    return (max(a_left, b_left) + min(a_right, b_right)) / 2
            elif a_left > b_right:
                # got to decrease the pointer in a, since a_left is too large
                right_ptr = ptr_a - 1
            else:
                left_ptr = ptr_a + 1

    def findMedian(self, X : List[int]) -> float:
        if not X:
            return float('nan')
        # odd len
        if len(X) % 2:
            return X[len(X) // 2]
        # even len
        mid = len(X) // 2
        return (X[mid - 1] + X[mid]) / 2


import pytest

@pytest.mark.parametrize('expected, args', [
    (2, ([1, 2, 3], [])),
    (2, ([1, 2], [3])),
    (2, ([1, 3], [2])),
    (2, ([1], [2, 3])),
    (1, ([1], [])),
    (2, ([1, 2, 3], [1, 2, 3])),
    (3, ([1, 3, 5], [2, 4])),
    (2.5, ([1, 2], [3, 4])),
    (2.5, ([2,3,4], [1]))
])
def test_main(expected, args):
    assert Solution().findMedianSortedArrays(*args) == expected
