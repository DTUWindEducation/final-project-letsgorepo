'''
Open .nc files
This is an extra file, that can run the .nc files,
so an overview can be obtained.
'''
# ______Packages_____
import xarray as xr
from pathlib import Path
import glob

file = '1997-1999.nc'  # file to open

# We go outside the src folder to find the inputs folder
THIS_FILE = Path(file).parent
inputs_dir = THIS_FILE.parent / 'inputs'

# read the .nc files
nc_files = glob.glob(str(inputs_dir / '*.nc'))  # search for .nc files

# length = len(nc_files)  # Use len() to get the number of files

for nc_file in nc_files:
    ds = xr.open_dataset(nc_file, engine="netcdf4")

    # Convert the dataset to a DataFrame
    df = ds.to_dataframe().reset_index()

    # close the data 
    ds.close()
    print(df)
