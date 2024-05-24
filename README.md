## Overview

This project requires the following dependencies:
- [NumPy](https://pypi.org/project/numpy/)
- [GDAL](https://pypi.org/project/GDAL/)
- [pyproj](https://pypi.org/project/pyproj/)
- [QGIS](https://www.qgis.org/pt_BR/site/forusers/download.html)

You can set up the project using either a Python virtual environment (`venv`) or Conda. Follow the instructions below to create the environment and install the dependencies.

## Setting Up with `venv` or in Local Machine with PIP

### Prerequisites

- Python installed on your system. Ensure you have Python 3.8 or later.

### Steps

1. **Create a Virtual Environment:**

    ```bash
    python -m venv .venv
    ```

2. **Activate the Virtual Environment:**

    - On Windows:

      ```bash
      .venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```bash
      source .venv/bin/activate
      ```

3. **Install Dependencies:**

    ```bash
    pip install numpy pyproj GDAL
    ```

4. **Install QGIS:**

    Download and install QGIS from the [official QGIS website](https://www.qgis.org/pt_BR/site/forusers/download.html).

Obs: If you encounter errors like `    from qgis.core import * ModuleNotFoundError: No module named 'qgis'`, please refer to [Issues](https://docs.qgis.org/3.34/en/docs/pyqgis_developer_cookbook/intro.html). For `.venv`, adding the following line before the import of `qgis` should solve (in Ubuntu):

```python
import sys
sys.path.insert(0,"/usr/lib/python3/dist-packages")
from qgis.core import *
```
## Setting Up with Conda

### Prerequisites

- Conda installed on your system. You can install Conda by downloading and installing [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution).

### Steps

1. **Clone the Repository:**

    ```bash
    git clone git@github.com:hmoyen/current-maps.git
    cd current-maps
    ```

2. **Create a Conda Environment:**

    ```bash
    conda create --name myenv python=3.8
    ```

3. **Activate the Conda Environment:**

    ```bash
    conda activate myenv
    ```

4. **Install Dependencies:**

    ```bash
    conda install numpy pyproj gdal
    ```

5. **Install QGIS:**

    You can install QGIS through Conda by following the instructions on the [QGIS website](https://plugins.qgis.org/planet/tag/conda/). Typically, this involves adding a specific channel and then installing QGIS:

    ```bash
    conda install qgis --channel conda-forge
    ```

## Verifying Installation

After installing the dependencies, you can verify the installation by running the following Python commands:

```python
import numpy as np
import pyproj
import osgeo.gdal
import qgis
print("All dependencies are successfully installed!")
```
# Running the scripts

## `read.py`

This script reads a `.p3d` file and extract the vector field that to `.txt` files.

##  `gdal_geotiff`

This code will then read the `.txt` files to create a `.tif` file with all the data of the current field. The generated `.tiff` can be used in the `index.html` file in `tornado-web` repo. Run in terminal (in the virtual environment, if you are using one):

```
python3 gdal_geotiff.py

```

