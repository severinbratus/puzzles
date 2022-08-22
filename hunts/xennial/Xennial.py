#!/usr/bin/env python
# coding: utf-8

from collections.abc import Generator
import cv2
import numpy as np
from collections import deque
from functools import cache
from itertools import repeat, product
from sortedcontainers import SortedDict
# from random import *
from typing import Tuple
from nptyping import NDArray
from math import inf


Point = Tuple[int, ...]


def hashify(image : NDArray) -> NDArray:
    '''Return a character array representation of the maze in the image given.

    Each 16x16 pixel area is mapped to a character represenation (# for walls, $ for treasures etc)
    '''
    char_width = 16
    char_height = 16
    image_height_in_chars = 39
    image_width_in_chars = 53

    char_repr = np.empty((image_height_in_chars, image_width_in_chars), object)

    for char_row, char_col in product(range(image_height_in_chars), range(image_width_in_chars)):
        y = char_row * char_height
        x = char_col * char_width
        char_image = np.copy(image[y:y + char_height, x:x + char_width])

        char = quick_repr(int(np_hash(char_image)))
        char_repr[char_row, char_col] = char

    return char_repr


def clean(image):
    '''Round the image array with unprecise RGB values, e.g. convert 254 to 255

    The expected values are hardcoded.
    '''
    correct_vec = np.vectorize(correct)
    return correct_vec(image)


def correct(value):
    expected = [162, 50, 62, 255]
    for expected_value in expected:
        if abs(value - expected_value) < 5:
            return expected_value
    return value


def value_set(array):
    '''Return the set of unique values in the array'''
    return set(array.flatten())

# This array establishes the correspondence between 16x16 pixel block hashes, and characters.
# A cheap way to avoid doing OCR on an image w/ a monospace custom font, and preserving whitespace.

HASH_TO_CHAR = dict([
    (-2764148011662737855, '#'),
    (-2820236508719897226, '.'),
    (-8144433900243051436, '$'),
    (-6932731916743976535, '.'), # actually `@`, rendered as `.`
    (2315865820819430126, 'A'),
    (9124188176027256220, 'B'),
    (5121848818809575714, 'C'),
    (3319386803164075856, 'D'),
    (-3354114278570584666, 'E'),
    (-4660276543934757421, 'F'),
    (-3761540897678092013, 'G'),
    (772770210378714535, 'H'),
    (3892035078691099998, 'I'),
    (8362810459577788786, 'a'),
    (1282293228143785119, 'b'),
    (6822681657312074680, 'c'),
    (5654541670866747532, 'd'),
    (-8581590679190271494, 'e'),
    (-5582945093516910282, 'f'),
    (1011880605818605489, 'g'),
    (-536531549812453152, 'h'),
    (2890774637198736773, 'i')
])


def quick_repr(digest):
    return HASH_TO_CHAR.get(digest, '?')


def np_hash(array):
    return hash(tuple(array.flatten()))


def crop(char_array):
    '''Crop out margins from the char array repr of the display'''
    return char_array[2:2+33+1, 1:1+45+1]


def char_array_repr(char_array):
    return [''.join(row) for row in char_array]


def conjoin(char_arrays):
    '''Take a nested list, where rows contain 2d arrays and first concatenate the arrays in
    each row, and then the resulting horizontal arrays
    '''
    return np.concatenate(list(map(lambda row: np.concatenate(row, axis=1), char_arrays)))


def read_char_array():
    # Read `char_array` from file
    global char_array
    with open('char_array.txt') as fin:
        data = [list(line.strip()) for line in fin.readlines()]
    char_array = np.array(data, object)

    # Compute `char_array`, a large map of 4x3 screens
    char_arrays = [[crop(hashify(clean(cv2.imread(f"screens/scr-{screen_col}-{screen_row}.png")))) # type: ignore
            for screen_col in range(3)] for screen_row in range(4)]

    char_arrays_joined = conjoin(char_arrays)
    char_array = char_arrays_joined


