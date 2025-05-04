import numpy as np
from scipy.stats import weibull_min
from scipy.integrate import quad
from assessment.interpolate_4_loc import interpolate_speed
from assessment.Weibull import process_weibull

def compute_aep(data_wind_df, coord, turbine_data, height=100, air_density=1.225, eta=1.0):
    """
    Args:
        data_wind_df (pd.DataFrame): Wind resource data.
        coord (tuple): Coordinates (latitude, longitude) for interpolation.
        turbine_data (pd.DataFrame): Turbine power curve data with columns ['wind_speed', 'power_output'].
        height (int): Height of wind speed data (default: 100m).
        air_density (float): Air density in kg/m³ (default: 1.225).
        eta (float): Availability of the wind turbine (default: 1.0).
    """
    # Step 1: Fit Weibull distribution to wind speed data
    shape, scale = process_weibull(data_wind_df, coord, height)

    # Step 2: Define the Weibull PDF
    def weibull_pdf(u):
        return (shape / scale) * (u / scale)**(shape - 1) * np.exp(-(u / scale)**shape)

    # Step 3: Define the power curve function
    def power_curve(u):
        # Interpolate the turbine power curve
        return np.interp(u, turbine_data['wind_speed'], turbine_data['power_output'], left=0, right=0)

    # Step 4: Integrate the product of the power curve and Weibull PDF
    u_in = turbine_data['wind_speed'].min()  # Cut-in wind speed
    u_out = turbine_data['wind_speed'].max()  # Cut-out wind speed

    # Integrate using scipy.integrate.quad
    integral, _ = quad(lambda u: power_curve(u) * weibull_pdf(u), u_in, u_out)

    # Step 5: Compute AEP
    hours_per_year = 8760  # Total hours in a year
    aep = eta * hours_per_year * integral / 1e6  # Convert to MWh

    return aep
