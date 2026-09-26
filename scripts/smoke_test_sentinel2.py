"""Smoke test — query real Sentinel-2 scenes from AWS Earth Search.

Usage:
    py -3.11 scripts/smoke_test_sentinel2.py
    py -3.11 scripts/smoke_test_sentinel2.py --bbox 29.90 31.65 30.15 31.95
    py -3.11 scripts/smoke_test_sentinel2.py --cloud 5.0 --limit 3

This script makes a LIVE network request to the Element84 Earth Search
public STAC API. It is intended for manual verification only.

Default query area: Egypt — New Administrative Capital (30.02°N, 31.80°E)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running from repo root without pip install
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from terraseek.ingest.sentinel2_provider import (
    KEY_BANDS,
    EARTH_SEARCH_URL,
    SENTINEL2_COLLECTION,
    has_rgb_nir,
    has_swir,
    has_visual_composite,
    search_sentinel2_live,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Smoke test: discover Sentinel-2 L2A scenes via STAC",
    )
    parser.add_argument(
        "--bbox",
        nargs=4,
        type=float,
        default=[29.90, 31.65, 30.15, 31.95],
        metavar=("SOUTH", "WEST", "NORTH", "EAST"),
        help="TerraSeek-format bounding box (default: Egypt NAC area)",
    )
    parser.add_argument(
        "--start",
        default="2023-01-01",
        help="Start date YYYY-MM-DD (default: 2023-01-01)",
    )
    parser.add_argument(
        "--end",
        default="2024-01-01",
        help="End date YYYY-MM-DD (default: 2024-01-01)",
    )
    parser.add_argument(
        "--cloud",
        type=float,
        default=15.0,
        help="Max cloud cover %% (default: 15.0)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Max scenes to return (default: 5)",
    )
    args = parser.parse_args()

    print("=" * 72)
    print("  TerraSeek — Sentinel-2 STAC Data Discovery Probe")
    print("=" * 72)
    print()
    print(f"  Endpoint:    {EARTH_SEARCH_URL}")
    print(f"  Collection:  {SENTINEL2_COLLECTION}")
    print(f"  BBOX (SWNE): {args.bbox}")
    print(f"  Date range:  {args.start} -> {args.end}")
    print(f"  Max cloud:   {args.cloud}%")
    print(f"  Limit:       {args.limit}")
    print()

    try:
        scenes = search_sentinel2_live(
            bbox_terraseek=args.bbox,
            date_start=args.start,
            date_end=args.end,
            max_cloud_cover=args.cloud,
            limit=args.limit,
        )
    except Exception as exc:
        print(f"  ERROR: {exc}")
        print()
        print("  The STAC endpoint may be unreachable. Check your network.")
        sys.exit(1)

    print(f"  Scenes discovered: {len(scenes)}")
    print()

    if not scenes:
        print("  No scenes matched the query. Try widening the date range")
        print("  or increasing the cloud cover threshold.")
        sys.exit(0)

    for i, scene in enumerate(scenes, 1):
        print(f"  -- Scene {i} " + "-" * 50)
        print(f"  Item ID:     {scene.item_id}")
        print(f"  Datetime:    {scene.datetime}")
        print(f"  Cloud cover: {scene.cloud_cover:.1f}%")
        print(f"  Platform:    {scene.platform}")
        print(f"  Tile:        {scene.tile_id}")
        print(f"  EPSG:        {scene.epsg}")
        print(f"  BBOX:        {scene.bbox}")
        print()

        # Band availability
        print(f"  Band availability:")
        for band_key, meta in KEY_BANDS.items():
            available = scene.bands_available.get(band_key, False)
            status = "[Y]" if available else "[N]"
            gsd_label = f"{meta['gsd_m']}m"
            print(f"    {status}  {band_key:<8}  ({meta['sentinel_band']}, native {gsd_label})")

        print()
        print(f"  RGB + NIR usable:     {'YES' if has_rgb_nir(scene) else 'NO'}")
        print(f"  SWIR available:       {'YES' if has_swir(scene) else 'NO'}")
        print(f"  Visual composite:     {'YES' if has_visual_composite(scene) else 'NO'}")
        print()

        # Show asset URLs for first scene only
        if i == 1:
            print(f"  Asset URLs (scene 1 only):")
            for key, asset in sorted(scene.assets.items()):
                gsd_str = f" ({asset.gsd}m)" if asset.gsd else ""
                print(f"    {key:<12} {asset.title}{gsd_str}")
                print(f"               {asset.href[:100]}...")
            print()

    print("=" * 72)
    print("  Probe complete. Data discovery verified.")
    print("  This probe does NOT perform spectral analysis,")
    print("  change detection, or construction detection.")
    print("=" * 72)


if __name__ == "__main__":
    main()
