#!/usr/bin/env python3

from solve import DetectSquares

def test_1():
    obj = DetectSquares()
    obj.add([0, 0])
    assert obj.count([0, 0]) == 0
    obj.add([1, 0])
    assert obj.count([0, 0]) == 0
    assert obj.count([1, 0]) == 0
    obj.add([1, 1])
    assert obj.count([0, 0]) == 0
    assert obj.count([1, 0]) == 0
    assert obj.count([1, 1]) == 0
    obj.add([0, 1])
    assert obj.count([0, 0]) == 1
    assert obj.count([1, 0]) == 1
    assert obj.count([1, 1]) == 1
    assert obj.count([0, 1]) == 1


def test_2():
    obj = DetectSquares()

    obj.add([0, 0])
    obj.add([0, 1])
    obj.add([1, 0])
    obj.add([1, 1])

    obj.add([2, 0])
    obj.add([0, 2])
    obj.add([2, 2])

    assert obj.count([0, 0]) == 2

    assert obj.count([1, 0]) == 1
    assert obj.count([1, 1]) == 1
    assert obj.count([0, 1]) == 1

    assert obj.count([2, 0]) == 1
    assert obj.count([2, 2]) == 1
    assert obj.count([0, 2]) == 1

def test_3():
    obj = DetectSquares()
    obj.add([3, 10])
    obj.add([11, 2])
    obj.add([3, 2])
    obj.add([11, 2])
    assert obj.count([11, 10]) == 2
