'''
Open .nc files
This is an extra file, that can run the .nc files,
so an overview can be obtained.
''' 
#______Packages_____
import xarray as xr
from pathlib import Path
import glob

file = '2015-2017.nc'  #file to open

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
print(df)