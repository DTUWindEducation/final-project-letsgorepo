# wind_loader.py

from pathlib import Path
import xarray as xr
import numpy as np
import pandas as pd

class WindDataLoader:
    def __init__(self, file_path):
        """
        Initialize the loader with the path to the NetCDF file.
        """
        self.file_path = file_path
        self.dataset = None

    def load_data(self):
        """
        Load the NetCDF file into an xarray dataset.
        """
        self.dataset = xr.open_dataset(self.file_path, engine="netcdf4")
        return self.dataset

    def compute_and_format_dataframe(self):
        """
        Compute wind speed and direction at 10m and 100m and return a formatted DataFrame.
        """
        if self.dataset is None:
            self.load_data()

        df = self.dataset.to_dataframe().reset_index()

        # Compute wind speed
        df['wind_speed_10'] = np.sqrt(df['u10']**2 + df['v10']**2)
        df['wind_speed_100'] = np.sqrt(df['u100']**2 + df['v100']**2)

        # Compute wind direction (meteorological convention)
        df['wind_direction_10'] = (270 - np.arctan2(df['v10'], df['u10']) * 180 / np.pi) % 360
        df['wind_direction_100'] = (270 - np.arctan2(df['v100'], df['u100']) * 180 / np.pi) % 360

        # Combine into long-form DataFrame
        df_long = pd.concat([
            df[['wind_speed_10', 'wind_direction_10', 'latitude', 'longitude', 'valid_time']].rename(columns={
                'wind_speed_10': 'ref_wind_speed',
                'wind_direction_10': 'ref_wind_direction',
                'valid_time': 'time'
            }).assign(height=10),
            df[['wind_speed_100', 'wind_direction_100', 'latitude', 'longitude', 'valid_time']].rename(columns={
                'wind_speed_100': 'ref_wind_speed',
                'wind_direction_100': 'ref_wind_direction',
                'valid_time': 'time'
            }).assign(height=100)
        ], axis=0, ignore_index=True)

        return df_long, df  # long-form for downstream; full df for inspection/debug
