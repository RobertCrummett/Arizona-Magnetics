""" Parse raw GXF data file, Save as Xarray

Raw data retrieved from:
https://pubs.usgs.gov/of/2001/ofr-01-0081/html/arizona.htm

Author: R Nate Crummett
"""

from pathlib import Path

import numpy as np
from pyproj import CRS
import xarray as xr

##############################################
# Raw data path
raw_dir = Path("Raw")
data_path = raw_dir / Path("az1000ag_gxf")

# Output NETCDF path
grid_dir = Path("Grids")
lcc_nad27_path = grid_dir / Path("az1000ag_lcc_nad27.nc")

##############################################
#
#    No edits necessary below this line
#
##############################################
# Make sure output directory exists

if not grid_dir.is_dir():
    grid_dir.mkdir()

##############################################
# Projection data extracted manually from raw data file

projection = "lcc"  # lambert conformal conic 2SP
datum = "NAD27"  # NAD27 datum
lat_1, lat_2 = 33, 45  # first and second standard parallels
lat_0 = 31  # latitude of natural origin
lon_0 = -112  # centeral meridian
semimajor = 6378206.4  # semi major axis
e = 0.082271854  # eccentricity
units = "m"  # units of meters
false_easting = 0  # easting at false origin meters
false_northing = 0  # northing at false origin meters
scale = 1  # ellipsoid scale factor

xsize = 1_134  # grid X size
ysize = 1_285  # grid Y size
xorigin = -269_500  # grid X origin meters
yorigin = 35_000  # grid Y origin meters
rotation = 0  # grid rotation degrees
ptsep = 500  # column seperation meters
rwsep = 500  # grid seperation meters
null_value = -1e32  # grid null value

# Compute flatness from provided eccentricity
flatness = 1 - np.sqrt(1 - e**2)  # flatness

# Assemble proj information into CRS object
lcc_nad27_dict = dict(
    proj=projection,
    lat_1=lat_1,
    lat_2=lat_2,
    lat_0=lat_0,
    lon_0=lon_0,
    datum=datum,
    a=semimajor,
    f=flatness,
    x_0=false_easting,
    y_0=false_northing,
    k_0=scale,
    units=units,
)

crs_lcc_nad27 = CRS.from_dict(lcc_nad27_dict)

#############################################
# Parse raw data

# Preallocate space
data = np.empty(xsize * ysize, dtype=float)

# Parse raw file
with open(data_path, "r") as file:
    # Discard header lines...
    for line in file:
        if "#GRID" in line:
            break
    # Translate text to float32 array
    index = 0
    for line in file:
        elements = np.array(line.split(), dtype=float)  # Does not assume line size
        elements[elements == null_value] = np.nan  # Null values are set to nan
        span = len(elements)
        data[index : index + span] = elements
        index += span

# Reshape data array
# Easting (y) should be first coordinate
data = data.reshape((ysize, xsize))

# Construct positions
x = np.arange(0.0, xsize * rwsep, rwsep) + xorigin
y = np.arange(0.0, ysize * ptsep, ptsep) + yorigin

# Format all as Xarray
ds = xr.Dataset(
    data_vars=dict(tfa=(["yc", "xc"], data)),
    coords=dict(x=(["xc"], x), y=(["yc"], y)),
    attrs=dict(
        description="Arizona Aeromagnetic Anomaly Map, Continued 1000 Feet Above Ground",
        dx=rwsep,
        dy=ptsep,
        proj_wkt=crs_lcc_nad27.to_wkt(),
    ),
)

# Write data to disk
ds.to_netcdf(lcc_nad27_path)
