#!/usr/bin/python

def solve(fish : list[int],
          niter : int = 80,
          reprp : int = 7,
          pubty : int = 9) -> int:

    for i in range(niter):
        nu_fish = [0]*pubty
        for i in range(1, pubty):
            nu_fish[i-1] = fish[i]
        
        nu_fish[reprp-1] += fish[0]
        nu_fish[pubty-1] = fish[0]

        fish = nu_fish

    return sum(fish)

with open('input') as fin:
    data = [int(x) for x in fin.readline().split(',')]
    fish = [0]*9
    for record in data:
        fish[record] += 1

print(solve(fish, 256))
