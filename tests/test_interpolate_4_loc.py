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

# # Create test data
# @pytest.fixture
# def wr_data_df():
#     times = pd.date_range("2025-01-01", periods=2, freq="H")
#     data = []
#     for lon in [7.75, 7.76]:
#         for lat in [55.5, 55.51]:
#             for t in times:
#                 data.append({
#                     'longitude': lon,
#                     'latitude': lat,
#                     'time': t,
#                     'ref_wind_speed': 5 + lon + lat,  # Ensure different values
#                     'ref_wind_direction': 100 + lon + lat,
#                     'height': 100
#                 })
#     return pd.DataFrame(data)

# def test_interpolate_speed(wr_data_df):
#     # Note: RegularGridInterpolator uses (x, y) coordinates
#     target_coord = (7.755, 55.505)  # (lon, lat)
#     result = interpolate_speed(wr_data_df, target_coord)
#     assert isinstance(result, np.ndarray)
#     assert result.shape[0] == 2
#     assert np.all(np.isfinite(result))

# def test_interpolate_direction(wr_data_df):
#     target_coord = (7.755, 55.505)  # (lon, lat)
#     result = interpolate_direction(wr_data_df, target_coord)
#     assert isinstance(result, np.ndarray)
#     assert result.shape[0] == 2
#     assert np.all(np.isfinite(result))

# def test_plot_interpolation(wr_data_df):
#     target_coord = (7.755, 55.505)
#     int_speed = interpolate_speed(wr_data_df, target_coord)
#     int_dir = interpolate_direction(wr_data_df, target_coord)
#     fig = plot_interpolation(int_speed, int_dir, target_coord)
#     assert isinstance(fig, plt.Figure)

import numpy as np
import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent / "src"))

from assessment.interpolate_4_loc import (
    interpolate_speed, interpolate_direction, plot_interpolation,
    interpolate_max_ws_100, compute_alpha_from_two_heights,
    compute_wind_speed_at_height
)

def test_everything_runs(tmp_path):
    # Create dummy data: 2 longitude points, 2 latitude points, 2 time steps, 2 heights
    data = []
    lons = [7.8, 7.85]
    lats = [55.6, 55.65]
    times = pd.date_range("2022-01-01", periods=2, freq="H")
    heights = [10, 100]

    for t in times:
        for h in heights:
            for lon in lons:
                for lat in lats:
                    data.append({
                        'longitude': lon,
                        'latitude': lat,
                        'time': t,
                        'height': h,
                        'ref_wind_speed': np.random.uniform(5, 15),
                        'ref_wind_direction': np.random.uniform(0, 360)
                    })
    df = pd.DataFrame(data)

    # Define target coordinate for interpolation
    target_coord = np.array([[7.825, 55.625]])

    # Call all functions from the module to ensure full code coverage
    df_speed = interpolate_speed(df, target_coord)
    df_dir = interpolate_direction(df, target_coord)

    _ = plot_interpolation(df_speed['wind_speed_100m'], df_dir['wind_direction_100m'], target_coord)

    lat, lon, max_ws = interpolate_max_ws_100(df, height=100)
    assert isinstance(lat, float) and isinstance(lon, float)

    df_alpha = compute_alpha_from_two_heights(df)
    assert 'alpha' in df_alpha.columns

    df_at_z = compute_wind_speed_at_height(df, target_height=80, ref_height=100, df_alpha=df_alpha)
    assert 'Windspeed at z [m/s]' in df_at_z.columns

