#!/usr/bin/env python3

from operator import add, sub, mul, floordiv

ops = [add, sub, mul, floordiv]

syms = {
    add: '+',
    sub: '-',
    mul: '*',
    floordiv: '/',
}


def applicable(a, b, op) -> bool:
    return op != floordiv or (b != 0 and a % b == 0)


def solve(args: list[int], target: int) -> None | list[str]:
    '''Given a list of four positive integers, find a way to combine operations of +, -, *, and -, to obtain target.

    Inspired by an exercise the IQ-test-like assessment at Optiver.
    I think I failed it.

    Anyways, this method is rather brute-force, since it does not even optimize for the commutativity of + and *.
    '''
    if args == [target]:
        return []
    for i, a in enumerate(args):
        for j, b in enumerate(args):
            if i != j:
                for op in ops:
                    if applicable(a, b, op):
                        new_args = list(args)
                        del new_args[i]
                        del new_args[j if j < i else j - 1]
                        new_args.append(op(a, b))
                        result = solve(new_args, target)
                        if result != None:
                            return [f'{args}: {a} {syms[op]} {b} ==>> {op(a, b)}'] + result


print(*solve([9, 7, 4, 6], 36), sep='\n', end='\n\n')
print(*solve([6, 6, 6, 6], 36), sep='\n', end='\n\n')
print(*solve([6, 6, 6, 6, 6], 36), sep='\n', end='\n\n')
