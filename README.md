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

The core functionality of this project is organized in the `assessment` Python package located in `src/assessment/`.

## Overview of package*

This package provides a set of tools for wind data reading, analysis, and visualization — specifically designed for wind energy applications such as wind resource assessment and wind farm planning.

### Modules included
`__init__`
Is the defalt file that the package should have.

---

`defclasses`
Here we defined a class for loading wind data. It includes file path, open the files, and turn them into dataframe as a preperation to calculate later.

---

`read_input`
Functions for reading NetCDF and wind turbine CSV input data, including calculations of the reference wind speed (the combination of 'u' and 'v', and reference wind directions)

---

`interpolate_4_loc`
In this module we have three functions, which are 
- `interpolate speed`: Interpolate the wind speed at a specific point inside the boundary box.
- `interpolate direction`: Interpolate the wind direction at a specific point inside the boundary box.
- `compute alpha`: Compute each alpha at time series by 10m and 100m.
- `compute apeed at height`: Calculate wind speed at a specific height using power law, taking 10m or 100m as the reference height.

---

`wind_rose`: Plot wind rose diagram that showes the frequencies of different wind direction at a given location (inside the box) and a given height.

---

`AEP`: Compute AEP of a specifed wind turbine (NREL 5 MW or NREL 15 MW) at a given location inside the box for a given year in the period we have provided the wind data
#### Two 'unnecessary files'
`open_nc_files`: This is only for opening the .nc files and see what's inside, and for checking if our function open the file correctly in order.
`sort_read_inputs`: This is an 'extra function' to sort the data according to for different coordinate. It will be used if we need to calculate something for a single location of those four.



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

![Program architecture](inputs/Program_architecture.png)

<div style="font-style: italic; text-align: center;">

</div>

## Classes description*

### `WindDataLoader` Class
The `WindDataLoader` class is designed to load wind speed and direction data from NetCDF files and compute reference wind values at multiple heights (10m and 100m). It provides a structured way to extract, process, and format wind data into a pandas DataFrame for further analysis.
### Key Features

- **Data Loading**: Opens and loads NetCDF files using `xarray`.
- **Wind Speed and Direction Calculation**: Computes wind speed and meteorological wind direction at 10m and 100m based on `u`/`v` components.
- **Data Conversion**: Converts the dataset into a long-form pandas DataFrame, ready for analysis or visualization.
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

First we cloned our team's repo. Then we worked on our own branches with different tasks, commited to our own branches from time to time. After we made our code work, at the time we need to use others outputs to continue working, we merged into main (with all agreements). Then repeated the process until finished.

## Peer review （can be deleted if we dont want it）

[ADD TEXT HERE!]

## Import in Anaconda prompt
conda install anaconda::xarray

windrose:
- Open Anaconda prompt ans go to folder "cd Git 46120\final-project-letsgorepo" or whatever path you have.
- pip install windrose