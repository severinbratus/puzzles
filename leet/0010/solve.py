#!/usr/bin/env python3

from typing import NamedTuple


class Atom(NamedTuple):
    pattern : str


class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        return Solution.solve(s, Solution.atomize(p), 0, 0)


    @staticmethod
    def solve(string : str | list[str], atoms : list[Atom], string_index : int, atom_index : int) -> bool:
        '''Return True iff string s[s_i:] matches pattern of p[p_i:]'''
        if atom_index == len(atoms):
            # if there are no atoms, then only an empty string matches
            # return atom_index == len(atoms)
            return string_index == len(string)

        elif atoms[atom_index].pattern.isalpha():

            # we have a literal atom
            if string_index >= len(string) or string[string_index] != atoms[atom_index].pattern:
                return False
            return Solution.solve(string, atoms, string_index + 1, atom_index + 1)

        elif atoms[atom_index].pattern == '.':
            if string_index == len(string):
                return False

            return Solution.solve(string, atoms, string_index + 1, atom_index + 1)

        else:
            atom = atoms[atom_index].pattern
            assert(atom[1] == '*')
            if atom == '.*':
                return any(Solution.solve(string, atoms, next_string_index, atom_index + 1)
                           for next_string_index in range(string_index, len(string) + 1))

            char = atom[0]
            # Now this is where we can decide where the next atom begins
            return any(Solution.solve(string, atoms, string_index + length, atom_index + 1)
                       for length in Solution.get_possible_lengths(string, string_index, char))


    @staticmethod
    def get_possible_lengths(string, string_index, char):
        length = 0
        yield length
        while string_index + length < len(string) and string[string_index + length] == char:
            length += 1
            yield length

    @staticmethod
    def atomize(p : str) -> list[Atom]:
        result = []

        for i in range(0, len(p)):
            if i + 1 != len(p) and p[i + 1] == '*':
                result.append(Atom(pattern=(p[i] + p[i + 1])))
            elif p[i] != '*':
                result.append(Atom(pattern=p[i]))

        return result
