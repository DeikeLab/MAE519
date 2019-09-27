'''
Use this script to read in the PIV results that were calculated using PIVLab in
Matlab.
'''

import piv_mae519.interface_PIVLab_with_python
import numpy as np
import matplotlib.pyplot as plt

folder = r'D:\data_MILES_D\190923_PIV_mae519\piv_pump8V_fps4100_exposure190_dx49um_particleMass6g\\'
casename = r'piv_pump8V_fps4100_exposure190_dx49um_particleMass6g'

# get the list of "a" frames to read in
first_a_frame = 1
last_a_frame = 9999
a_frame_skip = 2
a_frames = np.arange(first_a_frame,last_a_frame,a_frame_skip)

# data for scaling the flowfield to meters/second
dx_orig = 49e-6 # meters
dt_orig = 1./4100 # seconds
a_b_frame_diff = 1 # how many frames between each "a" and "b" pair

# call the function which reads in the data
ff_unscaled = piv_mae519.interface_PIVLab_with_python.reconstruct_from_Matlab(folder,casename,a_frames)

# convert it to meters/second
ff = ff_unscaled * dx_orig / (dt_orig*a_b_frame_diff)

vel_use = ff_unscaled[:,:,:,0].flatten()
vel_use = vel_use[~np.isnan(vel_use)]

plt.figure()
plt.hist(vel_use,bins=300)