'''
Use this script to create a .mat file containing the parameters that
'''

import piv_mae519.interface_PIVLab_with_python

d = {}

# Where the data is
d['folder'] = r'C:\Users\danjr\Documents\Teaching\MAE519_Fall2019\PIV_testing_largescale\\'
d['casename'] = r'piv_pump8V_fps1400_exposure400_dx80um'

# Which frames to use
d['start_frame'] = 1 # the first "a" frame
d['end_frame'] = 999 # the last "a" frame
d['a_frame_skip'] = 2 # how many frames between each "a" frame
d['frame_diff'] = 1 # how many frames between "a" and "b" frames

# window
d['n_passes'] = 2 # how many passes PIVLab should do. each pass size is 2x larger than the next one
d['final_area'] = 32 # the window size for the final pass

# change this if you want to have multiple .mat files for a single PIV movie (say, to compare different processing parameters)
d['name_for_save'] = d['casename']

# use the function to create the .mat file
d = piv_mae519.interface_PIVLab_with_python.create_dict_and_mat(d,overwrite_dict=True,temp_folder=d['folder'])