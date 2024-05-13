# Import Python packages

# Library to perform array operations
from matplotlib import pyplot as plt
import numpy as np 
import matplotlib

# Module to set filesystem paths appropriate for user's operating system
from pathlib import Path
# Library to work with netCDF files
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap # type: ignore


directory_path = Path.cwd()  # Current working directory
file_name = 'oscar_vel11537.nc'
file_path = directory_path / file_name

# Open the file using the netCDF4 library
file_id = Dataset(file_path)

# Print the metadata for the "Power" variable
# print(file_id.variables)
lats = file_id.variables['latitude'][:]
lons = file_id.variables['longitude'][:]
depths = file_id.variables['depth'][:]
times = file_id.variables['time'][:]
us = file_id.variables['u'][:]
vs = file_id.variables['v'][:]
print(us[0,0,22,22])
print(lats[22])
print(lons[22])

# Convert longitude coordinates to the desired format (degrees east)
llcrnrlon_east = -47.0 + 360  # Lower left corner longitude (converted to degrees east)
urcrnrlon_east = -35.0 + 360  # Upper right corner longitude (approximate, converted to degrees east)

# Define Basemap with longitude coordinates in degrees east format
map = Basemap(projection='merc', 
              llcrnrlat=-29.0,    # Lower left corner latitude (approximate location of Rio de Janeiro)
              llcrnrlon=llcrnrlon_east,  # Lower left corner longitude (converted to degrees east)
              urcrnrlat=-20.0,    # Upper right corner latitude
              urcrnrlon=urcrnrlon_east,  # Upper right corner longitude (approximate, converted to degrees east)
              resolution='i')

lon,lat = np.meshgrid(lons,lats)
x,y = map(lon,lat)
map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='#cc9955', lake_color='aqua', zorder = 0)
map.drawcoastlines(color = '0.15')


# map.quiver(x[22], y[22], 
#     us[0,0,22,22], vs[0,0,22,22],
#     cmap=plt.cm.autumn)

# Plot vectors
map.quiver(x, y, us[0, 0], vs[0, 0], scale=8)

plt.show()

plt.title('Current map')
plt.show()
