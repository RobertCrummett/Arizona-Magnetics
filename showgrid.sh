######################################
# Files
COLORMAP_FILE='arizona_magnetic.cpt'
GRID_FILE='Grids/grid_wgs84.nc'
LEGEND_FILE='legend.txt'

######################################

# Check for colormap existance
if [ -e $COLORMAP_FILE ]
then
  echo "exists!"
else
  echo "dne" 
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

DECLINATION=9.8

######################################
# Plotting figure

gmt begin mag
  # Import Oasis Montaj colormap
  gmt grd2cpt -C${COLORMAP_FILE} ${GRID_FILE}

  # Grid arizona magentic data with shading (-I)
  # -B controls border
  # -I controls intensity, ie, shading
  gmt grdimage ${GRID_FILE} -R${REGION} -JL${LCC_2SP_PROJECTION} -B -B+t"Arizona Total-Field Anomaly" -I+d

  # Contours on the grid
  gmt grdcontour ${GRID_FILE} -C100 -S5 -Wthinnest -L-800/800 -t70

  # Add state boundaries and artifically clip the borders of AZ by filling the other states
  # -A filters out all features greater than min_area=80000km
  # -D controls boundary resulution, h=high
  # -S controls watercolor
  gmt coast -R${REGION} ${BORDER_STATES} -Sskyblue -Dh -A4000

  # Add a colorbar in nT
  gmt psscale -C${COLORMAP_FILE} -I -DJMR+v -Bxaf -By+l"nT"

  # Add length scale and legend
  gmt basemap -LjBL+o1/0.75+c34+w100k+f+u -F+gwhite+c4p/44p/4p/4p+p0.75+s2p/-2p+r
  gmt text legend.txt

  # Add magnetic compass rose
  gmt basemap -TmjTL+d${DECLINATION}+i0.5+o0.45/0.25+p0.5+w1.4c

gmt end show
