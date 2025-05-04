# ----Import packages
import numpy as np
import pandas as pd
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

    dir_10_interp = []
    dir_100_interp = []

    for time in T:
        subset = wr_data_df[wr_data_df['time'] == time]

        # Separate by height
        df_10 = subset[subset['height'] == 10]
        df_100 = subset[subset['height'] == 100]

        # Create 2D grids (longitude x latitude) for wind direction
        grid_10 = df_10.pivot(index='longitude', columns='latitude', values='ref_wind_speed').values
        grid_100 = df_100.pivot(index='longitude', columns='latitude', values='ref_wind_speed').values

        # Create interpolators
        interp_10 = RegularGridInterpolator((X, Y), grid_10)
        interp_100 = RegularGridInterpolator((X, Y), grid_100)

        # Interpolate at the given target coordinate
        dir_10_interp.append(interp_10(target_coord))
        dir_100_interp.append(interp_100(target_coord))

    # Build result DataFrame
    result_df = pd.DataFrame({
        'time': T,
        'wind_speed_10m': np.array(dir_10_interp).flatten(),
        'wind_speed_100m': np.array(dir_100_interp).flatten()
    })

    # save result
    # --- Define paths ---
    current_dir = Path(__file__).parent.resolve()  # Folder where the script is located
    output_dir = current_dir.parent.parent / "outputs"  # Go up 2 levels, then into "output"
    # --- Create the output folder if it doesn't exist ---
    output_dir.mkdir(exist_ok=True)  
 
    # --- Save `result_df` to CSV in the output folder ---
    output_file = output_dir / "windspeed_interpolated_results.csv"  # Define filename
    result_df.to_csv(output_file, index=False)  # Save as CSV (no index)

    return result_df


def interpolate_direction(wr_data_df, target_coord):
    # Ensure the data is sorted
    wr_data_df = wr_data_df.sort_values(['longitude', 'latitude', 'time'])

    # Get unique sorted grid axes
    X = np.sort(wr_data_df['longitude'].unique())  # lon
    Y = np.sort(wr_data_df['latitude'].unique())   # lat
    T = np.sort(wr_data_df['time'].unique())       # time
    
    dir_10_interp = []
    dir_100_interp = []

    for time in T:
        subset = wr_data_df[wr_data_df['time'] == time]

        # Separate by height
        df_10 = subset[subset['height'] == 10]
        df_100 = subset[subset['height'] == 100]

        # Create 2D grids (longitude x latitude) for wind direction
        grid_10 = df_10.pivot(index='longitude', columns='latitude', values='ref_wind_direction').values
        grid_100 = df_100.pivot(index='longitude', columns='latitude', values='ref_wind_direction').values

        # Create interpolators
        interp_10 = RegularGridInterpolator((X, Y), grid_10)
        interp_100 = RegularGridInterpolator((X, Y), grid_100)

        # Interpolate at the given target coordinate
        dir_10_interp.append(interp_10(target_coord))
        dir_100_interp.append(interp_100(target_coord))

    # Build result DataFrame
    result_df = pd.DataFrame({
        'time': T,
        'wind_direction_10m': np.array(dir_10_interp).flatten(),
        'wind_direction_100m': np.array(dir_100_interp).flatten()
    })

    # save result
    # --- Define paths ---
    current_dir = Path(__file__).parent.resolve()  # Folder where the script is located
    output_dir = current_dir.parent.parent / "outputs"  # Go up 2 levels, then into "output"
    # --- Create the output folder if it doesn't exist ---
    output_dir.mkdir(exist_ok=True)  
 
    # --- Save `result_df` to CSV in the output folder ---
    output_file = output_dir / "winddirection_interpolated_results.csv"  # Define filename
    result_df.to_csv(output_file, index=False)  # Save as CSV (no index)

    return result_df


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
# LOOK we turned the code below to the code above, impressive right? :D


def interpolate_max_ws_100(wr_data_df, height):
    '''Calculate the location inside the box, with maximum windspeed using
    interpolation

    Args:
        wr_data_df (pd.DataFrame): A DataFrame containing wind resource data
        with columns including 'latitude', 'longitude', 'height',
        and 'ref_wind_speed'.
        height (int or float): The hub height at which to filter
        wind speed data for interpolation (e.g., 100).

    Returns:
        tuple: A tuple (latitude, longitude, wind_speed) corresponding
        to the location within the defined grid that has the maximum
        interpolated wind speed.'''

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

    points = first_4_values[['latitude', 'longitude']].to_numpy()
    ref_wind_speed = first_4_values['ref_wind_speed'].to_numpy()

    # Build interpolator
    interpolator = LinearNDInterpolator(points, ref_wind_speed)

    # Create a new list with interpolated values for each grid point
    interpolated_values = []
    for i in grid_points:
        interpolated_value = interpolator(np.array(i))
        interpolated_values.append((i[0], i[1], interpolated_value))

    # Find the maximum ref_wind_speed in the interpolated values
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
    height', 'ref_wind_speed']
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
    df_ref = data_wind_df[data_wind_df['height'] ==
                          ref_height].copy().reset_index(drop=True)

    # Merge the df_alpha with the df_ref based on time, latitude, and longitude
    df_ref = df_ref.merge(df_alpha[['time', 'latitude', 'longitude', 'alpha']],
                          on=['time', 'latitude', 'longitude'], how='left')

    # Calculate wind speed at target height using power law formula
    ws_ref = df_ref['ref_wind_speed'].values
    alpha_values = df_ref['alpha'].values  # alpha values for each record

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

    # --- Define paths ---
    current_dir = Path(__file__).parent.resolve()
    output_dir = current_dir.parent.parent / "outputs"

    # --- Create the output folder if it doesn't exist ---
    output_dir.mkdir(exist_ok=True)

    # --- Save `result_df` to CSV in the output folder ---
    output_file = output_dir / "wind_speed_at_target_height.csv"
    result_df.to_csv(output_file, index=False)  # Save as CSV (no index)

    return result_df
