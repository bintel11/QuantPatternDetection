import os
import pytest
import pandas as pd
from plot_utils import save_pattern_plot
from config import PATTERNS_DIR, PREPROCESSED_FILE

@pytest.fixture(scope="module")
def sample_pattern_df():
    """Load a small sample from preprocessed CSV"""
    if not os.path.exists(PREPROCESSED_FILE):
        raise FileNotFoundError(f"{PREPROCESSED_FILE} not found. Run main.py first.")
    
    df = pd.read_csv(PREPROCESSED_FILE)
    # Use first 10 rows as dummy pattern
    return df.head(10)

def test_plot_creates_file(tmp_path, sample_pattern_df):
    """Check that pattern plot is saved"""
    dummy_pattern = {
        'df': sample_pattern_df,
        'cup_start': 0,
        'cup_end': 5,
        'handle_start': 5,
        'handle_end': 9
    }

    file_name = os.path.join(tmp_path, "dummy_plot.png")
    save_pattern_plot(dummy_pattern, "BTCUSDT", file_name)

    assert os.path.exists(file_name), "Plot file was not created"
