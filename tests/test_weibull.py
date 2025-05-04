import sys
from pathlib import Path

# Add the src folder to the Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

import pytest
import numpy as np
import pandas as pd
from assessment.weibull import weibull_model, process_weibull


def test_weibull_model():
    """Test the Weibull model function."""
    x = np.array([1, 2, 3, 4, 5])
    c = 2.0  # Scale parameter
    k = 1.5  # Shape parameter

    result = weibull_model(x, c, k)

    assert isinstance(result, np.ndarray)
    assert len(result) == len(x)
    assert np.all(result >= 0)  # PDF values should be non-negative


@pytest.fixture
def wind_data():
    """Fixture to generate synthetic wind speed data."""
    np.random.seed(42)
    return pd.DataFrame({
        'wind_speed_10m': np.random.weibull(2.0, 500) * 5,
        'wind_speed_100m': np.random.weibull(2.2, 500) * 6
    })


def test_process_weibull_valid(wind_data):
    """Test process_weibull with valid inputs."""
    c_opt, k_opt, pdf_range = process_weibull(
        data_wind_df=wind_data,
        coord=(59.44, 24.75),
        height=10,
        power_range=50,
        wind_speed_min=0,
        wind_speed_max=25
    )

    assert isinstance(c_opt, float)
    assert isinstance(k_opt, float)
    assert isinstance(pdf_range, np.ndarray)
    assert len(pdf_range) == 50
    assert 0 < c_opt < 20
    assert 0 < k_opt < 10


@pytest.mark.parametrize("height", [10, 100])
def test_process_weibull_valid_heights(wind_data, height):
    """Test process_weibull with valid heights."""
    c_opt, k_opt, pdf_range = process_weibull(
        data_wind_df=wind_data,
        coord=(59.44, 24.75),
        height=height,
        power_range=50,
        wind_speed_min=0,
        wind_speed_max=25
    )

    assert isinstance(c_opt, float)
    assert isinstance(k_opt, float)
    assert isinstance(pdf_range, np.ndarray)


def test_process_weibull_invalid_height(wind_data):
    """Test process_weibull with an invalid height."""
    with pytest.raises(ValueError, match="Height must be either 10 or 100 meters."):
        process_weibull(
            data_wind_df=wind_data,
            coord=(59.44, 24.75),
            height=30,  # Invalid height
            power_range=50,
            wind_speed_min=0,
            wind_speed_max=25
        )


def test_process_weibull_empty_data():
    """Test process_weibull with an empty DataFrame."""
    wind_data = pd.DataFrame({
        'wind_speed_10m': [],
        'wind_speed_100m': []
    })

    with pytest.raises(ValueError, match="No valid wind speed data available for height 10m."):
        process_weibull(
            data_wind_df=wind_data,
            coord=(59.44, 24.75),
            height=10,
            power_range=50,
            wind_speed_min=0,
            wind_speed_max=25
        )


def test_process_weibull_nan_handling():
    """Test process_weibull with NaN values in the wind speed data."""
    wind_data = pd.DataFrame({
        'wind_speed_10m': [5, 6, np.nan, 7, 8],
        'wind_speed_100m': [6, np.nan, 8, 9, 10]
    })

    c_opt, k_opt, pdf_range = process_weibull(
        data_wind_df=wind_data,
        coord=(59.44, 24.75),
        height=10,
        power_range=50,
        wind_speed_min=0,
        wind_speed_max=25
    )

    assert isinstance(c_opt, float)
    assert isinstance(k_opt, float)
    assert isinstance(pdf_range, np.ndarray)











