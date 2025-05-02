import pytest
import sys
import numpy as np
import pandas as pd
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "output"))
THIS_FILE = Path('main.py').parent  # current script directory or use __file__
outputs_dir = THIS_FILE.parent / 'outputs'  # inputs folder is at the same level as src
test_int_ws = outputs_dir / 'windspeed_interpolated_results.csv'

def test_intep():
    test_int_ws_read = pd.read_csv(test_int_ws)
    val = test_int_ws_read.iloc[0,1]
    
    assert np.isclose(val, 5.16, atol=0.5)