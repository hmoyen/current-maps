import sys
import os

sys.path.insert(0,"/usr/lib/python3/dist-packages")

from qgis.core import *

qgs = QgsApplication([], False)


# Load providers

qgs.initQgis()

# Set up the QGIS project instance
project = QgsProject.instance()

# Enable on-the-fly CRS transformation
QgsProject.instance().setCrs(QgsCoordinateReferenceSystem('EPSG:3857'))

# Define the URI for the CSV file and set the CRS to EPSG:4326
uri = "file:///home/lena/workspace_IC/tornado-web/current-maps/meshgrid_data.csv?encoding=UTF-8&delimiter=,&xField=Longitude&yField=Latitude"
vlayer = QgsVectorLayer(uri, "CSV Layer", "delimitedtext")

# Configure the vector field symbol layer
vector_field_layer = QgsVectorFieldSymbolLayer()
vector_field_layer.setXAttribute('U')
vector_field_layer.setYAttribute('V')
vector_field_layer.setVectorFieldType(QgsVectorFieldSymbolLayer.Cartesian)
vector_field_layer.setScale(4)

arrow = QgsArrowSymbolLayer.create(
            {
                "arrow_width": "1",
                "head_length": "3",
                "head_thickness": "2",
                "head_type": "0",
                "arrow_type": "0",
                "is_curved": "0",
                "arrow_start_width": "1"
            }
        )

# Create an arrow symbol
arrow_symbol = QgsMarkerSymbol()

vector_field_layer.subSymbol().changeSymbolLayer(0, arrow) 

# vector_field_layer.copyDataDefinedProperties(arrow_symbol)
arrow_symbol.changeSymbolLayer(0, vector_field_layer)

# Set the renderer to use the arrow symbol
vlayer.renderer().setSymbol(arrow_symbol)

vlayer.triggerRepaint()
# Set the CRS to EPSG:4326
crs = QgsCoordinateReferenceSystem("EPSG:4326")
vlayer.setCrs(crs)

# Check if the layer is valid
if not vlayer.isValid():
    print("Layer failed to load!")

# Add the vector layer to the project
project.addMapLayer(vlayer)

# Define the raster layer (OpenStreetMap) and its CRS
urlWithParams = 'type=xyz&url=https://a.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0&crs=EPSG3857'
rlayer = QgsRasterLayer(urlWithParams, 'OpenStreetMap', 'wms')

# Check if the raster layer is valid
if not rlayer.isValid():
    print("Raster layer failed to load!")

# Add the raster layer to the project
project.addMapLayer(rlayer)

# Write the project to a file
project.write('my_new_qgis_project.qgs')

# Exit QGIS
qgs.exitQgis()