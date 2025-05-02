#_____Import packages_____
import time                         # For measuring execution time
from pathlib import Path            # For identifying path of file
import glob                         #
import sys                          #
import os                           #
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','src')))

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
data_wind_df, df_data = read_resource_calc_wref('1997-1999.nc')  #OBS this is for 100m
print(f"ref wind speed for 2 heights: \n", data_wind_df)

from assessment.read_input import read_turbine
data_turb5_df, data_turb15_df = read_turbine('NREL_Reference_5MW_126.csv')

coord = (55.75,7.8) #define specific coordinates to interpolate from
#____KEEP!!!____
# from assessment.interpolate_4_loc import interpolate_speed, interpolate_wind_direction
# val_speed = interpolate_speed(data_wind_df, coord)
# print(val_speed)
# val_dir = interpolate_wind_direction(df_data, coord)
# print(val_dir)
from assessment.interpolate_4_loc import interpolate_max_ws_100
height = 100 #or 10
result = interpolate_max_ws_100(data_wind_df, height)
print(result)
#____KEEP!!!____
#____DELETE!!!____
THIS_FILE = Path('main.py').parent  # current script directory or use __file__
outputs_dir = THIS_FILE.parent / 'outputs'  # inputs folder is at the same level as src
val_dir = outputs_dir / 'winddirection_interpolated_results.csv'
val_sp = outputs_dir / 'windspeed_interpolated_results.csv'
df_wind_direction = pd.read_csv(val_dir)
df_wind_speed = pd.read_csv(val_sp)
val = df_wind_speed.iloc[0,1]
#print(val)
#____DELETE!!!____

from assessment.interpolate_4_loc import compute_wind_speed_at_height
from assessment.interpolate_4_loc import compute_alpha_from_two_heights
df_alpha = compute_alpha_from_two_heights(data_wind_df)
target_height = 80
ws_at_80m = compute_wind_speed_at_height(
    data_wind_df,
    target_height,
    ref_height=100,
    df_alpha = df_alpha
)
#print(f"wind speed at {target_height} [m]: \n", ws_at_80m)
# print(df_alpha)

from assessment.wind_rose import plot_wind_rose
windrose = plot_wind_rose(df_wind_speed, df_wind_direction)

#_____End timer____
end_time = time.time()                                      # End timer
running_time = end_time - start_time                        # Difference=time
print(f"Running time = {running_time:.2f}s")                # Print timer