def bfs_heuristical(init_node, is_terminal, get_adj, heuristic_margin : int) -> list[Point]:
    '''BFS with heuristic-based pruning. Return a path (a sequence of coordinates)'''
    queue = deque()
    parents = SortedDict()

    queue.append(init_node)
    parents[init_node] = None

    max_heuristic = -1
    node = None

    while queue:
        node = queue.popleft()

        # Record the node with max h-function value
        node_heuristic = heuristic(node)
        if node_heuristic > max_heuristic:
            max_heuristic = node_heuristic

        # If `heuristic_margin` == 0, only go to nodes, that have the max h-fun value

        if is_terminal(node):
            break
        for adj_node in get_adj(node):
            if not contains(parents, adj_node) and (heuristic(adj_node) >= max_heuristic - heuristic_margin): # or random() < hp):
                parents[adj_node] = node
                queue.append(adj_node)

    # backtrace
    path = []
    while node:
        path.append(node)
        node = parents[node]
    path.reverse()

    return path


def heuristic(u) -> int:
    '''Heuristic: sum of set cluster bits'''
    return sum(u[11:])


def contains(d, v) -> bool:
    '''Return true iff node `v`, or any superset-node of `v`, is in `d`.'''
    if v in d:
        return True
    us = d.irange(v[:2], (v[0], v[1]+1))
    return any(is_superset(u, v) for u in us)


def is_superset(a : Point, b : Point) -> bool:
    '''Node `a` is a superset of node `b` iff a[:2] == b[:2] and a[i] >= b[i] for all approriate i.'''
    return all(ax >= bx for ax, bx in zip(a, b))


diffs = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def get_adj_23(char_array, node) -> Generator[Point, None, None]:
    '''Determine possible adjacent nodes for nodes of 23 bits.

    23 = 7 + 7 + 9
    7 bits for node row, 7 bits for node column, 9 bits for keys a-f
    '''
    for diff in diffs:
        near_node = tuple(node[index] + diff[index] if index < 2 else node[index] for index in range(len(node)))
        # If there is a wall, the agent definitely cannot move there
        char = char_array[near_node[0], near_node[1]]
        # Then if there is a key there, one bit the last 9 bits of the state vector is elevated
        if 'a' <= char <= 'i':
            yield tuple(1 if i == 2 + ord(char) - ord('a') else near_node[i] for i in range(len(near_node)))
        # So if there is a door and the agent has the key (had visited a key tile), they can enter
        elif 'A' <= char <= 'I':
            if near_node[2 + ord(char) - ord('A')] == 1:
                yield near_node
        # If it is not a door, and not a key, and not a wall, it must be empty space, good to go
        elif char != '#':
            yield near_node


def get_adj_34(char_array, node, cluster_index, terminal_node) -> Generator[Tuple[int, ...], None, None]:
    '''Determine possible adjacent nodes, with cluster history

    23 = 7 + 7 + 9 + 11
    In addition to 23 bits, add 11 bits for cluster history
    '''
    for near_node in get_adj_23(char_array, node):
        # If it is a cluster node, elevate one bit
        if near_node[:2] in cluster_index:
            yield tuple(1 if i == 11 + cluster_index[near_node[:2]] else near_node[i] for i in range(len(near_node)))
        # Only move to the last square after visiting all clusters
        if near_node[:2] == terminal_node:
            if all(near_node[11:]):
                yield near_node
            else:
                continue
        # Otherwise
        else:
            yield near_node


def repr_node_keys(node):
    return ''.join([key_symbol for key_index, key_symbol in enumerate('abcdefghi') if node[2 + key_index]])


def path_to_moves(path):
    '''Convert a path of nodes into a sequence of moves'''
    return [pair_to_move(prev, nxt) for prev, nxt in zip(path, path[1:])]


def pair_to_move(prev_node, next_node):
    '''Return move direction (0 for east, 1 for south, etc) based on two nodes one move away from each other.'''
    assert(max_coord_diff(prev_node[:2], next_node[:2]) == 1)
    if next_node[0] > prev_node[0]:
        assert(next_node[1] == prev_node[1])
        return 1
    elif next_node[0] < prev_node[0]:
        assert(next_node[1] == prev_node[1])
        return 3
    elif next_node[1] > prev_node[1]:
        assert(next_node[0] == prev_node[0])
        return 0
    elif next_node[1] < prev_node[1]:
        assert(next_node[0] == prev_node[0])
        return 2
    # else:
    #     # This should not happen
    #     assert(next_node == prev_node)
    #     assert(0)


