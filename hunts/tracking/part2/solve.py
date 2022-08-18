#!/usr/bin/env python3

def octet_to_byte(octet):
    return int(octet, 2).to_bytes(1, 'big')

with open('ppb.bin.log') as fin:
    bytesdata = b''.join(list(map(octet_to_byte, fin.read().strip().split())))

strdata = bytesdata.decode()

with open('data.txt', 'w') as fout:
    print(strdata, file=fout)

data = eval(strdata)

# data = [
#     {
#         'date': '1-Dec-2018',
#         'readings': [
#             {
#                 'time': 0, # 0--23
#                 'id': '7D6...',
#                 'contaminants': {
#                     '#16F': 40255
#                     ...
#                 }
#             }
#         ]
#     },
#     ...
# ]

def add_date(reading, date):
    reading['date'] = date
    return reading

readings = [add_date(reading, day_record['date']) for day_record in data for reading in day_record['readings']]

# for day_record in data:
#     for reading in day_record['readings']:
for reading in readings:
    reading['total'] = sum(reading['contaminants'].values())

import numpy as np

totals = [reading['total'] for day_record in data for reading in day_record['readings']]

sigma = np.std(totals)
mu = np.mean(totals)

# for day_record in data:
#     for reading in day_record['readings']:
for reading in readings:
    reading['z-score'] = (reading['total'] - mu) / sigma

def is_anomalous(z):
    return abs(z) >= 1

# what now?
num_anomalies = len(list(filter(lambda reading: is_anomalous(reading['z-score']), readings)))
anomalies = list(filter(lambda reading: is_anomalous(reading['z-score']), readings))

# there is only one anomalous reading.
# if we take its ID, which otherwise serves no purpose (?).
anomaly_id = anomalies[0]['id']
print(bytearray.fromhex(anomaly_id).decode())
