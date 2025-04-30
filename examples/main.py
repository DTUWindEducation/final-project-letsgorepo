#_____Import packages_____
import time                         # For measuring execution time
from pathlib import Path            # For identifying path of file
import glob                         #
import sys                          #
import os                           #
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

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


from assessment.open_nc_files import df

#this function works
from assessment.read_input import read_resource_calc_wref
df = read_resource_calc_wref('1997-1999.nc')   #OBS this is for 100m
#print(f"read_resource_results: \n", df[['wind_speed_10', 'wind_direction_10', 'wind_speed_100', 'wind_direction_100']])

#
from assessment.read_input import read_turbine
output = read_turbine('NREL_Reference_5MW_126.csv')

#this function also works
from assessment.sort_read_inputs import sort_four_locations
locations_sorted = sort_four_locations(df)
#print(f"locations_sorted = \n", locations_sorted)

#works but with the help of GPT so dont know why /lol
from assessment.interpolate_4_loc import interpolate_4_loc
target_coord = [55.6, 7.9]
interp_ws_10m, interp_ws_100m = interpolate_4_loc(locations_sorted, target_coord)
#print("Interpolated wind speed at 10m (first 5):", interp_ws_10m[:5])
#print("Interpolated wind speed at 100m (first 5):", interp_ws_100m[:5])

from assessment.interpolate_4_loc import compute_wind_speed_at_height
ws_at_80m = compute_wind_speed_at_height(locations_sorted, target_height=80)
print(ws_at_80m)


#_____End timer____
end_time = time.time()                                      # End timer
running_time = end_time - start_time                        # Difference=time
print(f"Running time = {running_time:.2f}s")                # Print timer