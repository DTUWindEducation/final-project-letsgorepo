[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zjSXGKeR)

[! '*' means it's a mandatory rubric for pass]
# Notes for the readme
OBS!!!!! the provided input .nc files have latitude and longitude the other way around
The .nc files are wind ressource
The .csv files are specific wind turbines

# Questions for teachers ?????
What is the more clever way to name w, P, cp, thrust, ct? A for-loop? (in read_input.py file)

Is there an extension for opening .nc files?
# Our Great Package

Team: [ADD TEXT HERE!]

## Overview of package*

[ADD TEXT HERE!]

## Quick-start guide (Installation instructions*)
main.py
    Explenation
________________________________________________________________________________
read_input.py
    ----------------------------------------------------------------------------
    read_resource_calc_wref
        INPUT
        File to search for when looking for the path to the .nc files

        OUTPUT
    -----------------------------------------------------------------------------
    read_turbine
        INPUT
        OUTPUT
________________________________________________________________________________
sort_read_inputs.py
    ----------------------------------------------------------------------------
    fort_four_locations:
        INPUT
        The read values from read_values.py
        
        OUTPUT
        1st column    2nd column      3rd column      4th column      5th column
        Latitude      Longitude       Height          Windspeed       Wind direction
_________________________________________________________________________________
interpolate_4_loc.py


EXTRA
open_nc_files.py
    Opens the .nc files since these files cannot be opened. It was used to know what columns to consider when calculating. 

## Code Architecture (include diagram)*

[ADD TEXT HERE!]

## Classes description*

### `WindDataLoader` Class
The `WindDataLoader` class is designed to load wind speed and direction data from NetCDF files and compute reference wind values at multiple heights (10m and 100m). It provides a structured way to extract, process, and format wind data into a pandas DataFrame for further analysis.

---

### Key Features

- **Data Loading**: Opens and loads NetCDF files using `xarray`.
- **Wind Speed and Direction Calculation**: Computes wind speed and meteorological wind direction at 10m and 100m based on `u`/`v` components.
- **Data Conversion**: Converts the dataset into a long-form pandas DataFrame, ready for analysis or visualization.

---

### Methods

#### `__init__(self, file_path)`
Initializes the loader with the path to a NetCDF file.

#### `load_data(self)`
Loads the NetCDF dataset using `xarray` and returns it.

#### `compute_and_format_dataframe(self)`
Computes wind speed and direction at 10m and 100m, and returns a structured long-form DataFrame with relevant fields including:
- `ref_wind_speed`
- `ref_wind_direction`
- `latitude`, `longitude`
- `time`, `height`

## Git flow/ collaboration methodology*

[ADD TEXT HERE !]

## Peer review

[ADD TEXT HERE!]

## Import in Anaconda prompt
conda install anaconda::xarray

windrose:
- Open Anaconda prompt ans go to folder "cd Git 46120\final-project-letsgorepo" or whatever path you have.
- pip install windrose