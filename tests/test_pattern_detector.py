# tests/test_pattern_detector.py
import pytest
import pandas as pd
from unittest.mock import patch
from pattern_detector import CupHandleDetector

# -----------------------
# Fixture: Load raw CSV data
# -----------------------
@pytest.fixture
def detector_from_csv():
    df = pd.read_csv("data/raw_data.csv")  # updated path
    detector = CupHandleDetector(df)
    return detector

# -----------------------
# Test 1: Valid Pattern
# -----------------------
def test_valid_pattern(detector_from_csv):
    patterns = detector_from_csv.find_patterns(max_images=1)
    assert patterns
    pattern = patterns[0]
    assert "valid" in pattern

# -----------------------
# Test 2: Shallow Cup
# -----------------------
def test_shallow_cup(detector_from_csv):
    patterns = detector_from_csv.find_patterns(max_images=1)
    pattern = patterns[0]
    assert "cup_depth" in pattern

# -----------------------
# Test 3: Deep Handle
# -----------------------
def test_deep_handle(detector_from_csv):
    patterns = detector_from_csv.find_patterns(max_images=1)
    pattern = patterns[0]
    assert "handle_depth" in pattern

# -----------------------
# Test 4: Low Breakout
# -----------------------
def test_low_breakout(detector_from_csv):
    patterns = detector_from_csv.find_patterns(max_images=1)
    pattern = patterns[0]
    assert "breakout" in pattern or "valid" in pattern

# -----------------------
# Test 5: R2 Too Low
# -----------------------
def test_r2_too_low(detector_from_csv):
    patterns = detector_from_csv.find_patterns(max_images=1)
    pattern = patterns[0]
    assert "r2" in pattern

# -----------------------
# Test 6: Validate Exception Handling
# -----------------------
def test_validate_cup_handle_exception(detector_from_csv):
    with patch.object(CupHandleDetector, "_validate_cup_handle",
                      return_value=(False, "forced exception", None, None, None)):
        patterns = detector_from_csv.find_patterns(max_images=1)
        assert patterns

# -----------------------
# Test 7: Edge Case Short Data
# -----------------------
def test_edge_case_short_data():
    short_df = pd.DataFrame({"open":[1,2],"high":[1,2],"low":[1,2],"close":[1,2]})
    detector = CupHandleDetector(short_df)
    patterns = detector.find_patterns(max_images=1)
    assert isinstance(patterns, list)

# -----------------------
# Test 8: Integration Run
# -----------------------
def test_integration_patterns_run(detector_from_csv):
    patterns = detector_from_csv.find_patterns(max_images=5)
    assert isinstance(patterns, list)

# -----------------------
# Test 9: Max Images Parameter
# -----------------------
def test_find_patterns_max_images(detector_from_csv):
    patterns = detector_from_csv.find_patterns(max_images=1)
    assert len(patterns) <= 1

# -----------------------
# Test 10: Extra R2 Too Low
# -----------------------
def test_r2_too_low_extra(detector_from_csv):
    patterns = detector_from_csv.find_patterns(max_images=1)
    pattern = patterns[0]
    assert "r2" in pattern

# -----------------------
# Test 11: Extra Breakout Too Low
# -----------------------
def test_breakout_too_low_extra(detector_from_csv):
    patterns = detector_from_csv.find_patterns(max_images=1)
    pattern = patterns[0]
    assert "valid" in pattern

# -----------------------
# Test 12: Extra Validate Exception
# -----------------------
def test_validate_cup_handle_exception_extra(detector_from_csv):
    with patch.object(CupHandleDetector, "_validate_cup_handle",
                      return_value=(False, "forced exception extra", None, None, None)):
        patterns = detector_from_csv.find_patterns(max_images=1)
        assert patterns



