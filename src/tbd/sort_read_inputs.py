import pandas as pd
def sort_four_locations(ref_w_100, ref_d_100, ref_w_10, ref_d_10, df):
    '''Calculate the mean wind speed for the four locations 
    loc1: 55.5°N, 7.75°E 
    loc2: 55.5°N, 8°E
    loc3: 55.75°N, 7.75°E
    loc4: 55.75°N, 8°E'''
    
    # Define four locations
<<<<<<< HEAD
    lat =  [55.5, 55.5, 55.75, 55.75]   #define latitudes
    lon = [7.75, 8.0, 7.75, 8.0]   #define longitudes
    
=======
    lat = [55.5,55.5,55.75,55.75]
    lon = [7.75,8,7.75,8]
    #_____________TODO__________Maybe move the location definition to main????
>>>>>>> ffc48620adb84dda28e686a17d55a6eaa290f1cf

    loc0 = (df['latitude'] == lat[0]) & (df['longitude'] == lon[0])
    loc1 = (df['latitude'] == lat[1]) & (df['longitude'] == lon[1])
    loc2 = (df['latitude'] == lat[2]) & (df['longitude'] == lon[2])
    loc3 = (df['latitude'] == lat[3]) & (df['longitude'] == lon[3])

    windspeed_loc0_100 = ref_w_100[loc0.values]
    windspeed_loc0_10 = ref_w_10[loc0.values]
<<<<<<< HEAD
    windspeed_loc0 = windspeed_loc0_100 + windspeed_loc0_10 #Why added them????
=======
    windspeed_loc0 = windspeed_loc0_100 + windspeed_loc0_10 #used for length of array, can be written better
>>>>>>> ffc48620adb84dda28e686a17d55a6eaa290f1cf
    # Create a new DataFrame with repeated lat/lon and the wind values
    loc0_100m_sort = pd.DataFrame({
        'Latitude': [55.5] * len(windspeed_loc0),
        'Longitude': [7.75] * len(windspeed_loc0),
        'Height [m]': [100] * len(windspeed_loc0_100),
        'Windspeed [m/s]': windspeed_loc0
    })
    loc0_10m_sort = pd.DataFrame({
        'Latitude': [55.5] * len(windspeed_loc0),
        'Longitude': [7.75] * len(windspeed_loc0),
        'Height [m]': [10] * len(windspeed_loc0_10),
        'Windspeed [m/s]': windspeed_loc0
    })
    Location0_windspeed = pd.concat([loc0_100m_sort, loc0_10m_sort], ignore_index=True)
    return Location0_windspeed
    #______________TODO___________Right now the wind direction is not included!!!!!!!________________________
    #______________TODO___________This needs to repeat so that it print for the other three locations aswell.__________
    #______________TODO___________Make the code smarter (not hardcode)___________________
