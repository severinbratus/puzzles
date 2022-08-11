from itertools import product
from functools import cache

vec = tuple[int]

from sys import argv

def main():
    with open(argv[1]) as fin:
        lines = [line.strip() for line in fin.readlines()]

    # Read the algorithm and the matrix
    algorithm = lines[0]
    matrix = lines[2:]

    # Provide the desired depth of enhancement as a command-line argument
    reps = int(argv[2])
    margin = reps  +  10

    # Do not remember why these are defined in main(). Haste?

    @cache
    def f(i,  j,  rep):
        '''Find the symbol at (i, j) after `rep` enhancements.
        '''
        # Find andacent point
        adj = ((i + di, j + dj) for di,  dj in product((-1, 0, +1), (-1, 0, +1)))
        # Recurse to find the characters at a lower level of enhancement
        chars = (g(ni,  nj,  rep - 1) for ni, nj in adj)
        retval = algorithm[int(''.join([('1' if c == '#' else '0') for c in chars]), 2)]
        return retval

    def g(i,  j,  rep):
        '''Non-cached helper function for `f`

        Return the original symbol of the matrix in case of no enhancement.
        Otherwise, recurse with `f`.
        '''
        if rep == 0:
            return (matrix[i][j] if inrange(matrix,  i,  j) else '.')
        return f(i,  j,  rep)

    new_matrix = [[g(i,  j,  reps)
        for j in range(-margin,  len(matrix[0]) + margin)] for i in range(-margin,  len(matrix) + margin)]

    print(*[''.join(line) for line in new_matrix],  sep='\n')
    print(sum(line.count('#') for line in new_matrix))


def inrange(mtx,  i,  j):
    '''True iff (`i`, 'j`) is in range of dimensions of `mtx`, a 2-margin array
    '''
    return 0 <= i < len(mtx) and 0 <= j < len(mtx[0])

if __name__ == '__main__':
    main()

## Do not remember why this did not work (reviewing many months after).

#   # what i wanted to do:
#    # cache the cached fun-s
#    funs = [0]*(reps + 1)
#    funs[0] = lambda i, j: (matrix[i][j] if inrange(matrix,  i,  j) else '.')
#    for rep in range(1,  reps + 1):
#
#        pfun = funs[rep-1]
##        @cache
#        def fun(i,  j):
#            print(f'{i=}, {j=}')
#            adj = ((i + di,  j + dj) for di,  dj in product((-1, 0, +1), (-1, 0, +1)))
#            print(pfun)
#            chars = (pfun(ni,  nj) for ni,  nj in adj)
#            retval = algorithm[int(''.join([('1' if c == '#' else '0') for c in chars]),  2)]
#            return retval
#
#        funs[rep] = fun
