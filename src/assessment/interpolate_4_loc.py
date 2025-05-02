#----Import packages
from scipy.interpolate import griddata
import numpy as np
import pandas as pd

def interpolate_4_loc(wr_data_df, target_coord):
    '''
    Interpolate wind speed and direction at 10m and 100m heights for a given location
    from 4 surrounding stations over time.
    
    target_coord: [lat, lon]
    '''

    # Sort by time to ensure correct grouping
    wr_data_df = wr_data_df.sort_values('time').reset_index(drop=True)
    
    times = wr_data_df['time'].unique()
    interp_wspd_10m = []
    interp_wspd_100m = []
    interp_wdir_10m = []
    interp_wdir_100m = []

    for t in times:
        df_t = wr_data_df[wr_data_df['time'] == t]
        
        points = df_t[['latitude', 'longitude']].values
        wspd_10m = df_t['ref_wind_speed'].values

        # Convert wind direction to u, v
        dir_rad_10m = np.radians(df_t['ref_wind_direction'].values)
        u10 = -wspd_10m * np.sin(dir_rad_10m)
        v10 = -wspd_10m * np.cos(dir_rad_10m)

        # Interpolate speeds
        interp_wspd_10m.append(griddata(points, wspd_10m, target_coord, method='linear'))

        # Interpolate u and v components, then convert back to direction
        iu10 = griddata(points, u10, target_coord, method='linear')
        iv10 = griddata(points, v10, target_coord, method='linear')
        iwdir_10m = (np.degrees(np.arctan2(-iu10, -iv10)) + 360) % 360
        interp_wdir_10m.append(iwdir_10m)

        df = {'time': times,
        'wspd_10m': np.array(interp_wspd_10m),
        'wdir_10m': np.array(interp_wdir_10m),}
    return df

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
