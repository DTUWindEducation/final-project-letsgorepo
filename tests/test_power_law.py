import pytest
import sys
import numpy as np
import pandas as pd
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))
from assessment.interpolate_4_loc import compute_alpha_from_two_heights, compute_wind_speed_at_height

def test_alpha_value():
    data = [
        {"time": "1997-01-01T00:00", "latitude": 55.75, "longitude": 7.75, "height": 10, "ref_wind_speed": 5.557057},
        {"time": "1997-01-01T00:00", "latitude": 55.75, "longitude": 7.75, "height": 100, "ref_wind_speed": 5.623321},
    ]
    df = pd.DataFrame(data)

    df_alpha = compute_alpha_from_two_heights(df)
    expected_alpha = np.log(5.623321 / 5.6) / np.log(100 / 10)

    assert np.isclose(df_alpha['alpha'].iloc[0], expected_alpha, atol=0.5)


def test_wind_speed_at_z():
    data = [
        {"time": "2020-01-01T00:00", "latitude": 55.75, "longitude": 7.75, "height": 10, "ref_wind_speed": 5.557057},
        {"time": "2020-01-01T00:00", "latitude": 55.75, "longitude": 7.75, "height": 100, "ref_wind_speed": 5.623321},
    ]
    df = pd.DataFrame(data)

    df_alpha = compute_alpha_from_two_heights(df)
    expected_alpha = np.log(5.623321 / 5.6) / np.log(100 / 10)

    df_wind_at_z = compute_wind_speed_at_height(df, target_height=80, ref_height=100, df_alpha=df_alpha)
    expected_ws_80 = 5.623321 * (80 / 100) ** expected_alpha

    assert np.isclose(df_wind_at_z['Windspeed at z [m/s]'].iloc[0], expected_ws_80, atol=0.5)