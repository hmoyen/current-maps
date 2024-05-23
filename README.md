## Requirements

- Python 3.6  (to use `comparison.py` - in Windows)
- `pyproj` library
- `matplotlib` library
- `mpl_toolkits.basemap` library
- Custom `localcartesian` module (`.pyd` file)
- local cartesian python (https://github.com/geoffviola/local_cartesian_python/tree/master)

## Installation

1. **Python 3.6**:
   Ensure you have Python 3.6 installed. You can download it from the official Python website: [Python 3.6](https://www.python.org/downloads/release/python-360/)

2. **Required Libraries**:
   Install the required libraries using `pip`:

   ```bash
   pip install pyproj matplotlib basemap mplleaflet

## Observation

Due to this known issue: [Issue](https://github.com/plotly/plotly.py/issues/3624), we need to modify exporter.py file in mplleaflet. 

```
I'm not using Plotly directly but mplleaflet and I got the same error. I managed to make it work by replacing in this exporter.py file
        offset_order = offset_dict[collection.get_offset_position()]
by
        offset_order = offset_dict[collection._offset_position]

Hope it helps someone!
``
