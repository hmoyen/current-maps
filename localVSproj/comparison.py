import numpy as np
import pyproj
from localcartesian import LocalCartesian
from mpl_toolkits.basemap import Basemap
from matplotlib import pyplot as plt

lat0, lon0 = -23.99218, -46.30013  # Set origin

p = pyproj.Proj(f'+proj=tmerc +lat_0={lat0} +lon_0={lon0} +a=6378137.0 +b=6356752.3142 +units=m +ellps=WGS84 +no_defs')

# Read x values from the first .txt file
with open('extracted_posx.txt', 'r') as file:
    x_values = [float(value.strip()) for value in file.read().split(',')]

# Read y values from the second .txt file
with open('extracted_posy.txt', 'r') as file:
    y_values = [float(value.strip()) for value in file.read().split(',')]

# Initialize lists to store transformed latitudes and longitudes
transformed_latitudes = []
transformed_longitudes = []
transformed_latitudes_local = []
transformed_longitudes_local = []

obj = LocalCartesian(0.0, 0.0, 0.0)
obj.reset(lat0, lon0, 0.0)

# Iterate over x values and transform using both pyproj and LocalCartesian
for x in x_values:
    lon, lat = p(x, 0, inverse=True)
    transformed_longitudes.append(lon)

    lat_local, lon_local, alt_local = obj.reverse(x, 0, 0)
    transformed_longitudes_local.append(lon_local)

# Iterate over y values and transform using both pyproj and LocalCartesian
for y in y_values:
    lon, lat = p(0, y, inverse=True)
    transformed_latitudes.append(lat)

    lat_local, lon_local, alt_local = obj.reverse(0, y, 0)
    transformed_latitudes_local.append(lat_local)

# Convert lists to numpy arrays
transformed_longitudes = np.array(transformed_longitudes)
transformed_longitudes_local = np.array(transformed_longitudes_local)
transformed_latitudes = np.array(transformed_latitudes)
transformed_latitudes_local = np.array(transformed_latitudes_local)

# Calculate differences
diff_longitudes = np.abs(transformed_longitudes - transformed_longitudes_local)
diff_latitudes = np.abs(transformed_latitudes - transformed_latitudes_local)

# Print the results
print("Differences in Longitudes:", diff_longitudes)
print("Differences in Latitudes:", diff_latitudes)

print("Are longitudes almost equal? ", np.allclose(transformed_longitudes, transformed_longitudes_local))
print("Are latitudes almost equal? ", np.allclose(transformed_latitudes, transformed_latitudes_local))

with open('extracted_velx.txt', 'r') as file:
    lines = file.readlines()

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

map = Basemap(projection='merc',
              llcrnrlat=-24.083556500669236,
              llcrnrlon=-46.407426753421646,
              urcrnrlat=-23.943702371688417,
              urcrnrlon=-46.25227967206122,
              resolution='i',
              epsg=5641)

lon, lat = np.meshgrid(transformed_longitudes, transformed_latitudes)
x, y = map(lon, lat)

map.arcgisimage(verbose=True)
map.quiver(x, y, matrix_x, matrix_y, scale=40, color='r')

plt.show()
