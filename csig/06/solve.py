#!/usr/bin/env python3

def mean(g):
    return sum(g) / len(g)

def solution(a):
    means = [mean(g) for g in a]
    means_uniq = sorted(set(means), key=means.index)

    return [[i for i in range(len(a)) if means[i] == mean] for mean in means_uniq]
