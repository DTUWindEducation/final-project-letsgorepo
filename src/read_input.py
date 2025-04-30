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
        ds_data = xr.open_dataset(nc_file, engine="netcdf4")

        # Calculate reference windspeed at 10m and 100m height
        wind_speed_10 = np.sqrt(ds_data.u10**2 + ds_data.v10**2)  # Calculate wind speed [m/s]
        wind_direction_10 = (np.arctan2(ds_data.v10, ds_data.u10) * 180 / np.pi + 360) % 360  # Calculate wind direction [deg]
        wind_speed_100 = np.sqrt(ds_data.u100**2 + ds_data.v100**2)  # Calculate wind speed [m/s]
        wind_direction_100 = (np.arctan2(ds_data.v100, ds_data.u100) * 180 / np.pi + 360) % 360  # Calculate wind direction [deg]
        # MAYBE THIS IS THE OTHER WAY AROUND ???????
        height_10 = np.full_like(wind_speed_10, 10)  # Create an array of 10m with the same shape as wind_speed_10
        height_100 = np.full_like(wind_speed_100, 100)  # Create an array of 100m with the same shape as wind_speed_100
        # Construct the height array
        height_10 = xr.DataArray(height_10, dims=('valid_time', 'latitude', 'longitude'))
        height_100 = xr.DataArray(height_100, dims=('valid_time', 'latitude', 'longitude'))
        
        # Concatenate wind speeds and directions
        wind_speed = xr.concat([wind_speed_10, wind_speed_100], dim='valid_time')
        wind_direction = xr.concat([wind_direction_10, wind_direction_100], dim='valid_time')
        height = xr.concat([height_10, height_100], dim='valid_time')  # Concatenate the height arrays
        
        #Construct the dataset
        # ds_data['Height [m]'] = ('valid_time', 'latitude', 'longitude', height)
        # ds_data['Wind speed [m/s]'] = ('valid_time', 'latitude', 'longitude', wind_speed)
        # ds_data['Wind direction [deg]'] = ('valid_time', 'latitude', 'longitude', wind_direction)
        # ds_data['Latitude'] = ('valid time', ds_data.latitude)
        # ds_data['Longitude'] = ('vali time', ds_data.longitude)
        
        # Convert the dataset to a DataFrame for printing
        df_data = ds_data.to_dataframe().reset_index()  # 

        # # save as CSV
        # #csv_path = "1997-1999.csv"
        # #df.to_csv(csv_path, index=False)
        
        return len(ds_data)
        #return ds_data, df_data

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