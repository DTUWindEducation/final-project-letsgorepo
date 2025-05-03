import xarray as xr
import numpy as np
import pandas as pd
from pathlib import Path
import glob
import csv

from assessment.defclasses import WindDataLoader  #remember to add the 'assessment.':)

def read_resource_calc_wref(file):
    """
    Process all .nc files in the inputs folder and return combined DataFrames.
    """
    THIS_FILE = Path(file).parent
    inputs_dir = THIS_FILE.parent / 'inputs'
    nc_files = glob.glob(str(inputs_dir / '*.nc'))

    all_long_dfs = []
    all_raw_dfs = []

    for nc_file in nc_files:
        loader = WindDataLoader(nc_file)
        df_long, df_raw = loader.compute_and_format_dataframe()
        all_long_dfs.append(df_long)
        all_raw_dfs.append(df_raw)

    # Combine all files into one DataFrame (optional)
    combined_long_df = pd.concat(all_long_dfs, ignore_index=True)
    combined_raw_df = pd.concat(all_raw_dfs, ignore_index=True)

    return combined_long_df, combined_raw_df


def read_turbine(file):
    # We go outside the src folder to find the inputs folder
    THIS_FILE = Path(file).parent  # current script directory or use __file__
    inputs_dir = THIS_FILE.parent / 'inputs'  # inputs folder is at the same level as src
    
    # read the .csv files
    csv_files = glob.glob(str(inputs_dir / '*.csv'))  # search for .csv files in the inputs directory (str so that glob.glob can recodnise)

    # for csv_file in csv_files:#MAYBE USE FOR LOOP INSTEAD
    turb_15 = pd.read_csv(csv_files[0])
    turb_5 = pd.read_csv(csv_files[1])

    #MAYBE there's a clever way to do this??????
    w5, P5, Cp5, Thrust5, Ct5 = turb_5.iloc[:, 0], turb_5.iloc[:, 1], turb_5.iloc[:, 2], turb_5.iloc[:, 3], turb_5.iloc[:, 4]
    w15, P15, Cp15 = turb_15.iloc[:, 0], turb_15.iloc[:, 1], turb_15.iloc[:, 2]
    size = w15.shape[0]
    Ct15 = np.zeros((size))
    
    return turb_5, turb_15