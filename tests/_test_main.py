import os
import pandas as pd
from main import main
from pattern_detector import CupHandleDetector
from plot_utils import save_pattern_plot

# Test folders and files
PATTERNS_DIR = "patterns"
REPORT_FILE = "report.csv"
PREPROCESSED_FILE = "data/preprocessed_data.csv"

def setup_module(module):
    """Setup test environment: clear previous test outputs."""
    os.makedirs(PATTERNS_DIR, exist_ok=True)

    # Delete old PNGs
    for f in os.listdir(PATTERNS_DIR):
        if f.endswith(".png"):
            os.remove(os.path.join(PATTERNS_DIR, f))

    # Delete report and preprocessed_data if exists
    if os.path.exists(REPORT_FILE):
        os.remove(REPORT_FILE)
    if os.path.exists(PREPROCESSED_FILE):
        os.remove(PREPROCESSED_FILE)


def test_cup_handle_detector():
    """Test CupHandleDetector with synthetic small dataset."""
    # Generate tiny synthetic dataset
    df = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=60, freq="T"),
        "open": range(100, 160),
        "high": range(101, 161),
        "low": range(99, 159),
        "close": range(100, 160),
        "volume": [10]*60,
        "symbol": ["BTCUSDT"]*60
    })

    detector = CupHandleDetector(df, "BTCUSDT")
    patterns = detector.find_patterns(max_images=2)

    assert isinstance(patterns, list)
    assert all("cup_start" in p and "handle_end" in p for p in patterns)


def test_main_runs():
    """Test main.py end-to-end with synthetic preprocessed data."""
    # Save synthetic preprocessed_data.csv
    df = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=100, freq="T"),
        "open": range(100, 200),
        "high": range(101, 201),
        "low": range(99, 199),
        "close": range(100, 200),
        "volume": [10]*100,
        "symbol": ["BTCUSDT"]*50 + ["ETHUSDT"]*50
    })
    df.to_csv(PREPROCESSED_FILE, index=False)

    # Run main
    main()

    # Check report.csv created
    assert os.path.exists(REPORT_FILE)
    report_df = pd.read_csv(REPORT_FILE)
    assert not report_df.empty

    # Check patterns folder PNG files
    png_files = [f for f in os.listdir(PATTERNS_DIR) if f.endswith(".png")]
    assert len(png_files) > 0
    # IDs should start from 0 and be contiguous
    ids = sorted(int(f.split("_")[-1].split(".")[0]) for f in png_files)
    assert ids[0] == 0


def teardown_module(module):
    """Clean up after tests."""
    if os.path.exists(REPORT_FILE):
        os.remove(REPORT_FILE)
    for f in os.listdir(PATTERNS_DIR):
        if f.endswith(".png"):
            os.remove(os.path.join(PATTERNS_DIR, f))
    if os.path.exists(PREPROCESSED_FILE):
        os.remove(PREPROCESSED_FILE)
