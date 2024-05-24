import numpy as np
import pyproj
from osgeo import gdal, osr
from qgis.core import *

lat0, lon0 = -23.99218, -46.30013  # Set origin

p = pyproj.Proj(f'+proj=ortho +lat_0={lat0} +lon_0={lon0} +units=m a=6378137.0 +b=6356752.3142 +no_defs')

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

def getGeoTransform(extent, nlines, ncols):
    resx = (extent[2] - extent[0]) / ncols
    resy = (extent[3] - extent[1]) / nlines
    return [extent[0], resx, 0, extent[3], 0, -resy]

# Define the data extent (min. lon, min. lat, max. lon, max. lat)
extent = [transformed_longitudes[0], transformed_latitudes[-1], transformed_longitudes[-1], transformed_latitudes[0]]  # South America
# Calculate the orientation for each pixel
orientation = np.arctan2(matrix_x, matrix_y) * (180 / np.pi)  # Convert radians to degrees
# Normalize the orientation values to the range [0, 360)
orientation = np.mod(orientation, 360)

# Get GDAL driver for GeoTIFF
driver = gdal.GetDriverByName('GTiff')

# Get dimensions
nlines, ncols = matrix_x.shape
data_type = gdal.GDT_Float32

# Create a new GeoTIFF file
grid_data = driver.Create('vector_field_santos.tif', ncols, nlines, 1, data_type)

# Write orientation data to the single band
grid_data.GetRasterBand(1).WriteArray(orientation)

# Lat/Lon WSG84 Spatial Reference System
srs = osr.SpatialReference()
srs.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

# Setup projection and geo-transform
grid_data.SetProjection(srs.ExportToWkt())
grid_data.SetGeoTransform(getGeoTransform(extent, nlines, ncols))

# Save the file
file_name = 'vector_field_santos.tif'
print(f'Generated GeoTIFF: {file_name}')
driver.CreateCopy(file_name, grid_data, 0)

# Close the file
driver = None
grid_data = None

# Create a reference to the QgsApplication.
qgs = QgsApplication([], True)


pipe = QgsRasterPipe()
rlayer = QgsRasterLayer(file_name, "orientation")
provider = rlayer.dataProvider()
file_writer = QgsRasterFileWriter(file_name)
if not pipe.set(provider.clone()):
    print("Failed to set raster pipe.")
else:
    file_writer.writeRaster(
        pipe,
        provider.xSize(),
        provider.ySize(),
        provider.extent(),
        provider.crs())
    print("TIF file processed successfully.")

qgs.exitQgis()