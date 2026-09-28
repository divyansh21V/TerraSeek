"""Business logic for TerraSeek investigations.

Separated from HTTP routes so the logic is testable independently.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import uuid
from datetime import UTC, date, datetime

from terraseek.demo_data import (
    DEMO_AOIS,
    DEMO_CANDIDATES,
    _worldview_url,
    get_candidate_by_id,
    get_candidates_for_aoi,
)
from terraseek.models import (
    CandidateDetail,
    CandidateSummary,
    DecisionRequest,
    DecisionResponse,
    EvidenceChannel,
    EvidenceItem,
    ExportPackage,
    InvestigationRequest,
    InvestigationResponse,
    PrioritySignals,
    QualityCheck,
    TimelineEntry,
)
from terraseek.ranking import compute_query_relevance, compute_ranking_score, priority_label
from terraseek.storage import load_decisions, load_investigation, save_decision, save_investigation

# --- In-memory session stores ---

_investigations: dict[str, dict] = {}
_decisions: dict[str, dict] = {}  # key = "{investigation_id}:{candidate_id}"


def _now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _bbox_overlaps(bbox_a: list[float], bbox_b: list[float]) -> bool:
    """Check if two [south, west, north, east] bounding boxes overlap."""
    s1, w1, n1, e1 = bbox_a
    s2, w2, n2, e2 = bbox_b
    if n1 < s2 or n2 < s1:
        return False
    return not (e1 < w2 or e2 < w1)


def _date_ranges_overlap(start_a: date, end_a: date, start_b: str, end_b: str) -> bool:
    """Check if two date ranges overlap."""
    sb = date.fromisoformat(start_b)
    eb = date.fromisoformat(end_b)
    return start_a <= eb and sb <= end_a


def _find_matching_aoi_key(bbox: list[float]) -> str | None:
    """Find which demo AOI the submitted bbox overlaps with."""
    for key, aoi in DEMO_AOIS.items():
        if _bbox_overlaps(bbox, aoi["bbox"]):
            return key
    return None


def _build_candidate_detail(
    raw: dict,
    investigation_id: str,
    query_relevance: float,
    ranking_score: float,
    priority: str,
) -> CandidateDetail:
    """Convert a raw demo-data dict into a CandidateDetail model."""
    signals = dict(raw["priority_signals"])
    signals["query_relevance"] = query_relevance

    dec_key = f"{investigation_id}:{raw['id']}"
    decision_data = _decisions.get(dec_key, {})
    if not decision_data and investigation_id != "standalone":
        decision_data = load_decisions(investigation_id).get(raw["id"], {})

    evidence_channels = {
        "spectral_signal": _channel(
            signals["visual_change_strength"],
            "Spectral and visual change strength in the selected comparison.",
        ),
        "semantic_match": _channel(
            query_relevance,
            "Relevance of the query terms to the candidate evidence keywords.",
        ),
        "temporal_persistence": _channel(
            signals["temporal_persistence"],
            "Persistence of the observed signal across the available timeline.",
        ),
        "spatial_context": _channel(
            signals["contextual_relevance"],
            "Relationship between the candidate and the requested area/context.",
        ),
        "quality_assurance": _channel(
            signals["data_suitability"],
            "Suitability of the imagery for this investigation and resolution.",
        ),
        "confounder_risk": _channel(
            1.0 - signals["confounder_risk"],
            "Lower raw confounder risk produces a stronger evidence score.",
        ),
    }

    return CandidateDetail(
        id=raw["id"],
        investigation_id=investigation_id,
        location_name=raw["location_name"],
        latitude=raw["latitude"],
        longitude=raw["longitude"],
        investigation_priority=priority,
        ranking_score=ranking_score,
        priority_signals=PrioritySignals(**signals),
        evidence_channels=evidence_channels,
        before_image_url=_worldview_url(raw["before_bbox"], raw["before_date"]),
        before_date=raw["before_date"],
        before_source=raw["before_source"],
        after_image_url=_worldview_url(raw["after_bbox"], raw["after_date"]),
        after_date=raw["after_date"],
        after_source=raw["after_source"],
        observed=[EvidenceItem(**e) for e in raw["observed"]],
        inferred=[EvidenceItem(**e) for e in raw["inferred"]],
        limitations=raw["limitations"],
        timeline=[TimelineEntry(**t) for t in raw["timeline"]],
        quality_checks=[QualityCheck(**q) for q in raw["quality_checks"]],
        contextual_evidence=[EvidenceItem(**e) for e in raw["contextual_evidence"]],
        warnings=raw["warnings"],
        analyst_decision=decision_data.get("decision"),
        analyst_notes=decision_data.get("notes"),
    )


def _channel(score: float, rationale: str) -> EvidenceChannel:
    """Convert a normalized signal into an honest qualitative status."""
    if score >= 0.75:
        status = "STRONG"
    elif score >= 0.5:
        status = "MODERATE"
    else:
        status = "WEAK"
    return EvidenceChannel(score=round(score, 4), status=status, rationale=rationale)


# --- Public service functions ---


def run_investigation(request: InvestigationRequest) -> InvestigationResponse:
    """Execute an investigation and return ranked candidates."""
    investigation_id = f"inv-{uuid.uuid4().hex[:12]}"

    # Find matching AOI
    aoi_key = _find_matching_aoi_key(request.aoi_bbox)

    # Gather candidates
    if aoi_key:
        raw_candidates = get_candidates_for_aoi(aoi_key)
    else:
        # Fallback: check all candidates for bbox overlap
        raw_candidates = []
        for c in DEMO_CANDIDATES:
            c_bbox = [
                c["latitude"] - 0.5,
                c["longitude"] - 0.5,
                c["latitude"] + 0.5,
                c["longitude"] + 0.5,
            ]
            if _bbox_overlaps(request.aoi_bbox, c_bbox):
                raw_candidates.append(c)

    # Filter by date range overlap
    raw_candidates = [
        c
        for c in raw_candidates
        if _date_ranges_overlap(
            request.date_start,
            request.date_end,
            c["date_range_start"],
            c["date_range_end"],
        )
    ]

    # Score and rank
    scored: list[tuple[dict, float, float, str]] = []
    for c in raw_candidates:
        qr = compute_query_relevance(request.query, c["keywords"])
        signals = dict(c["priority_signals"])
        signals["query_relevance"] = qr
        score = compute_ranking_score(signals)
        priority = priority_label(score)
        scored.append((c, score, qr, priority))

    # Sort by score descending
    scored.sort(key=lambda x: x[1], reverse=True)

    # Build summary list
    summaries: list[CandidateSummary] = []
    for c, score, qr, priority in scored:
        summaries.append(
            CandidateSummary(
                id=c["id"],
                location_name=c["location_name"],
                latitude=c["latitude"],
                longitude=c["longitude"],
                investigation_priority=priority,
                ranking_score=score,
                summary=c["observed"][0]["value"] if c["observed"] else "",
                before_date=c["before_date"],
                after_date=c["after_date"],
                primary_evidence=c["inferred"][0]["value"] if c["inferred"] else "",
            )
        )

    # Store investigation for export
    investigation = {
        "query": request.query,
        "aoi_name": request.aoi_name,
        "aoi_bbox": request.aoi_bbox,
        "date_start": request.date_start.isoformat(),
        "date_end": request.date_end.isoformat(),
        "candidate_ids": [c["id"] for c, *_ in scored],
        "scores": {c["id"]: {"score": s, "qr": qr} for c, s, qr, _ in scored},
    }
    _investigations[investigation_id] = investigation
    save_investigation(investigation_id, investigation, _now())

    return InvestigationResponse(
        investigation_id=investigation_id,
        query=request.query,
        aoi_name=request.aoi_name,
        date_range=f"{request.date_start.isoformat()} to {request.date_end.isoformat()}",
        candidate_count=len(summaries),
        candidates=summaries,
    )


def get_candidate_detail(
    candidate_id: str,
    investigation_id: str | None = None,
) -> CandidateDetail | None:
    """Retrieve full detail for a candidate."""
    raw = get_candidate_by_id(candidate_id)
    if raw is None:
        return None

    inv_id = investigation_id or "standalone"

    # Recover stored scores if available
    inv = _investigations.get(inv_id)
    if inv is None and investigation_id:
        inv = load_investigation(inv_id)
        if inv:
            _investigations[inv_id] = inv
    inv = inv or {}
    scores = inv.get("scores", {}).get(candidate_id, {})
    qr = scores.get("qr", 0.5)

    signals = dict(raw["priority_signals"])
    signals["query_relevance"] = qr
    score = compute_ranking_score(signals)
    priority = priority_label(score)

    return _build_candidate_detail(raw, inv_id, qr, score, priority)


def record_decision(req: DecisionRequest) -> DecisionResponse:
    """Record an analyst decision for a candidate."""
    investigation = _investigations.get(req.investigation_id) or load_investigation(
        req.investigation_id
    )
    if investigation is None:
        raise ValueError(f"Investigation '{req.investigation_id}' not found")
    if req.candidate_id not in investigation["candidate_ids"]:
        raise ValueError(
            f"Candidate '{req.candidate_id}' is not part of investigation '{req.investigation_id}'"
        )
    key = f"{req.investigation_id}:{req.candidate_id}"
    now = _now()

    _decisions[key] = {
        "decision": req.decision.value,
        "notes": req.notes,
        "recorded_at": now,
    }
    save_decision(req.investigation_id, req.candidate_id, _decisions[key], now)

    return DecisionResponse(
        status="recorded",
        investigation_id=req.investigation_id,
        candidate_id=req.candidate_id,
        decision=req.decision.value,
        recorded_at=now,
    )


def export_investigation(investigation_id: str) -> ExportPackage | None:
    """Build a complete exportable evidence package."""
    inv = _investigations.get(investigation_id) or load_investigation(investigation_id)
    if inv is None:
        return None

    candidates: list[CandidateDetail] = []
    for cid in inv["candidate_ids"]:
        detail = get_candidate_detail(cid, investigation_id)
        if detail:
            candidates.append(detail)

    # Collect decisions for this investigation
    inv_decisions: dict[str, dict] = {}
    inv_decisions.update(load_decisions(investigation_id))
    for key, val in _decisions.items():
        if key.startswith(f"{investigation_id}:"):
            inv_decisions[key.split(":", 1)[1]] = val

    package = ExportPackage(
        exported_at=_now(),
        investigation_id=investigation_id,
        query=inv["query"],
        aoi_name=inv["aoi_name"],
        aoi_bbox=inv["aoi_bbox"],
        date_range=f"{inv['date_start']} to {inv['date_end']}",
        candidates=candidates,
        decisions=inv_decisions,
        system_info={
            "version": "0.2.0",
            "data_source": "Local prototype dataset (NASA MODIS via Worldview)",
            "mode": "demo_fixture",
            "reproducible": True,
            "ranking_method": "Deterministic weighted signal scoring",
            "resolution_note": "MODIS 250 m/pixel — site-scale detection only",
            "limitations": [
                "This package is a deterministic prototype fixture, not live provider data.",
                "MODIS resolution is insufficient for structure-level confirmation.",
            ],
        },
    )
    signing_key = os.getenv("TERRASEEK_SIGNING_KEY")
    if signing_key:
        unsigned = package.model_dump(exclude={"signature"})
        canonical = json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
        signature = hmac.new(signing_key.encode(), canonical, hashlib.sha256).hexdigest()
        package = package.model_copy(update={"signature": signature})
    return package
