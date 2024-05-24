## Setup Instructions

To set up this project, you'll need to create a conda environment and install the required packages listed in `requirements.txt`.

### Prerequisites

- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) installed on your system.

```
conda create --name <env> --file requirements.txt

```
## Create TIFF file to use with Leaflet

First, run the `read.py` script to extract data from the `.p3d` file. Next, you should be able to create the TIFF file running the script `gdal_geotiff`. This TIFF file can be used inside the `index.html` script in `tornado-web` repo.
