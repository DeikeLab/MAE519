# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 16:00:18 2019

@author: danjr
"""

import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt

'''
Come up with an arbitrary velocity field with some missing values
'''

# Define the number of columns and rows in the test velocity field
n_x = 50
n_y = 40

# Get  2-D arrays of the x and y locations at each point in the velocity field
x = np.arange(n_x)
y = np.arange(n_y)
X,Y = np.meshgrid(x,y)

# define an arbitrary velocity field
u = np.cos(X/10)+np.sin(Y/10)

# specify the coordinates at which to replace the velocity with nan
nan_coords = [(15,22),(36,40)]

# for each of these coordinates, store the original (target) value, and replace it with nan
orig_values = []
for nan_coord in nan_coords:
    orig_values.append(u[nan_coord[0],nan_coord[1]].copy())
    u[nan_coord[0],nan_coord[1]] = np.nan
    
'''
Use griddata to replace the nan values
'''
    
# this is hod you'd find the nan coordinates if you didn't arbitrarily chooose which ones were nan
nan_coords = np.argwhere(np.isnan(u))

# "flatten" the velocity array and point coordiates, to make it look as if it is a "point cloud" of data
u_flat = u.flatten()
coords = np.array([Y.flatten(),X.flatten()]).T

# which indices in the flattened array have actual (not nan) velocity values
not_nan = ~np.isnan(u.flatten())

# define a new velocity field in which the nans will be replaced with interpolated values
u_interpolated = u.copy()

# for inputs to the inteprolation, use just the coordinates and velocity values that are known
known_coords = coords[not_nan,:]
known_u = u_flat[not_nan]

# replace the nan valuesof u with the interpolated values
u_interpolated[np.isnan(u)] = scipy.interpolate.griddata(known_coords,known_u,nan_coords,method='linear')

# check how well it did
for i,nan_coord in enumerate(nan_coords):
    print('At (x,y)=('+str(nan_coord[1])+','+str(nan_coord[0])+'), the value was '+str(orig_values[i])+' before being nan-ed, and replaced with '+str(u_interpolated[nan_coord[0],nan_coord[1]])+'.')
    
# show velocity field before/after interpolation
fig,axs = plt.subplots(1,2,figsize=(9,4))
axs[0].imshow(u)
axs[0].set_title('Before interpolation')
axs[1].imshow(u_interpolated)
axs[1].set_title('After interpolation')