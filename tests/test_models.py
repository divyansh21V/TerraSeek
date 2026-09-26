"""Unit tests for TerraSeek Pydantic models."""

from datetime import date
import pytest
from pydantic import ValidationError

from terraseek.models import AnalystDecision, DecisionRequest, InvestigationRequest


def test_investigation_request_valid():
    req = InvestigationRequest(
        query="Detect construction near Neom",
        aoi_name="Neom/OXAGON",
        aoi_bbox=[28.0, 35.0, 28.5, 35.5],
        date_start=date(2023, 1, 1),
        date_end=date(2024, 1, 1),
    )
    assert req.query == "Detect construction near Neom"
    assert req.aoi_bbox == [28.0, 35.0, 28.5, 35.5]


def test_investigation_request_invalid_bbox():
    with pytest.raises(ValidationError):
        InvestigationRequest(
            query="Short query",
            aoi_name="Test",
            aoi_bbox=[28.0, 35.0],  # Must have 4 floats
            date_start=date(2023, 1, 1),
            date_end=date(2024, 1, 1),
        )


def test_decision_request_valid():
    req = DecisionRequest(
        investigation_id="inv-123",
        candidate_id="cand-001",
        decision=AnalystDecision.CONFIRMED,
        notes="High confidence site alteration observed.",
    )
    assert req.decision == AnalystDecision.CONFIRMED
    assert req.notes == "High confidence site alteration observed."
