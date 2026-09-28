"""FastAPI route definitions for TerraSeek.

Thin wrappers around services — no business logic here.
"""

from __future__ import annotations

import os

from fastapi import APIRouter, Depends, Header, HTTPException, Query

from terraseek.demo_data import get_available_aois
from terraseek.jobs import get as get_job
from terraseek.jobs import submit as submit_job
from terraseek.models import (
    DecisionRequest,
    DecisionResponse,
    InvestigationRequest,
    InvestigationResponse,
    JobResponse,
    STACSearchRequest,
    STACSearchResponse,
)
from terraseek.providers import EarthSearchProvider, ProviderError
from terraseek.services import (
    export_investigation,
    get_candidate_detail,
    record_decision,
    run_investigation,
)

router = APIRouter()


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Enable simple deployment auth without making offline demo mode painful."""
    expected = os.getenv("TERRASEEK_API_KEY")
    if expected and x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


@router.get("/health")
def health():
    """System health check."""
    return {
        "status": "healthy",
        "version": "0.2.0",
        "data_source": "local_prototype",
        "mode": "demo_fixture",
        "capabilities": ["investigate", "evidence_channels", "analyst_decisions", "json_export"],
    }


@router.get("/aois")
def list_aois():
    """List available areas of interest for the prototype."""
    return get_available_aois()


@router.post(
    "/investigate",
    response_model=InvestigationResponse,
    dependencies=[Depends(require_api_key)],
)
def investigate(request: InvestigationRequest):
    """Submit an investigation query and receive ranked candidates."""
    return run_investigation(request)


@router.post(
    "/jobs/investigate",
    response_model=JobResponse,
    dependencies=[Depends(require_api_key)],
)
def investigate_async(request: InvestigationRequest):
    """Queue an investigation when the UI should remain responsive."""
    job_id = submit_job(lambda: run_investigation(request).model_dump(mode="json"))
    return JobResponse(id=job_id, status="queued")


@router.get("/jobs/{job_id}", response_model=JobResponse)
def job_status(job_id: str):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found")
    return JobResponse(**job)


@router.post(
    "/catalog/search",
    response_model=STACSearchResponse,
    dependencies=[Depends(require_api_key)],
)
def catalog_search(request: STACSearchRequest):
    """Search a live STAC provider using the standard Item Search contract."""
    try:
        return EarthSearchProvider().search(request)
    except ProviderError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


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


@router.post(
    "/decisions",
    response_model=DecisionResponse,
    dependencies=[Depends(require_api_key)],
)
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
