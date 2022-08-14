#!/usr/bin/env python3

# https://stats.stackexchange.com/q/581923/363251
# https://stats.stackexchange.com/a/582186/363251

# Rolling a 100-sided die costs 1$. The player can roll many times, and once they stop rolling
# the value of the last roll is their reward. When should the player stop rolling to maximize profit?

from functools import cache

mem = dict()

def global_cache(f):

    global mem

    def g(*args):
        if args not in mem:
            mem[args] = f(*args)
        return mem[args]

    return g

@global_cache
def best_profit(last_roll, rolls):
    # If the maximal possible profit in the next roll is less than or equal to zero, there is no profit in playing at all.
    if 100 - (rolls + 1) <= 0:
        return last_roll - rolls
    # If the profit of stopping is greater than or equal to the maximal possible profit of continuing, stop.
    if last_roll - rolls >= 100 - (rolls + 1):
        return last_roll - rolls

    return max(last_roll - rolls, 0.01 * sum(best_profit(next_roll, rolls + 1) for next_roll in range(1, 100+1)))

print(best_profit(0, 0))
print(list(filter(lambda args: best_profit(*args) != args[0] - args[1] and args[0] >= 87, mem)))
