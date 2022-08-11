#!/usr/bin/python

from math import floor, ceil
from functools import reduce
from itertools import product
from copy import deepcopy

pair_t = list[int,int]
idx_t = list[int]

def sadd(args : list[pair_t]) -> pair_t:
    '''Snail number addition
    '''
    return reduce(bsadd, args)

def bsadd(a : pair_t, b : pair_t) -> pair_t:
    '''Snail number addition binary operator
    '''
    return s_reduce(deepcopy([a, b]))

def n_deref(tree : pair_t, idx : idx_t) -> pair_t:
    '''Nested indexation / dereference
    '''
    cur = tree
    for i in idx:
        cur = cur[i]
    return cur

def n_assign(tree : pair_t, idx : idx_t, val : int):
    '''Nested assignment

    Alters tree.
    '''
    n_deref(tree, idx[:-1])[idx[-1]] = val

def find_nest(pair : pair_t, depth = 4) -> idx_t:
    '''Find the left-most pair_t nested inside d pair_ts, where d is depth.
    
    None is returned if no such pair_t is found.
    '''
    if depth == 0:
        return []
    
    for i in range(2):
        if type(pair[i]) == list:
            scan = find_nest(pair[i], depth-1)
            if scan != None:
                return [i] + scan
        
    return None

def find_reg_num(pair : pair_t, idx : idx_t, right : bool = True) -> idx_t:
    '''Find the nearest regular number to the right, or left, of pair_t indexed by "idx".

    If no there is no such number, return None.
    '''

    if idx == []:
        return None

    hyp = list(idx)
    hyp[-1] = idx[-1] + (1 if right else -1)

    if 0 <= hyp[-1] < 2:
        return hyp + extreme(n_deref(pair, hyp), not right)

    hyp.pop()
    return find_reg_num(pair, hyp, right)

def extreme(pair : pair_t, right : bool) -> idx_t:
    return leaf_idxs(pair)[-1 if right else 0]

def leaf_idxs(pair : pair_t) -> list[idx_t]:
    if type(pair) == int:
        return [[]]
    return ([[0] + idx for idx in leaf_idxs(pair[0])] +
            [[1] + idx for idx in leaf_idxs(pair[1])])

def s_reduce(pair : pair_t):
    '''Snail number reduction
    '''
    pair_cpy = deepcopy(pair)

    filter_fn = lambda idx: n_deref(pair_cpy, idx) >= 10

    done = False
    while not done:

        done = True

        # If any pair is nested inside four pairs,
        #   the leftmost such pair explodes.

        # find the left-most pair nested inside four pair
        target_idx : idx_t = find_nest(pair_cpy, depth = 4)
        if target_idx != None:
            explode(pair_cpy, target_idx)

            done = False
            continue

        # If any regular number is 10 or greater,
        #   the leftmost such regular number splits.
       
        reg_num_idxs = list(filter(filter_fn, leaf_idxs(pair_cpy)))
        if reg_num_idxs:
            split(pair_cpy, reg_num_idxs[0])
            
            done = False
            #continue

    return pair_cpy

def explode(tree : pair_t, target_idx : idx_t) -> None:
    '''Explode target pair of regular numbers in tree

    Alters tree.
    '''
    for i in range(2):
        # the index of a regular number
        #   to the left or right of the target pair
        reg_num_idx = find_reg_num(tree, target_idx, right = bool(i))
        if reg_num_idx != None:
            n_assign(tree, reg_num_idx,
                n_deref(tree, reg_num_idx) + n_deref(tree, target_idx)[i]) 

    # replace the pair with 0
    n_assign(tree, target_idx, 0)

def split(tree : pair_t, target_idx : idx_t) -> None:
    '''Split target regular number in tree
    
    Alters tree.
    '''
    val = n_deref(tree, target_idx) / 2
    n_assign(tree, target_idx, [floor(val), ceil(val)])

def magnitude(pair : pair_t) -> int:
    if type(pair) == int:
        return pair
    else:
        return 3 * magnitude(pair[0]) + 2 * magnitude(pair[1])

from sys import argv

def main():
    with open(argv[1]) as fin:
        numbers = [eval(line) for line in fin.readlines()]

    print(magnitude(sadd(numbers)))
    print(max(magnitude(bsadd(a,b))
        for a,b in product(numbers,numbers) if a != b))

if __name__ == '__main__':
    main()
