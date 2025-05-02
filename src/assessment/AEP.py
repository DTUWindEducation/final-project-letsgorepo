import numpy as np
from scipy.stats import weibull_min
from assessment.interpolate_4_loc import interpolate_speed
from assessment.Weibull3 import process_weibull
import pandas as pd

def compute_aep(data_wind_df, coord, turbine_data, height=100, air_density=1.225):
    # Step 1: Interpolate wind speeds at the specified location
    interpolated_df = interpolate_speed(data_wind_df, coord)

    # Extract wind speed data for the specified height
    if height == 10:
        wind_speeds = interpolated_df['wind_speed_10m']
    elif height == 100:
        wind_speeds = interpolated_df['wind_speed_100m']
    else:
        raise ValueError("Height must be either 10 or 100 meters.")

    # Remove NaNs
    wind_speeds = wind_speeds[~np.isnan(wind_speeds)]

    # Step 2: Fit Weibull distribution to wind speed data
    shape, scale = process_weibull(data_wind_df, coord, height)

    # Step 3: Compute AEP using the Weibull PDF and turbine power curve
    wind_speed_bins = turbine_data['wind_speed'].values
    power_output = turbine_data['power_output'].values

    # Weibull PDF for each wind speed bin
    weibull_pdf = (shape / scale) * (wind_speed_bins / scale)**(shape - 1) * np.exp(-(wind_speed_bins / scale)**shape)

    # Compute AEP (sum of power * probability * hours in a year)
    hours_per_year = 8760  # Total hours in a year
    aep = np.sum(power_output * weibull_pdf * hours_per_year) / 1e6  # Convert to MWh

    return aep