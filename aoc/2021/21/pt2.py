#!/usr/bin/python

from itertools import product
from functools import cache
from collections.abc import Iterable

def endgame(scores : Iterable[int]) -> bool:
    return any(score >= 21 for score in scores)

def wmod(x : int) -> int:
    return 1 + (x - 1) % 10

trip_rolls = tuple(sum(trip) for trip in product(range(1,3+1), repeat=3))

@cache
def play(posns : tuple[int], scores : tuple[int]) -> list[int, int]:
    '''Return for each player, the number of universes they will win in, given the current player positions and scores, and assuming that the first player takes the next turn.
    '''
    count = [0, 0]
    nu_posns = list(posns)
    nu_scores = list(scores)
    for poss_trip_roll in trip_rolls:
        nu_posns[0] = wmod(posns[0] + poss_trip_roll)
        nu_scores[0] = scores[0] + nu_posns[0]
        if (endgame(nu_scores)): # if first player wins:
            count[0] += 1
            continue    # the second player does not get a turn

        # now the second player takes the turn
        nu_count = play(tuple(reversed(nu_posns)), tuple(reversed(nu_scores)))
        count = add(count, reversed(nu_count))

    return count
        
def add(a : Iterable[int], b : Iterable[int]) -> list[int]:
    return list(ax + bx for ax, bx in zip(a, b))

print(play((7, 10), (0, 0)))
