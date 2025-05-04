import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt         # For plot
from pathlib import Path                # For identifying path


def weibull_model(x, c, k):  # x-Wind speed.c-Scale.k-Shape.
    """
    Weibull probability density function (PDF).

    Parameters
    ----------
    x : array-like or float
        Wind speed values (m/s).
    c : float
        Scale parameter of the Weibull distribution.
    k : float
        Shape parameter of the Weibull distribution.

    Returns
    -------
    array-like or float
        Probability density values corresponding to input wind speeds.
    """
    return (k / c) * (x / c)**(k - 1) * np.exp(-(x / c)**k)


def process_weibull(data_wind_df, coord, height, power_range, wind_speed_min,
                    wind_speed_max):

    """
    Fit a Weibull distribution to wind speed data and return the PDF.

    Parameters
    ----------
    data_wind_df : pandas.DataFrame
        DataFrame containing wind speed data.
    coord : tuple
        Coordinates of the location (e.g., (lat, lon)) for label.
    height : int
        Height at which to analyze wind speed (must be 10 or 100 meters).
    power_range : int
        Number of points in the generated wind speed range for Weibull PDF.
    wind_speed_min : float
        Minimum wind speed (m/s) for evaluating the Weibull PDF.
    wind_speed_max : float
        Maximum wind speed (m/s) for evaluating the Weibull PDF.

    Returns
    -------
    c_opt : float
        Optimized scale parameter of the fitted Weibull distribution.
    k_opt : float
        Optimized shape parameter of the fitted Weibull distribution.
    pdf_range : ndarray
        Array of Weibull PDF values evaluated over the wind speed range.

    Notes
    -----
    Saves a histogram of wind speed data with the fitted Weibull distribution
    as "Weibull distribution.png" in the `outputs` directory.
    """
    # Interpolate wind speeds using interpolate_4_loc results
    interpolated_df = data_wind_df

    # Select the correct height column
    if height == 10:
        wind_speeds = interpolated_df['wind_speed_10m']
    elif height == 100:
        wind_speeds = interpolated_df['wind_speed_100m']
    else:
        raise ValueError("Height must be either 10 or 100 meters.")

    # Remove NaNs just in case
    wind_speeds = wind_speeds[~np.isnan(wind_speeds)]

    # Prepare histogram data for fitting
    hist, bin_edges = np.histogram(wind_speeds, bins=30, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Fit Weibull distribution using curve_fit
    params_opt, params_cov = curve_fit(weibull_model, bin_centers,
                                       hist, p0=[5, 2])  # Initial guess [c, k]
    c_opt, k_opt = params_opt  # Scale and shape parameters

    # Plot histogram and fitted Weibull distribution
    plt.figure(figsize=(8, 5))
    plt.hist(wind_speeds, bins=30, density=True, alpha=0.6, color='skyblue',
             label='Wind Speed Data')
    x = np.linspace(min(wind_speeds), max(wind_speeds), 100)
    plt.plot(x, weibull_model(x, c_opt, k_opt), 'r-', lw=2,
             label=f'Weibull Fit (c={c_opt:.2f}, k={k_opt:.2f})')
    plt.title(f"Weibull Fit at {height}m for Location {coord}")
    plt.xlabel("Wind Speed (m/s)")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # Define path
    current_dir = Path(__file__).parent.resolve()
    output_dir = current_dir.parent.parent / "outputs"
    # --- Create the output folder if it doesn't exist ---
    output_dir.mkdir(exist_ok=True)
    # Save plot
    output_path = output_dir / "Weibull distribution.png"
    plt.gcf().savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    length = np.linspace(wind_speed_min, wind_speed_max, power_range)
    pdf_range = weibull_model(length, c_opt, k_opt)

    return c_opt, k_opt, pdf_range
