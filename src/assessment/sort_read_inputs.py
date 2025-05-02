import pandas as pd

def sort_four_locations(ref_w_100, ref_d_100, ref_w_10, ref_d_10, ds_ncfiles, lat_coord, lon_coord):
    '''Calculate the mean wind speed for the four locations 
    loc1: 55.5°N, 7.75°E 
    loc2: 55.5°N, 8°E
    loc3: 55.75°N, 7.75°E
    loc4: 55.75°N, 8°E'''
    
    # Sort dataset for .nc files into the four locations. Coordinates for locations specefied as arrays.
    # Find the nearest number to locations. 
    # !!! OBS: Latitude and longitude are reversed in nc files !!!
    loc0 = ds_ncfiles.sel({'longitude': lat_coord[0], 'latitude': lon_coord[0]}, method="nearest")
    loc1 = ds_ncfiles.sel({'longitude': lat_coord[0], 'latitude': lon_coord[1]}, method="nearest")
    loc2 = ds_ncfiles.sel({'longitude': lat_coord[1], 'latitude': lon_coord[0]}, method="nearest")
    loc3 = ds_ncfiles.sel({'longitude': lat_coord[1], 'latitude': lon_coord[1]}, method="nearest")

    #all = ds_ncfiles[loc0].sel(latitude=loc0.latitude.values, longitude=loc0.longitude.values, method='nearest')
    
    #windspeed_loc0_100 = ref_w_100.sel(loc0['latitude'])
    #windspeed_loc0_10 = ref_w_10[loc0.values]

    # Convert the dataset to a DataFrame
    df_loc0 = loc0.to_dataframe().reset_index()  #  
    return df_loc0
    #___________OLD CODE___________________
    #loc0 = (df['latitude'] == lat[0]) & (df['longitude'] == lon[0]) #dont do equal to, but find the nearest number
    #loc1 = (df['latitude'] == lat[1]) & (df['longitude'] == lon[1])
    #loc2 = (df['latitude'] == lat[2]) & (df['longitude'] == lon[2])
    #loc3 = (df['latitude'] == lat[3]) & (df['longitude'] == lon[3])

    # windspeed_loc0_100 = ref_w_100[loc0.values]
    # windspeed_loc0_10 = ref_w_10[loc0.values]
    # windspeed_loc0 = windspeed_loc0_100 + windspeed_loc0_10 #used for length of array, can be written better
    # # Create a new DataFrame with repeated lat/lon and the wind values
    # loc0_100m_sort = pd.DataFrame({
    #     'Latitude': [55.5] * len(windspeed_loc0),
    #     'Longitude': [7.75] * len(windspeed_loc0),
    #     'Height [m]': [100] * len(windspeed_loc0_100),
    #     'Windspeed [m/s]': windspeed_loc0_100
    # })
    # loc0_10m_sort = pd.DataFrame({
    #     'Latitude': [55.5] * len(windspeed_loc0),
    #     'Longitude': [7.75] * len(windspeed_loc0),
    #     'Height [m]': [10] * len(windspeed_loc0_10),
    #     'Windspeed [m/s]': windspeed_loc0_10
    # })
    # Location0_windspeed = pd.concat([loc0_100m_sort, loc0_10m_sort], ignore_index=True)
    # return Location0_windspeed
    #______________TODO___________Right now the wind direction is not included!!!!!!!________________________
    #______________TODO___________This needs to repeat so that it print for the other three locations aswell.__________
    #______________TODO___________Make the code smarter (not hardcode)___________________
