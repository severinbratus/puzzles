#!/usr/bin/env python3

#!/usr/bin/env python3

from itertools import product

def solution(s):

    n = len(s)
    ans = 0
    for i in range(1, (n - 2) + 1):
        for j in range(i + 1, n):
            a = s[:i]
            b = s[i:j]
            c = s[j:]
            if len(a) and len(b) and len(c):
                if a + b != b + c and a + b != c + a and b + c != c + a:
                    ans += 1
    return ans



from itertools import product

def solution(field, x, y):
    canvas = [[-1 for j in range(len(field[0]))] for i in range(len(field))]
    reveal(field, x, y, canvas)
    return canvas


def reveal(field, x, y, canvas):
    '''Mutate on canvas'''
    if field[x][y]:
        return
    canvas[x][y] = count_mines(field, x, y)
    if canvas[x][y] == 0:
        for x_a, y_a in get_adj(field, x, y):
            if canvas[x_a][y_a] == -1:
                reveal(field, x_a, y_a, canvas)


def count_mines(field, x, y):
    return sum(int(field[x_a][y_a]) for x_a, y_a in get_adj(field, x, y))


def get_adj(field, x, y):
    w = len(field)
    h = len(field[0])
    for diff in product(range(-1, 2), repeat=2):
        if diff != (0, 0):
            x_a = x + diff[0]
            y_a = y + diff[1]
            if 0 <= x_a < w and 0 <= y_a < h:
                yield x_a, y_a


from collections import Counter

def solution(a):
    all_number_digits = [len(str(x)) for x in a]
    number_digits_counter = Counter(all_number_digits)
    number_digits_min = min(all_number_digits)
    number_digits_max = max(all_number_digits)

    # print(number_digits_counter)

    # add for all the addends, where a[i] is in the second position
    ans = sum(a) * len(a)
    print(ans)
    for i in range(len(a)):
        # add for all the addends, where a[i] is in the first position
        for number_digits in range(number_digits_min, number_digits_max + 1):
            # print(f"{number_digits=}")
            # print(f"{a[i]=}")
            comp = a[i] * (10 ** number_digits) * number_digits_counter[number_digits]
            # print(f"{comp=}")
            # print()
            ans += comp
    return ans
