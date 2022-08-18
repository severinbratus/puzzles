#!/usr/bin/env python3

def survey(level):
    '''Return an object that concisely represent `level`, which is possibly enormous'''

    if type(level) == list:
        return [survey(level[0]), "..."]
    elif type(level) == dict:
        return {key: survey(value) for key, value in level.items()}
    else:
        return level

# {
#   "regions": [
#     {
#       "regionID": "BE4E78",
#       "readings": [
#         {
#           "readingID": "A",
#           "reading": [
#             1,
#             "..."
#           ],
#           "date": "1-Dec-2018"
#         },
#         "..."
#       ]
#     },
#     "..."
#   ]
# }

# there is 50 regions.
# each one has 26 readings, by date.
# each reading has 200 entries.

# plan: compute the region(s) with the anomaly in flood capacity, try region ID-s as passwords again?

def hex_to_ascii(hx):
    try:
        return bytearray.fromhex(hx).decode()
    except:
        return None

# for region_id in region_ids:
#     print(region_id, hex_to_ascii(region_id))

with open('flood.txt') as fin:
    data = eval(fin.read())

region_ids = [region["regionID"] for region in data["regions"]]

def compute_capacity(heights):

    left_max = [0] * len(heights)
    for index, height in enumerate(heights):
        if index == 0:
            left_max[index] = height
        else:
            left_max[index] = max(left_max[index - 1], height)

    right_max = [0] * len(heights)
    for index, height in zip(range(len(heights) - 1, -1, -1), reversed(heights)):
        if index == len(heights) - 1:
            right_max[index] = height
        else:
            right_max[index] = max(right_max[index + 1], height)

    level = [min(x, y) for x, y in zip(left_max, right_max)]

    return sum(x - y for x, y in zip(level, heights))


for region in data["regions"]:
    for reading in region["readings"]:
        reading["capacity"] = compute_capacity(reading["reading"])
        reading["regionID"] = region["regionID"]

anomalies = []
diffs = []

for region in data["regions"]:
    for past_reading, reading in zip(region["readings"], region["readings"][1:]):
        diffs.append(reading['capacity'] - past_reading['capacity'])
        if reading['capacity'] - past_reading['capacity'] > 1000:
            anomalies.append((past_reading, reading))

print('Extreme diffs:')
for anomaly in anomalies:
    print(anomaly[1]['capacity'] - anomaly[0]['capacity'])
print()

import numpy as np

sigma = np.std(diffs)
mu = np.mean(diffs)
med = np.median(diffs)

print('Mean:', mu)
print('Std. dev.:', sigma)
print('Median:', med)

# Mean: 14.908
# Std. dev.: 268.9062474841371
# Median: 0.5
#
# Median close to zero. Mean skewed in positive direction because of extreme outliers.

# anomaly_ids = [pair[0]['regionID'] for pair in anomalies]

anomaly_id_triples = [(pair[0]['regionID'], pair[0]['readingID'], pair[1]['readingID']) for pair in anomalies]

answer = ''.join([triple[2] for triple in anomaly_id_triples])
