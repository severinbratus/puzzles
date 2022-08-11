#!/usr/bin/env python
# coding: utf-8

# In[3]:


import cv2
import numpy as np
from collections import *
from functools import *
from itertools import *
from heapq import *
from sortedcontainers import SortedDict
from random import *


# In[10]:


def hashify(img : np.array) -> np.array:
    '''Return a character array representation of the maze in image.

    Each 16x16 pixel area is mapped to a character represenation (# for walls, $ for treasures etc)
    '''
    xsz = 16
    ysz = 16
    yn = 39
    xn = 53
    
    retval = np.empty((yn, xn), object)
    
    for i, j in product(range(yn), range(xn)):
        y = i * ysz
        x = j * xsz
        subimg = np.copy(img[y:y+ysz, x:x+xsz])

        q = quick_repr((h := int(np_hash(subimg))))
        retval[i, j] = q

    return retval
    
def clean(img):
    '''Clean the image array of unprecise RGB values, e.g. convert 254 becomes 255

    The expected values are hardcoded.
    '''
    correct_vec = np.vectorize(correct)
    return correct_vec(img)

def correct(x):
    nums = [162, 50, 62, 255]
    for num in nums:
        if abs(x - num) < 5:
            return num
    return x
        
def val_set(arr):
    '''Return the set of unique values in the array'''
    return set(arr.flatten())

# This array establishes the correspondence between 16x16 pixel block hashes, and characters.
# A cheap way to avoid OCR with a monospace custom font, preserving whitespace.

rules = [(-2764148011662737855, '#'),
 (-2820236508719897226, '.'),
 (-8144433900243051436, '$'),
 (-6932731916743976535, '.'), # formerly @
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
 (2890774637198736773, 'i')]

rulesd = {k:v for k,v in rules}

def quick_repr(x):
    return rulesd.get(x, '?')

def np_hash(arr):
    return hash(tuple(arr.flatten()))

def crop(carr):
    return carr[2:2+33+1, 1:1+45+1]

def carr_repr(carr):
    return [''.join(row) for row in carr]

def conjoin(carrs):
    '''Take a nested list, where rows contain 2d arrays and first concatenate the arrays in
    each row, and then the resulting horizontal arrays
    '''
    return np.concatenate(list(map(lambda row: np.concatenate(row, axis=1), carrs)))


# In[9]:


# Read `carr` from file
with open('carrs.txt') as fin:
    data = [list(line.strip()) for line in fin.readlines()]
carr = np.array(data, object)


# In[3]:


# Compute `carr`, a large map of 4x3 screens
carrs = [[crop(hashify(clean(cv2.imread(f"screens/scr-{scrx}-{scry}.png"))))
          for scrx in range(3)] for scry in range(4)]
carrs_joined = conjoin(carrs)
carr = carrs_joined


# In[6]:


def bfsh(init, termf, adj, hn : int) -> list[tuple[int]]:
    '''BFS with heuristic-based pruning. Return a path (a sequence of coordinates)'''
    q = deque()
    d = SortedDict()

    q.append(init)
    d[init] = None
    
    maxh = -1
    
    while q:
        u = q.popleft()
        
        # Record the node with max h-function value
        uh = h(u)
        if uh > maxh:
            print(u, len(q))
            maxh = uh
            
        # If `hn` == 0, only go to nodes, that have the max h-fun value
        
        if termf(u):
            break
        for v in adj(u):
            if not cont(d, v) and (h(v) >= maxh - hn): # or random() < hp):
                d[v] = u
                q.append(v)
    
    # backtrace
    path = []
    while u:
        path.append(u)
        u = d[u]
    path.reverse()
    
    return path

def h(u) -> int:
    '''Heuristic: sum of set cluster bits'''
    return sum(u[11:])

def cont(d, v) -> bool:
    '''Return true iff node `v`, or any superset-node of `v`, is contained in `d`.'''
    if v in d:
        return True
    us = d.irange(v[:2], (v[0], v[1]+1))
    return any(is_superset(u, v) for u in us)

def is_superset(a, b):
    '''Node `a` is a superset of node `b` iff a[:2] == b[:2] and a[i] >= b[i] for all approriate i.'''
    return all(ax >= bx for ax, bx in zip(a, b))

