"""Unit tests for TerraSeek services."""

from datetime import date

from terraseek.models import AnalystDecision, DecisionRequest, InvestigationRequest
from terraseek.services import (
    _bbox_overlaps,
    _date_ranges_overlap,
    export_investigation,
    get_candidate_detail,
    record_decision,
    run_investigation,
)


def test_bbox_overlaps():
    box_a = [28.0, 35.0, 28.5, 35.5]
    box_b = [28.2, 35.2, 28.8, 35.8]
    box_c = [30.0, 40.0, 31.0, 41.0]

    assert _bbox_overlaps(box_a, box_b) is True
    assert _bbox_overlaps(box_a, box_c) is False


def test_date_ranges_overlap():
    start_a = date(2023, 1, 1)
    end_a = date(2024, 1, 1)

    assert _date_ranges_overlap(start_a, end_a, "2023-06-01", "2023-12-01") is True
    assert _date_ranges_overlap(start_a, end_a, "2021-01-01", "2022-01-01") is False


def test_run_investigation_and_candidate_flow():
    req = InvestigationRequest(
        query="Find newly built structures and urban expansion",
        aoi_name="Egypt — Greater Cairo & New Administrative Capital",
        aoi_bbox=[29.5, 31.0, 30.5, 32.5],
        date_start=date(2015, 1, 1),
        date_end=date(2024, 1, 1),
    )

    resp = run_investigation(req)
    assert resp.investigation_id.startswith("inv-")
    assert resp.candidate_count > 0
    first_candidate = resp.candidates[0]

    # Retrieve candidate detail
    detail = get_candidate_detail(first_candidate.id, resp.investigation_id)
    assert detail is not None
    assert detail.id == first_candidate.id
    assert len(detail.quality_checks) > 0

    # Record decision
    dec_req = DecisionRequest(
        investigation_id=resp.investigation_id,
        candidate_id=first_candidate.id,
        decision=AnalystDecision.CONFIRMED,
        notes="Verified solar array persistent expansion.",
    )
    dec_resp = record_decision(dec_req)
    assert dec_resp.status == "recorded"
    assert dec_resp.decision == "CONFIRMED"

    # Export investigation
    export_pkg = export_investigation(resp.investigation_id)
    assert export_pkg is not None
    assert export_pkg.investigation_id == resp.investigation_id
    assert first_candidate.id in export_pkg.decisions
    assert export_pkg.decisions[first_candidate.id]["decision"] == "CONFIRMED"
    assert set(detail.evidence_channels) == {
        "spectral_signal",
        "semantic_match",
        "temporal_persistence",
        "spatial_context",
        "quality_assurance",
        "confounder_risk",
    }


def test_decision_cannot_cross_investigations():
    req = InvestigationRequest(
        query="Find construction expansion near the city",
        aoi_name="Egypt — Greater Cairo & New Administrative Capital",
        aoi_bbox=[29.5, 31.0, 30.5, 32.5],
        date_start=date(2015, 1, 1),
        date_end=date(2024, 1, 1),
    )
    first = run_investigation(req)
    second = run_investigation(
        InvestigationRequest(
            query="Find deforestation near the river",
            aoi_name="Amazon Basin — Altamira Region",
            aoi_bbox=[-4.0, -53.0, -2.5, -51.0],
            date_start=date(2015, 1, 1),
            date_end=date(2024, 1, 1),
        )
    )

    from pytest import raises

    with raises(ValueError, match="not part of investigation"):
        record_decision(
            DecisionRequest(
                investigation_id=second.investigation_id,
                candidate_id=first.candidates[0].id,
                decision=AnalystDecision.REJECTED,
            )
        )
