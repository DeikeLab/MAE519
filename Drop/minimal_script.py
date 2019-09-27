# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 16:32:24 2019

@author: baneel
"""

import matplotlib.pyplot as plt
from skimage import io
from skimage.measure import find_contours
plt.ion()
plt.rcParams['image.cmap'] = 'gray'

### USER INPUT
im_name = 'path_to_image'
threshold = 120

### SCRIPT
im = io.imread(im_name)
# list of contours
contours = find_contours(im, threshold)

# plot
fig, ax = plt.subplots()
ax.imshow(im)
for c in contours:
    row, col = c.T
    ax.plot(col, row)
