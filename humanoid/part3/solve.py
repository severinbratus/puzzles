from collections.abc import Generator
from collections import deque
from typing import NamedTuple


Point = tuple[int, int]

class Fragment(NamedTuple):
    start : tuple[int, int]
    path : list[str]


def get_vicinity(point):
    for diff in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        yield addv(point, diff)


def addv(a : Point, b : Point) -> Point:
    return tuple(x + y for x, y in zip(a, b))


def subv(a : Point, b : Point) -> Point:
    return tuple(x - y for x, y in zip(a, b))


def prettyprint(mapa : dict, path : list[Point], filename : str, finish_points : list[Point]):
    with open(filename, 'w') as fout:
        for y in range(128):
            for x in range(128):
                print(char_repr((y, x), mapa, path, finish_points), end='', file=fout)
            print(file=fout)

def char_repr(point, mapa, path, finish_points):
    if point not in mapa or mapa[point] == set() or mapa[point] == set(point): return ' '
    if point in finish_points: return 'F'
    if point in path: return '-'
    return '.'

symbol_to_diff = {
    'L': (-1, 0),
    'R': (+1, 0),
    'U': (0, -1),
    'D': (0, +1)
}

diff_to_symbol : dict[Point, str] = {diff: symbol for symbol, diff in symbol_to_diff.items()}


def get_points(fragment : Fragment) -> Generator[tuple[Point, str | None], None, None]:

    point = fragment.start
    yield point, None

    if len(fragment.path) == 0:
        return

    if fragment.path[-1] in ['S', 'F', 'X']:
        end_symbol = fragment.path[-1]
        real_path = fragment.path[:-1]
    else:
        end_symbol = None
        real_path = list(fragment.path)

    for index, symbol in enumerate(real_path):

        point = addv(point, symbol_to_diff[symbol])

        if index != len(real_path) - 1:
            yield point, None

        else:
            if end_symbol != 'X':
                yield point, end_symbol


def backtrace(parents, point, target):

    path_reversed = [point]

    while point != target:

        point = parents[point]
        path_reversed.append(point)

    return list(reversed(path_reversed))


def symbolize(path : list[Point]) -> str:
    return ''.join([diff_to_symbol[subv(next_point, point)] for point, next_point in zip(path, path[1:])])


def make_fragment(line):
    parts = line.strip().split()
    start = tuple(map(int, parts[0].split(',')))

    if len(parts) == 1:
        path = []
    else:
        path = parts[1].split(',')

    return Fragment(start=start, path=path)


# build a graph from all the fragmented strands

if __name__ == '__main__':

    with open('data.txt') as fin:
        lines = fin.readlines()

    fragments = [make_fragment(line) for line in lines]

    terrain : dict[Point, set[Point]] = {}

    start_points = set()
    finish_points = set()

    # assemble fragments of the network together, one by one

    for fragment in fragments:

        for point, symbol in get_points(fragment):

            assert symbol != 'X'

            if symbol == 'F':
                finish_points.add(point)
            elif symbol == 'S':
                start_points.add(point)

            terrain.setdefault(point, set())

            for close_point in get_vicinity(point):

                terrain.setdefault(close_point, set())

                if close_point in terrain:

                    terrain[point].add(close_point)
                    terrain[close_point].add(close_point)


    # now find the shortest path from S to an F w/ BFS

    assert len(start_points) == 1
    start_point = next(iter(start_points))

    queue = deque(start_points)
    queued = set(start_points)

    parents = {}

    finish_point = None

    while queue:

        point = queue.popleft()

        if point in finish_points:
            finish_point = point
            break

        for adj_point in terrain[point]:

            if adj_point not in queued:

                queued.add(adj_point)
                queue.append(adj_point)

                parents[adj_point] = point


    path = backtrace(parents, finish_point, start_point)
    print(symbolize(path))

    prettyprint(terrain, [], 'terrain.txt', finish_points)
    prettyprint(terrain, path, 'terrain-pathed.txt', finish_points)
