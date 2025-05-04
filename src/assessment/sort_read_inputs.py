def sort_four_locations(ds_ncfiles, lat_coord, lon_coord):
    '''Calculate the mean wind speed for the four locations
    loc1: 55.5°N, 7.75°E
    loc2: 55.5°N, 8°E
    loc3: 55.75°N, 7.75°E
    loc4: 55.75°N, 8°E'''

    # Sort dataset for .nc files into the four locations. Coordinates for
    # locations specefied as arrays.
    # Find the nearest number to locations.
    # !!! OBS: Latitude and longitude are reversed in nc files !!!
    loc0 = ds_ncfiles.sel({'longitude': lat_coord[0], 'latitude':
                           lon_coord[0]}, method="nearest")
    # loc1 = ds_ncfiles.sel({'longitude': lat_coord[0], 'latitude':
    #                       lon_coord[1]}, method="nearest")
    # loc2 = ds_ncfiles.sel({'longitude': lat_coord[1], 'latitude':
    #                       lon_coord[0]}, method="nearest")
    # loc3 = ds_ncfiles.sel({'longitude': lat_coord[1], 'latitude':
    #                       lon_coord[1]}, method="nearest")

    # Convert the dataset to a DataFrame
    df_loc0 = loc0.to_dataframe().reset_index()
    return df_loc0
