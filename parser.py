''' Parse raw GXF data file, Save as Xarray

Raw data retrieved from:
https://pubs.usgs.gov/of/2001/ofr-01-0081/html/arizona.html
'''
from pathlib import Path

import numpy as np
import xarray as xr

##############################################
# Da#ta paths
data_path = Path("az1000ag_gxf")
output_path = Path(f"{data_path.stem}.nc")

# Meta data
xorigin = -269_500
yorigin = 35_000
rotation = 0
ptsep = 500
rwsep = 500
units = "meters"
mapproj = "NAD27 / az_lambert\nNAD27,6378206.4,0.082271854,0\nLambert Conic Conformal (2SP),33,45,31,-112,0,0"
xsize = 1_134
ysize = 1_285
null_value = -1e32

#############################################
# Preallocate space
data = np.empty(xsize*ysize, dtype = float)

# Parse raw file
with open(data_path, "r") as file:
    # Discard header lines....
    for line in file:
        if "#GRID" in line:
            break
    # Translate text to float32 array
    index = 0
    for line in file:
        elements = np.array(line.split(), dtype = float)
        elements[elements == null_value] = np.nan # Null values are set to nan
        span = len(elements)
        data[index:index+span] = elements
        index += span

# Reshape data array
# Easting (y) should be first coordinate
data = data.reshape((ysize, xsize)) 

# Construct positions
x    = np.arange(0.0, xsize * rwsep, rwsep) + xorigin
y    = np.arange(0.0, ysize * ptsep, ptsep) + yorigin

# Format all as Xarray
ds = xr.Dataset(
        data_vars = dict(tfa = (["yc", "xc"], data)),
        coords = dict(x = (["xc"], x),
                      y = (["yc"], y)),
        attrs = dict(
            description = "Arizona Aeromagnetic Anomaly Map, Continued 1000 Feet Above Ground",
            dx = rwsep,
            dy = ptsep,
            units = units,
            mapproj = mapproj, 
            xorigin = xorigin,
            yorigin = yorigin,
            rotation = rotation))

# Write data to disk
ds.to_netcdf(output_path)