def max_coord_diff(a : Point, b : Point) -> int:
    return max(abs(x - y) for x, y in zip(a, b))


def repr_path_in_basic(path):
    '''Return the path in the Xennial BASIC format'''
    ' '.join([str(3200), "DATA", ','.join(map(str, path_to_moves(path)))])

def inc_vec(vec : Point, target_index) -> Point:
    return tuple((value + 1 if index == target_index else value) for index, value in enumerate(vec))


def path_cost(cluster_distances, path):
    '''Compute the total path cost'''
    return sum(map(lambda pair: cluster_distances[pair], zip(path, path[1:])))


## Cluster the treasures

# Treasure locations
locs = list(filter(lambda loc: char_array[loc[0], loc[1]] == '$', product(*map(range, char_array.shape))))
# For each treasure location, identify other treasure locations closeby.
groups : set[frozenset[Point]] = set(frozenset(filter(lambda loc_: max_coord_diff(loc, loc_) <= 5, locs)) for loc in locs)
# For each such group, join it with other such groups if they have at least one treasure in common.
# (their intersection is not empty)
clusters : list[frozenset[Point]] = list(set(group.union(*filter(lambda other_group: group.intersection(other_group), groups)) for group in groups))
# Enumerate clusters, and provide a table for look-up
loc_to_cluster_index : dict[Point, int] = {loc: i for i, cluster in enumerate(clusters) for loc in cluster}
treasures = set(loc_to_cluster_index.keys())

# Pick one location as a `centre` for each cluster
cluster_centres : set[Point] = set(min(iter(cluster)) for cluster in clusters)
# Look up cluster centres by cluster index
cluster_index_to_centre = {loc_to_cluster_index[centre]: centre for centre in cluster_centres}
# Look up whole clusters by cluster index
cluster_indexes = sorted(list(cluster_index_to_centre))
assert list(range(11)) == cluster_indexes
cluster_index_to_cluster : dict[int, set[Point]] = {cluster_index: set(loc for loc in treasures if loc_to_cluster_index[loc] == cluster_index) for cluster_index in cluster_indexes}


assert(all((cluster_centre in treasures) for cluster_centre in cluster_centres))


def compute_cluster_distances() -> SortedDict:
    """Idea: compute a dictionary with distances from each node.

    (approx 128x128 combinations for the location, 2^9=512 for the key configuration)
    Prune search to only the nodes reachable within some limit, say 1000 steps from the others.
    """
    init_node = (1, 1, *repeat(0, 9))

    queue = deque()
    queue.append(init_node)
    queued = set()

    cluster_distances : dict[tuple[Point, Point], int] = dict()

    is_targeted = lambda node: node[:2] in cluster_centres or node[:2] == (117, 124)
    get_adj = lambda node: get_adj_23(char_array, node)
    max_depth = 1500

    iteration = 0

    while queue:
        node = queue.popleft()
        iteration += 1

        for distance, next_node in bfs_depthed(node, is_targeted, get_adj, max_depth):
            cluster_distances[node, next_node] = distance
            if next_node not in queued:
                queued.add(next_node)
                queue.append(next_node)

    return SortedDict(cluster_distances)


# cluster_distances : SortedDict = compute_cluster_distances()

def bfs_vanilla(init, is_terminal, get_adj):
    '''Regular BFS (?)'''
    queue = deque()
    parents = SortedDict()

    queue.append(init)
    parents[init] = None

    while queue:
        node = queue.popleft()

        if is_terminal(node):
            break

        for adj_node in get_adj(node):
            if adj_node not in parents:
                parents[adj_node] = node
                queue.append(adj_node)

    # catch worst case
    if not is_terminal(node): # type: ignore
        raise ValueError(f"No escape! Init.: {init}")

    # backtrace
    path = []
    while node: # type: ignore
        path.append(node)
        node = parents[node]
    path.reverse()

    return path

# Remember to glue cycles into the cluster-path to visit all treasures

init_node = (1,1, *tuple(repeat(0, 9 + 11)))
term_node = (117, 124, *tuple(repeat(1, 9 + 11)))

