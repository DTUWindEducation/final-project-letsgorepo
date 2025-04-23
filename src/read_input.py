import xarray as xr
import numpy as np
import pandas as pd
from pathlib import Path
import glob
import csv

def read_resource_calc_wref(file):  #'1997-1999.nc'
    '''Docstring'''
    # We go outside the src folder to find the inputs folder
    THIS_FILE = Path(file).parent  # current script directory or use __file__
    inputs_dir = THIS_FILE.parent / 'inputs'  # inputs folder is at the same level as src

    # read the .nc files
    nc_files = glob.glob(str(inputs_dir / '*.nc'))  # search for .nc files in the inputs directory (str so that glob.glob can recodnise)

    # length = len(nc_files)  # Use len() to get the number of files

    for nc_file in nc_files:
        # print(f"Processing file: {nc_file}")
    
        # Open the .nc file using xarray
        ds = xr.open_dataset(nc_file, engine="netcdf4")
    
        # Convert the dataset to a DataFrame
        df = ds.to_dataframe().reset_index()  #  

        # Calculate reference windspeed at 100m
        wind_speed_10 = np.sqrt(df.iloc[:, 5]**2 + df.iloc[:, 6]**2)  # Calculate wind speed [m/s]
        wind_direction_10 = (np.arctan2(df.iloc[:, 6], df.iloc[:, 5]) * 180 / np.pi + 360) % 360  # Calculate wind direction [deg]
        wind_speed_100 = np.sqrt(df.iloc[:, 7]**2 + df.iloc[:, 8]**2)  # Calculate wind speed [m/s]
        wind_direction_100 = (np.arctan2(df.iloc[:, 8], df.iloc[:, 7]) * 180 / np.pi + 360) % 360  # Calculate wind direction [deg]
        # MAYBE THIS IS THE OTHER WAY AROUND ???????

        #print(f'wind speed at 10m: {wind_speed_10}')
        #print(f'wind direction at 10m: {wind_direction_10}')
        #print(f'wind speed at 100m: {wind_speed_100}')
        #print(f'wind direction at 100m: {wind_direction_100}')

        # # save as CSV
        # #csv_path = "1997-1999.csv"
        # #df.to_csv(csv_path, index=False)
        
        # close the data 
        ds.close()
        return wind_speed_100, wind_direction_100, wind_speed_10, wind_direction_10

def read_turbine(file):
    # We go outside the src folder to find the inputs folder
    THIS_FILE = Path(file).parent  # current script directory or use __file__
    inputs_dir = THIS_FILE.parent / 'inputs'  # inputs folder is at the same level as src
    
    # read the .csv files
    csv_files = glob.glob(str(inputs_dir / '*.csv'))  # search for .csv files in the inputs directory (str so that glob.glob can recodnise)

    # for csv_file in csv_files:#MAYBE USE FOR LOOP INSTEAD
    turb_15 = pd.read_csv(csv_files[0])
    turb_5 = pd.read_csv(csv_files[1])

    #MAYBE there's a clever way to do this??????
    w5, P5, Cp5, Thrust5, Ct5 = turb_5.iloc[:, 0], turb_5.iloc[:, 1], turb_5.iloc[:, 2], turb_5.iloc[:, 3], turb_5.iloc[:, 4]
    w15, P15, Cp15 = turb_15.iloc[:, 0], turb_15.iloc[:, 1], turb_15.iloc[:, 2]
    size = w15.shape[0]
    Ct15 = np.zeros((size))
    
    return turb_5, turb_15