# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 14:55:21 2019

@author: ldeike
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

folder = r'D:\data_MILES_D\190923_PIV_mae519\piv_pump8V_fps1400_exposure400_dx80um\VEO_4K\\'

im_a = plt.imread(folder+r'piv_pump8V_fps1400_exposure400_dx80um_000001_Cam_VEO_4K_Cine1.tif')
im_b = plt.imread(folder+r'piv_pump8V_fps1400_exposure400_dx80um_000002_Cam_VEO_4K_Cine1.tif')

window_size = 16
x0 = 900
y0 = 900
x1,x2 = x0,x0+window_size
y1,y2 = y0,y0+window_size


#fig,axs = plt.subplots(1,2,figsize=(9,4))
#axs[0].imshow(im_a[y1:y2,x1:x2],cmap='gray',extent=im_extent)
#axs[1].imshow(im_b[y1:y2,x1:x2],cmap='gray',extent=im_extent)

def convolve(dx,dy):
    win_b = im_b[y0+dy:y0+dy+window_size,x0+dx:x0+dx+window_size]
    win_a = im_a[y0:y0+window_size,x0:x0+window_size]
    return np.sum(win_a.astype(float)*win_b.astype(float))


#dx_vec = np.arange(-32,32)
#dy_vec = np.arange(-32,32)
search_size = 24
dx_vec = np.arange(-search_size,search_size)
dy_vec = np.arange(-search_size,search_size)
res = np.zeros((len(dy_vec),len(dx_vec)))
for xi,dx in enumerate(dx_vec):
    for yi,dy in enumerate(dy_vec):
        res[yi,xi] = convolve(dx,dy)
        
        
def make_fig(dx,dy):
            
    fig,axs = plt.subplots(1,3,figsize=(13,4))
    
    axs[0].imshow(im_a,vmin=0,vmax=60000,cmap='gray',origin='lower')
    axs[1].imshow(im_b,vmin=0,vmax=60000,cmap='gray',origin='lower')
    
    axs[0].set_title('Image A')
    axs[1].set_title('Image B')
    
    for ax in axs[0:2]:
        
        #ax.set_xlim(x1-window_size/2,x2+window_size/2)
        #ax.set_ylim(y1-window_size/2,y2+window_size/2)
        ax.set_xlim(x1-search_size,x2+search_size)
        ax.set_ylim(y1-search_size,y2+search_size)
        
    rect_a = Rectangle((x1,y1),window_size,window_size,facecolor='none',edgecolor='r',lw=3)
    axs[0].add_patch(rect_a)
    
    rect_a = Rectangle((x1,y1),window_size,window_size,facecolor='none',edgecolor='r',lw=3,ls='--')
    axs[1].add_patch(rect_a)
    
    window_a = im_a[y0:y0+window_size,x0:x0+window_size]
    
    alpha_min = 00000
    alpha_max = 80000
    
    im_transparent = np.moveaxis(np.array([np.zeros_like(window_a).astype(float)]*4),0,-1)
    im_transparent[:,:,0] = 1
    im_transparent[:,:,-1] = (window_a-alpha_min)/(alpha_max-alpha_min)
    im_transparent[im_transparent<0] = 0
    im_transparent[im_transparent>1] = 1
    
    im_extent = np.array([x1-0.5,x2+0.5,y2+0.5,y1-0.5])
    axs[0].imshow(im_transparent,extent=im_extent)
    
    axs[0].plot(x0+window_size/2,y0+window_size/2,'o',color=[0,1,0])

    im_extent = np.array([x1-0.5+dx,x2+0.5+dx,y2+0.5+dy,y1-0.5+dy])
    axs[1].imshow(im_transparent,extent=im_extent,origin='lower')
    
    rect_b = Rectangle((x1+dx,y1+dy),window_size,window_size,facecolor='none',edgecolor='r',lw=3,ls='-')
    axs[1].add_patch(rect_b)
    
    axs[1].plot(x0+window_size/2,y0+window_size/2,'o',color=[0,1,0],markerfacecolor='none')
    axs[1].plot(x0+window_size/2+dx,y0+window_size/2+dy,'o',color=[0,1,0],)
    axs[1].plot([x0+window_size/2+dx,x0+window_size/2],[y0+window_size/2+dy,y0+window_size/2],'-',color=[0,1,0],)
    
    res_extent = [np.min(dx_vec)-0.5,np.max(dx_vec)+0.5,np.min(dy_vec)-0.5,np.max(dx_vec+0.5)]
    axs[2].imshow(res,extent=res_extent,origin='lower')
    #axs[2].set_xlim(-window_size,window_size)
    #axs[2].set_ylim(-window_size,window_size)
    axs[2].set_xlim(-search_size,search_size)
    axs[2].set_ylim(-search_size,search_size)
    
    axs[2].plot(0,0,'o',color=[0,1,0],markerfacecolor='none')
    axs[2].plot(dx,dy,'o',color=[0,1,0])
    axs[2].plot([0,dx],[0,dy],'-',color=[0,1,0])
    
    for ax in [axs[0],axs[1]]:
        ax.set_xlabel('$x$')
        ax.set_ylabel('$y$')
    axs[2].set_xlabel('$\Delta x$')
    axs[2].set_ylabel('$\Delta y$')
    axs[2].set_title('Cross-correlation')
    
    fig.tight_layout()
    
    return fig

for i in np.arange(20):
    dx = np.random.randint(low=np.min(dx_vec),high=np.max(dx_vec))
    dy = np.random.randint(low=np.min(dy_vec),high=np.max(dy_vec))
    fig = make_fig(dx,dy)
    fig.savefig(r'D:\data_MILES_D\190923_PIV_mae519\piv_correlation_animation_smaller\\frame_'+str(i)+'.png')