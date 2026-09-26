"""Local prototype dataset for TerraSeek vertical slice.

All geographic coordinates are real locations of documented large-scale
construction or land-use change projects. Satellite imagery URLs point to
NASA Worldview (MODIS Terra True Color), which is public-domain imagery
provided by NASA EOSDIS.

Resolution note: MODIS imagery is ~250m/pixel. Individual structures are not
visible. Large-scale site expansion (urbanisation, land clearing, port
reclamation) IS visible as albedo / colour change.

This module is designed to be replaced by live STAC retrieval without
changing the frontend or the service interface.
"""

from __future__ import annotations


def _worldview_url(bbox: str, date: str, width: int = 640, height: int = 480) -> str:
    """Build a NASA Worldview snapshot URL for MODIS True Color imagery."""
    return (
        "https://wvs.earthdata.nasa.gov/api/v1/snapshot"
        f"?REQUEST=GetSnapshot"
        f"&LAYERS=MODIS_Terra_CorrectedReflectance_TrueColor"
        f"&CRS=EPSG:4326"
        f"&TIME={date}"
        f"&WRAP=day"
        f"&BBOX={bbox}"
        f"&FORMAT=image/jpeg"
        f"&WIDTH={width}"
        f"&HEIGHT={height}"
    )


# --- Pre-defined AOIs ---

DEMO_AOIS: dict[str, dict] = {
    "egypt_cairo": {
        "name": "Egypt — Greater Cairo & New Administrative Capital",
        "bbox": [29.5, 31.0, 30.5, 32.5],
    },
    "amazon_altamira": {
        "name": "Amazon Basin — Altamira Region",
        "bbox": [-4.0, -53.0, -2.5, -51.0],
    },
}


# --- Candidate records ---
# Each record is a dict matching the CandidateDetail model fields,
# minus investigation_id, analyst_decision, and analyst_notes (set at runtime).

