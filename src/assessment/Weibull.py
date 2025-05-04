
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
#from assessment.interpolate_4_loc import interpolate_speed

# Weibull model function
def weibull_model(x, c, k): #x-Wind speed values.c-Scale parameter.k-Shape parameter.
    return (k / c) * (x / c)**(k - 1) * np.exp(-(x / c)**k)

def process_weibull(data_wind_df, coord, height):
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
    params_opt, params_cov = curve_fit(weibull_model, bin_centers, hist, p0=[5, 2])  # Initial guess for [c, k]
    c_opt, k_opt = params_opt  # Scale and shape parameters

    # Print Weibull parameters
    print(f"{height}m - Weibull Scale Parameter (c): {c_opt:.2f}")
    print(f"{height}m - Weibull Shape Parameter (k): {k_opt:.2f}")

    # Plot histogram and fitted Weibull distribution
    plt.figure(figsize=(8, 5))
    plt.hist(wind_speeds, bins=30, density=True, alpha=0.6, color='skyblue', label='Wind Speed Data')
    x = np.linspace(min(wind_speeds), max(wind_speeds), 100)
    plt.plot(x, weibull_model(x, c_opt, k_opt), 'r-', lw=2, label=f'Weibull Fit (c={c_opt:.2f}, k={k_opt:.2f})')
    plt.title(f"Weibull Fit at {height}m for Location {coord}")
    plt.xlabel("Wind Speed (m/s)")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    pdf_range = weibull_model(x, c_opt, k_opt)

    return c_opt, k_opt, pdf_range

# Define path
    current_dir = Path(_file_).parent.resolve()  # Folder where the script is located
    output_dir = current_dir.parent.parent / "outputs"  # Go up 2 levels, then into "output"
    # --- Create the output folder if it doesn't exist ---
    output_dir.mkdir(exist_ok=True)

# Save 10m plot
    output_path = output_dir / "weibull_10m.png"
    plt.gcf().savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

# Save 100m plot
    output_path = output_dir / "weibull_10m.png"
    plt.gcf().savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
