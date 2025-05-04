import pandas as pd
from pathlib import Path

from windrose import WindroseAxes
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from matplotlib import pyplot as plt

def plot_wind_rose(ws_csv, wd_csv):
    # Define path
    current_dir = Path(__file__).parent.resolve()  # Folder where the script is located
    output_dir = current_dir.parent.parent / "outputs"  # Go up 2 levels, then into "output"
    # --- Create the output folder if it doesn't exist ---
    output_dir.mkdir(exist_ok=True)  
    
    # Define the input
    ws_10 = ws_csv['wind_speed_10m'].to_numpy()
    ws_100 = ws_csv['wind_speed_100m'].to_numpy()
    wd_10 = wd_csv['wind_direction_10m'].to_numpy()
    wd_100 = wd_csv['wind_direction_100m'].to_numpy()

    # --- Plot for 10m ---
    plt.figure(figsize=(10, 8)).clear()  # Force fresh figure
    ax1 = WindroseAxes.from_ax()  # Create new axes
    ax1.bar(wd_10, ws_10, normed=True)
    ax1.set_legend(title='Wind Speed (m/s)')
    
    # Set title - METHOD 1 (Direct)
    ax1.set_title("WIND ROSE AT 10M", fontsize=16, weight='bold', y=1.08)

    # Format radius axis to percentages
    fmt = '%.0f%%' 
    yticks = mtick.FormatStrFormatter(fmt)
    ax1.yaxis.set_major_formatter(yticks)

    # Save 10m plot
    output_path = output_dir / "wind_rose_10m.png"
    # Save 10m plot
    output_path = output_dir / "wind_rose_10m.png"
    plt.gcf().savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    #______100m_____
    plt.figure(figsize=(10, 8)).clear()  # Force fresh figure
    ax2 = WindroseAxes.from_ax()  # Create new axes
    ax2.bar(wd_100, ws_100, normed=True)
    ax2.set_legend(title='Wind Speed (m/s)')
    
     # Set title - METHOD 1 (Direct)
    ax2.set_title("WIND ROSE AT 100M", fontsize=16, weight='bold', y=1.08)

    # Format radius axis to percentages
    fmt = '%.0f%%' 
    yticks = mtick.FormatStrFormatter(fmt)
    ax2.yaxis.set_major_formatter(yticks)

    # Save 100m plot
    output_path = output_dir / "wind_rose_100m.png"
    plt.gcf().savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
   