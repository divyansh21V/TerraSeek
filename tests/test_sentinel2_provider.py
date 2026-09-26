"""Unit tests for the Sentinel-2 STAC data discovery provider.

All tests use local fixture data. NO network requests are made.
These tests verify parsing, filtering, and availability checking only.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from terraseek.ingest.sentinel2_provider import (
    KEY_BANDS,
    Sentinel2Scene,
    build_stac_search_body,
    filter_by_cloud_cover,
    has_rgb_nir,
    has_swir,
    has_visual_composite,
    parse_stac_response,
    terraseek_bbox_to_stac,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def stac_response() -> dict:
    """Load the standard 3-item Sentinel-2 STAC response fixture."""
    with open(FIXTURES_DIR / "stac_sentinel2_response.json", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Bounding-box conversion
# ---------------------------------------------------------------------------

class TestBboxConversion:
    """Verify TerraSeek ↔ STAC bbox order conversion."""

    def test_terraseek_to_stac(self):
        # TerraSeek: [south, west, north, east]
        # STAC:      [west, south, east, north]
        ts = [29.90, 31.65, 30.15, 31.95]
        assert terraseek_bbox_to_stac(ts) == [31.65, 29.90, 31.95, 30.15]

    def test_negative_coordinates(self):
        # Amazon: south/west are negative
        ts = [-4.0, -53.0, -2.5, -51.0]
        assert terraseek_bbox_to_stac(ts) == [-53.0, -4.0, -51.0, -2.5]


# ---------------------------------------------------------------------------
# STAC search body construction
# ---------------------------------------------------------------------------

class TestSearchBody:
    """Verify the STAC POST /search request body."""

    def test_basic_body(self):
        body = build_stac_search_body(
            bbox_stac=[31.65, 29.90, 31.95, 30.15],
            date_start="2023-01-01",
            date_end="2024-01-01",
            max_cloud_cover=15.0,
            limit=10,
        )
        assert body["collections"] == ["sentinel-2-l2a"]
        assert body["bbox"] == [31.65, 29.90, 31.95, 30.15]
        assert "2023-01-01" in body["datetime"]
        assert "2024-01-01" in body["datetime"]
        assert body["query"]["eo:cloud_cover"]["lte"] == 15.0
        assert body["limit"] == 10

    def test_custom_cloud_and_limit(self):
        body = build_stac_search_body(
            bbox_stac=[0, 0, 1, 1],
            date_start="2020-06-01",
            date_end="2020-06-30",
            max_cloud_cover=5.0,
            limit=50,
        )
        assert body["query"]["eo:cloud_cover"]["lte"] == 5.0
        assert body["limit"] == 50


# ---------------------------------------------------------------------------
# Response parsing — successful cases
# ---------------------------------------------------------------------------

class TestParseSuccess:
    """Verify correct parsing of well-formed STAC responses."""

    def test_parses_all_three_items(self, stac_response):
        scenes = parse_stac_response(stac_response)
        assert len(scenes) == 3

    def test_item_ids(self, stac_response):
        scenes = parse_stac_response(stac_response)
        ids = {s.item_id for s in scenes}
        assert ids == {
            "S2B_36RUU_20231215_0_L2A",
            "S2A_36RUU_20231210_0_L2A",
            "S2B_36RUU_20231205_0_L2A",
        }

    def test_scene_metadata_fields(self, stac_response):
        scenes = parse_stac_response(stac_response)
        scene = next(s for s in scenes if s.item_id == "S2B_36RUU_20231215_0_L2A")

        assert scene.cloud_cover == 3.42
        assert scene.platform == "sentinel-2b"
        assert scene.collection == "sentinel-2-l2a"
        assert scene.tile_id == "36RUU"
        assert scene.epsg == 32636
        assert len(scene.bbox) == 4
        assert "2023-12-15" in scene.datetime

    def test_asset_count(self, stac_response):
        scenes = parse_stac_response(stac_response)
        scene = scenes[0]
        # Fixture has 9 assets per item: blue, green, red, nir, swir16, swir22,
        # visual, scl, thumbnail
        assert len(scene.assets) == 9

    def test_asset_gsd_preserved(self, stac_response):
        scenes = parse_stac_response(stac_response)
        scene = scenes[0]
        assert scene.assets["red"].gsd == 10
        assert scene.assets["swir16"].gsd == 20  # Native 20 m — NOT 10 m
        assert scene.assets["swir22"].gsd == 20
        assert scene.assets["scl"].gsd == 20

    def test_asset_href_present(self, stac_response):
        scenes = parse_stac_response(stac_response)
        scene = scenes[0]
        for asset in scene.assets.values():
            assert asset.href.startswith("https://")

    def test_datetime_present_on_all(self, stac_response):
        scenes = parse_stac_response(stac_response)
        for scene in scenes:
            assert len(scene.datetime) > 0
            assert "2023-12" in scene.datetime


# ---------------------------------------------------------------------------
# Response parsing — error/edge cases
# ---------------------------------------------------------------------------

class TestParseErrors:
    """Verify graceful handling of malformed or missing data."""

    def test_empty_feature_collection(self):
        empty = {"type": "FeatureCollection", "features": []}
        assert parse_stac_response(empty) == []

    def test_missing_features_key(self):
        assert parse_stac_response({"type": "FeatureCollection"}) == []

    def test_completely_empty_dict(self):
        assert parse_stac_response({}) == []

    def test_non_dict_input(self):
        assert parse_stac_response("not a dict") == []  # type: ignore[arg-type]

    def test_feature_without_id_skipped(self):
        data = {"features": [{"properties": {"datetime": "2023-01-01"}, "assets": {}}]}
        scenes = parse_stac_response(data)
        assert scenes == []

    def test_feature_with_non_dict_assets(self):
        data = {
            "features": [{
                "id": "test-item",
                "properties": {"datetime": "2023-01-01"},
                "assets": {"bad": "not-a-dict"},
            }],
        }
        scenes = parse_stac_response(data)
        assert len(scenes) == 1
        assert "bad" not in scenes[0].assets

    def test_missing_cloud_cover_defaults_to_negative(self):
        data = {
            "features": [{
                "id": "no-cloud",
                "properties": {"datetime": "2023-01-01"},
                "assets": {},
            }],
        }
        scenes = parse_stac_response(data)
        assert scenes[0].cloud_cover == -1.0


# ---------------------------------------------------------------------------
# Cloud cover filtering
# ---------------------------------------------------------------------------

class TestCloudFilter:
    """Verify client-side cloud cover post-filtering."""

    def test_filter_at_15_percent(self, stac_response):
        scenes = parse_stac_response(stac_response)
        filtered = filter_by_cloud_cover(scenes, 15.0)
        # Fixture has 3.42%, 12.8%, 42.1% — only first two should pass
        assert len(filtered) == 2
        for s in filtered:
            assert s.cloud_cover <= 15.0

    def test_filter_strict_5_percent(self, stac_response):
        scenes = parse_stac_response(stac_response)
        filtered = filter_by_cloud_cover(scenes, 5.0)
        assert len(filtered) == 1
        assert filtered[0].cloud_cover == 3.42

    def test_filter_zero_percent(self, stac_response):
        scenes = parse_stac_response(stac_response)
        filtered = filter_by_cloud_cover(scenes, 0.0)
        assert len(filtered) == 0

    def test_filter_100_percent_passes_all(self, stac_response):
        scenes = parse_stac_response(stac_response)
        filtered = filter_by_cloud_cover(scenes, 100.0)
        assert len(filtered) == 3

    def test_unknown_cloud_cover_excluded(self):
        """Scenes with cloud_cover = -1 (unknown) should be excluded."""
        data = {
            "features": [{
                "id": "unknown-cloud",
                "properties": {"datetime": "2023-01-01"},
                "assets": {},
            }],
        }
        scenes = parse_stac_response(data)
        assert scenes[0].cloud_cover == -1.0
        filtered = filter_by_cloud_cover(scenes, 100.0)
        assert len(filtered) == 0  # -1 < 0, so excluded


# ---------------------------------------------------------------------------
# Band availability detection
# ---------------------------------------------------------------------------

class TestBandAvailability:
    """Verify detection of key Sentinel-2 band assets."""

    def test_all_key_bands_present(self, stac_response):
        scenes = parse_stac_response(stac_response)
        scene = scenes[0]
        for band_key in KEY_BANDS:
            assert scene.bands_available[band_key] is True

    def test_has_rgb_nir_complete(self, stac_response):
        scenes = parse_stac_response(stac_response)
        assert has_rgb_nir(scenes[0]) is True

    def test_has_swir_complete(self, stac_response):
        scenes = parse_stac_response(stac_response)
        assert has_swir(scenes[0]) is True

    def test_has_visual_composite(self, stac_response):
        scenes = parse_stac_response(stac_response)
        assert has_visual_composite(scenes[0]) is True

    def test_missing_rgb_bands(self, stac_response):
        """Removing RGB/NIR assets should make has_rgb_nir return False."""
        data = copy.deepcopy(stac_response)
        for key in ("red", "green", "blue", "nir"):
            data["features"][0]["assets"].pop(key, None)

        scenes = parse_stac_response(data)
        scene = scenes[0]

        assert scene.bands_available["red"] is False
        assert scene.bands_available["green"] is False
        assert scene.bands_available["blue"] is False
        assert scene.bands_available["nir"] is False
        assert has_rgb_nir(scene) is False
        # SWIR should still be fine
        assert has_swir(scene) is True

    def test_missing_swir_bands(self, stac_response):
        """Removing SWIR assets should make has_swir return False."""
        data = copy.deepcopy(stac_response)
        data["features"][0]["assets"].pop("swir16", None)
        data["features"][0]["assets"].pop("swir22", None)

        scenes = parse_stac_response(data)
        scene = scenes[0]

        assert has_swir(scene) is False
        # RGB should still be fine
        assert has_rgb_nir(scene) is True

    def test_empty_assets(self):
        """A scene with zero assets should report all bands missing."""
        data = {"features": [{"id": "empty-assets", "properties": {}, "assets": {}}]}
        scenes = parse_stac_response(data)
        scene = scenes[0]

        for band_key in KEY_BANDS:
            assert scene.bands_available[band_key] is False
        assert has_rgb_nir(scene) is False
        assert has_swir(scene) is False
        assert has_visual_composite(scene) is False
