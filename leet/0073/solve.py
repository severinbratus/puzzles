#!/usr/bin/env python3

from typing import List

class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        row = True
        col = True
        n = len(matrix)
        m = len(matrix[0])

        def null_row(i):
            for j in range(m):
                matrix[i][j] = 0

        def null_col(j):
            for i in range(n):
                matrix[i][j] = 0

        for i in range(n):
            for j in range(m):
                value = matrix[i][j]
                if value == 0:
                    if i == 0:
                        row = False
                    else:
                        matrix[i][0] = 0
                    if j == 0:
                        col = False
                    else:
                        matrix[0][j] = 0

        for i in range(1, n):
            if matrix[i][0] == 0:
                null_row(i)
        for j in range(1, m):
            if matrix[0][j] == 0:
                null_col(j)

        # null first row and col last, if at all
        if not row:
            null_row(0)
        if not col:
            null_col(0)



import pytest

@pytest.mark.parametrize('expected, arg', [
    (
        [[1,0,1],[0,0,0],[1,0,1]],
        [[1,1,1],[1,0,1],[1,1,1]],
    ),
    (
        [[0,0,0,0],[0,4,5,0],[0,3,1,0]],
        [[0,1,2,0],[3,4,5,2],[1,3,1,5]],
    ),
])
def test_main(expected, arg):
    Solution().setZeroes(arg)
    assert expected == arg
