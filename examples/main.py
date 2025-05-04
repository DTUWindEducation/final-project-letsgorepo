#_____Import packages_____
import time                         # For measuring execution time
from pathlib import Path            # For identifying path of file
import glob                         #
import sys                          #
import os                           #
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','src')))

# ____________ USER DEFINES _____________
# Define coordinates and height
coord = (7.8, 55.74)        # Coordinates for interpolation
height = 100                # or 10
# Define reference height
target_height = 80          # need to be between 0 and 100, if above 100, target_height = 100
# Define time period for AEP
time_start = '1997-01-01'   # or from 1997-01-01 to 2008-12-31
time_end = '1997-12-31'
# Define turbine
turb_nr = 5                 # or 15

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

from assessment.read_input import read_resource_calc_wref
data_ref_wind_df, data_nc_wind_df = read_resource_calc_wref('1997-1999.nc')

from assessment.read_input import read_turbine
data_turb5_df, data_turb15_df = read_turbine(f'NREL_Reference_5MW_126.csv')
# Define the variable name dynamically
turbine_name = f"data_turb{turb_nr}_df"  # 'data_turb5_df' or 'data_turb15_df'
# Access the actual DataFrame using globals()
turbine = globals()[turbine_name]

from assessment.interpolate_4_loc import interpolate_speed, interpolate_direction, plot_interpolation
val_speed = interpolate_speed(data_ref_wind_df, coord)
val_dir = interpolate_direction(data_ref_wind_df, coord)
all_in_one = plot_interpolation(val_speed, val_dir, coord)

from assessment.interpolate_4_loc import interpolate_max_ws_100
max_lat, max_lon, max_ws = interpolate_max_ws_100(data_ref_wind_df, height)
print(f"The highest wind speed with {max_ws[0]} [m/s], when interpolating, can be found at coordinate{max_lat, max_lon} (lat, lon)")

# Get interpolated csv files
THIS_FILE = Path('main.py').parent  # current script directory or use __file__
outputs_dir = THIS_FILE.parent / 'outputs'  # inputs folder is at the same level as src
val_dir = outputs_dir / 'winddirection_interpolated_results.csv'
val_sp = outputs_dir / 'windspeed_interpolated_results.csv'
df_wind_direction = pd.read_csv(val_dir)
df_wind_speed = pd.read_csv(val_sp)
val = df_wind_speed.iloc[0,1]

from assessment.interpolate_4_loc import compute_wind_speed_at_height
from assessment.interpolate_4_loc import compute_alpha_from_two_heights
df_alpha = compute_alpha_from_two_heights(data_ref_wind_df)
ws_at_target_height = compute_wind_speed_at_height(
    data_ref_wind_df,
    target_height,
    height,
    df_alpha = df_alpha
)

from assessment.aep import power_range
min_ws, max_ws, power_length, filtered = power_range(data_ref_wind_df, height, turbine, time_start, time_end)

from assessment.weibull import process_weibull
c, k, pdf_range_period = process_weibull(df_wind_speed, coord, height, power_length, min_ws, max_ws)

from assessment.wind_rose import plot_wind_rose
windrose = plot_wind_rose(df_wind_speed, df_wind_direction)

from assessment.aep import calc_aep, calc_aep_per_speed
AEP_for_turb = calc_aep(filtered, pdf_range_period)
print(f"Annual Energy production from {time_start} to {time_end} is {AEP_for_turb} MWh")
result = calc_aep_per_speed(filtered, pdf_range_period, turbine)


#_____End timer____
end_time = time.time()                                      # End timer
running_time = end_time - start_time                        # Difference=time
print(f"Running time = {running_time:.2f}s")                # Print timer