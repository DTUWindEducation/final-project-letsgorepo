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

#
from assessment.open_nc_files import df

from assessment.read_input import read_resource_calc_wref
ref_ws_100, ref_wd_100, ref_ws_10, ref_wd_10 = read_resource_calc_wref('1997-1999.nc')   #OBS this is for 100m

from assessment.read_input import read_turbine
output = read_turbine('NREL_Reference_5MW_126.csv')

from assessment.sort_read_inputs import sort_four_locations
location1 = sort_four_locations(ref_ws_100, ref_wd_100, ref_ws_10, ref_wd_10, df)
print(location1)
from assessment.interpolate_4_loc import interpolate_4_loc
loc1 = [55.5, 7.75]
loc2 = [55.5, 8.0]
loc3 = [55.75, 7.75]
loc4 = [55.75, 8.0]
coord = [55.6, 7.9]

val = interpolate_4_loc(loc1, loc2, loc3, loc4, coord)
#print(f"Interpolated wind speed: {val} m/s")

#_____End timer____
end_time = time.time()                                      # End timer
running_time = end_time - start_time                        # Difference=time
print(f"Running time = {running_time:.2f}s")                # Print timer