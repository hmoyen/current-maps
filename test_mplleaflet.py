import numpy as np
import pyproj
import mplleaflet
from matplotlib import pyplot as plt

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


lon, lat = np.meshgrid(transformed_longitudes, transformed_latitudes)
fig, ax = plt.subplots()

# kw = dict(color='black', alpha=0.8, scale=50)
q = ax.quiver(lon, lat, matrix_x, matrix_y,scale=40, color='r')

# root, ext = os.path.splitext(__file__)
# mapfile = root  + '.html'
# # Create the map
# mplleaflet.show(path=mapfile, tiles=('https://api.mapbox.com/styles/v1/jwasserman/cir51iqda0010bmnic1s5sb71/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoiandhc3Nlcm1hbiIsImEiOiJjaW9kNnRiaXUwNGh0dmFrajlqZ25wZnFsIn0.CU4YynqRJkmG1PwWDMBJSA', '<a href="https://mapbox.com/about/maps">© 2017 Mapbox</a> | <a href=https://www.openstreetmap.org/about">© OpenStreetMap</a>'))
gj = mplleaflet.fig_to_geojson(fig=fig)
import folium

feature_group0 = folium.FeatureGroup(name='quiver')

mapa = folium.Map(location=[lat.mean(), lon.mean()], tiles="Cartodb Positron",
                  zoom_start=7)

for feature in gj['features']:
    if feature['geometry']['type'] == 'Point':
        lon, lat = feature['geometry']['coordinates']
        div = feature['properties']['html']

        icon_anchor = (feature['properties']['anchor_x'],
                       feature['properties']['anchor_y'])

        icon = folium.features.DivIcon(html=div,
                                       icon_anchor=icon_anchor)
        marker = folium.Marker([lat, lon], icon=icon)
        feature_group0.add_child(marker)
    else:
        msg = "Unexpected geometry {}".format
        raise ValueError(msg(feature['geometry']))

url = 'http://gmrt.marine-geo.org/cgi-bin/mapserv?map=/public/mgg/web/gmrt.marine-geo.org/htdocs/services/map/wms_merc.map'
wms = folium.WmsTileLayer(url,
                                   name='GMRT',
                                   format='image/png',
                                   layers='topo',
                                   transparent=True)
feature_group1 = folium.FeatureGroup(name='Topo')
feature_group1.add_child(wms)
mapa.add_child(feature_group0)
mapa.add_child(feature_group1)
mapa.add_child(folium.map.LayerControl())
mapa.save('html')
