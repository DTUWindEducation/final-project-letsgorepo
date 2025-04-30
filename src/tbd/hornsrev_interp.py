# interp.py

import numpy as np
import pandas as pd
from pathlib import Path
from scipy.interpolate import griddata
from read_input import read_input_calc_wref


def interpolate_to_point(
    file_path: str,
    target_lat: float,
    target_lon: float
) -> pd.DataFrame:
    """
    Interpolate wind speed and direction to a target point (lat, lon)
    for each timestamp from a NetCDF file.

    Args:
        file_path (str): Path to the NetCDF file.
        target_lat (float): Latitude of the interpolation point.
        target_lon (float): Longitude of the interpolation point.

    Returns:
        pd.DataFrame: DataFrame with interpolated values.
    """
    # Re-read raw data to get full DataFrame (optional: refactor read_input to return df)
    import xarray as xr

    ds = xr.open_dataset(file_path, engine="netcdf4")
    df = ds.to_dataframe().reset_index()
    ds.close()

    # Group data by time to interpolate at each timestamp
    result_rows = []
    grouped = df.groupby("time")

    for timestamp, group in grouped:
        points = group[["latitude", "longitude"]].values

        # Interpolate wind speed magnitude
        u = group["u10"].values
        v = group["v10"].values
        speed = np.sqrt(u ** 2 + v ** 2)
        speed_interp = griddata(
            points, speed, [(target_lat, target_lon)], method="linear"
        )[0]

        # Interpolate u and v components separately to get direction
        u_interp = griddata(points, u, [(target_lat, target_lon)], method="linear")[0]
        v_interp = griddata(points, v, [(target_lat, target_lon)], method="linear")[0]

        direction_interp = (np.arctan2(v_interp, u_interp) * 180 / np.pi + 360) % 360

        result_rows.append({
            "time": timestamp,
            "latitude": target_lat,
            "longitude": target_lon,
            "wind_speed": speed_interp,
            "wind_direction": direction_interp
        })

    result_df = pd.DataFrame(result_rows)
    return result_df


if __name__ == "__main__":
    # Example usage
    root = Path(__file__).resolve().parent
    input_file = root / "inputs" / "1997-1999.nc"

    target_lat = 7.875
    target_lon = 55.625

    interpolated_df = interpolate_to_point(str(input_file), target_lat, target_lon)
    interpolated_df.to_csv("interpolated_point_E.csv", index=False)

    print("✅ Interpolation complete. Output saved to interpolated_point_E.csv")