# full_path = [init_node[:11]]

# Assert all treasures are collected in the path
# assert all(any(node[:2] == loc for node in path) for loc in treasures)

def irange_lookup(key):
    global compute_cluster_distances
    return cluster_distances.irange(tuple([key]), tuple([inc_vec(key, len(key)-1)]))

@cache
def n_paths(key, depth):
    if key[:2] == (117, 124): return 1
    if depth == 0: return 0
    return sum(n_paths(v, depth - 1) for k, v in cluster_distances.irange(tuple([key]), tuple([inc_vec(key, len(key)-1)])))


@cache
def min_distance(key, depth = 11):
    if key == term_node:
        return 0
    if depth == 0: return inf
    return min(min_distance(next_key, depth - 1) + cluster_distances[key, next_key] for key_, next_key in cluster_distances.irange(tuple([key]), tuple([inc_vec(key, len(key)-1)])))


@cache
def or_vec(vec, target_index):
    """Set i-th bit in a vector"""
    return tuple(1 if index == target_index else value for index, value in enumerate(vec))


def part_cache(f):
    '''Do not take `d` into account when caching.'''
    part_cache.cache_ = {}
    def g(key, visited = tuple(repeat(0, 11)), d = 14):
        if (key, visited) not in part_cache.cache_:
                part_cache.cache_[key, visited] = f(key, visited, d)
        return part_cache.cache_[key, visited]
    return g


@part_cache
def min_path(key, visited = tuple(repeat(0, 11)), d = 14) -> tuple[int, list[Point]] | None:
    """
    Return the minimal path from the current `key` and `visited` to (117, 124, ...) and (1, 1, 1, ...).
    Return `None` if no such path exists or depth is exceeded.

    The return value is a pair of the distance and the path in reverse, with `key` excluded
    """

    # Base case
    if key[:2] == (117, 124):
        if visited == (1,1,1, 1,1,1, 1,1,1, 1,1):
            # The minimal path is empty
            return (0, [])
        else:
            # All clusters have to be visited
            return None

    # Limit recursion depth
    if d == 0:
        return None

    # Recursive case: visit unvisited cluster locs, or the final loc,
    # and take the minimal path to the end for all of these.
    # Then, add the distance to that loc, and take the over-all min of the whole path.
    irange = cluster_distances.irange(tuple([key]), tuple([inc_vec(key, len(key)-1)]))
    return min(remove_none(adhoc(key, visited, d, next_key) for _, next_key in irange if next_key[:2] == (117, 124) or not visited[loc_to_cluster_index[next_key[:2]]]), default=None)


def remove_none(generator):
    for item in generator:
        if item is not None:
            yield item


def adhoc(key, visited, d, k):
    """Minimal path from key to end, with `k` in the front"""
    tmp = min_path(k,
                   visited if (k[:2] not in treasures) else or_vec(visited, loc_to_cluster_index[k[:2]]),
                   d - 1)
    if tmp == None: return None
    return (tmp[0] + cluster_distances[key, k], tmp[1] + [k])


def backtrace(parents, term_node):
    '''Backtrace the path based on parents'''
    path = []
    node = term_node
    while node:
        path.append(node)
        node = parents[node]
    path.reverse()
    return path


def global_gen_cache(f):
    global memory
    memory = {}
    def g(*args):
        if args not in memory:
            memory[args] = list(f(*args))
        return iter(memory[args])
    return g


def bfs_depthed(init_node, is_targeted, get_adj, max_depth):
    '''BFS until exceeding some depth threshold.
    Yield distance from source, and node
    '''
    queue = deque()
    parents = SortedDict()
    yielded = set()
    depth = 0

    queue.append(init_node)
    parents[init_node] = None

    while queue:
        layer_size = len(queue)

        for _ in range(layer_size):
            node = queue.popleft()

            # Check if we found a check-point (cluster node)
            if is_targeted(node):
                if node not in yielded:
                    yielded.add(node)
                    yield depth, node

            for adj_node in get_adj(node):
                if adj_node not in parents:
                    parents[adj_node] = node
                    queue.append(adj_node)

        depth += 1
        if depth >= max_depth:
            return
