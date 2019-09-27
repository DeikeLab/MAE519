'''
Use this module to read in PIV results computed with the PIVLab toolbox in
Matlab.
'''

import numpy as np
import scipy.io
import os.path
import pickle

def save_dict(d,overwrite=True):
    '''
    Save a dict of PIV parameters to a pickled file. 
    '''
    
    fpath = d['folder']+d['name_for_save']+'.pkl'
    
    # if overwrite=False and the file already exists, don't save...
    if overwrite==False and os.path.isfile(fpath)==True:
        print('The file already exists: not overwriting! Set overwrite=True to overwrite.')
        return
    
    # save the file with pickle
    with open(fpath,'wb') as f:
        print('Saving the dict.')
        pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)

def create_dict_and_mat(d,overwrite_dict=False,temp_folder=None):
    '''
    Creates a .mat file of PIV parameters which is read by the MATLAB file 
    run_pivlab_tiffImages.m. Additionally, returns an updated version of the
    dict d containing the same information.
    
    Parameters
    ----------
    d : dict
        Dict with the PIV processing parameters.
        
    Comments
    ----------
    Keys in d should include:
        casename
        folder (where the images are located and the results will be saved)
        dt_orig (the time interval between sequential images)
        dx_orig (the pixel scaling)
        n_passes (the number of passes PIVLab should make)
        area1-area4 (the areas of each pass)
        start_frame (the first frame to use)
        frame_skip (number of frames between paired a and b frames)
        a_frame_skip (number of frames between a frames)        
    '''
    
    # casename plus an underscore
    d['casename_start'] = d['casename']+'_'

    # name for saving the file, if not provided
    if ('name_for_save' in d)==False:
        d['name_for_save'] = d['casename']
    
    # calcualte the a frames
    d['a_frames'] = np.arange(d['start_frame'],d['end_frame'],d['a_frame_skip'])
    
    # calculate the pass areas
    n_passes = d['n_passes']
    final_area = d['final_area']
    areas = np.array([0]*4)
    areas[n_passes-1] = final_area
    for n in range(n_passes-1):
        areas[n] = final_area*2**(n_passes-1-n)
    
    # PIV parameters
    d['n_passes'] = n_passes
    d['area1'] = areas[0]
    d['area2'] = areas[1]
    d['area3'] = areas[2]
    d['area4'] = areas[3]
    d['step1'] = d['area1']/2
    
    # resolution of final product
    d['dx'] = d['dx_orig']*d['final_area']/2. # assuming 50% overlap
    d['dt'] = d['dt_orig']*d['a_frame_skip']
    d['vel_factor'] = d['dx_orig']/(d['dt_orig']*d['frame_diff']) # original pixel spacing divided by time between a and b frames
    
    # save the information as a .mat file for Matlab to read
    scipy.io.savemat(d['folder']+d['name_for_save']+'_matlabParams.mat',d)
    
    # save the updated dict
    save_dict(d,overwrite=overwrite_dict)
    
    return d

def reconstruct_from_Matlab(folder,casename,a_frames):
    '''
    Construct a 4D numpy array with the computed flowfield from the output from
    PIVLab.
    
    Parameters
    ----------
    
    folder : str
        The directory in which the text files produced by PIVLab are stored.
        
    casename_start : str
        The beginning part of each .txt file, not including the underscore or
        frame number or velocity component.
        
    a_frames : np.ndarray
        A 1-d array containing the indices of the "a" frames.
        
    Returns
    ----------
    
    ff : np.ndarray
        The flowfield, an array of shape 4, in which the first axis corresponds
        to the time, the second axis corresponds to the row in the image (the y
        position), the third axis corresponds to the column in the image (the x
        position), the the final axis corresponds to the component of the 
        velocity vector. Therefore ff[0,0,0,0] will return the x-component of
        the velocity (u) in the first snapshot of the flow, at the left-most,
        lowest position in the field of view. ff[0,0,0,1] will return the y-
        componen of the flow (v) at the same time/position.
    '''

    def _read_vel(a):
        '''
        Get the u and v velocity components for a single "a frame"
        '''
        filepath_u = folder+casename+'_'+'{:06d}'.format(a)+'_u.txt'
        filepath_v = folder+casename+'_'+'{:06d}'.format(a)+'_v.txt'
        u = np.genfromtxt(filepath_u,delimiter=',')
        v = np.genfromtxt(filepath_v,delimiter=',')*-1        
        return u,v
    
    # get shape from first frame
    u0,v0 = _read_vel(a_frames[0])
    ny,nx = np.shape(u0) # the number of rows and columns in the PIV field
    
    # initialize the flowfield array
    ff = np.zeros((len(a_frames),ny,nx,2))
    
    # go through each point in time, and add the velocity vector field to ff
    for ai,a in enumerate(a_frames):
        u,v = _read_vel(a)
        ff[ai,:,:,0] = u
        ff[ai,:,:,1] = v
    
    return ff