""" Reproject NETCDF file to WGS 84

Author: R Nate Crummett
"""

from pathlib import Path

import numpy as np
from pyproj import CRS, Transformer
import xarray as xr

###################################################
# Input file
grid_path = Path("Grids")
lcc_nad27_path = grid_path / Path("az1000ag_lcc_nad27.nc")

# Target CRS to reproject into
crs_target = CRS.from_epsg(4326)

# Output file
target_path = grid_path / Path("az1000ag_wgs84.nc")

###################################################
#
#    No edits necessary below this line
#
###################################################
# Import data
dataset_lcc_nad27 = xr.load_dataset(lcc_nad27_path)

# Extract CSR from data
crs_lcc_nad27 = CRS.from_wkt(dataset_lcc_nad27.proj_wkt)

# Grid positional data
x = dataset_lcc_nad27.x.values
y = dataset_lcc_nad27.y.values
X, Y = np.meshgrid(x, y)

# Create transformation between CRS's
trans = Transformer.from_crs(crs_lcc_nad27, crs_target, always_xy=True)
longitude, latitude = trans.transform(X, Y)

####################################################
# Save output

# Format all as Xarray
ds = xr.Dataset(
    data_vars=dict(tfa=(["yc", "xc"], dataset_lcc_nad27.tfa.values)),
    coords=dict(lon=(["yc", "xc"], longitude), lat=(["yc", "xc"], latitude)),
    attrs=dict(
        description="Arizona Aeromagnetic Anomaly Map, Continued 1000 Feet Above Ground",
        proj_wkt=crs_target.to_wkt(),
    ),
)

# Write reprojected data to NETCDF
ds.to_netcdf(target_path)
