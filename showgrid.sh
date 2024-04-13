##########################################
# Gridding Files
COLORMAP_FILE='Oasis-Montaj-Colors/arizona-magnetics.cpt'
GRID_FILE='Grids/arizona-magnetics-wgs84.nc'

# Text Files
LEGEND_FILE='legend.txt'
SIGNATURE_FILE='signature.txt'

##########################################
# 
#   No edits necessary below this line
#
##########################################

# Check for colormap existance -- if does no exist, run lua script
if ! [ -e $COLORMAP_FILE ]
then
  echo "Creating Oasis Montaj colormap for Arizona total-field anomaly data"
  lua Oasis-Montaj-Colors/rescale_cpt.lua
fi

# Check for grid existance -- if does not exist, generate from python scipts
if ! [ -e $GRID_FILE ]
then
  echo "Gridding Arizona total-field anomaly data"
  python3 preprocess.py
  python3 reproject.py
  python3 regridding.py
  rm Grids/az1000ag*
fi

######################################
# Variables

# Geographic region
# - west/east/south/north
REGION='-115/-108.8/31.2/37.1'

# Lambert Conic Conformal Projection, 2SP
# - lon0/lat0/lat1/lat2/figure_scale
LCC_2SP_PROJECTION='-112/31/33/45/12c'

# Fill border states with white to 'clip' the magnetic grid
BORDER_COLOR=200
BORDER_WIDTH=0.9
BORDER_STATES=''

for STATE in 'CA' 'NV' 'NM' 'CO' 'UT'
do
  BORDER_STATES+="-EUS.${STATE}+g${BORDER_COLOR}+p${BORDER_WIDTH} "
done
BORDER_STATES+="-EMX+g${BORDER_COLOR}+p${BORDER_WIDTH}"

# Modern magentic declination around the middle of AZ
DECLINATION=9.8

######################################
# Plotting figure

gmt begin mag
  # Import Oasis Montaj colormap
  gmt grd2cpt -C${COLORMAP_FILE} ${GRID_FILE}

  # Grid arizona magentic data with shading (-I)
  # -B controls border
  # -I controls intensity, ie, shading
  gmt grdimage ${GRID_FILE} -R${REGION} -JL${LCC_2SP_PROJECTION} -B -B+t"Arizona Total-Field Anomaly" -I+d-55

  # Contours on the grid
  gmt grdcontour ${GRID_FILE} -C100 -S5 -Wthinnest -L-800/800 -t70

  # Add state boundaries and artifically clip the borders of AZ by filling the other states
  # -A filters out all features greater than min_area=80000km
  # -D controls boundary resulution, h=high
  # -S controls watercolor
  gmt coast -R${REGION} ${BORDER_STATES} -Sskyblue -Dh -A4000

  # Add a colorbar in nT
  gmt psscale -C${COLORMAP_FILE} -I -DJMR+o10p/0p+v -Bxa50f -By+l"nT"

  # Add length scale and legend
  gmt basemap -LjBL+o2/0.85+c34+w100k+f+u -F+gwhite+c2p/2p/2p/4p+p0.75+s2p/-2p+r -Bg
  
  # Add projection information
  gmt text -F+a+f6p+jBL,Times-Roman,black+jBL ${LEGEND_FILE}

  # Add magnetic compass rose
  gmt basemap -TmjTL+d${DECLINATION}+i0.5+o0.45/0.25+p0.5+w1.4c

  # Add signature to base map
  gmt text -F+a-21+f6p,Times-Roman,black+jBR ${SIGNATURE_FILE}

gmt end show
