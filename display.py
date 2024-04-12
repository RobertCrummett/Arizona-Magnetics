from pathlib import Path

import numpy as np
import pygmt
import xarray as xr

data_path = Path("az1000_wgs84.nc")
dataset = xr.load_dataset(data_path)
# masked_data = np.ma.masked_where(dataset.tfa.values == np.nan, dataset.tfa.values)

data = dataset.tfa.values
data[data == np.nan] = 0.0
dataset.tfa.values = data

grid = xr.DataArray(
    dataset.tfa,
    dataset.coords,
)

import matplotlib.pyplot as plt

plt.imshow(grid.values)
plt.show()

fig = pygmt.Figure()

region = [
    np.min(dataset.lon.values),
    np.max(dataset.lon.values),
    np.min(dataset.lat.values),
    np.max(dataset.lat.values),
]

fig.grdimage(
    grid = grid,
    region = region,
    projection = "L-112/31/33/45/12c",
    nan_transparent = True,
    cmap = "turbo",
    frame = "afg",
)

fig.show()
