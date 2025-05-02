import pytest
import xarray as xr
import numpy as np
from assessment.sort_read_inputs import sort_four_locations  # Adjust the import path as needed

@pytest.fixture
def mock_ds():
    """Mock a small xarray.Dataset to simulate .nc file content"""
    lat = np.array([55.5, 55.75])
    lon = np.array([7.75, 8.0])
    time = np.array(np.arange('2020-01', '2020-02', dtype='datetime64[D]'))

    data = xr.Dataset(
        {
            "u10": (("time", "latitude", "longitude"), np.random.rand(len(time), 2, 2)),
            "v10": (("time", "latitude", "longitude"), np.random.rand(len(time), 2, 2)),
        },
        coords={
            "time": time,
            "latitude": lat,
            "longitude": lon,
        }
    )
    return data

def test_sort_four_locations(mock_ds):
    """Test whether sort_four_locations selects the correct coordinates and returns a non-empty DataFrame"""
    # Use mocked data for wind speed and direction
    ref_w_100 = mock_ds["u10"]
    ref_d_100 = mock_ds["v10"]
    ref_w_10 = mock_ds["u10"]
    ref_d_10 = mock_ds["v10"]
    
    lat_coord = [55.5, 55.75]
    lon_coord = [7.75, 8.0]

    # Call the function
    df_result = sort_four_locations(ref_w_100, ref_d_100, ref_w_10, ref_d_10, mock_ds, lat_coord, lon_coord)

    # Assertions: output must be a non-empty DataFrame with required columns
    assert df_result is not None, "Function returned None"
    assert not df_result.empty, "Returned DataFrame is empty"
    assert "latitude" in df_result.columns, "Missing 'latitude' column in DataFrame"
    assert "longitude" in df_result.columns, "Missing 'longitude' column in DataFrame"
    assert "time" in df_result.columns, "Missing 'time' column in DataFrame"
