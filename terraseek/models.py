"""Pydantic models for TerraSeek API."""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# --- Enumerations ---

class AnalystDecision(str, Enum):
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"
    DEFERRED = "DEFERRED"
    NEEDS_MORE_IMAGERY = "NEEDS_MORE_IMAGERY"


class SignalStrength(str, Enum):
    STRONG = "STRONG"
    MODERATE = "MODERATE"
    WEAK = "WEAK"
    NONE = "NONE"


class CheckStatus(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"


class TimelineSignal(str, Enum):
    UNCHANGED = "UNCHANGED"
    WEAK_SIGNAL = "WEAK_SIGNAL"
    STRONG_SIGNAL = "STRONG_SIGNAL"
    PERSISTENT = "PERSISTENT"
    NO_DATA = "NO_DATA"


# --- Request / Response models ---

class InvestigationRequest(BaseModel):
    query: str = Field(..., min_length=5, description="Investigation query in natural language")
    aoi_name: str = Field(..., description="Named area of interest")
    aoi_bbox: list[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        description="Bounding box [south, west, north, east]",
    )
    date_start: date
    date_end: date


class EvidenceItem(BaseModel):
    label: str
    value: str
    signal_strength: SignalStrength


class QualityCheck(BaseModel):
    check_name: str
    status: CheckStatus
    detail: str


class TimelineEntry(BaseModel):
    date: str
    observation: str
    signal: TimelineSignal
    source: str


class PrioritySignals(BaseModel):
    query_relevance: float = Field(ge=0.0, le=1.0)
    visual_change_strength: float = Field(ge=0.0, le=1.0)
    temporal_persistence: float = Field(ge=0.0, le=1.0)
    data_suitability: float = Field(ge=0.0, le=1.0)
    contextual_relevance: float = Field(ge=0.0, le=1.0)
    confounder_risk: float = Field(ge=0.0, le=1.0, description="0=low risk, 1=high risk")


class EvidenceChannel(BaseModel):
    """One inspectable evidence dimension behind a candidate result."""

    score: float = Field(ge=0.0, le=1.0)
    status: str
    rationale: str


class CandidateSummary(BaseModel):
    id: str
    location_name: str
    latitude: float
    longitude: float
    investigation_priority: str
    ranking_score: float
    summary: str
    before_date: str
    after_date: str
    primary_evidence: str


class CandidateDetail(BaseModel):
    id: str
    investigation_id: str
    location_name: str
    latitude: float
    longitude: float

    investigation_priority: str
    ranking_score: float
    priority_signals: PrioritySignals
    evidence_channels: dict[str, EvidenceChannel]

    before_image_url: str
    before_date: str
    before_source: str
    after_image_url: str
    after_date: str
    after_source: str

    observed: list[EvidenceItem]
    inferred: list[EvidenceItem]
    limitations: list[str]

    timeline: list[TimelineEntry]
    quality_checks: list[QualityCheck]
    contextual_evidence: list[EvidenceItem]
    warnings: list[str]

    analyst_decision: Optional[str] = None
    analyst_notes: Optional[str] = None


class InvestigationResponse(BaseModel):
    investigation_id: str
    query: str
    aoi_name: str
    date_range: str
    candidate_count: int
    candidates: list[CandidateSummary]


class DecisionRequest(BaseModel):
    investigation_id: str
    candidate_id: str
    decision: AnalystDecision
    notes: Optional[str] = None


class DecisionResponse(BaseModel):
    status: str
    investigation_id: str
    candidate_id: str
    decision: str
    recorded_at: str


class ExportPackage(BaseModel):
    export_version: str = "0.2.0"
    exported_at: str
    investigation_id: str
    query: str
    aoi_name: str
    aoi_bbox: list[float]
    date_range: str
    candidates: list[CandidateDetail]
    decisions: dict[str, dict]
    system_info: dict
