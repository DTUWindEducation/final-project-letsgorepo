#----Import packages
from scipy.interpolate import RegularGridInterpolator
import numpy as np
import pandas as pd

def interpolate_speed(wr_data_df, target_coord):
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

def interpolate_wind_direction(wr_data_df, target_coord):
    """
    Interpolates wind direction at a target location for multiple heights using u and v components.
    
    Args:
        wr_data_df (pd.DataFrame): Input data with columns 'latitude', 'longitude', 'u10', 'u100', 'v10', 'v100', 'time'.
        target_coord (tuple): Target (lat, lon) to interpolate.
        
    Returns:
        pd.DataFrame: Time series with interpolated wind directions for each height.
    """
    heights = [10, 100]
    
    # Ensure column names match
    wr_data_df = wr_data_df.rename(columns={
        'Latitude': 'latitude',
        'Longitude': 'longitude'
    })
    
    results = []
    
    for height in heights:
        # Create a copy for this height
        df_height = wr_data_df.copy()
        
        # Add height-specific u and v components
        df_height['u'] = df_height[f'u{height}']
        df_height['v'] = df_height[f'v{height}']
        
        df_height = df_height.sort_values('time')
        times = df_height['time'].unique()
        interpolated_directions = []
        
        for t in times:
            df_t = df_height[df_height['time'] == t]
            
            # Get 2x2 grid (sorted unique lat/lon)
            latitudes = sorted(df_t['latitude'].unique())
            longitudes = sorted(df_t['longitude'].unique())
            
            if len(latitudes) != 2 or len(longitudes) != 2:
                raise ValueError(f"Expected 2x2 grid, got {len(latitudes)}x{len(longitudes)} at time {t}")
            
            # Build u and v component grids
            u_grid = np.empty((2, 2))
            v_grid = np.empty((2, 2))
            
            for i, lat in enumerate(latitudes):
                for j, lon in enumerate(longitudes):
                    u_value = df_t[
                        (df_t['latitude'] == lat) & 
                        (df_t['longitude'] == lon)
                    ]['u'].values
                    
                    v_value = df_t[
                        (df_t['latitude'] == lat) & 
                        (df_t['longitude'] == lon)
                    ]['v'].values
                    
                    if len(u_value) == 1 and len(v_value) == 1:
                        u_grid[i, j] = u_value[0]
                        v_grid[i, j] = v_value[0]
                    else:
                        raise ValueError(f"Ambiguous/missing data at lat={lat}, lon={lon}, time={t}")
            
            # Interpolate u and v components
            interp_u = RegularGridInterpolator((latitudes, longitudes), u_grid, method='linear')
            interp_v = RegularGridInterpolator((latitudes, longitudes), v_grid, method='linear')
            
            u_interp = interp_u([target_coord])[0]
            v_interp = interp_v([target_coord])[0]
            
            # Calculate wind direction (0° = north, 90° = east)
            wind_dir = (270 - np.degrees(np.arctan2(v_interp, u_interp))) % 360
            interpolated_directions.append(wind_dir)
        
        results.append(pd.DataFrame({
            'time': times,
            f'wind_direction_{height}m': interpolated_directions
        }))
    
    # Merge results for all heights
    result_df = results[0]
    for df in results[1:]:
        result_df = result_df.merge(df, on='time', how='outer')

    return result_df.sort_values('time')
