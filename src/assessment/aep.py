#____Import packages_____
import numpy as np
import pandas as pd
#from scipy.stats import weibull_min

def calc_aep(turb, wind, t_start, t_end, height):
    """
    Calculate Annual Energy Production (AEP) from wind and turbine data.
    
    Args:
        turb (pd.DataFrame): Turbine data including 'Wind Speed [m/s]' and 'Power [kW]'.
        wind (pd.DataFrame): Wind measurement data including 'time', 'ref_wind_speed', and 'height'.
        t_start (str): Start of the time period (e.g. '2020-01-01').
        t_end (str): End of the time period (e.g. '2020-12-31').
        height (int or float): The hub height at which to filter wind data.

    Returns:
        float: Estimated Annual Energy Production (AEP) in kWh.
    """
    # Get wind speed from mast
    ws_time = wind[(wind['time'] >= t_start) & 
                   (wind['time'] <= t_end)] # filter for time range
    ws_height_time = ws_time[ws_time['height'] == height] # filter for height
    
    # Construct arrays
    result_ws = ws_height_time['ref_wind_speed'].to_numpy()
    #result_time = ws_height_time['time'].to_numpy()

    # Fit Weibull distribution to the wind speed data
    #shape, loc, scale = weibull_min.fit(wind_speeds, floc=0)


    # Get power from turb
    turb_wind = turb['Wind Speed [m/s]'].to_numpy()
    turb_power = turb[turb['Power [kW]'] > 0] #filter the power = 0 kW

    # Get the cut in and cut out speed
    u_in = turb_wind['Wind Speed [m/s]'].min
    u_out = turb_wind['Wind Speed [m/s]'].max

    # Filter turbine curve to include only speeds within [u_in, u_out]
    mask = (turb_wind >= u_in) & (turb_wind <= u_out)
    wind_speed_range = turb_wind[mask]
    power_range = turb_power[mask]

    # Evaluate Weibull PDF over wind speed range
    #pdf_range = weibull_min.pdf(wind_speed_range, c=shape, scale=scale)
    
    # Numerical integration
    η = 1.0  # Turbine availability (efficiency factor)
    hours_per_year = 8760
    integrand = power_range #* pdf_range (weibull input)
    aep = η * hours_per_year * np.trapz(integrand, wind_speed_range)

    return aep