DEMO_CANDIDATES: list[dict] = [
    # ------------------------------------------------------------------ #
    # CANDIDATE 1 — Egypt New Administrative Capital (NAC)
    # ------------------------------------------------------------------ #
    {
        "id": "EG-NAC-001",
        "aoi_key": "egypt_cairo",
        "location_name": "New Administrative Capital — Central District, Egypt",
        "latitude": 30.02,
        "longitude": 31.80,
        "date_range_start": "2015-01-01",
        "date_range_end": "2024-12-31",
        "keywords": [
            "construction", "built", "structures", "urban", "development",
            "city", "capital", "expansion", "buildings", "infrastructure",
        ],
        "before_date": "2016-02-15",
        "before_source": "NASA MODIS Terra — Worldview",
        "before_bbox": "29.90,31.65,30.15,31.95",
        "after_date": "2023-12-15",
        "after_source": "NASA MODIS Terra — Worldview",
        "after_bbox": "29.90,31.65,30.15,31.95",
        "priority_signals": {
            "query_relevance": 0.0,
            "visual_change_strength": 0.92,
            "temporal_persistence": 0.95,
            "data_suitability": 0.80,
            "contextual_relevance": 0.88,
            "confounder_risk": 0.10,
        },
        "observed": [
            {
                "label": "Surface albedo change",
                "value": "MODIS imagery shows transition from sandy desert surface to darker developed surface across ~700 km²",
                "signal_strength": "STRONG",
            },
            {
                "label": "Spatial extent",
                "value": "Change footprint extends approximately 35 km east-west by 20 km north-south",
                "signal_strength": "STRONG",
            },
            {
                "label": "Observation period",
                "value": "Before: 2016-02-15 | After: 2023-12-15 — 7.8 year span",
                "signal_strength": "STRONG",
            },
        ],
        "inferred": [
            {
                "label": "Site-scale built-up expansion",
                "value": "Albedo and colour change pattern is consistent with large-scale urbanisation on previously undeveloped desert",
                "signal_strength": "STRONG",
            },
            {
                "label": "Temporal persistence",
                "value": "Change signal present in all available cloud-free observations from 2019 onwards (5 of 5 checked)",
                "signal_strength": "STRONG",
            },
            {
                "label": "Confounder assessment",
                "value": "Desert environment — low seasonal vegetation variability, low cloud frequency in winter observations",
                "signal_strength": "STRONG",
            },
        ],
        "limitations": [
            "MODIS 250 m resolution cannot confirm individual structures or building types.",
            "System does not autonomously confirm construction — analyst verification required.",
            "No ground-truth data is available in this prototype.",
            "Spectral change alone cannot distinguish construction from mining or land grading.",
        ],
        "timeline": [
            {"date": "2016-02-15", "observation": "Baseline: undeveloped desert surface", "signal": "UNCHANGED", "source": "MODIS Terra"},
            {"date": "2018-01-15", "observation": "Initial land grading visible at site scale", "signal": "WEAK_SIGNAL", "source": "MODIS Terra"},
            {"date": "2019-11-15", "observation": "Distinct albedo change across central area", "signal": "STRONG_SIGNAL", "source": "MODIS Terra"},
            {"date": "2021-02-15", "observation": "Expansion continues — footprint larger", "signal": "STRONG_SIGNAL", "source": "MODIS Terra"},
            {"date": "2023-12-15", "observation": "Development footprint fully established", "signal": "PERSISTENT", "source": "MODIS Terra"},
        ],
        "quality_checks": [
            {"check_name": "Cloud contamination", "status": "PASS", "detail": "Selected observations have < 5% cloud cover over AOI."},
            {"check_name": "Sensor consistency", "status": "PASS", "detail": "All observations from MODIS Terra — no cross-sensor normalisation needed."},
            {"check_name": "Spatial resolution", "status": "WARNING", "detail": "MODIS 250 m/pixel — sufficient for site-scale detection, insufficient for structure-level."},
            {"check_name": "Temporal coverage", "status": "PASS", "detail": "5 cloud-free observations across 7.8-year span."},
            {"check_name": "Registration alignment", "status": "PASS", "detail": "MODIS geolocation accuracy < 50 m — adequate for site-scale comparison."},
        ],
        "contextual_evidence": [
            {
                "label": "Proximity to existing urban area",
                "value": "Site is ~45 km east of central Cairo, adjacent to the Ring Road",
                "signal_strength": "STRONG",
            },
            {
                "label": "Transport infrastructure",
                "value": "Major highway corridors visible connecting site to existing road network",
                "signal_strength": "MODERATE",
            },
        ],
        "warnings": [
            "MODIS resolution cannot distinguish construction from other land-modification activities (e.g., quarrying, landfill).",
            "Before/after comparison uses selected dates — intermediate changes may exist between observation dates.",
        ],
    },

    # ------------------------------------------------------------------ #
    # CANDIDATE 2 — New Alamein, Egypt (Coastal Development)
    # ------------------------------------------------------------------ #
    {
        "id": "EG-ALM-002",
        "aoi_key": "egypt_cairo",
        "location_name": "New Alamein City — Mediterranean Coast, Egypt",
        "latitude": 30.84,
        "longitude": 28.95,
        "date_range_start": "2016-01-01",
        "date_range_end": "2024-12-31",
        "keywords": [
            "construction", "built", "resort", "coastal", "development",
            "city", "expansion", "tourism", "buildings", "urban",
        ],
        "before_date": "2017-03-15",
        "before_source": "NASA MODIS Terra — Worldview",
        "before_bbox": "30.70,28.75,30.95,29.15",
        "after_date": "2023-11-15",
        "after_source": "NASA MODIS Terra — Worldview",
        "after_bbox": "30.70,28.75,30.95,29.15",
        "priority_signals": {
            "query_relevance": 0.0,
            "visual_change_strength": 0.65,
            "temporal_persistence": 0.70,
            "data_suitability": 0.75,
            "contextual_relevance": 0.60,
            "confounder_risk": 0.25,
        },
        "observed": [
            {
                "label": "Coastal surface change",
                "value": "MODIS imagery shows new reflective surfaces appearing along previously undeveloped coastline",
                "signal_strength": "MODERATE",
            },
            {
                "label": "Observation period",
                "value": "Before: 2017-03-15 | After: 2023-11-15 — 6.7 year span",
                "signal_strength": "STRONG",
            },
        ],
        "inferred": [
            {
                "label": "Coastal built-up expansion",
                "value": "Change pattern is consistent with resort/urban construction along coastline",
                "signal_strength": "MODERATE",
            },
            {
                "label": "Temporal persistence",
                "value": "Change signal present in 3 of 4 checked observations from 2020 onwards",
                "signal_strength": "MODERATE",
            },
        ],
        "limitations": [
            "Coastal proximity introduces surf/sand reflectance variability.",
            "MODIS 250 m resolution cannot distinguish buildings from other coastal modifications.",
            "Seasonal beach width variation may affect albedo comparison.",
        ],
        "timeline": [
            {"date": "2017-03-15", "observation": "Baseline: undeveloped coastal desert", "signal": "UNCHANGED", "source": "MODIS Terra"},
            {"date": "2019-03-15", "observation": "Possible early-stage land preparation", "signal": "WEAK_SIGNAL", "source": "MODIS Terra"},
            {"date": "2021-03-15", "observation": "New reflective features along coast", "signal": "STRONG_SIGNAL", "source": "MODIS Terra"},
            {"date": "2023-11-15", "observation": "Expanded development footprint", "signal": "PERSISTENT", "source": "MODIS Terra"},
        ],
        "quality_checks": [
            {"check_name": "Cloud contamination", "status": "PASS", "detail": "< 5% cloud cover on selected dates."},
            {"check_name": "Sensor consistency", "status": "PASS", "detail": "All MODIS Terra."},
            {"check_name": "Spatial resolution", "status": "WARNING", "detail": "250 m/pixel — marginal for coastal construction detection."},
            {"check_name": "Coastal artefacts", "status": "WARNING", "detail": "Surf, tidal, and sand-drift artefacts possible at this resolution."},
        ],
        "contextual_evidence": [
            {
                "label": "Proximity to highway",
                "value": "Site adjacent to Alexandria–Matrouh highway (visible in imagery)",
                "signal_strength": "MODERATE",
            },
        ],
        "warnings": [
            "Coastal reflectance changes may partly reflect natural sand/surf variability rather than construction.",
            "Moderate confounder risk — analyst should verify with higher-resolution imagery if available.",
        ],
    },

    # ------------------------------------------------------------------ #
    # CANDIDATE 3 — Amazon Basin, land clearing near Altamira
    # ------------------------------------------------------------------ #
    {
        "id": "BR-ALT-001",
        "aoi_key": "amazon_altamira",
        "location_name": "Land Clearing — Altamira Region, Pará, Brazil",
        "latitude": -3.45,
        "longitude": -51.95,
        "date_range_start": "2014-01-01",
        "date_range_end": "2024-12-31",
        "keywords": [
            "clearing", "deforestation", "land", "expansion", "construction",
            "built", "development", "infrastructure", "dam", "road",
        ],
        "before_date": "2015-08-15",
        "before_source": "NASA MODIS Terra — Worldview",
        "before_bbox": "-3.70,-52.20,-3.20,-51.70",
        "after_date": "2023-08-15",
        "after_source": "NASA MODIS Terra — Worldview",
        "after_bbox": "-3.70,-52.20,-3.20,-51.70",
        "priority_signals": {
            "query_relevance": 0.0,
            "visual_change_strength": 0.85,
            "temporal_persistence": 0.90,
            "data_suitability": 0.65,
            "contextual_relevance": 0.75,
            "confounder_risk": 0.30,
        },
        "observed": [
            {
                "label": "Vegetation cover change",
                "value": "MODIS imagery shows transition from dense forest (dark green) to cleared/exposed surface (brown/tan) across multiple patches",
                "signal_strength": "STRONG",
            },
            {
                "label": "Observation period",
                "value": "Before: 2015-08-15 | After: 2023-08-15 — 8.0 year span, same month to control seasonality",
                "signal_strength": "STRONG",
            },
        ],
        "inferred": [
            {
                "label": "Large-scale land clearing",
                "value": "Pattern consistent with progressive deforestation for infrastructure or agriculture — multiple distinct cleared patches",
                "signal_strength": "STRONG",
            },
            {
                "label": "Temporal persistence",
                "value": "Cleared areas persist across 4 of 4 dry-season observations from 2019 onwards",
                "signal_strength": "STRONG",
            },
            {
                "label": "Proximity to Belo Monte dam complex",
                "value": "Clearing pattern near the Xingu River — associated infrastructure development possible",
                "signal_strength": "MODERATE",
            },
        ],
        "limitations": [
            "Cannot distinguish construction from agricultural clearing at MODIS resolution.",
            "Amazon wet-season cloud cover limits available observations to July–October dry season.",
            "Smoke from regional fires may affect image quality during dry season.",
        ],
        "timeline": [
            {"date": "2015-08-15", "observation": "Baseline: dense tropical forest cover", "signal": "UNCHANGED", "source": "MODIS Terra"},
            {"date": "2017-08-15", "observation": "Initial clearing patches visible", "signal": "WEAK_SIGNAL", "source": "MODIS Terra"},
            {"date": "2019-08-15", "observation": "Clearing expanded — road-like linear features", "signal": "STRONG_SIGNAL", "source": "MODIS Terra"},
            {"date": "2021-08-15", "observation": "Significant area converted", "signal": "STRONG_SIGNAL", "source": "MODIS Terra"},
            {"date": "2023-08-15", "observation": "Clearing persistent and expanded", "signal": "PERSISTENT", "source": "MODIS Terra"},
        ],
        "quality_checks": [
            {"check_name": "Cloud contamination", "status": "WARNING", "detail": "Dry-season observations used, but residual cloud/haze possible."},
            {"check_name": "Sensor consistency", "status": "PASS", "detail": "All MODIS Terra."},
            {"check_name": "Spatial resolution", "status": "WARNING", "detail": "250 m/pixel — detects site-scale clearing but not individual structures."},
            {"check_name": "Seasonal control", "status": "PASS", "detail": "All observations from August — seasonal vegetation cycle controlled."},
            {"check_name": "Fire/smoke artefact", "status": "WARNING", "detail": "Amazon dry season has active fires — some haze possible."},
        ],
        "contextual_evidence": [
            {
                "label": "Proximity to Xingu River",
                "value": "Clearing concentrated within 30 km of the Xingu River and Belo Monte dam complex",
                "signal_strength": "STRONG",
            },
            {
                "label": "Road network",
                "value": "Linear clearing patterns suggest road construction connecting cleared areas",
                "signal_strength": "MODERATE",
            },
        ],
        "warnings": [
            "Tropical forest clearing does not necessarily indicate construction — agriculture and logging produce similar spectral change.",
            "Dry-season fire smoke may affect colour balance in some observations.",
            "Higher confounder risk compared to arid-region candidates.",
        ],
    },
]


def get_available_aois() -> dict[str, dict]:
    """Return the pre-defined AOIs available for investigation."""
    return DEMO_AOIS


def get_candidates_for_aoi(aoi_key: str) -> list[dict]:
    """Return candidate records that belong to the given AOI key."""
    return [c for c in DEMO_CANDIDATES if c["aoi_key"] == aoi_key]


def get_candidate_by_id(candidate_id: str) -> dict | None:
    """Return a single candidate record by its ID, or None."""
    for c in DEMO_CANDIDATES:
        if c["id"] == candidate_id:
            return c
    return None
