#!/usr/bin/python

from itertools import cycle

N = 2
posns = [7, 10]
assert(len(posns) == N)
scores = [0] * N

die = cycle(range(1, 100+1))
rolls = 0

def endgame(scores : list[int]) -> bool:
    return any(score >= 1000 for score in scores)

def wmod(x : int, m : int) -> int:
    return 1 + (x - 1) % m

while not endgame(scores):
    for pl_idx in range(N):
        tomove = sum(next(die) for _ in range(3))
        rolls += 3
        posns[pl_idx] = wmod(posns[pl_idx] + tomove, 10)
        
        scores[pl_idx] += posns[pl_idx]

        if (flag := endgame(scores)): break
    if endgame(scores): break

print(min(scores) * rolls)