diffs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def adj23(carr, u) -> list[tuple]:
    '''Determine possible adjacent nodes'''
    for diff in diffs:
        v = tuple(u[i] + diff[i] if i < 2 else u[i] for i in range(len(u)))
        # If there is a wall, the agent definitely cannot move there
        c = carr[v[0], v[1]]
        # Then if there is a key there, one bit the last 9 bits of the state vector is elevated
        if 'a' <= c <= 'i':
            yield tuple(1 if i == 2 + ord(c) - ord('a') else v[i] for i in range(len(v)))
        # So if there is a door and the agent has the key (had visited a key tile), they can enter
        elif 'A' <= c <= 'I':
            if v[2 + ord(c) - ord('A')] == 1:
                yield v
        # If it is not a door, and not a key, and not a wall, it must be empty space, good to go
        elif c != '#':
            yield v

def adj34(carr, u, cluster_idx, term) -> list[tuple]:
    '''Determine possible adjacent nodes, considering cluster history'''
    for v in adj23(carr, u):
        # If it is a cluster node, elevate one bit
        if v[:2] in cluster_idx:
            yield tuple(1 if i == 11 + cluster_idx[v[:2]] else v[i] for i in range(len(v)))
        # Only move to the last square after visiting all clusters
        if v[:2] == term:
            if all(v[11:]):
                yield v
            else:
                continue
        # Otherwise
        else:
            yield v

def keys_repr(v):
    return ''.join([a for i,a in enumerate('abcdefghi') if v[2+i]])

def nodes2moves(nodes):
    return [nodes2move(prev, nxt) for prev, nxt in zip(nodes, nodes[1:])]
            
def nodes2move(prev, nxt):
    '''Return move direction (0 for east, 1 for south, etc) based on two consequtive moves

    The least elegant function in this notebook
    '''
    if dist(prev[:2], nxt[:2]) != 1:
        print(f"{dist(prev[:2], nxt[:2])=}")
    assert(dist(prev[:2], nxt[:2]) == 1)
    if nxt[0] > prev[0]:
        assert(nxt[1] == prev[1])
        return 1
    elif nxt[0] < prev[0]:
        assert(nxt[1] == prev[1])
        return 3
    elif nxt[1] > prev[1]:
        assert(nxt[0] == prev[0])
        return 0
    elif nxt[1] < prev[1]:
        assert(nxt[0] == prev[0])
        return 2
    else:
        # This should not happen
        assert(nxt == prev)
        print(prev, nxt)
        assert(0)
        
def dist(a, b):
    return max(abs(ax - bx) for ax, bx in zip(a, b))

def repr_path(path):
    '''Print the path in the Xennial BASIC format'''
    print(3200, "DATA", ','.join(map(str, nodes2moves(path))))

def inc_vec(v, i):
    return tuple(vx + 1  if vi == i else vx for vi, vx in enumerate(v))

def path_cost(cdist, path):
    # compute total path
    return sum(map(lambda uv: cdist[uv], zip(path, path[1:])))


# In[10]:


locs = list(filter(lambda loc: carr[loc[0], loc[1]] == '$', product(*map(range, carr.shape))))

preclusters = set(frozenset(filter(lambda loc_: dist(loc, loc_) <= 5, locs)) for loc in locs)

clusters = list(set(precluster.union(*filter(lambda precluster_: precluster.intersection(precluster_), preclusters)) for precluster in preclusters))

cluster_idx = {loc: i for i, cluster in enumerate(clusters) for loc in cluster}
cluster_locs = set(next(iter(cluster)) for cluster in clusters)
cluster_loc_idx = {cluster_idx[loc]: loc for loc in cluster_locs}
cluster_locs_idx = {i: set(loc for loc in cluster_idx if cluster_idx[loc] == i) for i in range(11)}

cluster_locs_idx


# In[7]:


all(cluster_loc in cluster_idx for cluster_loc in cluster_locs)


# In[12]:


init = (1,1, *tuple(repeat(0, 9 + 11)))
term = (117, 124, *tuple(repeat(1, 9 + 11)))
path11 = map(lambda u: u[:11], path)
cpath11 = list(filter(lambda u: u[:2] in cluster_idx or u[:2] == init[:2] or u[:2] == term[:2], path11))
cpath11


# In[22]:


def f(x, x2):
    return tuple(list(x2) + list(x[2:]))

ccpath11 = list(map(lambda x: x if x[:2] not in cluster_idx else f(x, cluster_loc_idx[cluster_idx[x[:2]]]), cpath11))
ccpath11, path_cost(cdist, ccpath11)
# This confirms (or at least does not disprove) that `min_path` finds the minimal path


# In[128]:


cpath11 = [init[:11]] + list(reversed(m_path[1]))
for p, np in zip(cpath11, cpath11[1:]):
    print(p, np, cdist[p, np])


# In[62]:


