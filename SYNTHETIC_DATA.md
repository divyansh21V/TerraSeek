# SYNTHETIC_DATA.md — Synthetic & Test Data Strategy

> Last updated: 2026-09-25
> Status: Draft — no synthetic data exists yet

---

## 1. Purpose

TerraSeek needs synthetic data for:
1. **Development** — Work without real satellite imagery downloads
2. **Testing** — Deterministic, fast, version-controlled fixtures
3. **Demos** — Showcase functionality without API keys or bandwidth
4. **AI evaluation** — Golden datasets for prompt/agent testing

---

## 2. Synthetic Data Categories

### 2.1 Synthetic Satellite Imagery

| Data Type | Format | Description | Status |
|---|---|---|---|
| RGB scene | GeoTIFF (COG) | 3-band raster, ~512x512 px, realistic CRS | `[ASSUMPTION]` |
| Multispectral | GeoTIFF | Sentinel-2 band layout (13 bands) | `[ASSUMPTION]` |
| SAR | GeoTIFF | Single band, float32, backscatter values | `[OPEN QUESTION]` |
| DEM | GeoTIFF | Single band, float32, elevation values | `[OPEN QUESTION]` |
| Cloud mask | GeoTIFF | Binary mask, uint8 | `[ASSUMPTION]` |

Generation approach:
- Use `rasterio` + `numpy` to generate programmatic rasters
- Include realistic GeoTransform and CRS metadata
- Keep files small (< 1 MB each)
- Store in `tests/fixtures/rasters/`

### 2.2 Synthetic STAC Responses

| Data Type | Format | Description |
|---|---|---|
| STAC Item | JSON | Single search result with metadata |
| STAC ItemCollection | JSON | Multi-result search response |
| STAC Collection | JSON | Catalog collection metadata |

Generation approach:
- Hand-craft realistic JSON following STAC 1.0 spec
- Include geometry, temporal extent, band metadata
- Store in `tests/fixtures/stac/`

### 2.3 Query Evaluation Dataset

| Data Type | Format | Description |
|---|---|---|
| NL queries → structured intent | JSONL | Golden dataset for intent extraction |
| NL queries → expected tools | JSONL | Expected tool calls for each query |
| NL queries → expected results | JSONL | Expected analysis output |

Example entry:
```json
{
  "query": "Show NDVI changes in Kerala mangroves between 2023 and 2024",
  "expected_intent": {
    "analysis_type": "temporal_comparison",
    "index": "ndvi",
    "location": "Kerala mangroves",
    "time_range": ["2023-01-01", "2024-12-31"]
  },
  "expected_tools": ["search_catalogs", "download_asset", "compute_index", "compare_temporal"],
  "difficulty": "medium"
}
```

Store in `tests/fixtures/eval/`

---

## 3. Synthetic Data Generation Scripts

`[ASSUMPTION]` Location: `scripts/generate_fixtures.py`

Scripts needed:
1. `generate_rasters.py` — Create synthetic GeoTIFFs
2. `generate_stac_responses.py` — Create mock STAC catalog responses
3. `generate_eval_dataset.py` — Create/validate AI evaluation datasets

---

## 4. Real Data Snapshots

For integration tests that need realistic (but small) data:
- Download a real 256x256 crop of Sentinel-2 data
- Strip to 3 bands for size
- Anonymize location metadata if needed
- Store in `tests/fixtures/snapshots/`
- Document the source and license

`[OPEN QUESTION]` Which real datasets to snapshot?

---

## 5. Data Versioning

- All fixture data is version-controlled in Git
- Maximum individual file size: 5 MB `[ASSUMPTION]`
- Use Git LFS for anything larger `[OPEN QUESTION]`
- Include a `tests/fixtures/README.md` describing each fixture

---

## Related Documents

- Testing → [TESTING.md](TESTING.md)
- Data model → [DATA_MODEL.md](DATA_MODEL.md)
- AI evaluation → [AI_SYSTEM.md](AI_SYSTEM.md)
# Synthetic data contract

The implementation contract derived from the Sentinel-2 research thesis is maintained in [`docs/SENTINEL2_SYNTHETIC_DATA_SPEC.md`](docs/SENTINEL2_SYNTHETIC_DATA_SPEC.md). It is the source of truth for synthetic provenance, band/resolution handling, quality masks, indices, ground truth, and validation gates.
