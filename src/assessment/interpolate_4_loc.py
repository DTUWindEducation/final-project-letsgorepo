#----Import packages
from scipy.interpolate import griddata
import numpy as np

def interpolate_4_loc(wr_data_df, target_coord):
    '''
    Interpolate wind speed and direction at 10m and 100m heights for a given location
    from 4 surrounding stations over time.
    
    target_coord: [lat, lon]
    '''

    # Sort by time to ensure correct grouping
    wr_data_df = wr_data_df.sort_values('time').reset_index(drop=True)
    
    times = wr_data_df['time'].unique()
    interp_wspd_10m = []
    interp_wspd_100m = []
    interp_wdir_10m = []
    interp_wdir_100m = []

    for t in times:
        df_t = wr_data_df[wr_data_df['time'] == t]
        
        points = df_t[['latitude', 'longitude']].values
        wspd_10m = df_t['ref_wind_speed'].values

        # Convert wind direction to u, v
        dir_rad_10m = np.radians(df_t['ref_wind_direction'].values)
        u10 = -wspd_10m * np.sin(dir_rad_10m)
        v10 = -wspd_10m * np.cos(dir_rad_10m)

        # Interpolate speeds
        interp_wspd_10m.append(griddata(points, wspd_10m, target_coord, method='linear'))

        # Interpolate u and v components, then convert back to direction
        iu10 = griddata(points, u10, target_coord, method='linear')
        iv10 = griddata(points, v10, target_coord, method='linear')
        iwdir_10m = (np.degrees(np.arctan2(-iu10, -iv10)) + 360) % 360
        interp_wdir_10m.append(iwdir_10m)

        df = {'time': times,
        'wspd_10m': np.array(interp_wspd_10m),
        'wdir_10m': np.array(interp_wdir_10m),}
    return df

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