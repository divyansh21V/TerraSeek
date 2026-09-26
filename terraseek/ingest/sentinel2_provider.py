"""Sentinel-2 L2A data discovery provider — AWS Earth Search STAC API.

This module provides a MINIMAL data-discovery probe for Sentinel-2 imagery.
It queries the Element84 Earth Search public STAC endpoint and returns
normalized scene metadata.

Scope — this module ONLY proves data discovery and asset availability.
It does NOT perform:
  - Spectral analysis (NDVI, NDBI, or any index computation)
  - Change detection or change masks
  - Construction detection or built-up classification
  - Image download, raster processing, or pixel-level analysis

Resolution notes (from ESA Sentinel-2 User Guide):
  - Bands B02, B03, B04, B08: native 10 m ground sample distance
  - Bands B05, B06, B07, B8A, B11, B12: native 20 m ground sample distance
  - Bands B01, B09, B10: native 60 m ground sample distance
  B11/B12 are native 20 m bands — they must NOT be described as 10 m data.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EARTH_SEARCH_URL = "https://earth-search.aws.element84.com/v1"
SENTINEL2_COLLECTION = "sentinel-2-l2a"
SEARCH_TIMEOUT_SECONDS = 30

# Key Sentinel-2 bands that TerraSeek cares about, grouped by native GSD.
# This mapping is used only for *availability checking*, not processing.
KEY_BANDS: dict[str, dict[str, Any]] = {
    # ---- 10 m native resolution ----
    "blue":   {"sentinel_band": "B02", "gsd_m": 10, "purpose": "RGB composite"},
    "green":  {"sentinel_band": "B03", "gsd_m": 10, "purpose": "RGB composite"},
    "red":    {"sentinel_band": "B04", "gsd_m": 10, "purpose": "RGB composite / NDVI numerator"},
    "nir":    {"sentinel_band": "B08", "gsd_m": 10, "purpose": "NDVI / vegetation analysis"},
    # ---- 20 m native resolution ----
    "swir16": {"sentinel_band": "B11", "gsd_m": 20, "purpose": "SWIR analysis (future NDBI)"},
    "swir22": {"sentinel_band": "B12", "gsd_m": 20, "purpose": "Supporting SWIR band"},
    # ---- Derived products ----
    "visual": {"sentinel_band": "TCI", "gsd_m": 10, "purpose": "True-colour RGB composite"},
    "scl":    {"sentinel_band": "SCL", "gsd_m": 20, "purpose": "Scene classification / quality mask"},
}


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Sentinel2Asset:
    """A single asset (band or derived product) within a Sentinel-2 scene."""

    key: str             # STAC asset key, e.g. "red", "swir16", "visual"
    href: str            # URL to the Cloud-Optimized GeoTIFF or JPEG
    title: str           # Human-readable label
    media_type: str      # MIME type
    gsd: float | None = None  # Ground sample distance in metres, if reported


@dataclass
class Sentinel2Scene:
    """Normalized metadata for a single Sentinel-2 L2A scene.

    This is a pure data-discovery record. It carries NO spectral analysis
    results and makes NO claims about construction or change.
    """

    item_id: str                             # STAC item ID
    datetime: str                            # ISO-8601 acquisition datetime
    bbox: list[float]                        # STAC order [west, south, east, north]
    cloud_cover: float                       # Percentage (0–100), -1 if unknown
    platform: str                            # e.g. "sentinel-2b"
    collection: str                          # e.g. "sentinel-2-l2a"
    tile_id: str                             # MGRS tile, e.g. "36RUU"
    epsg: int | None                         # Projected CRS EPSG code
    assets: dict[str, Sentinel2Asset]        # All parsed assets
    bands_available: dict[str, bool] = field(default_factory=dict)  # KEY_BANDS presence


# ---------------------------------------------------------------------------
# Bounding-box conversion
# ---------------------------------------------------------------------------

def terraseek_bbox_to_stac(bbox: list[float]) -> list[float]:
    """Convert TerraSeek bbox to STAC / GeoJSON bbox order.

    TerraSeek convention (models.py InvestigationRequest):
        [south_lat, west_lon, north_lat, east_lon]

    STAC / GeoJSON convention:
        [west_lon, south_lat, east_lon, north_lat]
    """
    south, west, north, east = bbox
    return [west, south, east, north]


# ---------------------------------------------------------------------------
# STAC search request builder
# ---------------------------------------------------------------------------

def build_stac_search_body(
    bbox_stac: list[float],
    date_start: str,
    date_end: str,
    max_cloud_cover: float = 15.0,
    limit: int = 10,
) -> dict[str, Any]:
    """Build a POST body for the STAC /search endpoint.

    Args:
        bbox_stac: Bounding box in STAC order [west, south, east, north].
        date_start: ISO date string YYYY-MM-DD.
        date_end: ISO date string YYYY-MM-DD.
        max_cloud_cover: Maximum acceptable cloud cover percentage (0–100).
        limit: Maximum number of items to return.

    Returns:
        Dictionary suitable for ``httpx.Client.post(url, json=body)``.
    """
    return {
        "collections": [SENTINEL2_COLLECTION],
        "bbox": bbox_stac,
        "datetime": f"{date_start}T00:00:00Z/{date_end}T23:59:59Z",
        "query": {
            "eo:cloud_cover": {"lte": max_cloud_cover},
        },
        "limit": limit,
        "sortby": [
            {"field": "properties.datetime", "direction": "desc"},
        ],
    }


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

def _extract_tile_id(properties: dict[str, Any]) -> str:
    """Best-effort extraction of the MGRS tile identifier."""
    # Different Earth Search versions use different property names.
    for key in ("s2:mgrs_tile", "s2:tile_id", "grid:code"):
        val = properties.get(key)
        if val:
            # grid:code may be prefixed, e.g. "MGRS-36RUU"
            return str(val).replace("MGRS-", "")
    return "unknown"


def _parse_single_item(feature: dict[str, Any]) -> Sentinel2Scene | None:
    """Parse a single STAC Feature into a Sentinel2Scene.

    Returns None if the feature is missing the mandatory ``id`` field.
    """
    item_id = feature.get("id")
    if not item_id:
        return None

    props = feature.get("properties") or {}

    cloud_cover = props.get("eo:cloud_cover")
    if cloud_cover is None:
        cloud_cover = -1.0  # Unknown — callers should treat as unreliable

    # Parse assets
    raw_assets: dict[str, Any] = feature.get("assets") or {}
    assets: dict[str, Sentinel2Asset] = {}
    for key, asset_data in raw_assets.items():
        if not isinstance(asset_data, dict):
            continue
        assets[key] = Sentinel2Asset(
            key=key,
            href=asset_data.get("href", ""),
            title=asset_data.get("title", key),
            media_type=asset_data.get("type", "unknown"),
            gsd=asset_data.get("gsd"),
        )

    # Key-band availability check
    bands_available = {band_key: (band_key in assets) for band_key in KEY_BANDS}

    return Sentinel2Scene(
        item_id=item_id,
        datetime=props.get("datetime", ""),
        bbox=feature.get("bbox", []),
        cloud_cover=float(cloud_cover),
        platform=props.get("platform", "unknown"),
        collection=feature.get("collection", SENTINEL2_COLLECTION),
        tile_id=_extract_tile_id(props),
        epsg=props.get("proj:epsg"),
        assets=assets,
        bands_available=bands_available,
    )


def parse_stac_response(response_data: dict[str, Any]) -> list[Sentinel2Scene]:
    """Parse a STAC FeatureCollection into a list of Sentinel2Scene objects.

    Handles empty responses, missing ``features`` key, and malformed items
    gracefully — never raises on bad input.
    """
    if not isinstance(response_data, dict):
        return []

    features = response_data.get("features")
    if not isinstance(features, list):
        return []

    scenes: list[Sentinel2Scene] = []
    for feature in features:
        if not isinstance(feature, dict):
            continue
        scene = _parse_single_item(feature)
        if scene is not None:
            scenes.append(scene)

    return scenes


# ---------------------------------------------------------------------------
# Post-processing filters
# ---------------------------------------------------------------------------

def filter_by_cloud_cover(
    scenes: list[Sentinel2Scene],
    max_cloud_cover: float,
) -> list[Sentinel2Scene]:
    """Client-side safety filter for cloud cover.

    Applied as a second pass after the STAC server-side query filter,
    in case the server's filter implementation is inexact.
    """
    return [s for s in scenes if 0 <= s.cloud_cover <= max_cloud_cover]


# ---------------------------------------------------------------------------
# Band availability checks
# ---------------------------------------------------------------------------

def has_rgb_nir(scene: Sentinel2Scene) -> bool:
    """Check whether a scene has the four 10 m bands needed for RGB + NIR."""
    return all(scene.bands_available.get(b, False) for b in ("red", "green", "blue", "nir"))


def has_swir(scene: Sentinel2Scene) -> bool:
    """Check whether native 20 m SWIR bands (B11, B12) are available.

    Note: these are native 20 m ground sample distance — NOT 10 m.
    """
    return all(scene.bands_available.get(b, False) for b in ("swir16", "swir22"))


def has_visual_composite(scene: Sentinel2Scene) -> bool:
    """Check whether the pre-rendered TCI (true-colour) composite is available."""
    return scene.bands_available.get("visual", False)


# ---------------------------------------------------------------------------
# Live STAC query — for manual smoke testing ONLY
# ---------------------------------------------------------------------------

def search_sentinel2_live(
    bbox_terraseek: list[float],
    date_start: str,
    date_end: str,
    max_cloud_cover: float = 15.0,
    limit: int = 10,
) -> list[Sentinel2Scene]:
    """Query the live AWS Earth Search STAC endpoint.

    **This function makes a real network request.**

    It is intended for manual smoke testing only and MUST NOT be called
    by the main application or by automated unit tests.

    Args:
        bbox_terraseek: TerraSeek-format bbox [south, west, north, east].
        date_start: ISO date YYYY-MM-DD.
        date_end: ISO date YYYY-MM-DD.
        max_cloud_cover: Maximum cloud cover percentage (0–100).
        limit: Maximum scenes to return.

    Returns:
        List of Sentinel2Scene objects, filtered by cloud cover.

    Raises:
        httpx.HTTPStatusError: Non-2xx response from STAC endpoint.
        httpx.ConnectError: Network connectivity failure.
    """
    bbox_stac = terraseek_bbox_to_stac(bbox_terraseek)
    body = build_stac_search_body(bbox_stac, date_start, date_end, max_cloud_cover, limit)

    url = f"{EARTH_SEARCH_URL}/search"

    with httpx.Client(timeout=SEARCH_TIMEOUT_SECONDS) as client:
        response = client.post(url, json=body)
        response.raise_for_status()
        data = response.json()

    scenes = parse_stac_response(data)
    # Client-side safety filter
    scenes = filter_by_cloud_cover(scenes, max_cloud_cover)

    return scenes
