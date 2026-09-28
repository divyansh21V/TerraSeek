"""FastAPI route definitions for TerraSeek.

Thin wrappers around services — no business logic here.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from terraseek.models import (
    DecisionRequest,
    DecisionResponse,
    InvestigationRequest,
    InvestigationResponse,
    ExportPackage,
)
from terraseek.services import (
    export_investigation,
    get_candidate_detail,
    record_decision,
    run_investigation,
)
from terraseek.demo_data import get_available_aois

router = APIRouter()


@router.get("/health")
def health():
    """System health check."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "data_source": "local_prototype",
        "mode": "demo_fixture",
        "capabilities": ["investigate", "evidence_channels", "analyst_decisions", "json_export"],
    }


@router.get("/aois")
def list_aois():
    """List available areas of interest for the prototype."""
    return get_available_aois()


@router.post("/investigate", response_model=InvestigationResponse)
def investigate(request: InvestigationRequest):
    """Submit an investigation query and receive ranked candidates."""
    if request.date_start > request.date_end:
        raise HTTPException(
            status_code=422,
            detail="date_start must be before date_end",
        )
    return run_investigation(request)


@router.get("/candidates/{candidate_id}")
def get_candidate(
    candidate_id: str,
    investigation_id: str = Query(default=None),
):
    """Retrieve full evidence detail for a specific candidate."""
    detail = get_candidate_detail(candidate_id, investigation_id)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Candidate '{candidate_id}' not found")
    return detail


@router.post("/decisions", response_model=DecisionResponse)
def submit_decision(request: DecisionRequest):
    """Record an analyst decision for a candidate."""
    # Validate candidate exists
    detail = get_candidate_detail(request.candidate_id)
    if detail is None:
        raise HTTPException(
            status_code=404,
            detail=f"Candidate '{request.candidate_id}' not found",
        )
    try:
        return record_decision(request)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/export/{investigation_id}")
def export(investigation_id: str):
    """Export a complete investigation evidence package as JSON."""
    package = export_investigation(investigation_id)
    if package is None:
        raise HTTPException(
            status_code=404,
            detail=f"Investigation '{investigation_id}' not found",
        )
    return package
