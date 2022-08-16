#!/usr/bin/env python3

from itertools import *

def split_into(line, block_size):
    return [line[index:index + block_size] for index in range(0, len(line), block_size)]


def decode(channel):

    is_valid = lambda byte: byte < len(channel)

    first_valid_byte = next(filter(is_valid, channel))

    byte = first_valid_byte

    while is_valid(byte):
        byte = channel[byte]

    return chr(byte)


with open('data.txt', 'r') as fin:
    lines = fin.readlines()

data = [[int(octet, 2) for octet in split_into(line.strip(), 8)] for line in lines]

password = ''.join([decode(channel) for channel in data])

print(password)
