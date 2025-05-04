# import pytest
# import sys
# import pandas as pd
# import numpy as np
# from pathlib import Path
# from src.assessment.aep import power_range, calc_aep, calc_aep_per_speed
# sys.path.append(str(Path(__file__).parent.parent / "src"))

# @pytest.fixture
# def sample_wind_data():
#     return pd.DataFrame({
#         'time': pd.date_range(start='2020-01-01', periods=5, freq='D').tolist() * 2,
#         'height': [100] * 5 + [10] * 5,
#         'ref_wind_speed': [4, 6, 8, 10, 12] * 2
#     })

# @pytest.fixture
# def sample_turbine_data():
#     return pd.DataFrame({
#         'Wind Speed [m/s]': np.array([3, 5, 7, 9, 11]),
#         'Power [kW]': np.array([0, 100, 500, 1000, 1500])
#     })

# def test_power_range_output(sample_wind_data, sample_turbine_data):
#     min_ws, max_ws, length, filtered = power_range(
#         sample_wind_data, height=100,
#         turb=sample_turbine_data,
#         t_start='2020-01-01', t_end='2020-01-05'
#     )
#     assert np.isclose(min_ws, 4)
#     assert np.isclose(max_ws, 12)
#     assert length == 4  # Only 4 points with power > 0
#     assert isinstance(filtered, pd.DataFrame)
#     assert not filtered.empty

# def test_calc_aep_returns_float(sample_turbine_data):
#     pdf = np.array([0.05, 0.1, 0.25, 0.4, 0.2])
#     filtered = sample_turbine_data[sample_turbine_data['Power [kW]'] > 0]
#     aep = calc_aep(filtered, pdf[1:])  # drop first since first power = 0
#     assert isinstance(aep, float)
#     assert aep > 0

# def test_calc_aep_per_speed_valid_output(sample_turbine_data):
#     pdf = np.array([0.0, 0.1, 0.3, 0.4, 0.2])  # same length as turbine power
#     filtered = sample_turbine_data
#     # This should NOT raise, even though PDF and turbine speeds align
#     try:
#         calc_aep_per_speed(filtered, pdf, coord="TestCoord")
#     except Exception as e:
#         pytest.fail(f"calc_aep_per_speed raised an exception: {e}")
