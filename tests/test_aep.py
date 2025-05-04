import numpy as np
import sys
import importlib.util

from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent.parent / "examples"))

from assessment.read_input import read_resource_calc_wref
from assessment.aep import power_range

# Path to examples/main.py
main_path = Path(__file__).parent.parent / "examples" / "main.py"

spec = importlib.util.spec_from_file_location("main", main_path)
main = importlib.util.module_from_spec(spec)
sys.modules["main"] = main
spec.loader.exec_module(main)

turb = main.turb_nr
t_start = main.time_start
t_end = main.time_end
wind = main.data_ref_wind_df
turbine_df = main.turbine
height = main.height


def test_power_range():
    df, df_long = read_resource_calc_wref('1997-1999.nc')
    min_ws, max_ws, power_length, filtered = power_range(wind, height, turbine_df, t_start, t_end)
    if turb == 15:
        len = 22
    elif turb == 5:
        len = 50
    else:
        raise ValueError("Turbine must be either 5 or 15 meters.")
    assert np.isclose(power_length, len, atol=1)