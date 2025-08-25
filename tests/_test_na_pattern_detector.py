import os
import pytest
import pandas as pd
from pattern_detector import CupHandleDetector
from config import PREPROCESSED_FILE, PATTERNS_DIR

@pytest.fixture(scope="module", autouse=True)
def ensure_preprocessed_exists():
    """
    Ensure preprocessed CSV exists before tests.
    """
    if not os.path.exists(PREPROCESSED_FILE):
        raise FileNotFoundError(f"{PREPROCESSED_FILE} not found. Run main.py first.")

def test_preprocessed_file_exists():
    """Check that preprocessed CSV is present"""
    assert os.path.exists(PREPROCESSED_FILE), "Preprocessed CSV not found"

def test_patterns_folder_has_images():
    """Ensure at least some pattern images exist"""
    images = os.listdir(PATTERNS_DIR)
    assert len(images) > 0, "No pattern images found in patterns folder"

def test_detector_finds_patterns():
    """Basic sanity check: detector runs without errors"""
    df = pd.read_csv(PREPROCESSED_FILE)
    if df.empty:
        pytest.skip("Preprocessed CSV is empty; skipping pattern detection test")

    symbol = df['symbol'].iloc[0]
    symbol_df = df[df['symbol'] == symbol].copy()
    detector = CupHandleDetector(symbol_df, symbol)
    results = detector.find_patterns(max_images=5)
    
    assert isinstance(results, list), "Detector did not return a list"
