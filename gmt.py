from pathlib import Path

import pygmt
import xarray as xr

data_path = Path("Grids/grid_wgs84.nc")
data = xr.load_dataarray(data_path)

fig = pygmt.Figure()

fig.coast(
    region = [-130, -70, 24, 52],
    projection = "L-100/35/33/45/12c",
    land = "gray",
    shorelines = "1/0.5p, gray30",
    borders = ["1/0.8p,gray30", "2/0.2p.gray30"],
    frame = True,
    dcw = [
        "US.TX+gorange",
        "US.KY+p1p,blue",
    ]
)

fig.grdimage(
    grid = data,
    cmap = "turbo",
    nan_transparent = True,
)

fig.show()
