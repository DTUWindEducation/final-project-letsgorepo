[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zjSXGKeR)

[! '*' means it's a mandatory rubric for pass]
# Notes for the readme
OBS!!!!! the provided input .nc files have latitude and longitude the other way around
The .nc files are wind ressource
The .csv files are specific wind turbines

# Questions for teachers ?????

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
interpolate_4_loc.py > interpolate_max_ws_100()
    Interpolates the first wind speed value at 100m, but for multiple locations, defined as an array whith latitude and longitude between 55.5 - 55.75 and 7.75 - 8.
    The location is 0.01 specific. 
    Returns the location and the max wind speed.
aep.pu > plot_aep()
    Calculates the AEP for the whole time period, with an interval of 1 month.
## Code Architecture (include diagram)*

[ADD TEXT HERE!]

## Classes description*

[ADD TEXT HERE!]

## Git flow/ collaboration methodology*

[ADD TEXT HERE !]

## Peer review

[ADD TEXT HERE!]

## Import in Anaconda prompt
conda install anaconda::xarray

pip install scipy

windrose:
- Open Anaconda prompt ans go to folder "cd Git 46120\final-project-letsgorepo" or whatever path you have.
- pip install windrose
- Remember to install in you environment