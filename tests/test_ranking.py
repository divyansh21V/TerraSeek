"""Unit tests for TerraSeek ranking logic."""

from terraseek.ranking import (
    compute_query_relevance,
    compute_ranking_score,
    priority_label,
)


def test_compute_query_relevance_exact_match():
    query = "solar farm construction"
    keywords = ["solar", "farm", "construction"]
    score = compute_query_relevance(query, keywords)
    assert score > 0.5


def test_compute_query_relevance_empty_query():
    query = "the in at"  # Only stop words
    keywords = ["solar", "farm"]
    score = compute_query_relevance(query, keywords)
    assert score == 0.5


def test_compute_ranking_score_calculation():
    signals = {
        "query_relevance": 0.8,
        "visual_change_strength": 0.9,
        "temporal_persistence": 0.7,
        "data_suitability": 0.8,
        "contextual_relevance": 0.6,
        "confounder_risk": 0.2,  # inverted: 1 - 0.2 = 0.8
    }
    score = compute_ranking_score(signals)
    assert 0.0 <= score <= 1.0
    assert score >= 0.7


def test_priority_labels():
    assert priority_label(0.85) == "HIGH"
    assert priority_label(0.60) == "MODERATE"
    assert priority_label(0.40) == "LOW"
    assert priority_label(0.15) == "MINIMAL"
