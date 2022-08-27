#!/usr/bin/env python3

from typing import List
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for string in strs:
            groups[''.join(sorted(string))].append(string)
        return sorted(groups.values())
