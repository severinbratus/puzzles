#!/usr/bin/env python3

import cv2
import numpy as np

ascii_to_bgr = {
    ' ': [255, 255, 255],
    '.': [200, 200, 200],
    '_': [190, 162, 129],
    'F': [0, 0, 0]
}

def hex_to_bgr(hx):
    return list(reversed([int(hx[i:i + 2], 16) for i in range(0, len(hx), 2)]))

with open('tissue-pathed.txt') as fin:
    chars = fin.readlines()

width = 128
height = width

canvas = np.zeros((height, width, 3))

for row in range(height):
    for col in range(width):
        canvas[row][col] = ascii_to_bgr[chars[row][col]]

canvas_resized = cv2.resize(canvas, (480, 480), interpolation=cv2.INTER_AREA)
cv2.imwrite('tissue-pathed.png', canvas_resized)
