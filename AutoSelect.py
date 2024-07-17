# matoplotlib, astropy
import os
import glob
import argparse  # Import argparse for command-line argument parsing
from typing import Self
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import astropy.units as u
# sunpy
import sunpy.coordinates  # NOQA
import sunpy.map
from sunpy.net import Fido
from sunpy.net import attrs as a

# pandas, numpy
import pandas as pd
import numpy as np
import sys
import time
import random



# Define a function to perform your image processing
def LoopAutoSelect(fits_file, path, x_step=10, y_step=10, size=512):
    img = sunpy.map.Map(fits_file)
    x1_position = 1000  # Adjust this value to your desired position
    x2_position = 3150  # Adjust this value to your desired position
    y1_position = 1000  # Adjust this value to your desired position
    y2_position = 3150
    #max_crit = 7172.25
    mean_crit = 304.85
    iqr_crit= 470

    dtype = [('x', int), ('y', int), ('mean', np.float16), ('IQR', np.float16)]
    df = np.array([], dtype=dtype)

    for x in range(x1_position, x2_position - size - 1, x_step):
        for y in range(y1_position, y2_position - size - 1, y_step):
            ROI = img.submap((x, y) * u.pixel, height=(size - 1) * u.pixel, width=(size - 1) * u.pixel)
            #max1 = np.max(ROI.data)
            mean1 = np.mean(ROI.data)
            iqr1=np.quantile(ROI.data, .75)-np.quantile(ROI.data, .25)
            

            # Check if subregion meets criteria
            if iqr1 > iqr_crit and mean1 > mean_crit:
            #if max1 > max_crit and mean1 > mean_crit:
                
                current_img = np.array([(x, y, mean1,iqr1)], dtype=dtype)
               
                if df.shape[0] == 0:
                    df = current_img
                else:
                    #detect overlaps    
                    dx = np.abs(df['x'] - x)
                    dy = np.abs(df['y'] - y)
                    dif_area_ratio = (size * (dx + dy) - dx * dy) / (size ** 2)
                    
                    # Overlap regions detection
                    overlap = dif_area_ratio < 0.50
           
                    
                    if any(overlap):
                        less_mean_max = (df['mean'] < mean1) | (df['IQR'] <=iqr1)
                        overlap_index_less = overlap & less_mean_max

                        # Remove rows with overlapping worse image from DataFrame
                        df = df[~overlap_index_less.flatten()]
                        
                        # files that overlap but greater
                        if all(overlap==overlap_index_less):
                            if df.shape[0] == 0:
                                df = current_img
                            else:
                                df = np.vstack([df,current_img])
  
                    else:
                        if df.shape[0] == 0:
                            df = current_img
                        else:
                            df = np.vstack([df,current_img])
    print('x,y \n',df['x'], df['y'] )
    if df.shape[0]!=0:
        _saveROI(img,df['x'].flatten(), df['y'].flatten(), size, path)
        print('Files have been saved')
    else:
        print('No loops detected')
                    
def _saveROI(img, x,y, size, output_path):
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    for i in range(len(x)):
        print('saving image for', x[i], y[i])
        ROI = img.submap((x[i], y[i]) * u.pixel, height=(size - 1) * u.pixel, width=(size - 1) * u.pixel)
        j = random.randint(0, 99)
        ROI.save(f'{output_path}/image{time.strftime("%H%M%S")}{j}.fits', overwrite=False)
    
    
# Define a function to parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Process fits files.")
    parser.add_argument("fits_file", help="Path to fits file")
    parser.add_argument("output_path", help="Output path for processed images")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    LoopAutoSelect(args.fits_file, args.output_path)
