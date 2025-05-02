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

[ADD TEXT HERE!]

## Git flow/ collaboration methodology*

[ADD TEXT HERE !]

## Peer review

[ADD TEXT HERE!]

## Import in Anaconda prompt
conda install anaconda::xarray