"""Pydantic models for TerraSeek API."""

from __future__ import annotations

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, model_validator

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
    query: str = Field(..., min_length=5, max_length=500, description="Investigation query in natural language")
    aoi_name: str = Field(..., min_length=2, max_length=160, description="Named area of interest")
    aoi_bbox: list[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        description="Bounding box [south, west, north, east]",
    )
    date_start: date
    date_end: date

    @model_validator(mode="after")
    def validate_investigation_bounds(self) -> InvestigationRequest:
        """Reject malformed AOIs before they reach providers or ranking."""
        south, west, north, east = self.aoi_bbox
        if not (-90 <= south < north <= 90):
            raise ValueError("aoi_bbox must use [south, west, north, east] latitude order")
        if not (-180 <= west < east <= 180):
            raise ValueError("aoi_bbox must use increasing longitude values")
        if self.date_start > self.date_end:
            raise ValueError("date_start must be before date_end")
        if (self.date_end - self.date_start).days > 3653:
            raise ValueError("date range cannot exceed 10 years")
        return self


class STACSearchRequest(BaseModel):
    """Provider-neutral STAC Item Search request."""

    bbox: list[float] = Field(..., min_length=4, max_length=4)
    date_start: date
    date_end: date
    collections: list[str] = Field(default_factory=lambda: ["sentinel-2-l2a"])
    max_cloud_cover: float | None = Field(default=20.0, ge=0.0, le=100.0)
    limit: int = Field(default=25, ge=1, le=100)

    @model_validator(mode="after")
    def validate_search_bounds(self) -> STACSearchRequest:
        west, south, east, north = self.bbox
        if not (-180 <= west < east <= 180 and -90 <= south < north <= 90):
            raise ValueError("bbox must be [west, south, east, north]")
        if self.date_start > self.date_end:
            raise ValueError("date_start must be before date_end")
        if (self.date_end - self.date_start).days > 3653:
            raise ValueError("date range cannot exceed 10 years")
        return self


class STACSearchResponse(BaseModel):
    provider: str
    catalog_url: str
    matched: int
    items: list[dict]


class JobResponse(BaseModel):
    id: str
    status: str
    result: dict | None = None
    error: str | None = None


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

    analyst_decision: str | None = None
    analyst_notes: str | None = None


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
    notes: str | None = None


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
    signature: str | None = None
    signature_algorithm: str = "HMAC-SHA256"
