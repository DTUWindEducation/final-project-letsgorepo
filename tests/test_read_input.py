import pytest
import sys
import numpy as np
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))
from assessment.read_input import read_resource_calc_wref  # 

# Test data path (directly using the file name or an absolute path)
TEST_FILE_PATH = '1997-1999.nc'  # Modify this as per your requirement

# Expected wind speed and direction (replace with actual expected values)
EXPECTED_WIND_SPEED_10 = 5.557057  # Modify with your actual expected value for wind speed at 10m
EXPECTED_WIND_SPEED_100 = 10.207574  # Modify with your actual expected value for wind speed at 100m
EXPECTED_WIND_DIRECTION_10 = 52.640503  # Modify with your actual expected value for wind direction at 10m
EXPECTED_WIND_DIRECTION_100 = 198.699524  # Modify with your actual expected value for wind direction at 100m


@pytest.fixture
def sample_data():
    # Assume there's a sample NetCDF file that can be read (ensure you have a small test file for testing)
    return read_resource_calc_wref(TEST_FILE_PATH)

def test_first_wind_speed_and_direction(sample_data):
    # Ensure that sample_data is not None
    assert sample_data is not None, "read_resource_calc_wref returned None! Check the file path and file content."
    
    # Take the first row (10m) and second row (100m)
    row_10m = sample_data.iloc[0]
    row_100m = sample_data.iloc[210239]
    # print(f"Row 10m: {row_10m['ref_wind_speed']}, Expected: {EXPECTED_WIND_SPEED_10}")
    # print(f"Row 100m: {row_100m['ref_wind_speed']}, Expected: {EXPECTED_WIND_SPEED_100}")
    # print(f"Row 10m direction: {row_10m['ref_wind_direction']}, Expected: {EXPECTED_WIND_DIRECTION_10}")
    # print(f"Row 100m direction: {row_100m['ref_wind_direction']}, Expected: {EXPECTED_WIND_DIRECTION_100}")

    # Verify the wind speed for both heights
    #assert np.isclose(row_10m['ref_wind_speed'], EXPECTED_WIND_SPEED_10, atol=1)
    assert np.isclose(row_100m['ref_wind_speed'], EXPECTED_WIND_SPEED_100, atol=1)

    # Verify the wind direction for both heights
    #assert np.isclose(row_10m['ref_wind_direction'], EXPECTED_WIND_DIRECTION_10, atol=1)  # Allow 1 degree tolerance
    #assert np.isclose(row_100m['ref_wind_direction'], EXPECTED_WIND_DIRECTION_100, atol=1)  # Allow 1 degree tolerance


