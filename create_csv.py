import numpy as np
import pyproj
from osgeo import gdal, osr
import sys
sys.path.append('c:/Users/helena_moyen/current-maps/.conda/Library/./python')
from qgis.core import *

lat0, lon0 = -23.99218, -46.30013  # Set origin

p = pyproj.Proj(f'+proj=ortho +lat_0={lat0} +lon_0={lon0} +ellps=WGS84 +units=m')

# Read x values from the first .txt file
with open('extracted_posx.txt', 'r') as file:
    x_values = [float(value.strip()) for value in file.read().split(',')]

# Read y values from the second .txt file
with open('extracted_posy.txt', 'r') as file:
    y_values = [float(value.strip()) for value in file.read().split(',')]

# Initialize lists to store transformed latitudes and longitudes
transformed_latitudes = []
transformed_longitudes = []

for i in range(max(len(x_values), len(y_values))):
    if i >= min(len(x_values), len(y_values)):
        lon, lat = p(0, y_values[i], inverse=True)
        transformed_latitudes.append(lat)
    else:
        lon, lat = p(x_values[i], y_values[i], inverse=True)
        transformed_latitudes.append(lat)
        transformed_longitudes.append(lon)

# Convert lists to numpy arrays
transformed_longitudes = np.array(transformed_longitudes)
transformed_latitudes = np.array(transformed_latitudes)

with open('extracted_velx.txt', 'r') as file:
    lines = file.readlines()
print(transformed_latitudes)
matrix_x = []
for line in lines:
    values = line.strip().split(',')
    matrix_x.append([float(value.strip()) for value in values if value.strip()])
matrix_x = np.array(matrix_x)

with open('extracted_vely.txt', 'r') as file:
    lines = file.readlines()

matrix_y = []
for line in lines:
    values = line.strip().split(',')
    matrix_y.append([float(value.strip()) for value in values if value.strip()])
matrix_y = np.array(matrix_y)


# Create meshgrid
lon_grid, lat_grid = np.meshgrid(transformed_longitudes, transformed_latitudes)

# Flatten the meshgrid
lon_flat = lon_grid.flatten()
lat_flat = lat_grid.flatten()

# Flatten the velocity components matrices
u_flat = matrix_x.flatten()
v_flat = matrix_y.flatten()

# Combine flattened latitudes, longitudes, u, and v into a single array
meshgrid_data = np.column_stack((lon_flat, lat_flat, u_flat, v_flat))

# Save to CSV file
np.savetxt('meshgrid_data.csv', meshgrid_data, delimiter=',', header='Longitude,Latitude,U,V', comments='')

print("CSV file 'meshgrid_data.csv' has been created.")
