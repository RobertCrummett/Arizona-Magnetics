from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata
import xarray as xr

#########################################
# Input data path
path_wgs84 = Path("az1000_wgs84.nc")

output_dir = Path("Grids")
output_file = Path("grid_wgs84.nc")

#########################################
# Load data
data_wgs84 = xr.load_dataset(path_wgs84)

#########################################
# Regrid data
xmin, xmax = data_wgs84.lon.min(), data_wgs84.lon.max()
ymin, ymax = data_wgs84.lat.min(), data_wgs84.lat.max()

# Approximate step sizes, even though these change across grid
# Need to figure out better way of doing this...
dy = data_wgs84.lat.values[1,0] - data_wgs84.lat.values[0,0]
dx = data_wgs84.lon.values[0,1] - data_wgs84.lon.values[0,0]

# Grid the latudes and longitudes
xi = np.arange(xmin, xmax + dx, dx)
yi = np.arange(ymin, ymax + dy, dy)
Xi, Yi = np.meshgrid(xi, yi)

# Regrid with linear interpolation
coords = np.stack((data_wgs84.lon.values.flatten(), data_wgs84.lat.values.flatten())).T
tfai = griddata(coords, data_wgs84.tfa.values.flatten(), (Xi, Yi), method = "linear")

#########################################
# Save data as array for GMT
da = xr.DataArray(
    tfai, 
    dims = ("lat", "lon"), 
    coords = dict(lat = yi, lon = xi),
    attrs = dict(
        description = "Arizona Aeromagnetic Anomaly Map, Continued 1000 Feet Above Ground, Regridded for GMT",
        proj_wkt= data_wgs84.proj_wkt,
    ),
)

# Write to disk
da.to_netcdf(output_dir / output_file)
