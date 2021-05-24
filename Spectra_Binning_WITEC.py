# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:40:55 2021

@author: dd
version: 1.1

Bins 2d spectral data into bins of size n*n and displays spectra from the 
selected pixel. Saves binned Y-Axis data to file.
Use to map low intensity signals. 

First, export WITec spectra as ASCII .txt files. 
Header, X-Axis and Y-Axis data are saved in seperate files by default.

Select pixel positions ONLY in raw image. 

Issues:
    * Mouse input to work properly, change Spyder settings in
    Preferences>IPhyton console>Graphics>Backend to Automatic.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#set bin size
n = 4  

#load data
data_folder = 'C:\\DARBAI\\Binning test\\InGaN\\'
header = pd.read_csv(data_folder + 'scan06 (Header).txt', header=None)
xlines = pd.read_csv(data_folder + 'scan06 (X-Axis).txt', header=None).to_numpy()
ylines = pd.read_csv(data_folder + 'scan06 (Y-Axis).txt', header=None).to_numpy() 


#collect information from header
filename = header.iloc[2].str.split('\\').tolist()[0][-1]
graph = header.iloc[3].str.split('=').tolist()[0][-1]
sizeX = int(header.iloc[4].str.split('=').tolist()[0][-1])
sizeY = int(header.iloc[5].str.split('=').tolist()[0][-1])

rawy = ylines.reshape(sizeX, sizeY, 1024)
biny = ylines.reshape(int(rawy.shape[0]//n), n, 
                      int(rawy.shape[1]//n), n, 1024).mean(3).mean(1)


#find max intensity in selected range of raw and binned data
# intensity = np.amax(rawy[:,:,350:550], axis=2)
# intensity_bin = np.amax(biny[:,:,350:550], axis=2)

#find sum intensity in all range of raw and binned data
# intensity = np.sum(rawy[:,:,:], axis=2)
# intensity_bin = np.sum(biny[:,:,:], axis=2)

#find sum intensity in selected range of raw and binned data
intensity = np.sum(rawy[:,:,350:550], axis=2)
intensity_bin = np.sum(biny[:,:,350:550], axis=2)

#plot 2d maps
fig, axs = plt.subplots(1,3, figsize=(17,6))
im0 = axs[0].imshow(intensity, interpolation=None, 
                    vmin=intensity.flatten().mean()-3*intensity.flatten().std(), 
                    vmax=intensity.flatten().mean()+3*intensity.flatten().std())
im1 = axs[1].imshow(intensity_bin, interpolation=None,
                    vmin=intensity_bin.flatten().mean()-3*intensity_bin.flatten().std(), 
                    vmax=intensity_bin.flatten().mean()+3*intensity_bin.flatten().std())
spectr1, = axs[2].plot(xlines, rawy[0,0,], c='blue', label='raw')
axs[2].set_ylim(0,
                max(rawy[0,0,])+2*rawy[0,0,].std())
spectr2, = axs[2].plot(xlines, biny[0,0,], c='red', label='binned')

major_ticks = np.arange(0, rawy.shape[0], 20)
axs[0].set_xticks(major_ticks)
axs[0].set_yticks(major_ticks)

for i in range(2):
    axs[i].set_xlabel('Pixel number')
    axs[i].set_ylabel('Pixel number')
    
axs[0].set_title('Raw data')
axs[1].set_title('Binned data, bin {}*{}'.format(n,n))
axs[2].set_title('File: {} \nScan:{}'.format(filename, graph))
axs[2].set_xlabel('Wavelength (nm)')
axs[2].set_ylabel('Intensity (a.u.)')
axs[2].legend(loc='best')

lhor0 = axs[0].axhline(0,0)
lver0 = axs[0].axvline(0,0)
lhor1 = axs[1].axhline(0,0)
lver1 = axs[1].axvline(0,0)

def onclick(event):
    ix, iy = event.xdata, event.ydata
    print ('x = {}, y = {}'.format(round(ix), round(iy)))

    col = int(round(ix))
    row = int(round(iy))
    
    global axs
    # axs[2].set_ylim(0,
    #             max(rawy[row,col,])+2*rawy[row,col,].std())
    axs[2].set_ylim(min(rawy[row,col,]),
                    max(rawy[row,col,])+3*rawy[row,col,].std())
    spectr1.set_ydata(rawy[row,col,])
    
    spectr2.set_ydata(biny[int(round(row//n)), int(round(col//n)),])
    
    lver0.set_xdata(col)
    lhor0.set_ydata(row)
    lver1.set_xdata(col//n)
    lhor1.set_ydata(row//n)
    
    fig.canvas.draw()
    fig.canvas.flush_events()

cid = fig.canvas.mpl_connect('button_press_event', onclick)

#save binned Y-Axis data to file
binnedy = biny.reshape(int(sizeX/n)*int(sizeY/n)*1024)
binnedy = np.round(binnedy,2)
np.savetxt(data_folder + "binned {}x{} (Y-Axis).txt".format(n,n), binnedy, 
           delimiter=",", fmt='%1.2f')
