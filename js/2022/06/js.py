#!/usr/bin/env python
# coding: utf-8


from collections import namedtuple
from itertools import product, repeat
from copy import deepcopy
from functools import partial, cache, reduce


small = False

# 10x10

values = [
    [0, 3, 0, 0, 0, 7, 0, 0, 0, 0],
    [0, 0, 0, 4, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [6, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 3, 0, 6],
    [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 6, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0, 2, 0]
]

region_map = '''
abbbcccccc
aabbbcddcc
aaeeffgdhh
aaiejggghh
aiijjklggh
apionkmmhh
atqooomrrr
ttqsouvwwv
tttssvvwwv
ttttssvvvv
'''.split('\n')[1:-1]


# 5x5

values = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2],
    [0, 0, 4, 0, 0],
    [3, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
] if small else values

region_map = '''
aabbb
caadb
ceafb
chhff
cchgf
'''.split('\n')[1:-1] if small else region_map


@cache
def get_region_id(cell):
    return at(region_map, cell)

def constrain(domains, covers, cell, value):
    '''Constrain the domain of cell with given value, possibly imposing new rules and constraints.
    An invariant: by the end of a call to `constrain` all the constraints for `cell` with `value` as its domain should be set in place.
    '''

    # A value must be in the domain.
    if value not in domains[cell]:
        return None

    # No constrainment possible.
    if invalid(domains, covers):
        return False

    exhibit(domains)
    print()

    # Only constrain once.
    # It makes no sense to constrain what is already certain.

    domains[cell] = [value]

    # For each cell in the same region, deduct value from domain
    _ = deduct(domains, covers, value, [near_cell for near_cell in regions[get_region_id(cell)] if near_cell != cell])
    if not _ or invalid(domains, covers): return None

    # Add a cover for the cells at the radius of value from this cell.
    covers.append(Cover(value, find_bounded_radius(cell, value)))

    # Reduce the domain of cells between this cell and the radius of value.
    for radius in range(1, value):
        _ = deduct(domains, covers, value, find_bounded_radius(cell, radius))
        if not _ or invalid(domains, covers): return None

    # See if there is any conclusions to be made based on the covers.
    for cover in covers:
        matched = list(filter(lambda cell: cover.value in domains[cell], cover.cells))

        if not matched:
            return None
        if len(matched) == 1 and len(domains[matched[0]]) != 1:
            _ = constrain(domains, covers, matched[0], cover.value)
            if not _ or invalid(domains, covers): return None

    # Trim the satisfied covers.
    trim(covers)

    # If the placement of a value in a cell's domain leads to contradiction, deduct that value from the domain.
    for cell in all_cells:
        for value in domains[cell]:
            alt_domains = deepcopy(domains)
            alt_covers = deepcopy(covers)

            # Alter domains.
            for radius in range(1, value):
                deduct_nonrec(alt_domains, value, find_bounded_radius(cell, radius))

            # Add a cover.
            alt_covers.append(Cover(value, find_bounded_radius(cell, value)))

            if invalid(alt_domains, alt_covers):
                deduct(domains, covers, value, [cell])

    # No contradiction
    return True

def trim(covers):
    satisfied_covers = list(filter(lambda cover: satisfied(domains, cover), covers))
    for cover in satisfied_covers:
        covers.remove(cover)

def satisfied(domains, cover):
    return any(domains[cell] == [cover.value] for cell in cover.cells)

def deduct(domains, covers, value, cells):
    '''Every time a value is deducted from the domain, it may be that the domain becomes limited to one value, and that value can be constrained.'''
    for cell in cells:
        if value in domains[cell]:
            if len(domains[cell]) == 2:
                # Constrain the value at cell
                _ = constrain(domains, covers, cell, complement(domains[cell], value))
                if not _: return None
            else:
                domains[cell].remove(value)
            if not domains[cell]:
                return False

    return True

def deduct_nonrec(domains, value, cells):
    for cell in cells:
        if value in domains[cell]:
            domains[cell].remove(value)

def complement(domain, value):
    assert(len(domain) == 2)
    assert(value in domain)
    return domain[1] if domain[0] == value else domain[0]

def at(matrix, cell):
    return matrix[cell[0]][cell[1]]

def find_radius(point, k):
    '''Find all points that are at Manhattan distance k from the given point.'''
    global height, width
    i, j = point
    # Iterate over possible coordinate differences, which should add up to k in abs value.
    for di in range(-k, k+1):
        abs_dj = abs(k) - abs(di)
        for sign_dj in (-1, 1):
            dj = sign_dj * abs_dj
            yield (i + di, j + dj)

def find_bounded_radius(point, k):
    return list(set(filter(lambda radius_point: in_range(radius_point, (height, width)), find_radius(point, k))))

def in_range(values, upper_bounds):
    return all(0 <= value < bound for value, bound in zip(values, upper_bounds))

def invalid(domains, covers):
    return any(domains[cell] == [] for cell in all_cells) or \
        any(not any(cover.value in domains[cell] for cell in cover.cells) for cover in covers)

def complete(domains, covers):
    assert(all(type(cover) == Cover for cover in covers))
    return not invalid(domains, covers) and all(len(domains[cell]) == 1 for cell in all_cells) and \
        all(satisfied(domains, cover) for cover in covers)

def hashd(obj):
    return hash(tuplify(obj))

def tuplify(obj):
    if type(obj) == list:
        return tuple(map(tuplify, obj))
    if type(obj) == dict:
        return tuple(sorted(map(lambda item: tuple(map(tuplify, item)), obj.items())))
    if type(obj) == set:
        return tuple(sorted(obj))
    else:
        return object

def show(domains):
    for i in range(height):
        print(''.join(str(domains[i, j]) for j in range(width)))
    print()

def exhibit(domains):
    global height, width
    widths = dict()
    reprs = dict()
    for col in range(width):
        widths[col] = max(len(repr(domains[(row,col)]).replace(' ','')) for row in range(height))
    for cell in all_cells:
        reprs[cell] = "[%s]" % repr(domains[cell]).replace(' ','')[1:-1].center(widths[cell[1]]-2)
    show(reprs)

def pretty(domains):
    print(*domains.items(), sep='\n')

Cover = namedtuple('Cover', ['value', 'cells'])
# Cell = namedtuple('Cell', ['row', 'col'])
Cell = tuple

height = len(region_map)
width = len(region_map[0])
assert(height == width)
all_cells = list(product(range(height), range(width)))

region_ids = set(''.join(region_map))
regions = {region_id: set(cell for cell in all_cells if get_region_id(cell) == region_id) for region_id in region_ids}

covers = [Cover(value, regions[region_id]) for region_id in region_ids for value in range(1, len(regions[region_id]) + 1)]

domains = {cell: list(range(1, len(regions[get_region_id(cell)]) + 1)) for cell in all_cells}

for cell in all_cells:
    if at(values, cell):
        result = constrain(domains, covers, cell, at(values, cell))
        assert(result)
