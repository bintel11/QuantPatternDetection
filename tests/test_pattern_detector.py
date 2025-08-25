# tests/test_pattern_detector.py

#10 passed
import pytest
import pandas as pd
from unittest.mock import patch
from pattern_detector import CupHandleDetector


# -----------------------
# Fixture: Load real data
# -----------------------
@pytest.fixture
def raw_detector():
    df = pd.read_csv("data/raw_data.csv")
    return CupHandleDetector(df)


# -----------------------
# 1. Valid Cup & Handle Pattern
# -----------------------
def test_valid_pattern(raw_detector):
    with patch.object(CupHandleDetector, "_validate_cup_handle",
                      return_value=(True, "", 0.95, 10, 3)):
        patterns = raw_detector.find_patterns(max_images=1)
        assert patterns[0]["valid"] is True
        assert patterns[0]["r2"] >= 0.85


# -----------------------
# 2. Shallow Cup Rejected
# -----------------------
def test_shallow_cup(raw_detector):
    with patch.object(CupHandleDetector, "_validate_cup_handle",
                      return_value=(False, "Cup depth too shallow", None, 1, None)):
        patterns = raw_detector.find_patterns(max_images=1)
        assert patterns[0]["valid"] is False
        assert "Cup depth too shallow" in patterns[0]["invalid_reason"]


# -----------------------
# 3. Deep Handle Rejected
# -----------------------
def test_deep_handle(raw_detector):
    with patch.object(CupHandleDetector, "_validate_cup_handle",
                      return_value=(False, "Handle retrace too deep", None, 10, 6)):
        patterns = raw_detector.find_patterns(max_images=1)
        assert patterns[0]["valid"] is False
        assert "Handle retrace too deep" in patterns[0]["invalid_reason"]


# -----------------------
# 4. Weak Breakout Rejected
# -----------------------
def test_low_breakout(raw_detector):
    with patch.object(CupHandleDetector, "_validate_cup_handle",
                      return_value=(False, "Breakout not strong enough (ATR filter)", 0.9, 10, 3)):
        patterns = raw_detector.find_patterns(max_images=1)
        assert patterns[0]["valid"] is False
        assert "Breakout not strong enough" in patterns[0]["invalid_reason"]


# -----------------------
# 5. R² Too Low Rejected
# -----------------------
def test_r2_too_low(raw_detector):
    with patch.object(CupHandleDetector, "_validate_cup_handle",
                      return_value=(False, "Cup not parabolic enough (R² too low)", 0.6, 12, 4)):
        patterns = raw_detector.find_patterns(max_images=1)
        assert patterns[0]["valid"] is False
        assert patterns[0]["r2"] == 0.6



# -----------------------
# 6. Exception Handling --FAil as find_patterns implementation does NOT raise exceptions
# -----------------------
def test_validate_cup_handle_exception(raw_detector):
    with patch.object(CupHandleDetector, "_validate_cup_handle",
                      side_effect=Exception("forced exception")):
        patterns = raw_detector.find_patterns(max_images=1)
        assert patterns[0]["valid"] is False
        assert "forced exception" in patterns[0]["invalid_reason"]


# -----------------------
# 6. Exception Handling
# -----------------------
# def test_validate_cup_handle_exception(raw_detector):
#     with patch.object(CupHandleDetector, "_validate_cup_handle",
#                       side_effect=Exception("forced exception")):
#         # Expect the exception to propagate
#         with pytest.raises(Exception, match="forced exception"):
#             raw_detector.find_patterns(max_images=1)


# -----------------------
# 7. Edge Case: Too Short Data
# -----------------------
def test_edge_case_short_data():
    df = pd.DataFrame({"close": [1, 2, 3], "high": [3, 3, 3], "low": [1, 1, 1], "volume": [100, 100, 100]})
    detector = CupHandleDetector(df)
    patterns = detector.find_patterns()
    assert patterns == []


# -----------------------
# 8. Integration Test
# -----------------------
def test_integration_patterns_run(raw_detector):
    # Don’t mock – run on real data
    patterns = raw_detector.find_patterns(max_images=3)
    assert isinstance(patterns, list)
    assert all("valid" in p for p in patterns)


# -----------------------
# 9. Max Images Limit
# -----------------------
def test_find_patterns_max_images(raw_detector):
    with patch.object(CupHandleDetector, "_validate_cup_handle",
                      return_value=(True, "", 0.9, 15, 5)):
        patterns = raw_detector.find_patterns(max_images=2)
        assert len(patterns) <= 2


# -----------------------
# 10. Extra R² Test
# -----------------------
def test_r2_too_low_extra(raw_detector):
    with patch.object(CupHandleDetector, "_validate_cup_handle",
                      return_value=(False, "Cup not parabolic enough (R² too low)", 0.7, 9, 3)):
        patterns = raw_detector.find_patterns(max_images=1)
        assert patterns[0]["valid"] is False
        assert patterns[0]["r2"] == 0.7


# -----------------------
# 11. Extra Breakout Test
# -----------------------
def test_breakout_too_low_extra(raw_detector):
    with patch.object(CupHandleDetector, "_validate_cup_handle",
                      return_value=(False, "No breakout above handle high", 0.88, 11, 4)):
        patterns = raw_detector.find_patterns(max_images=1)
        assert patterns[0]["valid"] is False
        assert "No breakout" in patterns[0]["invalid_reason"]


# -----------------------
# 12. Extra Exception Test --FAil as find_patterns implementation does NOT raise exceptions
# -----------------------
def test_validate_cup_handle_exception_extra(raw_detector):
    with patch.object(CupHandleDetector, "_validate_cup_handle",
                      side_effect=Exception("extra exception")):
        patterns = raw_detector.find_patterns(max_images=1)
        assert patterns[0]["valid"] is False
        assert "extra exception" in patterns[0]["invalid_reason"]

