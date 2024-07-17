
# matoplotlib, astropy
import os
import glob
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
from scipy import stats

import sys

class fitsImages:
    def __init__(self, ImagesFolderPath):
        self.location = ImagesFolderPath
        self.subImageCoords = []
        self.subImageLocation =[]

    def _getFitsMaps(self, subImages=False):
        if subImages:  
            FitsFullImages = glob.glob(f"{self.subImageLocation}/*.fits") 
        else:
            FitsFullImages = glob.glob(f"{self.location}/*.fits")
            
        Maps = sunpy.map.Map(FitsFullImages, sequence=True)
        return Maps

    def _onclick(self, event, CutoutSize):
        ix, iy = int(event.xdata), int(event.ydata)
        self.subImageCoords.append((ix, iy))
        rect = patches.Rectangle(
            (ix, iy), CutoutSize, CutoutSize, linewidth=1, edgecolor='r', facecolor='none')
        plt.gca().add_patch(rect)
        plt.draw()

    def SelecToCutOut(self, OutputFolderName="NewSubImages/", CutoutSize=512):
        self.subImageLocation = os.path.join(self.location, OutputFolderName)
        matplotlib.use('TkAgg')

        # Create the output folder if it doesn't exist
        os.makedirs(self.subImageLocation, exist_ok=True)
        FitsMaps = self._getFitsMaps()
        submaps_files = []
        i = 0

        for aia_map in FitsMaps:
            ###aia_map = sunpy.map.Map(img)
            fig = plt.figure(figsize=(10, 10))
            fig.canvas.mpl_connect(
                'button_press_event', lambda event: self._onclick(event, CutoutSize))
            aia_map.plot(clip_interval=(1, 99.99) * u.percent)
            plt.show(block=True)

            for (x, y) in self.subImageCoords:
                loop = aia_map.submap((x, y) * u.pixel, height=(CutoutSize-1) * u.pixel, width=(CutoutSize-1) * u.pixel)
                loop.save(f"{self.subImageLocation}subimg{i}.fits", overwrite=True)
                submaps_files.append(f"{self.subImageLocation}subimg{i}.fits")
                i += 1
            self.subImageCoords.clear()
        
        self.animate(subImages=True)
        return submaps_files
    
    def animate(self, subImages=False):
        matplotlib.use('TkAgg')
        fitsMaps=self._getFitsMaps(subImages)
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(projection=fitsMaps.maps[0])
        ani = fitsMaps.plot(axes=ax, clip_interval=(1, 99.99) * u.percent, interval=2000)
        plt.show()
    
   