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
file_name = 'gocd_a9800191_46062_199810.nc'
file_path = directory_path / file_name

# # Open the file using the netCDF4 library
file_id = Dataset(file_path)

# # Print the metadata for the "Power" variable
# print(file_id.variables)
lats = file_id.variables['latitude'][:]
lons = file_id.variables['longitude'][:]
# depths = file_id.variables['depth'][:]
times = file_id.variables['time'][:]
us = file_id.variables['u'][:]

# map = Basemap(projection='merc', 
#              llcrnrlat = -22.837625295276528,
#              llcrnrlon = -42.87537375028673,
#              urcrnrlat = -23.39036911317041,
#              urcrnrlon = -43.776860098328285 ,
#                 resolution = 'i'
#              )

# lon,lat = np.meshgrid(lons,lats)
# x,y = map(lon,lat)
# c_scheme = map.pcolor(x,y,np.squeeze(us[0,0,:,:]), cmap = 'jet')
# map.drawcoastlines()
# map.drawstates()
# map.drawcountries()

# plt.title('Current map')
# plt.show()
