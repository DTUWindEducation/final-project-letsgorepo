'''Open .nc files'''
#______Packages_____
import xarray as xr
import numpy as np
import pandas as pd
from pathlib import Path
import glob

file = '1997-1999.nc'  #file to open

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

    # close the data 
    ds.close()
    
    lat = [7.75, 8.0, 7.75, 8.0]   #define latitudes
    lon =  [55.5, 55.5, 55.75, 55.75]   #define longitudes

    loc0 = (df['latitude'] == lat[0]) & (df['longitude'] == lon[0])
    loc1 = (df['latitude'] == lat[1]) & (df['longitude'] == lon[1])
    loc2 = (df['latitude'] == lat[2]) & (df['longitude'] == lon[2])
    loc3 = (df['latitude'] == lat[3]) & (df['longitude'] == lon[3])

print(df)
print(loc0)
print(loc1)
print(loc2)
print(loc3)