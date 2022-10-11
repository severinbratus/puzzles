#!/usr/bin/env python3

import mip
from sys import argv

# Playing around...

m, x = mip.Model(), {}

b_1 = m.add_var(var_type=mip.INTEGER, name="b_1", lb=0, ub=2) # type: ignore
b_2 = m.add_var(var_type=mip.INTEGER, name="b_2", lb=0, ub=2) # type: ignore

c_1 = m.add_var(var_type=mip.BINARY, name='c_1')
c_2 = m.add_var(var_type=mip.BINARY, name='c_2')
c_3 = m.add_var(var_type=mip.BINARY, name='c_3')

# d = m.add_var(var_type=mip.INTEGER, name='d', lb=-8, ub=+8) # type: ignore
# d = int(argv[1])
# NOTE: so since this is linear programming, multiplication is not supported, gotta iterate over possible `d` explicitly.
d = -1

# m += (d != 0)

m += (c_1 + c_2 + c_3 == 1)

m += (2 + d * c_1 == b_1)
m += (4 + d * c_2 == b_1 + b_2)
m += (1 + d * c_3 == b_2)

m.optimize()

print('Solution:')
for var in m.vars:
    if var.x > 1e-6:
        print('{} : {}'.format(var.name, var.x))

# The code above models a smaller puzzle:
#
#   2 == 4(3) -- 1
#
# NOTE: 4 is incorrect, it should be 3 instead.
# b_1, b_2 (b for bridge) can take on values from 0 to 2, indicating the number of lines.
# c_1, c_2, c_3 are binary coefficients, exactly one of them being one.
# d is the displacement / correction, -7 <= d <= 7, d != 0.
