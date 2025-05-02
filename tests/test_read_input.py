import pytest
import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Add project src path
sys.path.append(str(Path(__file__).parent.parent / "src"))
from assessment.read_input import read_resource_calc_wref, read_turbine

# Test input path
TEST_FILE_PATH = "inputs/1997-1999.nc"  # Path to the test NetCDF file

# Expected wind speed and direction values (update to match your actual data)
EXPECTED_WIND_SPEED_100 = 10.207574
EXPECTED_WIND_DIRECTION_100 = 198.699524

@pytest.fixture
def sample_data():
    """Fixture to load sample resource data from NetCDF file."""
    return read_resource_calc_wref(TEST_FILE_PATH)

def test_first_wind_speed_and_direction(sample_data):
    """Test wind speed and direction at 100m height."""
    assert sample_data is not None, "read_resource_calc_wref returned None. Please check file path and contents."

    # Unpack the tuple
    df_long, _ = sample_data

    # Retrieve the row at the given index (adjust index as needed)
    row_100m = df_long.iloc[210239]

    # Check that wind speed and direction are within acceptable tolerance
    assert np.isclose(row_100m['ref_wind_speed'], EXPECTED_WIND_SPEED_100, atol=1), \
        f"Expected wind speed: {EXPECTED_WIND_SPEED_100}, but got: {row_100m['ref_wind_speed']}"
    assert np.isclose(row_100m['ref_wind_direction'], EXPECTED_WIND_DIRECTION_100, atol=1), \
        f"Expected wind direction: {EXPECTED_WIND_DIRECTION_100}, but got: {row_100m['ref_wind_direction']}"

def test_read_turbine_returns_two_dataframes():
    """Test if read_turbine returns two non-empty DataFrames with expected columns."""
    turb_5, turb_15 = read_turbine(TEST_FILE_PATH)

    # Check types
    assert isinstance(turb_5, pd.DataFrame), "turb_5 is not a DataFrame"
    assert isinstance(turb_15, pd.DataFrame), "turb_15 is not a DataFrame"

    # Check column names
    expected_columns_5 = ['Wind Speed [m/s]', 'Power [kW]', 'Cp [-]', 'Thrust [kN]', 'Ct [-]']
    expected_columns_15 = ['Wind Speed [m/s]', 'Power [kW]', 'Cp [-]']

    assert all(col in turb_5.columns for col in expected_columns_5), "turb_5 is missing expected columns"
    assert all(col in turb_15.columns for col in expected_columns_15), "turb_15 is missing expected columns"

    # Check if data is not empty
    assert not turb_5.empty, "turb_5 is empty"
    assert not turb_15.empty, "turb_15 is empty"
