# import numpy as np
# from scipy.stats import weibull_min
# import matplotlib.pyplot as plt
# from scipy.interpolate import RegularGridInterpolator
# import pandas as pd

# def process_weibull(data_wind_df, coord, height):
#     # Interpolate wind speeds at the specific location
#     val = interpolate_4_loc(data_wind_df, coord)

#     # Extract wind speed data for the specified height
#     if height == 10:
#         wind_speeds = val['wind_speed_10m'].values
#     elif height == 100:
#         wind_speeds = val['wind_speed_100m'].values
#     else:
#         raise ValueError("Height must be either 10 or 100 meters.")

#     # Fit Weibull distribution
#     shape, loc, scale = weibull_min.fit(wind_speeds, floc=0)  # Fix location to 0
#     print(f"{height}m - Weibull Shape Parameter: {shape:.2f}")
#     print(f"{height}m - Weibull Scale Parameter: {scale:.2f}")

#     # Plot Weibull distribution
#     plt.hist(wind_speeds, bins=50, density=True, alpha=0.6, color='g', label="Wind Speed Data")
#     x = np.linspace(0, max(wind_speeds), 100)
#     pdf = weibull_min.pdf(x, shape, scale=scale)
#     plt.plot(x, pdf, 'r-', label=f"Weibull Fit (shape={shape:.2f}, scale={scale:.2f})")
#     plt.xlabel("Wind Speed (m/s)")
#     plt.ylabel("Probability Density")
#     plt.title(f"Weibull Distribution Fit at {height}m")
#     plt.legend()
#     plt.grid()
#     plt.show()

#     return shape, scale
import numpy as np
from scipy.stats import weibull_min
import matplotlib.pyplot as plt
import pandas as pd

def process_weibull(data_wind_df, coord, height):
    """
    Interpolates wind speed at a given location and height,
    fits a Weibull distribution, and returns parameters.

    Args:
        wr_data_df (pd.DataFrame): Wind data with 'latitude', 'longitude', 'ref_wind_speed', 'height', 'time'.
        coord (tuple): Target location (lat, lon).
        height (int): Height (10 or 100 meters).

    Returns:
        dict: Fitted Weibull parameters {shape, loc, scale}.
    """
    # Interpolate wind speeds using your main function
    interpolated_df = interpolate_speed(data_wind_df, coord)

    # Select the correct height column
    if height == 10:
        wind_speeds = interpolated_df['wind_speed_10m'].values
    elif height == 100:
        wind_speeds = interpolated_df['wind_speed_100m'].values
    else:
        raise ValueError("Height must be either 10 or 100 meters.")

    # Remove NaNs just in case
    wind_speeds = wind_speeds[~np.isnan(wind_speeds)]

    # Fit the Weibull distribution (location fixed to 0)
    shape, loc, scale = weibull_min.fit(wind_speeds, floc=0)

    # Plot histogram and fitted PDF
    plt.figure(figsize=(8, 5))
    count, bins, _ = plt.hist(wind_speeds, bins=30, density=True, alpha=0.6, color='skyblue', label='Wind Speed Data')
    x = np.linspace(min(wind_speeds), max(wind_speeds), 100)
    plt.plot(x, weibull_min.pdf(x, shape, loc, scale), 'r-', lw=2, label='Weibull Fit')
    plt.title(f"Weibull Fit at {height}m for Location {coord}")
    plt.xlabel("Wind Speed (m/s)")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return {"shape": shape, "loc": loc, "scale": scale}