def bfsf(init, termf, adj):
    '''Regular BFS (?)'''
    q = deque()
    p = SortedDict()

    q.append(init)
    p[init] = None
    
    while q:
        u = q.popleft()
        
        if termf(u):
            break
        for v in adj(u):
            if v not in p:
                p[v] = u
                q.append(v)
    
    # catch worst case
    if not termf(u):
        raise ValueError(f"No escape. Init.: {init}")
    
    # backtrace
    path = []
    while u:
        path.append(u)
        u = p[u]
    path.reverse()
    
    return path


# In[77]:


full_path = [init[:11]]
for key, nkey in zip(cpath11, cpath11[1:]):
    #     print(nkey)
    point = full_path.pop()
    full_path += bfsf(point, lambda u: is_superset(u, nkey), lambda u: adj23(carr, u))
    if nkey[:2] in cluster_idx:
        # collect other treasures greedily
        visited = set(map(lambda u: u[:2], filter(lambda u: u[:2] in cluster_locs_idx[cluster_idx[nkey[:2]]], full_path)))
        print(visited)
        for _ in range(len(cluster_locs_idx[cluster_idx[nkey[:2]]]) - len(visited)):
            point = full_path.pop()
            full_path += bfsf(point,
                              lambda u: u[:2] in cluster_locs_idx[cluster_idx[nkey[:2]]] and u[:2] not in visited,
                              lambda u: adj23(carr, u))
            visited.add(full_path[-1][:2])
            
#     full_path.pop()
# full_path.append(cpath11[-1])


# In[82]:


len(full_path)


# In[81]:


all(any(p[:2] == loc for p in path) for loc in cluster_idx)


# In[79]:


repr_path(full_path)


# In[117]:


key = init
ks = cdist.irange(tuple([key]), tuple([inc_vec(key, len(key)-1)]))


# In[120]:


len(list(ks))


# In[125]:


@cache
def n_paths(key, d):
    if key[:2] == (117, 124): return 1
    if d == 0: return 0
#     print(list(cdist.irange(tuple([key]), tuple([inc_vec(key, len(key)-1)]))))
    return sum(n_paths(v, d-1) for k, v in cdist.irange(tuple([key]), tuple([inc_vec(key, len(key)-1)])))


# In[127]:


n_paths(init, 10)


# In[60]:


term = (117, 124, 1, 1, 1, 1, 1, 1, 1, 1, 1)
@cache
def max_dist(key, d = 11):
    if key == term:
        return 0
    if d == 0: return 3333
    return min(max_dist(k, d - 1) + cdist[key, k] for key_, k in cdist.irange(tuple([key]), tuple([inc_vec(key, len(key)-1)])))


# In[ ]:


#     if not len(list(ks)) == len(list(filter(lambda pair: pair[0] == key, cdist.keys()))):
#         raise ValueError("Ah?")


# In[ ]:


m = (3333, None)


# In[12]:


