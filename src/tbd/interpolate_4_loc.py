#----Import packages
from scipy.interpolate import griddata
import numpy as np

def interpolate_4_loc(loc1,loc2,loc3,loc4,coord):
    '''Takes windspeeds and winddirection from the four location (including the coordinates),
    and then interpolates in regards to a specific location'''
    # Samlpe data as 2D
    #lat = [loc1[0],loc2[0],loc3[0],loc4[0]]  #first column in input is latitude
    #long = [loc1[1],loc2[1],loc3[1],loc4[1]]  #second column in input is longitude
    points = np.array([
        [loc1[0],loc1[1]],
        [loc2[0],loc2[1]],
        [loc3[0],loc3[1]],
        [loc4[0],loc4[1]]])
    
    ws = np.array([9.794061,9.802940,9.771493,10.123184])
    result = griddata(points, ws, coord, method="linear")
    #interp_func = RectBivariateSpline(points, ws, coord, extrapolate=True)
    # New points to interpolate for
    return float(result[0])
    # Data to interpolate
    #__________TODO________make the interpolation work for our results....
