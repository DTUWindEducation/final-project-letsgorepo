import sys
import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# Add module path
sys.path.append(str(Path(__file__).parent.parent / "src"))
from assessment.interpolate_4_loc import (
    interpolate_speed,
    interpolate_direction,
    plot_interpolation
)

# Create test data
@pytest.fixture
def wr_data_df():
    times = pd.date_range("2025-01-01", periods=2, freq="H")
    data = []
    for lon in [7.75, 7.76]:
        for lat in [55.5, 55.51]:
            for t in times:
                data.append({
                    'longitude': lon,
                    'latitude': lat,
                    'time': t,
                    'ref_wind_speed': 5 + lon + lat,  # Ensure different values
                    'ref_wind_direction': 100 + lon + lat,
                    'height': 100
                })
    return pd.DataFrame(data)

def test_interpolate_speed(wr_data_df):
    # Note: RegularGridInterpolator uses (x, y) coordinates
    target_coord = (7.755, 55.505)  # (lon, lat)
    result = interpolate_speed(wr_data_df, target_coord)
    assert isinstance(result, np.ndarray)
    assert result.shape[0] == 2
    assert np.all(np.isfinite(result))

def test_interpolate_direction(wr_data_df):
    target_coord = (7.755, 55.505)  # (lon, lat)
    result = interpolate_direction(wr_data_df, target_coord)
    assert isinstance(result, np.ndarray)
    assert result.shape[0] == 2
    assert np.all(np.isfinite(result))

def test_plot_interpolation(wr_data_df):
    target_coord = (7.755, 55.505)
    int_speed = interpolate_speed(wr_data_df, target_coord)
    int_dir = interpolate_direction(wr_data_df, target_coord)
    fig = plot_interpolation(int_speed, int_dir, target_coord)
    assert isinstance(fig, plt.Figure)