init = (1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
m_path = min_path(init)

# In[4]:


cdist = SortedDict(cdist)


# In[5]:


@cache
def or_vec(v, i):
    """Set i-th bit in a vector"""
    return tuple(1 if vi == i else vx for vi, vx in enumerate(v))

def part_cache(f):
    '''Do not take `d` into account when caching.'''
    part_cache.cache_ = {}
    def g(key, visited = tuple(repeat(0, 11)), d = 14):
        if (key, visited) not in part_cache.cache_:
                part_cache.cache_[key, visited] = f(key, visited, d)
        return part_cache.cache_[key, visited]
    return g

@part_cache
def min_path(key, visited = tuple(repeat(0, 11)), d = 14) -> tuple[int, list[tuple[int]]]:
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
    ks = cdist.irange(tuple([key]), tuple([inc_vec(key, len(key)-1)]))
    return min(filter(lambda x: x != None, (adhoc(key, visited, d, k) for _, k in ks if k[:2] == (117, 124) or not visited[cluster_idx[k[:2]]])), default=None)

def adhoc(key, visited, d, k):
    """Minimal path from key to end, with `k` in the front"""
    tmp = min_path(k,
                   visited if (k[:2] not in cluster_idx) else or_vec(visited, cluster_idx[k[:2]]),
                   d - 1)
    if tmp == None: return None
    return (tmp[0] + cdist[key, k], tmp[1] + [k])


# In[94]:


def collect(carr, center, cluster, dest, visited = set()):
    assert(center[:2] in cluster)
    print(f"{sorted(list(visited))=}")
    point = center
    path = []
    visited.add(center[:2])
    for i in range(len(cluster) - len(visited)):
        path += bfsf(point, lambda u: u[:2] in cluster and u[:2] not in visited, lambda u: adj23(carr, u))
        point = path.pop()
        visited.add(point[:2])
#     # close the loop
#     path += bfs(point, lambda u: u[:2] == center[:2], lambda u: adj23(carr, u))
#     path.pop()

    # instead of closing the loop, look for the closest location in the destination
    path += bfsf(point, lambda u: u[:2] in dest, lambda u: adj23(carr, u))
    
    assert(frozenset(visited) == frozenset(cluster))
    print(f"{sorted(list(visited))=}")
    print(f"{sorted(list(cluster))=}")
    print(f"{list(filter(lambda u: u not in path, cluster))}")
    assert(all(loc in map(lambda u: u[:2], path) for loc in cluster))
    print()
    
    return path


# In[95]:


# Augment cycles which visit all the squares in cluster
# Not sure this works :/

path_ = path[:]
for cidx, cluster in enumerate(clusters):
    idx = next(filter(lambda i: path_[i][:2] in cluster, range(len(path_))))
    previsited = set(filter(lambda loc: loc in cluster, map(lambda u: u[:2], path_)))
    dest = set(map(lambda x: x[:2], path_[idx:]))
    augm = collect(carr, path_[idx], cluster, dest, visited=previsited)

    # `augm` contains `path_[idx]` in the beginning, and the dest node in the end
    sidx = next(filter(lambda i: path_[i][:2] == augm[-1][:2], range(len(path_))))
    
    assert(augm[0][:2] == path_[idx][:2])
    assert(augm[-1][:2] == path_[sidx][:2])
    
    path_ = path_[:idx] + augm + path_[sidx+1:]

len(path), len(path_)


# In[69]:


wp = list(filter(lambda u: u[:2] in cluster_locs or u[:2] == (1,1) or u[:2] == (117,124), path))


# In[47]:


# New start.
# Dijkstra, computing distances when needed.

def dijkstra(carr, init, adje, term, hn):
    '''Dijkstra based on ad hoc distance computation. Return the parent map `p`'''
    q = list()
    p = SortedDict()
    d = dict()

    p[init] = None
    d[init] = 0
    heappush(q, (d[init], init))
    
    maxh = -1
    
    while q:
        d_u, u = heappop(q)
        
        uh = h(u)
        if uh > maxh:
            print(u)
            maxh = uh
        
        if (d_u != d[u]) or spec_cond(p, d, u) or not (uh >= maxh - hn):
            continue
        
        for u2v, v in adje(u):
            if (v not in p or d[u] + u2v < d[v]):
                d[v] = d[u] + u2v
                p[v] = u
                heappush(q, (d[v], v))
    
    return p, d


# In[25]:


def backtrace(p, term):
    '''Backtrace the path based'''
    path = []
    u = term
    while u:
        path.append(u)
        u = p[u]
    path.reverse()
    return path

def gencache(f):
    global memory
    def g(*args):
        if args not in memory:
                memory[args]=list(f(*args))
        return iter(memory[args])
    return g

def bfsd(carr, init, termf, adj, maxd):
    '''BFS until exceeding some depth threshold.
    Yield distance from source, and node'''   
    q = deque()
    d = SortedDict()
    retvals = set()
    lvl = 0    
    
    q.append(init)
    d[init] = None

    while q:
        lvl_sz = len(q)
        
        for lvl_i in range(lvl_sz):
            u = q.popleft()

            # Check if we found a check-point (cluster node)
            if termf(u):
                if u not in retvals:
                    retvals.add(u)
                    yield lvl, u

            for v in adj(u):
                if v not in d:
                    d[v] = u
                    q.append(v)
        
        lvl += 1
        if lvl >= maxd:
            return


# In[28]:


# A fresh start yet again.

# Idea: compute a dictionary with distances from each node
# (approx 128x128 combinations for the location, 2^9=512 for the key configuration)
# Prune search to only the nodes reachable within some limit, say 1000 steps from the others.

init = (1, 1, *repeat(0, 9))

q = deque()
q.append(init)
seen = set()

cdist : dict[tuple[tuple[int], tuple[int]], int] = dict()

termf = lambda v: v[:2] in cluster_locs or v[:2] == (117,124)
adjf = lambda v: adj23(carr, v)
n = 1500

i = 0

while q:
    u = q.popleft()
    print(u, i)
    i += 1
    
    for u2v, v in bfsd(carr, u, termf, adjf, n):
        cdist[u, v] = u2v
        if v not in seen:
            seen.add(v)
            q.append(v)

