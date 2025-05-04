#----Import packages
from scipy.interpolate import RegularGridInterpolator
import numpy as np
import pandas as pd
from pathlib import Path            # For identifying path of file
from scipy.interpolate import RectBivariateSpline # For intepolation
from scipy.interpolate import LinearNDInterpolator # For interpolation
from scipy.interpolate import RegularGridInterpolator  # For interpolation
import matplotlib.pyplot as plt # For plotting

def interpolate_speed(wr_data_df, target_coord):
    # Ensure the data is sorted
    wr_data_df = wr_data_df.sort_values(['longitude', 'latitude', 'time'])

    # Get unique sorted grid axes
    X = np.sort(wr_data_df['longitude'].unique())  # lon
    Y = np.sort(wr_data_df['latitude'].unique())   # lat
    T = np.sort(wr_data_df['time'].unique())       # time

    # Pivot to make a 3D array (lon x lat x time)
    # Assume there is one measurement per (lon, lat, time)
    reshaped = wr_data_df.pivot_table(
        index=['longitude', 'latitude', 'time'],
        values='ref_wind_speed'
    ).unstack().sort_index()

    # Convert to 3D array
    ts_for_4_points = reshaped.values.reshape(len(X), len(Y), len(T))

    # Build interpolator (note: only over lon/lat)
    interp = RegularGridInterpolator((X, Y), ts_for_4_points)

    # Interpolate for the time series at target location
    ts_interp = interp(target_coord)  # shape: (num_time_steps,)
    
    # Optional: plot
    plt.plot(ts_interp)
    plt.title(f'Interpolated time series at {target_coord}')
    plt.xlabel('Time index')
    plt.ylabel('Wind speed')
    plt.grid(True)
    
    # Define path
    current_dir = Path(__file__).parent.resolve()  # Folder where the script is located
    output_dir = current_dir.parent.parent / "outputs"  # Go up 2 levels, then into "output"
    # --- Create the output folder if it doesn't exist ---
    output_dir.mkdir(exist_ok=True)  
    # Save plot
    output_path = output_dir / "interpolated_wind_speed.png"
    plt.gcf().savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    return ts_interp

def interpolate_direction(wr_data_df, target_coord):
    # Ensure the data is sorted
    wr_data_df = wr_data_df.sort_values(['longitude', 'latitude', 'time'])

    # Get unique sorted grid axes
    X = np.sort(wr_data_df['longitude'].unique())  # lon
    Y = np.sort(wr_data_df['latitude'].unique())   # lat
    T = np.sort(wr_data_df['time'].unique())       # time

    # Pivot to make a 3D array (lon x lat x time)
    # Assume there is one measurement per (lon, lat, time)
    reshaped = wr_data_df.pivot_table(
        index=['longitude', 'latitude', 'time'],
        values='ref_wind_direction'
    ).unstack().sort_index()

    # Convert to 3D array
    ts_for_4_points = reshaped.values.reshape(len(X), len(Y), len(T))

    # Build interpolator (note: only over lon/lat)
    interp = RegularGridInterpolator((X, Y), ts_for_4_points)

    # Interpolate for the time series at target location
    ts_interp = interp(target_coord)  # shape: (num_time_steps,)
    
    # Plot
    plt.plot(ts_interp)
    plt.title(f'Interpolated time series at {target_coord}')
    plt.xlabel('Time index')
    plt.ylabel('Wind direction')
    plt.grid(True)
    
    # Define path
    current_dir = Path(__file__).parent.resolve()  # Folder where the script is located
    output_dir = current_dir.parent.parent / "outputs"  # Go up 2 levels, then into "output"
    # --- Create the output folder if it doesn't exist ---
    output_dir.mkdir(exist_ok=True)  
    # Save plot
    output_path = output_dir / "interpolated_wind_direction.png"
    plt.gcf().savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    return ts_interp

# LOOK we turned the code below to the code above, impressive right? :D

# def interpolate_speed(wr_data_df, target_coord):
#         """
#         Interpolates wind speeds at a target location for multiple heights.
        
