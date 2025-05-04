<<<<<<< Updated upstream
# ----Import packages------------
=======
# ----Import packages
>>>>>>> Stashed changes
import numpy as np
from pathlib import Path            # For identifying path of file
from scipy.interpolate import LinearNDInterpolator  # For interpolation
from scipy.interpolate import RegularGridInterpolator  # For interpolation
import matplotlib.pyplot as plt  # For plotting


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

    return ts_interp


def plot_interpolation(int_ws, int_wd, target_coord):
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Plot wind speed
    ax1.plot(int_ws, color='tab:blue')
    ax1.set_ylabel('Wind Speed [m/s]', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.grid(True)
    ax1.set_title(f'Wind Speed and Direction at {target_coord}')

    # Plot wind direction
    ax2.plot(int_wd, color='tab:orange')
    ax2.set_ylabel('Wind Direction [°]', color='tab:orange')
    ax2.tick_params(axis='y', labelcolor='tab:orange')
    ax2.grid(True)
    ax2.set_xlabel('Time index')

    # Adjust layout
    plt.tight_layout()

    # Save plot
    current_dir = Path(__file__).parent.resolve()
    output_dir = current_dir.parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "wind_speed_and_direction_plot.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    return fig



def interpolate_max_ws_100(wr_data_df, height):
    '''Calculate the location inside the box, with maximum windspeed using
    interpolation

    Args:
        wr_data_df (pd.DataFrame): A DataFrame containing wind resource data
<<<<<<< Updated upstream
        with columns including 'latitude', 'longitude', 'height', and
        'ref_wind_speed'.
        height (int or float): The hub height at which to filter wind speed
        data for interpolation (e.g., 100).

    Returns:
        tuple: A tuple (latitude, longitude, wind_speed) corresponding to the
        location within the defined grid that has the maximum interpolated
        wind speed.'''
=======
        with columns including 'latitude', 'longitude', 'height',
        and 'ref_wind_speed'.
        height (int or float): The hub height at which to filter
        wind speed data for interpolation (e.g., 100).

    Returns:
        tuple: A tuple (latitude, longitude, wind_speed) corresponding
        to the location within the defined grid that has the maximum
        interpolated wind speed.'''
>>>>>>> Stashed changes

    lat_range = np.arange(55.5, 55.75, 0.01)
    lon_range = np.arange(7.75, 8, 0.01)
    # Create a mesh grid
    lat_grid, lon_grid = np.meshgrid(lat_range, lon_range)

    # Flatten and combine to (lat, lon) tuples
    grid_points = list(zip(lat_grid.ravel(), lon_grid.ravel()))

    # Filter rows where height is 100
    filtered_df = wr_data_df[wr_data_df['height'] == height]

    # Select first 4 rows where ref_wind_speed meets the condition
    # Ensure you're taking the first 4 unique lat, lon pairs
    first_4_values = filtered_df[
        ['latitude', 'longitude', 'ref_wind_speed']
        ].drop_duplicates(subset=['latitude', 'longitude'])

<<<<<<< Updated upstream
    points = first_4_values[
        ['latitude', 'longitude']
        ].to_numpy()  # Lat, Lon pairs
=======
    points = first_4_values[['latitude', 'longitude']].to_numpy()
>>>>>>> Stashed changes
    ref_wind_speed = first_4_values['ref_wind_speed'].to_numpy()

    # Build interpolator
    interpolator = LinearNDInterpolator(points, ref_wind_speed)

    # Create a new list with interpolated values for each grid point
    interpolated_values = []
    for i in grid_points:
<<<<<<< Updated upstream
        interpolated_value = interpolator(np.array(i))  # Interpolated ws
        interpolated_values.append((i[0], i[1], interpolated_value))

    # Find the maximum ref_wind_speed in the interpolated values
        # x[2] is the ref_wind_speed value
=======
        interpolated_value = interpolator(np.array(i))
        interpolated_values.append((i[0], i[1], interpolated_value))

    # Find the maximum ref_wind_speed in the interpolated values
>>>>>>> Stashed changes
    max_ref_wind_speed = max(interpolated_values, key=lambda x: x[2])
    # Extract the latitude, longitude, and the max ref_wind_speed
    max_lat, max_lon, max_ws = max_ref_wind_speed

    return max_lat, max_lon, max_ws


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


def compute_wind_speed_at_height(data_wind_df, target_height, ref_height,
                                 df_alpha=None):
    """
    Compute wind speed at a target height using power law profile.

    Parameters:
    - data_wind_df: pd.DataFrame with columns ['latitude', 'longitude', 'time',
<<<<<<< Updated upstream
    'height', 'ref_wind_speed']
=======
    height', 'ref_wind_speed']
>>>>>>> Stashed changes
    - target_height: float, the desired height z (e.g., 80)
    - ref_height: the reference height (either 10 or 100)
    - alpha: float, wind shear exponent (computed separately)
    - df_alpha: DataFrame containing alpha values with time, latitude,
    longitude, and alpha

    Returns:
    - result_df: pd.DataFrame with wind speeds at the target height
    """

    assert ref_height in [10, 100], "ref_height must be 10 or 100"

    # Filter data for the chosen reference height
<<<<<<< Updated upstream
    df_ref = data_wind_df[
        data_wind_df['height'] == ref_height
        ].copy().reset_index(drop=True)
=======
    df_ref = data_wind_df[data_wind_df['height'] ==
                          ref_height].copy().reset_index(drop=True)
>>>>>>> Stashed changes

    # Merge the df_alpha with the df_ref based on time, latitude, and longitude
    df_ref = df_ref.merge(df_alpha[['time', 'latitude', 'longitude', 'alpha']],
                          on=['time', 'latitude', 'longitude'], how='left')

    # Calculate wind speed at target height using power law formula
    ws_ref = df_ref['ref_wind_speed'].values
<<<<<<< Updated upstream
    alpha_values = df_ref['alpha'].values  # Alpha values for each record
=======
    alpha_values = df_ref['alpha'].values  # alpha values for each record
>>>>>>> Stashed changes

    # Apply the power law formula for each record using its alpha value
    ws_z = ws_ref * (target_height / ref_height) ** alpha_values

    # Add computed fields
    df_ref['ref_height'] = ref_height
    df_ref['z [m]'] = target_height
    df_ref['Windspeed at z [m/s]'] = ws_z

    # Keep only relevant columns for the result
    result_df = df_ref[['latitude', 'longitude', 'time', 'ref_wind_speed',
                        'alpha', 'Windspeed at z [m/s]', 'ref_height',
                        'z [m]']]

<<<<<<< Updated upstream
    # save result
=======
>>>>>>> Stashed changes
    # --- Define paths ---
    current_dir = Path(__file__).parent.resolve()
    output_dir = current_dir.parent.parent / "outputs"

    # --- Create the output folder if it doesn't exist ---
    output_dir.mkdir(exist_ok=True)

    # --- Save `result_df` to CSV in the output folder ---
<<<<<<< Updated upstream
    output_file = output_dir / "wind_speed_at_target_height.csv"  # Filename
=======
    output_file = output_dir / "wind_speed_at_target_height.csv"
>>>>>>> Stashed changes
    result_df.to_csv(output_file, index=False)  # Save as CSV (no index)

    return result_df
