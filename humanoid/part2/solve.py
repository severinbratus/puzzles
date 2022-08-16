#!/usr/bin/env python3

from collections import Counter

with open("data.txt") as fin:
    data = fin.read().strip()

counter = Counter(data)
base = [counter.most_common(1)[0][0]]

while base[-1] != ';':
    occurr_indexes = filter(lambda index: data[index] == base[-1], range(len(data)))
    chars_after = [data[index + 1] for index in occurr_indexes if index != len(data) - 1]
    counter_after = Counter(chars_after)
    base.append(counter_after.most_common(1)[0][0])

print(''.join(base))
