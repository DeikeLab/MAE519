# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 22:22:32 2019

@author: ldeike
"""

import numpy as np
import matplotlib.pyplot as plt
import video_creator as vc

ff = np.load(r'D:\data_MILES_D\190923_PIV_mae519\piv_pump8V_fps1400_exposure400_dx80um\ff.npy')
fps = 1400/5.
dx = 88e-6 * (32./2)

im_shape = np.shape(ff[0,...,0])
im_extent = np.array([0,im_shape[1],0,im_shape[0]])*dx - dx/2
x = np.arange(im_shape[1])*dx
y = np.arange(im_shape[0])*dx

#ff = np.load(r'D:\data_MILES_D\190923_PIV_mae519\piv_pump8V_fps4100_exposure190_dx49um\ff.npy')
#fps = 4100./2

#ff = np.load(r'D:\data_MILES_D\190923_PIV_mae519\piv_pump8V_fps4100_exposure190_dx49um_particleMass6g\ff.npy')
#fps = 4100./2

dt = 1./fps

times = np.arange(len(ff))*dt

# filter out the erroneous values
ff[ff>2] = np.nan
ff[ff<-2] = np.nan

'''
Show mean flow and fluctuations
'''
mean_flow = np.nanmean(ff,axis=0)
fluc = ff-mean_flow
u_rms = np.sqrt(np.nanmean(fluc**2,axis=0))

fig,axs = plt.subplots(2,2,figsize=(12,9))

axs[0,0].imshow(mean_flow[...,0],vmin=-1,vmax=1,cmap='seismic',extent=im_extent)
axs[0,1].imshow(mean_flow[...,1],vmin=-1,vmax=1,cmap='seismic',extent=im_extent)

axs[1,0].imshow(u_rms[...,0],vmin=0,vmax=1,extent=im_extent)
axs[1,1].imshow(u_rms[...,1],vmin=0,vmax=1,extent=im_extent)

fig.tight_layout()

'''
Show profiles along the axis
'''

x_shows = np.linspace(0.02,0.16,9)
fig = plt.figure()
ax = fig.add_subplot(111)
for x_show in x_shows:
    ix = np.argmin(np.abs(x-x_show))
    ax.plot(y,mean_flow[:,ix,0])
    
stophere

fig = plt.figure()
ax = fig.add_subplot(111)

vel = ff[...,1]
vel = vel[~np.isnan(vel)]


bins = np.linspace(-2,2,1001)
hist,bins = np.histogram(vel,bins=bins)
pdf = hist/np.diff(bins)/len(vel)
bin_centers = bins[:-1]+np.diff(bins)


ax.plot(bin_centers,pdf)


def get_hist(vel):
    vel_use = vel[~np.isnan(vel)]
    bins = np.linspace(-2,2,1001)
    hist,bins = np.histogram(vel_use,bins=bins)
    pdf = hist/np.diff(bins)/len(vel_use)
    bin_centers = bins[:-1]+np.diff(bins)
    return pdf,bin_centers

'''
Histogram of velocities, fluctuations in a central box
'''
fig,ax = plt.subplots()
xmin,xmax = 100,120
ymin,ymax = 42,52
ff_use = ff[:,ymin:ymax,xmin:xmax,:]
fluc_use = fluc[:,ymin:ymax,xmin:xmax,:]
for i,color in zip([0,1],['r','b']):
    pdf,bin_centers = get_hist(ff_use[...,i])
    ax.plot(bin_centers,pdf,'-',color=color)
    pdf,bin_centers = get_hist(fluc_use[...,i])
    ax.plot(bin_centers,pdf,'--',color=color)

stophere

fig = plt.figure(figsize=(4,5.5))

def draw_frame(t,fig,timing=None):
    
    axs = [fig.add_subplot(2,2,i+1) for i in range(4)]
    
    i = np.argmin(np.abs(times-t))
    
    axs[0].imshow(ff[i,:,:,0],vmin=-1,vmax=1,cmap='seismic',extent=im_extent)
    axs[1].imshow(ff[i,:,:,1],vmin=-1,vmax=1,cmap='seismic',extent=im_extent)

    axs[2].imshow(fluc[i,:,:,0],vmin=-1,vmax=1,cmap='seismic',extent=im_extent)
    axs[3].imshow(fluc[i,:,:,1],vmin=-1,vmax=1,cmap='seismic',extent=im_extent)
    
    #fig.tight_layout()
    
def draw_frame_justFlow(t,fig,timing=None):
    
    ax_u = fig.add_subplot(211)
    ax_v = fig.add_subplot(212,sharex=ax_u,sharey=ax_u)
    
    i = np.argmin(np.abs(times-t))
    ax_u.imshow(ff[i,:,:,0],vmin=-1,vmax=1,cmap='seismic',extent=im_extent)
    ax_v.imshow(ff[i,:,:,1],vmin=-1,vmax=1,cmap='seismic',extent=im_extent)
    
    ax_u.set_title('$t=$ '+'{:03.3f}'.format(t)+' s')
    
fps_movie = 30.
playback_rate = fps_movie/fps

timing = vc.LinearPlaybackDefinedSpeed(11,12,playback_rate)
scene = vc.Scene(draw_frame_justFlow,timing)
video = vc.Video([scene,],fig,fps=fps_movie)
video.write_video(r'D:\data_MILES_D\190923_PIV_mae519\piv_pump8V_fps1400_exposure400_dx80um\animation_flow.avi')