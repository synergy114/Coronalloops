### Acquiring SDO Images Documentation

#### Introduction
This documentation provides a step-by-step guide on acquiring images from the Solar Dynamics Observatory (SDO) using Python and the SunPy library. SDO provides high-resolution images of the Sun in multiple wavelengths, captured by instruments like the Atmospheric Imaging Assembly (AIA).

#### Prerequisites
- Python installed on your system (version 3.x recommended)
- Installation of required Python packages:
  - SunPy
  - Astropy
  
#### Step 1: Import Necessary Modules
Ensure you have the required modules imported at the beginning of your Python script:

```python
import os
from sunpy.net import Fido
from sunpy.net import attrs as a
from astropy.time import Time
```
#### Step 2: Define Query Parameters

Set the time range, instrument, wavelength, and sample rate for the images you want to download. Customize these parameters according to your requirements:

```python
start_time = Time('YYYY-MM-DDTHH:MM:SS')  # Start time of the observation
end_time = Time('YYYY-MM-DDTHH:MM:SS')    # End time of the observation
query = Fido.search(a.Time(start_time, end_time), 
                    a.Instrument('AIA'),        # Specify SDO instrument (AIA)
                    a.Wavelength(171),         # Specify wavelength (in Ångstrom)
                    a.Sample(111))             # Specify the sampling rate (in hours)
```

#### Step 3: Set Download Directory

Define the directory where you want to save the downloaded images. This directory can be customized based on your preferences:

```python
download_directory = os.path.join(os.path.expanduser('~'), 'FITS_AIA')
```

#### Step 4: Fetch and Download Images

Fetch the images matching the specified criteria and download them to the designated directory:

```python
Fido.fetch(query, download_dir=download_directory)
```