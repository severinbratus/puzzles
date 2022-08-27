#!/usr/bin/env python3

from typing import NamedTuple
from math import cos, asin, sqrt


class Order(NamedTuple):
    id : int
    coords : tuple[float, float]
    weight : int


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12756 * asin(sqrt(a))


def make_order(line):
    order_id, north, east, weight = eval(line.strip().replace(';', ','))
    return Order(id=order_id, coords=(north, east), weight=weight)


def get_distance(order_id_a, order_id_b, distances):
    if order_id_a < order_id_b:
        return distances[order_id_a, order_id_b]
    else:
        return distances[order_id_b, order_id_a]


def main():

    with open('data.txt') as fin:
        orders = [make_order(line) for line in fin.readlines()]

    default_capacity = 10 * 1000 * 1000

    depot_coords = (68.073611, 29.315278)
    depot_order = Order(id=1, coords=depot_coords, weight=0)

    ext_orders = orders + [depot_order]
    order_ids = list(range(1, 10 * 1000 + 2))

    orders_by_id : dict[int, Order] = {order.id: order for order in ext_orders}

    distances = dict()
    for order_id_a in range(1, 10 * 1000 + 2):
        if order_id_a % 1000 == 0:
            print(order_id_a)
        for order_id_b in range(order_id_a, 10 * 1000 + 2):
            order_a = orders_by_id[order_id_a]
            order_b = orders_by_id[order_id_b]
            distances[order_id_a, order_id_b] = distance(order_a.coords[0], order_a.coords[1], order_b.coords[0], order_b.coords[1])

    with open('distances.txt', 'w') as fout:
        print(distances, file=fout)
        for key, value in distances.items():
            print(*key, value, file=fout)

    weights : dict[int, int] = {order.id: order.weight for order in ext_orders}

    total_weight = sum(order.weight for order in orders)
    default_capacity = 10 * 1000 * 1000

    weight_delivered = 0
    current_order_id = depot_order.id
    current_capacity = default_capacity
    visited = set([depot_order.id])
    total_distance = 0

    while weight_delivered != total_weight:

        if weight_delivered % 10 == 0:
            print(f"{weight_delivered=}, {weight_delivered / total_weight=}")

        weight_delivered += weights[current_order_id]
        current_capacity -= weights[current_order_id]
        assert current_capacity >= 0

        # Look for the closest unresolved order that we have capacity for.
        # If there is no such node, go back to the depot.
        try:
            next_order_id = next(filter(lambda other_order_id: other_order_id not in visited and weights[other_order_id] < current_capacity, closest(current_order_id, order_ids, distances)))

        except StopIteration:
            next_order_id = depot_order.id
            # Restore capacity
            current_capacity = default_capacity

        total_distance += get_distance(next_order_id, current_order_id, distances)
        current_order_id = next_order_id
        visited.add(current_order_id)

    return total_distance


def closest(order_id, order_ids, distances):
    return sorted(order_ids, key=lambda other_order_id: get_distance(order_id, other_order_id, distances))


if __name__ == '__main__':
    print(main())
