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