# import pytest
# import xarray as xr
# import pandas as pd
# from pathlib import Path
# import glob

# @pytest.fixture
# def nc_file_path():
#     """Fixture to return a valid NetCDF file path in the inputs directory."""
#     inputs_dir = Path(__file__).parent.parent / "inputs"
#     nc_files = list(inputs_dir.glob("*.nc"))
#     assert nc_files, "No .nc files found in the inputs folder!"
#     return nc_files[0]  # Return the first .nc file for testing

# def test_nc_file_can_be_opened(nc_file_path):
#     """Test that the .nc file can be opened using xarray."""
#     ds = xr.open_dataset(nc_file_path, engine="netcdf4")
#     assert isinstance(ds, xr.Dataset), "Failed to open .nc file as xarray Dataset"
#     ds.close()

# def test_nc_file_can_be_converted_to_dataframe(nc_file_path):
#     """Test that the .nc file can be converted to a DataFrame and contains data."""
#     with xr.open_dataset(nc_file_path, engine="netcdf4") as ds:
#         df = ds.to_dataframe().reset_index()
    
#     # Check that the output is a DataFrame
#     assert isinstance(df, pd.DataFrame), "Converted object is not a DataFrame"

#     # Check that the DataFrame is not empty
#     assert not df.empty, "DataFrame from .nc file is empty"

#     # Check for expected columns (you can customize these based on your data)
#     expected_columns = ['time', 'latitude', 'longitude']  # Adjust based on your .nc file structure
#     missing_columns = [col for col in expected_columns if col not in df.columns]
#     assert not missing_columns, f"Missing expected columns: {missing_columns}"

import runpy
import pytest
from pathlib import Path

def test_open_nc_files_script_runs():
    # Get the script path
    script_path = Path(__file__).resolve().parent.parent / 'src' / 'assessment' / 'open_nc_files.py'

    # Execute the script using runpy
    runpy.run_path(str(script_path), run_name="__main__")
    
    # If we get here, it means the script ran without errors
    assert True  # Just asserting True to ensure the test passes
