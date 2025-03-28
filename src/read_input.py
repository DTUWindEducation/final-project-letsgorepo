import xarray as xr
import numpy as np
# import pandas as pd
from pathlib import Path
import glob

# We go outside the src folder to find the inputs folder
THIS_FILE = Path('1997-1999.nc').parent  # current script directory or use __file__
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

    # Calculate reference windspeed
    wind_speed = np.sqrt(df.iloc[:, 5]**2 + df.iloc[:, 6]**2)  # Calculate wind speed [m/s]
    wind_direction = (np.arctan2(df.iloc[:, 6], df.iloc[:, 5]) * 180 / np.pi + 360) % 360  # Calculate wind direction [deg]
    
    print(wind_direction)

    # close the data 
    ds.close()

# # save as CSV
# #csv_path = "1997-1999.csv"
# #df.to_csv(csv_path, index=False)