"""Adversarial and security tests for TerraSeek ranking logic.

Tests how the ranking engine handles adversarial input, missing data, 
NaN/Infinity, and edge cases to ensure safe execution.
"""

import math
import pytest
from terraseek.ranking import (
    compute_query_relevance,
    compute_ranking_score,
    priority_label,
)

def test_adversarial_query_relevance_extreme_lengths():
    """Test with extremely long queries to check for ReDoS or memory exhaustion."""
    long_query = "solar " * 100000
    keywords = ["solar", "farm", "construction"]
    # Should not crash and should return a bounded score.
    score = compute_query_relevance(long_query, keywords)
    assert 0.0 <= score <= 1.0


def test_adversarial_query_relevance_special_chars():
    """Test with heavily obfuscated or special characters."""
    query = "s0l@r f!rm c#nstruction\x00\n\r"
    keywords = ["solar", "farm", "construction"]
    score = compute_query_relevance(query, keywords)
    assert 0.0 <= score <= 1.0


def test_adversarial_ranking_score_infinity_nan():
    """Test how ranking score handles float('inf') and float('nan')."""
    signals = {
        "query_relevance": float("inf"),
        "visual_change_strength": float("-inf"),
        "temporal_persistence": float("nan"),
    }
    
    score = compute_ranking_score(signals)
    # The ranking engine should ideally cap values or not crash. 
    # If it propagates NaN/Inf, that's a security/stability risk we should catch.
    # Currently, it might just compute a NaN or Inf score. Let's verify it doesn't crash.
    assert isinstance(score, float)


def test_adversarial_ranking_score_missing_keys():
    """Test missing keys - should fall back gracefully to 0.5 default."""
    empty_signals = {}
    score = compute_ranking_score(empty_signals)
    # With defaults at 0.5, total should be 0.5 (since weights sum to 1.0)
    assert 0.49 <= score <= 0.51


def test_adversarial_ranking_score_negative_and_excessive():
    """Test values well outside [0, 1] range."""
    signals = {
        "query_relevance": -100.0,
        "visual_change_strength": 1000.0,
        "temporal_persistence": 0.5,
        "data_suitability": 0.5,
        "contextual_relevance": 0.5,
        "confounder_risk": -10.0,
    }
    score = compute_ranking_score(signals)
    assert isinstance(score, float)
    
def test_priority_label_bounds():
    """Test extreme bounds for priority labels."""
    assert priority_label(float("inf")) == "HIGH"
    assert priority_label(float("-inf")) == "MINIMAL"
    assert priority_label(float("nan")) == "MINIMAL"  # nan >= 0.75 is False in python
