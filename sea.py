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
file_name = 'oscar_vel7001.nc'
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
print(us[0,0,22,22])
print(lats[22])
print(lons[22])

map = Basemap(projection='merc', 
             llcrnrlat = 73.36334172095562,
             llcrnrlon = 31.108892096787862,
             urcrnrlat = 67.0777078459653,
             urcrnrlon = 20.26139309042267,
                resolution = 'i'
             )

lon,lat = np.meshgrid(lons,lats)
x,y = map(lon,lat)
c_scheme = map.pcolor(x,y,np.squeeze(us[0,0,:,:]), cmap = 'jet')
map.drawcoastlines()
map.drawstates()
map.drawcountries()

plt.title('Current map')
plt.show()
