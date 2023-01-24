#!/usr/bin/env python3

def solution(arr):
    max_len = len(max(arr, key=len))
    result = []
    for i in range(max_len):
        for word in arr:
            if i < len(word):
                result += word[i]
    return ''.join(result)
