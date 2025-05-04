import pytest
import sys
import numpy as np
import pandas as pd
from pathlib import Path

# Add path to src folder
sys.path.append(str(Path(__file__).parent.parent / "src"))

from assessment.Weibull import process_weibull  # Adjust the path/module if needed


def test_process_weibull_returns_valid_output_10m():
    # Generate synthetic data resembling Weibull distribution
    np.random.seed(42)
    wind_10m = np.random.weibull(a=2, size=1000) * 5
    df = pd.DataFrame({
        'wind_speed_10m': wind_10m,
        'wind_speed_100m': wind_10m * 1.1  # just to fill the column
    })

    c, k, pdf = process_weibull(df, coord="TestLoc", height=10)

    assert isinstance(c, float)
    assert isinstance(k, float)
    assert isinstance(pdf, np.ndarray)
    assert len(pdf) == 100
    assert np.all(pdf >= 0)


def test_process_weibull_returns_valid_output_100m():
    np.random.seed(0)
    wind_100m = np.random.weibull(a=2.2, size=1000) * 6
    df = pd.DataFrame({
        'wind_speed_10m': wind_100m * 0.9,
        'wind_speed_100m': wind_100m
    })

    c, k, pdf = process_weibull(df, coord="TestLoc", height=100)

    assert isinstance(c, float)
    assert isinstance(k, float)
    assert isinstance(pdf, np.ndarray)
    assert len(pdf) == 100


def test_invalid_height_raises_error():
    df = pd.DataFrame({
        'wind_speed_10m': np.random.rand(100),
        'wind_speed_100m': np.random.rand(100)
    })

    with pytest.raises(ValueError, match="Height must be either 10 or 100 meters."):
        process_weibull(df, coord="TestLoc", height=50)

# import pytest
# import sys
# import numpy as np
# import pandas as pd
# from pathlib import Path
# sys.path.append(str(Path(__file__).parent.parent / "src"))
# from assessment.Weibull import process_weibull  


# def generate_weibull_data(c, k, size=1000):
#     return c * np.random.weibull(k, size)

# def test_process_weibull_correct_output(mock_savefig, mock_show):
#     c_true, k_true = 8, 2  # Known Weibull parameters
#     wind_speed_data = generate_weibull_data(c_true, k_true)
#     df = pd.DataFrame({
#         'wind_speed_10m': wind_speed_data,
#         'wind_speed_100m': wind_speed_data + 1  # Slightly offset for 100m
#     })

#     # When
#     c_fit, k_fit, pdf_range = process_weibull(df, coord=(0, 0), height=10)

#     # Then
#     assert isinstance(c_fit, float)
#     assert isinstance(k_fit, float)
#     assert len(pdf_range) == 100
#     assert np.isclose(c_fit, c_true, rtol=0.2)  # Fit within 20%
#     assert np.isclose(k_fit, k_true, rtol=0.2)

# def test_process_weibull_invalid_height(mock_savefig, mock_show):
#     df = pd.DataFrame({
#         'wind_speed_10m': np.random.rand(100),
#         'wind_speed_100m': np.random.rand(100)
#     })

#     with pytest.raises(ValueError, match="Height must be either 10 or 100 meters."):
#         process_weibull(df, coord=(0, 0), height=50)

# def test_process_weibull_nan_handling(mock_savefig, mock_show):
#     df = pd.DataFrame({
#         'wind_speed_10m': [5, 6, np.nan, 7, 8],
#         'wind_speed_100m': [6, np.nan, 8, 9, 10]
#     })

#     c, k, pdf = process_weibull(df, coord=(1, 2), height=10)

#     assert isinstance(c, float)
#     assert isinstance(k, float)
#     assert isinstance(pdf, np.ndarray)
#     assert len(pdf) == 100

