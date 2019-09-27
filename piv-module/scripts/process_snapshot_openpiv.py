# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 16:31:06 2019

@author: ldeike
"""

# numpy and matplotlib are for math and making figures, respectively
import numpy as np
import matplotlib.pyplot as plt

# import the modules we need from openpiv
import openpiv.tools
import openpiv.process
import openpiv.validation

# time is used to see how long the PIV computation takes
import time

# The folder where the example data is located
folder = r'C:\Users\ldeike\Documents\MAE519_f2019\PIV\MAE519-piv-module\data\\'

# Set the spatial and temporal scaling
dx = 80e-6 # the distance associated with one pixel, in meters
dt = 1./1400 # the time between images acquired by the camera, in seconds

# Load the a and b images, and make their datatype np.int32 
frame_a  = openpiv.tools.imread(folder+'frame_000001.tif').astype(np.int32)
frame_b  = openpiv.tools.imread(folder+'frame_000002.tif').astype(np.int32)

# Set the PIV parameters. Overlap is typically half the window size.
window_size = 32.
overlap = window_size/2.
search_area = window_size

# Compute the correlation to get the velocity field, in units of pixels/timestep
t1 = time.time()
u, v, sig2noise = openpiv.process.extended_search_area_piv( frame_a, frame_b, window_size=window_size, overlap=overlap, dt=1, search_area_size=search_area, sig2noise_method='peak2peak' )
print('PIV calculation took '+str(time.time()-t1)+' seconds.')

# Filter out the points that had a low enough value of signal-to-noise ratio 
u, v, mask = openpiv.validation.sig2noise_val( u, v, sig2noise, threshold = 1.3 )

# Put the two components of velocity into a single 3d numpy array. moveaxis is used so the indexing is ff[row,column,velocity_component]
ff = np.moveaxis(np.array([u,v]),0,-1)

# "Scale" the velocity data by converting pixels/frame to meters/second
ff = ff*(dx/dt)

# Calculate the speed by taking the norm alog the "component" axis of the flowfield array
speed = np.linalg.norm(ff,axis=-1)

# Show a map of the flow speed
fig,ax = plt.subplots()
c=ax.imshow(speed,vmin=0,vmax=1)
cb = fig.colorbar(c)
cb.set_label('speed [m/s]')
ax.set_title('flow speed with window_size = '+str(int(window_size))+' pixels')
fig.tight_layout()