#         Args:
#             wr_data_df (pd.DataFrame): Input data with columns 'latitude', 'longitude', 'ref_wind_speed', 'time', 'height'.
#             target_coord (tuple): Target (lat, lon) to interpolate.
#             heights (list): List of heights (e.g., [10, 100]) to interpolate.
            
#         Returns:
#             pd.DataFrame: Time series with interpolated speeds for each height.
#         """
#         heights = [10, 100]
#         # Ensure column names match
#         wr_data_df = wr_data_df.rename(columns={
#             'Latitude': 'latitude',
#             'Longitude': 'longitude',
#             'Per wind speed': 'ref_wind_speed'
#         })
        
#         results = []
        
#         for height in heights:
#             # Filter by height and sort by time
#             df_height = wr_data_df[wr_data_df['height'] == height].copy()
#             df_height = df_height.sort_values('time')
            
#             times = df_height['time'].unique()
#             interpolated_speeds = []
            
#             for t in times:
#                 df_t = df_height[df_height['time'] == t]
                
#                 # Get 2x2 grid (sorted unique lat/lon)
#                 latitudes = sorted(df_t['latitude'].unique())
#                 longitudes = sorted(df_t['longitude'].unique())
                
#                 if len(latitudes) != 2 or len(longitudes) != 2:
#                     raise ValueError(f"Expected 2x2 grid, got {len(latitudes)}x{len(longitudes)} at time {t}")
                
#                 # Build wind speed grid
#                 wind_grid = np.empty((2, 2))
#                 for i, lat in enumerate(latitudes):
#                     for j, lon in enumerate(longitudes):
#                         value = df_t[
#                             (df_t['latitude'] == lat) & 
#                             (df_t['longitude'] == lon)
#                         ]['ref_wind_speed'].values
#                         if len(value) == 1:
#                             wind_grid[i, j] = value[0]
#                         else:
#                             raise ValueError(f"Ambiguous/missing data at lat={lat}, lon={lon}, time={t}")
                
#                 # Interpolate
#                 interp = RegularGridInterpolator((latitudes, longitudes), wind_grid, method='linear')
#                 interpolated_speeds.append(interp([target_coord])[0])
            
#             results.append(pd.DataFrame({
#                 'time': times,
#                 f'wind_speed_{height}m': interpolated_speeds
#             }))
        
#         # Merge results for all heights
#         result_df = results[0]
#         for df in results[1:]:
#             result_df = result_df.merge(df, on='time', how='outer')
        
#         # save result
#         # --- Define paths ---
#         current_dir = Path(__file__).parent.resolve()  # Folder where the script is located
#         output_dir = current_dir.parent.parent / "outputs"  # Go up 2 levels, then into "output"

#         # --- Create the output folder if it doesn't exist ---
#         output_dir.mkdir(exist_ok=True)  

#         # --- Save `result_df` to CSV in the output folder ---
#         output_file = output_dir / "windspeed_interpolated_results.csv"  # Define filename
#         result_df.to_csv(output_file, index=False)  # Save as CSV (no index)

#         return result_df.sort_values('time')


# def interpolate_max_ws_100(wr_data_df, height):
#     '''Calculate the location inside the box, with maximum windspeed using interpolation

#     Args:
#         wr_data_df (pd.DataFrame): A DataFrame containing wind resource data with columns including 
#             'latitude', 'longitude', 'height', and 'ref_wind_speed'.
#         height (int or float): The hub height at which to filter wind speed data for interpolation (e.g., 100).

#     Returns:
#         tuple: A tuple (latitude, longitude, wind_speed) corresponding to the location within the defined 
#         grid that has the maximum interpolated wind speed.'''
    
#     lat_range = np.arange(55.5, 55.75, 0.01)
#     lon_range = np.arange(7.75, 8, 0.01)
#     # Create a mesh grid
#     lat_grid, lon_grid = np.meshgrid(lat_range, lon_range)

#     # Flatten and combine to (lat, lon) tuples
#     grid_points = list(zip(lat_grid.ravel(), lon_grid.ravel()))

