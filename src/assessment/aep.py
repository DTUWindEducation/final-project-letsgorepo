# ____Import packages_____
import numpy as np
<<<<<<< Updated upstream
import matplotlib.pyplot as plt     # For plotting
=======
import matplotlib.pyplot as plt  # For plotting
>>>>>>> Stashed changes
from pathlib import Path            # For identifying path of file


def power_range(wind, height, turb, t_start, t_end):
    ws_time = wind[(wind['time'] >= t_start) &
                   (wind['time'] <= t_end)]  # filter for time range
    ws_height_time = ws_time[ws_time['height'] == height]  # filter for height

    min_ws = ws_height_time['ref_wind_speed'].min()
    max_ws = ws_height_time['ref_wind_speed'].max()

    # Get wind speed and power from filtered turb
    turb_wind = turb['Wind Speed [m/s]'].to_numpy()

    # Get the cut in and cut out speed
    u_i = turb_wind.min()
    u_o = turb_wind.max()

<<<<<<< Updated upstream
    # Filter turbine where power > 0 and wind speed is between u_in and u_out
    mask = (turb['Power [kW]'] > 0) & (turb['Wind Speed [m/s]'] >= u_i) & (
        turb['Wind Speed [m/s]'] <= u_o)
=======
    # Filter turbine data where power > 0 and ws is between u_in and u_out
    mask = (turb['Power [kW]'] > 0) & (turb['Wind Speed [m/s]'] >= u_i) & (turb['Wind Speed [m/s]'] <= u_o)
>>>>>>> Stashed changes
    filtered = turb[mask]

    power_length = (len(filtered))

    return min_ws, max_ws, power_length, filtered


def calc_aep(filtered, pdf):
    """
    Calculate Annual Energy Production (AEP) from wind and turbine data.

    Args:
<<<<<<< Updated upstream
        turb (pd.DataFrame): Turbine data including 'Wind Speed [m/s]' and
        'Power [kW]'.
=======
        turb (pd.DataFrame): Turbine data including 'Wind Speed [m/s]'
        and 'Power [kW]'.
>>>>>>> Stashed changes
        wind (pd.DataFrame): Wind measurement data including 'time',
        'ref_wind_speed', and 'height'.
        t_start (str): Start of the time period (e.g. '2020-01-01').
        t_end (str): End of the time period (e.g. '2020-12-31').
        height (int or float): The hub height at which to filter wind data.

    Returns:
        float: Estimated Annual Energy Production (AEP) in kWh.
    """

    # Get wind speed and power from filtered turb
    turb_wind_filtered = filtered['Wind Speed [m/s]'].to_numpy()
<<<<<<< Updated upstream
    turb_power_filtered = filtered['Power [kW]'].to_numpy()  # filter the P=0kW
=======
    turb_power_filtered = filtered['Power [kW]'].to_numpy()  # filter P = 0 kW
>>>>>>> Stashed changes

    # Get the cut in and cut out speed
    u_in = turb_wind_filtered.min()
    u_out = turb_wind_filtered.max()

    # Filter turbine curve to include only speeds within [u_in, u_out]
    mask = (turb_wind_filtered >= u_in) & (turb_wind_filtered <= u_out)
    wind_speed_range = turb_wind_filtered[mask]
    power_range = turb_power_filtered[mask]

    # Numerical integration
    η = 1.0  # Turbine availability (efficiency factor)
    hours_per_year = 8760
    integrand = power_range  * pdf
    aep = η * hours_per_year * np.trapz(integrand, wind_speed_range)
    aep_MWh = aep / 1000000

    return aep_MWh


def calc_aep_per_speed(filtered, pdf, coord):
    """
    Calculate Annual Energy Production (AEP) **per wind speed** from turbine
    and wind distribution data.

    Args:
        filtered (pd.DataFrame): Turbine power curve data with columns:
            - 'Wind Speed [m/s]' (wind speeds)
            - 'Power [kW]' (power output at each speed)
        pdf (np.array): Probability density function (PDF) of wind speeds
        (from Weibull fit).
                       Must align with the wind speeds in `filtered`.

    Returns:
        pd.DataFrame: AEP contribution per wind speed bin, with columns:
            - 'Wind Speed [m/s]'
            - 'Power [kW]'
            - 'Probability' (PDF value)
            - 'AEP [kWh/year]' (energy contribution per speed)
    """
    # Extract turbine power curve data
    turb_wind_speeds = filtered['Wind Speed [m/s]'].to_numpy()
    turb_power = filtered['Power [kW]'].to_numpy()

    # Filter out speeds where power = 0 (optional)
    mask = turb_power > 0
    wind_speeds = turb_wind_speeds[mask]
    power = turb_power[mask]

    # Ensure PDF aligns with wind speeds
    if len(pdf) != len(wind_speeds):
        raise ValueError("PDF length must match filtered wind speed bins!")
<<<<<<< Updated upstream
=======

    # # Calculate AEP per speed bin
    # η = 1.0  # Turbine availability factor
    # hours_per_year = 8760
    # aep_per_speed = power * pdf * hours_per_year * η

    # Create result DataFrame
    # result_df = pd.DataFrame({
    #     'Wind Speed [m/s]': wind_speeds,
    #     'Power [kW]': power,
    #     'Probability': pdf,
    #     'AEP [kWh/year]': aep_per_speed
    # })
>>>>>>> Stashed changes

    # Plot power vs wind speed
    plt.figure(figsize=(10, 5))
    plt.plot(wind_speeds, power)
    plt.xlabel('Wind Speed [m/s]')
    plt.ylabel('Power [kW]')
    plt.title(f"Power curve for location{coord}")
    plt.grid(True)

    # Define path
    current_dir = Path(__file__).parent.resolve()
    output_dir = current_dir.parent.parent / "outputs"
    # --- Create the output folder if it doesn't exist ---
    output_dir.mkdir(exist_ok=True)
    # Save plot
    output_path = output_dir / "Power curve.png"
    plt.gcf().savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
