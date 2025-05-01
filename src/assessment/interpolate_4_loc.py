#----Import packages
from scipy.interpolate import RegularGridInterpolator
import numpy as np
import pandas as pd

def interpolate_4_loc(wr_data_df, target_coord):
        """
        Interpolates wind speeds at a target location for multiple heights.
        
        Args:
            wr_data_df (pd.DataFrame): Input data with columns 'latitude', 'longitude', 'ref_wind_speed', 'time', 'height'.
            target_coord (tuple): Target (lat, lon) to interpolate.
            heights (list): List of heights (e.g., [10, 100]) to interpolate.
            
        Returns:
            pd.DataFrame: Time series with interpolated speeds for each height.
        """
        heights = [10, 100]
        # Ensure column names match
        wr_data_df = wr_data_df.rename(columns={
            'Latitude': 'latitude',
            'Longitude': 'longitude',
            'Per wind speed': 'ref_wind_speed'
        })
        
        results = []
        
        for height in heights:
            # Filter by height and sort by time
            df_height = wr_data_df[wr_data_df['height'] == height].copy()
            df_height = df_height.sort_values('time')
            
            times = df_height['time'].unique()
            interpolated_speeds = []
            
            for t in times:
                df_t = df_height[df_height['time'] == t]
                
                # Get 2x2 grid (sorted unique lat/lon)
                latitudes = sorted(df_t['latitude'].unique())
                longitudes = sorted(df_t['longitude'].unique())
                
                if len(latitudes) != 2 or len(longitudes) != 2:
                    raise ValueError(f"Expected 2x2 grid, got {len(latitudes)}x{len(longitudes)} at time {t}")
                
                # Build wind speed grid
                wind_grid = np.empty((2, 2))
                for i, lat in enumerate(latitudes):
                    for j, lon in enumerate(longitudes):
                        value = df_t[
                            (df_t['latitude'] == lat) & 
                            (df_t['longitude'] == lon)
                        ]['ref_wind_speed'].values
                        if len(value) == 1:
                            wind_grid[i, j] = value[0]
                        else:
                            raise ValueError(f"Ambiguous/missing data at lat={lat}, lon={lon}, time={t}")
                
                # Interpolate
                interp = RegularGridInterpolator((latitudes, longitudes), wind_grid, method='linear')
                interpolated_speeds.append(interp([target_coord])[0])
            
            results.append(pd.DataFrame({
                'time': times,
                f'wind_speed_{height}m': interpolated_speeds
            }))
        
        # Merge results for all heights
        result_df = results[0]
        for df in results[1:]:
            result_df = result_df.merge(df, on='time', how='outer')
        
        return result_df.sort_values('time')

    # wr_data_df = wr_data_df[wr_data_df['height'] == height].copy()
    # wr_data_df = wr_data_df.sort_values('time')

    # times = wr_data_df['time'].unique()
    # interpolated = []

    # for t in times:
    #     df_t = wr_data_df[wr_data_df['time'] == t]

    #     # Get lat/lon grid
    #     latitudes = sorted(df_t['latitude'].unique())
    #     longitudes = sorted(df_t['longitude'].unique())

    #     if len(latitudes) != 2 or len(longitudes) != 2:
    #         raise ValueError(f"Expected 2x2 grid, got {len(latitudes)}x{len(longitudes)} at time {t}")

    #     # Build wind grid
    #     wind_grid = np.empty((2, 2))
    #     for i, lat in enumerate(latitudes):
    #         for j, lon in enumerate(longitudes):
    #             value = df_t[(df_t['latitude'] == lat) & (df_t['longitude'] == lon)]['ref_wind_speed'].values
    #             if len(value) == 1:
    #                 wind_grid[i, j] = value[0]
    #             else:
    #                 raise ValueError(f"Ambiguous or missing value at lat={lat}, lon={lon} for time {t}")

    #     # Interpolate
    #     interp = RegularGridInterpolator((latitudes, longitudes), wind_grid, method='linear')
    #     interpolated.append(interp([target_coord])[0])
    #return interpolated_series.head()
    #return np.array(interpolated), times

# def interpolate_4_loc(wr_data_df, target_coord):
#     '''
#     Interpolate wind speed and direction at 10m and 100m heights for a given location
#     from 4 surrounding stations over time.
    
#     target_coord: [lat, lon]
#     '''

#     # Sort by time to ensure correct grouping
#     wr_data_df = wr_data_df.sort_values('time').reset_index(drop=True)
    
#     times = wr_data_df['time'].unique()
#     interp_wspd = []
#     interp_wdir = []

#     for t in times:
#         df_t = wr_data_df[wr_data_df['time'] == t]
        
#         points = df_t[['latitude', 'longitude']].values
#         wspd = df_t['ref_wind_speed'].values

#         # Convert wind direction to u, v
#         dir_rad = np.radians(df_t['ref_wind_direction'].values)
#         u10 = -wspd * np.sin(dir_rad)
#         v10 = -wspd * np.cos(dir_rad)

#         # Interpolate speeds
#         interp_wspd.append(griddata(points, wspd, target_coord, method='linear'))

#         # Interpolate u and v components, then convert back to direction
#         iu10 = griddata(points, u10, target_coord, method='linear')
#         iv10 = griddata(points, v10, target_coord, method='linear')
#         iwdir = (np.degrees(np.arctan2(-iu10, -iv10)) + 360) % 360
#         interp_wdir.append(iwdir)

#     df = {'time': times,
#     'wspd': np.array(interp_wspd),
#     'wdir': np.array(interp_wdir),}
#     return len(df)

# def interpolate_4_loc(wr_data_df, coord):
#     '''Takes windspeeds and winddirection from the four location (including the coordinates),
#     and then interpolates in regards to a specific location'''
#     points = wr_data_df[['latitude', 'longitude']].head(20).values
#     #pointsx = wr_data_df['latitude'].head(50).values
#     #pointsy = wr_data_df['longitude'].head(50).values
#     values = wr_data_df['ref_wind_speed'].head(50).values

#     interpolated_speed = []
#     for i in (values):
#         result = griddata(points, values, coord, method='nearest')
#         interpolated_speed.append(result)
    
#     return values
    #return np.array(interpolated_speed)