#     # Filter rows where height is 100
#     filtered_df = wr_data_df[wr_data_df['height'] == height]

#     # Select first 4 rows where ref_wind_speed meets the condition
#     # Ensure you're taking the first 4 unique lat, lon pairs
#     first_4_values = filtered_df[['latitude', 'longitude', 'ref_wind_speed']].drop_duplicates(subset=['latitude', 'longitude'])

#     points = first_4_values[['latitude', 'longitude']].to_numpy()  # Lat, Lon pairs
#     ref_wind_speed = first_4_values['ref_wind_speed'].to_numpy()  # Corresponding ref_wind_speed values
    
#     # Build interpolator
#     interpolator = LinearNDInterpolator(points,ref_wind_speed)

#     #Create a new list with interpolated values for each grid point
#     interpolated_values = []
#     for i in grid_points:
#         interpolated_value = interpolator(np.array(i))  # Get interpolated wind speed for this point
#         interpolated_values.append((i[0], i[1], interpolated_value))  # Append the (lat, lon, ref_wind_speed)
    
#     # Find the maximum ref_wind_speed in the interpolated values
#     max_ref_wind_speed = max(interpolated_values, key=lambda x: x[2])  # x[2] is the ref_wind_speed value
#     # Extract the latitude, longitude, and the max ref_wind_speed
#     max_lat, max_lon, max_ws = max_ref_wind_speed

#     # Print the corresponding latitude, longitude, and the max ref_wind_speed
#     print(f"Maximum Wind Speed: {max_ws} m/s")
#     print(f"At Latitude: {max_lat}, Longitude: {max_lon}")
    
#     return max_ref_wind_speed


# def interpolate_wind_direction(wr_data_df, target_coord):
#     """
#     Interpolates wind direction at a target location for multiple heights using u and v components.
    
#     Args:
#         wr_data_df (pd.DataFrame): Input data with columns 'latitude', 'longitude', 'u10', 'u100', 'v10', 'v100', 'time'.
#         target_coord (tuple): Target (lat, lon) to interpolate.
        
#     Returns:
#         pd.DataFrame: Time series with interpolated wind directions for each height.
#     """
#     heights = [10, 100]
    
#     # Ensure column names match
#     wr_data_df = wr_data_df.rename(columns={
#         'Latitude': 'latitude',
#         'Longitude': 'longitude'
#     })
    
#     results = []
    
#     for height in heights:
#         # Create a copy for this height
#         df_height = wr_data_df.copy()
        
#         # Add height-specific u and v components
#         df_height['u'] = df_height[f'u{height}']
#         df_height['v'] = df_height[f'v{height}']
        
#         df_height = df_height.sort_values('time')
#         times = df_height['time'].unique()
#         interpolated_directions = []
        
#         for t in times:
#             df_t = df_height[df_height['time'] == t]
            
#             # Get 2x2 grid (sorted unique lat/lon)
#             latitudes = sorted(df_t['latitude'].unique())
#             longitudes = sorted(df_t['longitude'].unique())
            
#             if len(latitudes) != 2 or len(longitudes) != 2:
#                 raise ValueError(f"Expected 2x2 grid, got {len(latitudes)}x{len(longitudes)} at time {t}")
            
#             # Build u and v component grids
#             u_grid = np.empty((2, 2))
#             v_grid = np.empty((2, 2))
            
#             for i, lat in enumerate(latitudes):
#                 for j, lon in enumerate(longitudes):
#                     u_value = df_t[
#                         (df_t['latitude'] == lat) & 
#                         (df_t['longitude'] == lon)
#                     ]['u'].values
                    
#                     v_value = df_t[
#                         (df_t['latitude'] == lat) & 
#                         (df_t['longitude'] == lon)
#                     ]['v'].values
                    
#                     if len(u_value) == 1 and len(v_value) == 1:
#                         u_grid[i, j] = u_value[0]
#                         v_grid[i, j] = v_value[0]
#                     else:
#                         raise ValueError(f"Ambiguous/missing data at lat={lat}, lon={lon}, time={t}")
            
