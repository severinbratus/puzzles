#!/usr/bin/env python3

# Compute the last digit of the n-th Fibonacci number.

def update(params):
    return (params[1], (params[0] + params[1]) % 10)

def solve(n):

    if n == 0 or n == 1: return n

    params = (0, 1)

    # The second element of the pair is the last digit of the second Fib number
    params2index = {(0, 1): 1}
    index2params = {1: (0, 1)}

    # Note that index2params[n] would be the solution in the case of n < T.

    for index in range(2, n):
        params = update(params)

        # If we have seen these params before, it is a period.
        if params in params2index:
            period = index - params2index[params]
            break

        params2index[params] = index
        index2params[index] = params

    return index2params[n % period][1]

last_digit = solve(100)

# f(x) = f(x - T)
# => f(x) = f(x % T)
#
# First we must find T, the smallest value such that f(x) = f(x + T) for some x.
# Iterate over value of x, compute f(x). Once you see a repetition, record T.

# For f as the Fib function, f(x) = f(x - 1) + f(x - 2).
# f: N -> N
# So two numerical parameters (f(i-1), f(i)), determine what f(i+1) and the successive values are.
# Once they repeat, we can enclose the period.
