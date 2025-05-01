#_____Import packages_____
import time                         # For measuring execution time
from pathlib import Path            # For identifying path of file
import glob                         #
import sys                          #
import os                           #


#_____Start timer for running time of code_____
start_time = time.time()            # Start timer

#____Import reference wind speed____ 
#____Get python to understand where src folder is____in main for now
# Get the path of the current file (main.py)
current_dir = os.path.dirname(__file__)

# Get the absolute path to the project root (one level up from main.py)
project_root = os.path.abspath(os.path.join(current_dir, '..'))

# Add the project root to the system path so Python can find the 'src' package
sys.path.insert(0, project_root)

from src.read_input import read_resource_calc_wref
data_wind_df = read_resource_calc_wref('1997-1999.nc')  #OBS this is for 100m

from src.read_input import read_turbine
data_turb5_df, data_turb15_df = read_turbine('NREL_Reference_5MW_126.csv')

coord = [5.61,7.6] #define specific coordinates to interpolate from
from src.interpolate_4_loc import interpolate_4_loc
val = interpolate_4_loc(data_wind_df, coord)
#print(f"Interpolated wind speed: {val} m/s")

#_____End timer____
end_time = time.time()                                      # End timer
running_time = end_time - start_time                        # Difference=time
print(f"Running time = {running_time:.2f}s")                # Print timer