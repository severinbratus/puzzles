#!/usr/bin/env python3

from itertools import product
from collections import deque, defaultdict
from typing import List
from functools import cache, partial

class Solution:
    def findLadders(self, begin_word: str, end_word: str, word_list: List[str]) -> List[List[str]]:

        # 1. Construct graph
        # Time & Space O(N^2)
        graph = defaultdict(set)
        ext_word_list = word_list + [begin_word]
        for word_a, word_b in product(ext_word_list, repeat=2):
            # print(word_a, word_b, Solution.is_step(word_a, word_b))
            if word_a != word_b and Solution.is_step(word_a, word_b):
                graph[word_a].add(word_b)
                graph[word_b].add(word_a)

        # 2. BFS
        # Time & Space O(N^2)
        queue = deque([begin_word])
        queued = set([begin_word])

        depth : dict[str, int] = dict()
        depth[begin_word] = 0

        shortest_depth = None

        # Track arents
        parentage : dict[str, list | None] = defaultdict(list)
        # begin_word has no parent
        parentage[begin_word] = None

        while queue:
            word = queue.popleft()
            if word == end_word:
                # We have found the shortest distance!
                shortest_depth = depth[word]

            # Do not go further than the shortest depth found
            if shortest_depth is not None and depth[word] > shortest_depth:
                break

            for adj_word in graph[word]:
                if adj_word not in queued:
                    queue.append(adj_word)
                    queued.add(adj_word)
                    depth[adj_word] = depth[word] + 1
                    parentage[adj_word] = [word]

                elif parentage[adj_word] is not None and depth[parentage[adj_word][0]] == depth[word]: # type: ignore
                    parentage[adj_word].append(word) # type: ignore

        # print("Graph:")
        # print(*graph.items(), sep='\n')
        # print("Parentage:")
        # print(*parentage.items(), sep='\n')

        @adhoc_cache
        def get_paths(parentage, end_word, begin_word) -> list[list[str]]:
            '''Find all paths from end_word to begin_word with the parentage lookup table / tree, excl end_word'''
            if end_word == begin_word:
                # No steps needed, empty path is the only path
                return [[]]

            else:
                parents = parentage[end_word]
                # assert len(parents) == len(set(parents))
                # For each possible parent, recurse to find the paths with that parent
                return [[parent] + path for parent in parents for path in get_paths(parentage, parent, begin_word)]

        return sorted([list(reversed(path)) + [end_word] for path in get_paths(parentage, end_word, begin_word)])


    @staticmethod
    def is_step(word_a, word_b) -> bool:
        return sum(char_a != char_b for char_a, char_b in zip(word_a, word_b)) == 1


def adhoc_cache(f):
    _cache = {}
    def g(a, b, c):
        if (b, c) not in _cache:
            _cache[(b, c)] = f(a, b, c)
        return _cache[(b, c)]
    return g
