# Import packages
import xarray as xr
#import pandas as pd
from pathlib import Path

# We go outside the src folder to find the inputs folder
# find path for .nc files
THIS_FILE = Path('1997-1999.nc')  # find where the specific file is
this_dir = THIS_FILE.parent  # define this path

# read the .nc files
nc_file_path = this_dir/'inputs/1997-1999.nc'  # call the path to find all .nc files
#wind_files = sorted(Path(nc_file_path).glob("*.nc"))
ds = xr.open_dataset(nc_file_path)


# turn it into DataFrame
df = ds.to_dataframe().reset_index()

# save as CSV
#csv_path = "1997-1999.csv"
#df.to_csv(csv_path, index=False)

print(f"saved {df}")

# close the data 
ds.close()