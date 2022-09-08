#!/usr/bin/env python3

class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        # Represent numbers as reversed integer lists.
        rnum1 : tuple[int] = tuple(reversed(list(map(int, num1))))
        rnum2 : tuple[int] = tuple(reversed(list(map(int, num2))))

        acc = []
        for index, digit in enumerate(rnum2):
            add(acc, digit_multiply(rnum1, digit, offset=index))

        trim(acc)

        return ''.join(str(x) for x in reversed(acc))


def add(dest : list[int], source : list[int] | tuple[int, ...]) -> None:
    carry = 0
    index = 0
    while index < len(source) or carry:
        a = dest[index] if index < len(dest) else 0
        b = source[index] if index < len(source) else 0
        summed = a + b + carry
        if index < len(dest):
            dest[index] = summed % 10
        else:
            dest.append(summed % 10)
        carry = summed // 10
        index += 1


def digit_multiply(source, digit : int, offset=0) -> list[int]:
    dest = []
    carry = 0
    index = 0
    while index < len(source) or carry:
        a = source[index] * digit if index < len(source) else 0
        summed = a + carry
        dest.append(summed % 10)
        carry = summed // 10
        index += 1

    for _ in range(offset):
        dest.insert(0, 0)

    return dest


def trim(dest : list[int]):
    while len(dest) > 1 and dest[-1] == 0:
        dest.pop()

