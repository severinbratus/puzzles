#!/usr/bin/env python3

class HashMap:
    store = {}
    key_offset = 0
    value_offset = 0

    def insert(self, x, y):
        self.store[x - self.key_offset] = y - self.value_offset

    def get(self, x):
        return self.store[x - self.key_offset] + self.value_offset

    def addToKey(self, x):
        self.key_offset += x

    def addToValue(self, y):
        self.value_offset += y

    def __repr__(self):
        return f"HashMap({self.store=}, {self.key_offset=}, {self.value_offset=})"


def solution(queryType, query):
    hm = HashMap()
    lookup = {
        "insert": hm.insert,
        "get": hm.get,
        "addToKey": hm.addToKey,
        "addToValue": hm.addToValue,
    }
    ans = 0
    for cmd_type, args, in zip(queryType, query):
        cmd = lookup[cmd_type]
        ret_val = cmd(*args)
        if cmd_type == "get":
            ans += ret_val
    return ans
