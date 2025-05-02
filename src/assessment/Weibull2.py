import numpy as np
from scipy.stats import weibull_min
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator
import pandas as pd
import weibull

def process_weibull(data_wind_df, coord, height):
    """
    Args:
        data_wind_df (pd.DataFrame): Wind resource data.
        coord (tuple): Coordinates (latitude, longitude) for interpolation.
        height (int): Height (10m or 100m) for which Weibull distribution is processed.
    """
    # Interpolate wind speeds at the specific location
    interpolated_data = interpolate_speed(data_wind_df, coord)

    # Extract wind speed data for the specified height
    if height == 10:
        wind_speeds = interpolated_data['wind_speed_10m'].values
    elif height == 100:
        wind_speeds = interpolated_data['wind_speed_100m'].values
    else:
        raise ValueError("Height must be either 10 or 100 meters.")

    # Fit Weibull distribution using the weibull library
    wb = weibull.Analysis(wind_speeds, unit='m/s')
    wb.fit()  # Fit the Weibull distribution

    # Print Weibull parameters
    shape = wb.beta  # Shape parameter
    scale = wb.eta   # Scale parameter
    print(f"{height}m - Weibull Shape Parameter: {shape:.2f}")
    print(f"{height}m - Weibull Scale Parameter: {scale:.2f}")

    # Plot Weibull distribution
    wb.probplot()  # Generate a probability plot
    wb.pdf()       # Generate a PDF plot

    return shape, scale