import xarray as xr
import numpy as np
import pandas as pd
from pathlib import Path
import glob


def read_resource_calc_wref(file):  # '1997-1999.nc'
    """
    Reads .nc wind data and calculates reference wind speed and direction
    at 10m and 100m heights for four predefined locations:
        - loc1: 55.5°N, 7.75°E
        - loc2: 55.5°N, 8.00°E
        - loc3: 55.75°N, 7.75°E
        - loc4: 55.75°N, 8.00°E

    Returns both a height-stacked long-format DataFrame and the raw DataFrame.
    """
    # We go outside the src folder to find the inputs folder
    THIS_FILE = Path(file).parent
    inputs_dir = THIS_FILE.parent / 'inputs'

    # read the .nc files
    nc_files = glob.glob(str(inputs_dir / '*.nc'))  # search for .nc files

    # length = len(nc_files)  # Use len() to get the number of files

    for nc_file in nc_files:
        # print(f"Processing file: {nc_file}")

        # Open the .nc file using xarray
        ds_data = xr.open_dataset(nc_file, engine="netcdf4")

        # Convert the dataset to a DataFrame for printing
        df_data = ds_data.to_dataframe().reset_index()

        # Calculate reference wind speed at 10m and 100m height
        df_data['wind_speed_10'] = np.sqrt(df_data['u10']**2 +
                                           df_data['v10']**2)
        df_data['wind_speed_100'] = np.sqrt(df_data['u100']**2 +
                                            df_data['v100']**2)
        # Calculate reference wind direction at 10m and 100m height
        df_data['wind_direction_10'] = (270 - np.arctan2(df_data['v10'],
                                        df_data['u10']) * 180 / np.pi) % 360
        df_data['wind_direction_100'] = (270 - np.arctan2(df_data['v100'],
                                         df_data['u100']) * 180 / np.pi) % 360

        # Reconstruct the data fram and rename
        df_long = pd.concat(
            [
                df_data[['wind_speed_10', 'wind_direction_10',
                         'latitude', 'longitude', 'valid_time']]
                .rename(columns={
                    'wind_speed_10': 'ref_wind_speed',
                    'wind_direction_10': 'ref_wind_direction',
                    'valid_time': 'time'
                    }).assign(height=10),
                df_data[['wind_speed_100', 'wind_direction_100',
                         'latitude', 'longitude', 'valid_time']]
                .rename(columns={
                    'wind_speed_100': 'ref_wind_speed',
                    'wind_direction_100': 'ref_wind_direction',
                    'valid_time': 'time'
                    }).assign(height=100)
            ], axis=0, ignore_index=True)  # stack vertically

    return df_long, df_data


def read_turbine(file):
    """
    Reads turbine power curve CSVs from the inputs folder.
    Returns data for 5 MW and 15 MW turbines.
    """
    # We go outside the src folder to find the inputs folder
    THIS_FILE = Path(file).parent
    inputs_dir = THIS_FILE.parent / 'inputs'

    # read the .csv files
    csv_files = glob.glob(str(inputs_dir / '*.csv'))  # search for .csv files

    # for csv_file in csv_files:#MAYBE USE FOR LOOP INSTEAD
    turb_15 = pd.read_csv(csv_files[0])
    turb_5 = pd.read_csv(csv_files[1])

    return turb_5, turb_15
