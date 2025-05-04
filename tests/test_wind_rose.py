import sys
import pytest
import pandas as pd
from pathlib import Path

# Ensure we can import the source code by adding the src directory to the path
sys.path.append(str(Path(__file__).parent.parent / "src"))
from assessment.wind_rose import plot_wind_rose
# Mock data to simulate CSV input
@pytest.fixture
def mock_wind_data():
    # Create mock wind speed and direction data
    wind_speed_data = {
        'wind_speed_10m': [5, 7, 10, 12],
        'wind_speed_100m': [4, 6, 9, 11]
    }
    wind_direction_data = {
        'wind_direction_10m': [0, 45, 90, 135],
        'wind_direction_100m': [0, 90, 180, 270]
    }

    # Convert the data into DataFrame objects
    df_wind_speed = pd.DataFrame(wind_speed_data)
    df_wind_direction = pd.DataFrame(wind_direction_data)
    
    return df_wind_speed, df_wind_direction

def test_plot_wind_rose(mock_wind_data):
    # Unpack the mock data
    df_wind_speed, df_wind_direction = mock_wind_data
    
    # Call the plot_wind_rose function to generate plots
    plot_wind_rose(df_wind_speed, df_wind_direction)
    
    # Define the output directory and expected files
    output_dir = Path(__file__).parent.parent / "outputs"
    file_10m = output_dir / "wind_rose_10m.png"
    file_100m = output_dir / "wind_rose_100m.png"
    
    # Check that the output files were created
    assert file_10m.exists(), f"Expected file {file_10m} does not exist"
    assert file_100m.exists(), f"Expected file {file_100m} does not exist"
