# fitsImages Class

## Overview

The `fitsImages` class is designed to facilitate the easy manipulation of FITS images. It provides methods to interactively select regions of interest within FITS images, extract sub-images (cutouts) from those regions, and save the sub-images to files. Additionally, it offers functionality to visualize and animate FITS images and their sub-images.

## Usage

To utilize the `fitsImages` class effectively, follow these steps:

1. **Import Dependencies**:
   - Make sure to import the required libraries installed in your working environment:
     ```python
  conda install matplotlib astropy sunpy pandas numpy scipy
     ```
     or 
      ```python
  pip install matplotlib astropy sunpy pandas numpy scipy
     ```
   - Import `SelectionCutOut.py` to your notebook/script
     ```python
     import SelectionCutOut
     from SelectionCutOut import fitsImages
     ```



2. **Instantiate `fitsImages` Object**:
   - Create an instance of the `fitsImages` class by passing the path to the folder containing the FITS images:
     ```python
     fits_images_obj = fitsImages("/path/to/images/folder/")
     ```

3. **Select Regions of Interest**:
   - Use the `SelecToCutOut()` method to select regions of interest within the FITS images and extract sub-images (cutouts). Optionally, specify an output folder name and cutout size:
     ```python
     fits_images_obj.SelecToCutOut(OutputFolderName="NewSubImages/", CutoutSize=512)
     ```
    - Select the left lower corner of the region of interest.

4. **Visualize and Animate Images**:
   - Utilize the `animate()` method to visualize and animate the original FITS images or their sub-images:
     ```python
     fits_images_obj.animate()
     ```

## Methods

The `fitsImages` class provides the following methods for manipulating FITS images:

- **`__init__(self, ImagesFolderPath)`**: Constructor method to initialize the `fitsImages` object with the path to the folder containing the FITS images.

- **`SelecToCutOut(self, OutputFolderName="NewSubImages/", CutoutSize=512)`**: Method to select regions of interest within the FITS images, extract sub-images (cutouts), save them to files and view the subimages as animation. Parameters:
  - `OutputFolderName`: Name of the output folder to store the sub-images (default is "NewSubImages/").
  - `CutoutSize`: Size of the square cutout (default is 512 pixels).

- **`animate(self, subImages=False)`**: Method to visualize and animate the FITS images or their sub-images. Parameters:
  - `subImages`: Boolean flag to indicate whether to animate sub-images (default is False).

## Notes


By following these guidelines and utilizing the provided `fitsImages` class, you can efficiently work with FITS images, extract sub-images, and visualize your data in Python.
