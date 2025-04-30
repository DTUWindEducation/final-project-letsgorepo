import numpy as np
import pandas as pd
from scipy.interpolate import griddata

def interpolate_4_loc(locations_sorted: pd.DataFrame, target_coord: tuple):
    """
    Interpolates wind speed time series at a given target coordinate using data
    from 4 surrounding locations at 10 m and 100 m heights.
    
    Parameters:
    - locations_sorted: pd.DataFrame with columns ['Latitude', 'Longitude', 'Height [m]', 'Windspeed [m/s]']
                        and 8 time series (4 locations × 2 heights)
    - target_coord: tuple of (latitude, longitude) for the point to interpolate at

    Returns:
    - interp_10m: np.ndarray of interpolated wind speed at 10 m
    - interp_100m: np.ndarray of interpolated wind speed at 100 m
    """
    # Identify unique coordinates and ensure exactly 4 locations
    coords = locations_sorted[['Latitude', 'Longitude']].drop_duplicates().values
    if coords.shape[0] != 4:
        raise ValueError("Expected data from exactly 4 locations.")

    # Create wind speed dict: {(lat, lon, height): array}
    grouped = locations_sorted.groupby(['Latitude', 'Longitude', 'Height [m]'])
    ws_dict = {
        (lat, lon, height): group['Windspeed [m/s]'].values
        for (lat, lon, height), group in grouped
    }

    # Extract wind speed series for 10 m and 100 m at 4 locations
    loc_coords = [tuple(c) for c in coords]
    ws_10m = [ws_dict[(lat, lon, 10)] for lat, lon in loc_coords]
    ws_100m = [ws_dict[(lat, lon, 100)] for lat, lon in loc_coords]

    # Stack each height group into shape (n_locations, n_timesteps)
    ws_10m_stack = np.vstack(ws_10m)
    ws_100m_stack = np.vstack(ws_100m)

    # Perform interpolation for each timestep
    points = np.array(loc_coords)
    n_timesteps = ws_10m_stack.shape[1]
    interp_10m = np.zeros(n_timesteps)
    interp_100m = np.zeros(n_timesteps)

    for i in range(n_timesteps):
        values_10 = ws_10m_stack[:, i]
        values_100 = ws_100m_stack[:, i]

        interp_10m[i] = griddata(points, values_10, target_coord, method='linear')
        interp_100m[i] = griddata(points, values_100, target_coord, method='linear')

    return interp_10m, interp_100m


def compute_wind_speed_at_height(df_sorted, target_height, alpha=0.143):
    """
    Compute wind speed at a target height using power law profile.

    Parameters:
    - df_sorted: pd.DataFrame with columns ['Latitude', 'Longitude', 'Height [m]', 'Windspeed [m/s]']
    - target_height: float, the desired height z (e.g., 80)
    - alpha: wind shear exponent (default is 0.143)

    Returns:
    - interpolated_df: pd.DataFrame with wind speeds at the target height for each location and time
    """

    # Split into two dataframes by height
    df_10 = df_sorted[df_sorted['Height [m]'] == 10].reset_index(drop=True)
    df_100 = df_sorted[df_sorted['Height [m]'] == 100].reset_index(drop=True)

    # Sanity check
    assert df_10.shape[0] == df_100.shape[0], "Mismatch in row count between 10m and 100m data"

    # Calculate wind speed at target height using power law for each time step
    ws_10 = df_10['Windspeed [m/s]'].values
    ws_100 = df_100['Windspeed [m/s]'].values

    # Interpolate wind speed at target height using the power law
    # First estimate alpha dynamically if you want (optional):
    # alpha = np.log(ws_100 / ws_10) / np.log(100 / 10)

    # Use power law formula
    ws_z = ws_10 * (target_height / 10) ** alpha

    # Build the result dataframe
    result_df = df_10.copy()
    result_df['Height [m]'] = target_height
    result_df['Windspeed [m/s]'] = ws_z

    return result_df



# #----Import packages
# from scipy.interpolate import griddata
# import numpy as np

# def interpolate_4_loc(loc1,loc2,loc3,loc4,coord):
#     '''Takes windspeeds and winddirection from the four location (including the coordinates),
#     and then interpolates in regards to a specific location'''
#     # Samlpe data as 2D
#     #lat = [loc1[0],loc2[0],loc3[0],loc4[0]]  #first column in input is latitude
#     #long = [loc1[1],loc2[1],loc3[1],loc4[1]]  #second column in input is longitude
#     points = np.array([
#         [loc1[0],loc1[1]],
#         [loc2[0],loc2[1]],
#         [loc3[0],loc3[1]],
#         [loc4[0],loc4[1]]])
    
#     ws = np.array([9.794061,9.802940,9.771493,10.123184])
#     result = griddata(points, ws, coord, method="linear")
#     #interp_func = RectBivariateSpline(points, ws, coord, extrapolate=True)
#     # New points to interpolate for
#     return float(result[0])
#     # Data to interpolate
#     #__________TODO________make the interpolation work for our results....
