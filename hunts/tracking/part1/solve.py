#!/usr/bin/env python3

with open('data.txt') as fin:
    data = fin.read().strip()

from base64 import *

# bytedata = b64decode(data)

def find_window(seq, pred, size=16):

    for index in range(len(seq) - size + 1):

        window = seq[index:index + size]
        if pred(window):

            yield window

def pred(window):
    return len(window) == len(set(window))

result = list(find_window(data, pred))
assert len(result) == 1

print(b64decode(result[0]).decode())
