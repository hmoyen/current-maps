import numpy as np
import pyproj
from mpl_toolkits.basemap import Basemap # type: ignore
from matplotlib import pyplot as plt

lat0, lon0 = -23.99218,  -46.30013 # Set origin

p = pyproj.Proj(f'+proj=tmerc +lat_0={lat0} +lon_0={lon0} +a=6378137.0 +b=6356752.3142 +units=m +ellps=WGS84 +no_defs') # Define WGS-84 Geodetic Datum Ellipsoidal Parameters

# Read x values from the first .txt file
with open('extracted_posx.txt', 'r') as file:
    x_values = [float(value.strip()) for value in file.read().split(',')]

# Read y values from the second .txt file
with open('extracted_posy.txt', 'r') as file:
    y_values = [float(value.strip()) for value in file.read().split(',')]

# Initialize lists to store transformed latitudes and longitudes
transformed_latitudes = []
transformed_longitudes = []

# Iterate over each pair of x and y values
for x in x_values:
    # Transform the x and y values
    lon, lat = p(x, 0, inverse=True)

    transformed_longitudes.append(lon)

for y in y_values:

    lon, lat = p(0,y,inverse=True )

    transformed_latitudes.append(lat)

# print(len(transformed_latitudes))
# print(len(transformed_longitudes))

with open('extracted_velx.txt', 'r') as file:
    # Read each line
    lines = file.readlines()

# Initialize an empty list to store the matrix elements
matrix_x = []

# Iterate through each line
for line in lines:
    # Split the values by comma
    values = line.strip().split(',')
     
    # Convert non-empty values to floats and append to the matrix list
    matrix_x.append([float(value.strip()) for value in values if value.strip()])

# Convert the list to a numpy array
matrix_x = np.array(matrix_x)
# print(matrix_x)

with open('extracted_vely.txt', 'r') as file:
    # Read each line
    lines = file.readlines()

# Initialize an empty list to store the matrix elements
matrix_y = []

# Iterate through each line
for line in lines:
    # Split the values by comma
    values = line.strip().split(',')
     
    # Convert non-empty values to floats and append to the matrix list
    matrix_y.append([float(value.strip()) for value in values if value.strip()])

# Convert the list to a numpy array
matrix_y = np.array(matrix_y)

# print(matrix_y)

map = Basemap(projection='merc',
              llcrnrlat=-24.083556500669236,
              llcrnrlon=-46.407426753421646,
              urcrnrlat=-23.943702371688417,
              urcrnrlon=-46.25227967206122,
              resolution='i',
               epsg = 5641)

lon,lat = np.meshgrid(transformed_longitudes,transformed_latitudes)
x,y = map(lon,lat)
# map.drawcoastlines()
# map.drawcountries()


map.arcgisimage(verbose=True)

map.quiver(x, y, matrix_x, matrix_y, scale=40, color='r')

plt.show()