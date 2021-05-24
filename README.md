# Spectra_binning_WITec
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