#             # Interpolate u and v components
#             interp_u = RegularGridInterpolator((latitudes, longitudes), u_grid, method='linear')
#             interp_v = RegularGridInterpolator((latitudes, longitudes), v_grid, method='linear')
            
#             u_interp = interp_u([target_coord])[0]
#             v_interp = interp_v([target_coord])[0]
            
#             # Calculate wind direction (0° = north, 90° = east)
#             wind_dir = (270 - np.degrees(np.arctan2(v_interp, u_interp))) % 360
#             interpolated_directions.append(wind_dir)
        
#         results.append(pd.DataFrame({
#             'time': times,
#             f'wind_direction_{height}m': interpolated_directions
#         }))
    
#     # Merge results for all heights
#     result_df = results[0]
#     for df in results[1:]:
#         result_df = result_df.merge(df, on='time', how='outer')
    
    
#     # save result
#     # --- Define paths ---
#     current_dir = Path(__file__).parent.resolve()  # Folder where the script is located
#     output_dir = current_dir.parent.parent / "outputs"  # Go up 2 levels, then into "output"

#     # --- Create the output folder if it doesn't exist ---
#     output_dir.mkdir(exist_ok=True)  

#     # --- Save `result_df` to CSV in the output folder ---
#     output_file = output_dir / "winddirection_interpolated_results.csv"  # Define filename
#     result_df.to_csv(output_file, index=False)  # Save as CSV (no index)


#     return result_df.sort_values('time')
  
def compute_alpha_from_two_heights(df):
    """
    Compute wind shear exponent alpha based on ref_wind_speed at 10m and 100m.
    Assumes df contains rows for both heights for each (time, lat, lon).
    Returns: dataframe with alpha per location and time.
    """
    df_10 = df[df['height'] == 10].reset_index(drop=True)
    df_100 = df[df['height'] == 100].reset_index(drop=True)

    assert df_10.shape[0] == df_100.shape[0], "Mismatch in 10m and 100m rows"

    ws_10 = df_10['ref_wind_speed'].values
    ws_100 = df_100['ref_wind_speed'].values

    alpha = np.log(ws_100 / ws_10) / np.log(100 / 10)

    df_alpha = df_10[['time', 'latitude', 'longitude']].copy()
    df_alpha['alpha'] = alpha

    return df_alpha

def compute_wind_speed_at_height(data_wind_df, target_height, ref_height, df_alpha=None):
    """
    Compute wind speed at a target height using power law profile.

    Parameters:
    - data_wind_df: pd.DataFrame with columns ['latitude', 'longitude', 'time', 'height', 'ref_wind_speed']
    - target_height: float, the desired height z (e.g., 80)
    - ref_height: the reference height (either 10 or 100)
    - alpha: float, wind shear exponent (computed separately)
    - df_alpha: DataFrame containing alpha values with time, latitude, longitude, and alpha

    Returns:
    - result_df: pd.DataFrame with wind speeds at the target height
    """

    assert ref_height in [10, 100], "ref_height must be 10 or 100"

    # Filter data for the chosen reference height
    df_ref = data_wind_df[data_wind_df['height'] == ref_height].copy().reset_index(drop=True)

    # Merge the df_alpha with the df_ref based on time, latitude, and longitude
    df_ref = df_ref.merge(df_alpha[['time', 'latitude', 'longitude', 'alpha']], on=['time', 'latitude', 'longitude'], how='left')

    # Calculate wind speed at target height using power law formula
    ws_ref = df_ref['ref_wind_speed'].values
    alpha_values = df_ref['alpha'].values  # Now we have alpha values for each record

    # Apply the power law formula for each record using its specific alpha value
    ws_z = ws_ref * (target_height / ref_height) ** alpha_values

    # Add computed fields
    df_ref['ref_height'] = ref_height
    df_ref['z [m]'] = target_height
    df_ref['Windspeed at z [m/s]'] = ws_z

    # Keep only relevant columns for the result
    # result_df = df_ref[['latitude', 'longitude', 'time', 'ref_wind_speed', 'Windspeed at z [m/s]', 'ref_height', 'z [m]']]

    return df_ref
