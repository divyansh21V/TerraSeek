# EVIDENCE_MODEL.md — Evidence Model & Provenance Schema

> Last updated: 2026-09-25  
> Status: `[CONFIRMED]` Product Experience Lock  

---

## 1. Evidence Engine Philosophy

TerraSeek rejects opaque "black box" machine learning metrics (e.g., `"AI Confidence: 92%"`). In operational remote sensing, uncalibrated probability scores are dangerous and indefensible.

Instead, TerraSeek treats every finding as an **Evidence Decomposition** composed of six distinct, inspectable evidence channels:

```text
                               ┌───────────────────────────┐
                               │   TERRASEEK RESULT CARD   │
                               └─────────────┬─────────────┘
                                             │
      ┌──────────────┬──────────────┬────────┴─────┬──────────────┬──────────────┐
      ▼              ▼              ▼              ▼              ▼              ▼
┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐
│ SPECTRAL  │  │ SEMANTIC  │  │ TEMPORAL  │  │  SPATIAL  │  │  QUALITY  │  │CONFOUNDER │
│  SIGNAL   │  │  MATCH    │  │PERSISTENCE│  │ MATCH /AOI│  │ ASSURANCE │  │ RISK CHECK│
└───────────┘  └───────────┘  └───────────┘  └───────────┘  └───────────┘  └───────────┘
```

---

## 2. Multi-Channel Evidence Taxonomy

### 2.1 Channel 1: Spectral Signal
- **Definition**: Quantifiable change in surface reflectance between baseline (T1) and observation (T2).
- **Metrics**: Normalized Difference Vegetation Index (\(\Delta\text{NDVI}\)), Normalized Difference Water Index (\(\Delta\text{NDWI}\)), NDBI (Built-up Index).
- **UX Display**:
  - `Spectral Diff: STRONG (+0.42 NDBI shift)`
  - Visual color bar indicating magnitude and index direction.

### 2.2 Channel 2: Semantic Match
- **Definition**: Vector similarity between the user's natural language query intent and the multi-modal visual embeddings of the scene.
- **Metrics**: Cosine similarity in calibrated embedding space.
- **UX Display**:
  - `Semantic Match: HIGH (0.88 cosine)`
  - Tag: `"Matches 'Earthmoving / Construction' feature pattern"`

### 2.3 Channel 3: Temporal Persistence
- **Definition**: Verification that the detected change persists across multiple subsequent observation dates, ruling out transient artifacts.
- **Metrics**: Number of supporting post-event scenes out of total available scenes.
- **UX Display**:
  - `Temporal Persistence: VERIFIED (3 of 3 post-event scenes show structure)`

### 2.4 Channel 4: Spatial Match & AOI Context
- **Definition**: Precision of spatial alignment between the detected candidate and the user's target AOI or proximity buffers (e.g., riverbanks, coastlines, roads).
- **Metrics**: Distance in meters from target vector geometry.
- **UX Display**:
  - `Spatial Match: EXACT (Within 120m of river geometry)`

### 2.5 Channel 5: Quality Assurance
- **Definition**: Assessment of sensor quality, atmospheric clarity, and resolution suitability.
- **Metrics**: STAC `eo:cloud_cover`, solar azimuth angle, spatial resolution (meters/pixel).
- **UX Display**:
  - `Image Quality: OPTIMAL (Cloud cover 1.8% | 10m Ground Sample Distance)`

### 2.6 Channel 6: Confounder & False Alarm Risk
- **Definition**: Automated evaluation of environmental and sensor factors that commonly produce false positives.
- **Metrics**: Risk ratings for cloud shadow, seasonality, illumination shift, and registration offset.
- **UX Display**:
  - `Confounder Risk: LOW (Seasonality risk 0.05 | Shadow risk 0.02)`

---

## 3. Confounder & False-Alarm Risk Matrix

| Confounder Category | Physical Cause | Automated System Check | System UX Warning Output |
|---|---|---|---|
| **Cloud & Shadow** | Clouds or terrain shadows blocking surface | Quality assessment mask (SCL/QA band) inspection | ⚠️ *"Cloud/shadow contamination detected in 14% of candidate pixels. Affected area masked."* |
| **Seasonality** | Vegetation green-up/browning or dry riverbeds | Multi-year historical NDVI baseline comparison for same month | ⚠️ *"High Seasonality Risk: Change matches historical dry-season pattern (Aug 2021-2023)."* |
| **Illumination Angle** | Solar elevation/azimuth shift between winter/summer | STAC solar elevation angle delta computation (\(\Delta\theta > 15^\circ\)) | ℹ️ *"Illumination difference: Solar elevation shift of 18.4° detected between T1 and T2."* |
| **Registration Offset** | Misalignment of pixels between T1 and T2 GeoTIFFs | Cross-correlation registration check on static land features | ⚠️ *"Registration Error: 2.1 pixel spatial shift detected. Re-alignment recommended."* |
| **Sensor Mismatch** | Comparing Sentinel-2 (Optical) directly to Landsat-8 without normalization | Sensor spectral response function harmonization check | ℹ️ *"Cross-sensor comparison (Sentinel-2 vs Landsat-8). Band normalization applied."* |

---

## 4. Provenance Chain Architecture

Every evidence finding is backed by an unalterable **Provenance Trace** linking the final analyst decision back to raw provider assets:

```text
[SOURCE PROVIDER]       Copernicus Open Access Hub / AWS STAC Registry
       │
       ▼
[SOURCE STAC ITEM]      S2B_MSIL2A_20240412T142729_N0510_R097_T18UYP
       │
       ▼
[PREPROCESSING RUN]     COG Fetch -> Band Stack -> GDAL Warp (EPSG:4326) -> Cloud Mask
       │
       ▼
[INDEXING & MODEL]      TerraSeek Embedder v1.2 (Model Checksum: `sha256:e3b0c442...`)
       │
       ▼
[QUERY EXECUTION]       Job ID: `job_884920` (Query: "Construction near river")
       │
       ▼
[EVIDENCE SCORING]      Spectral: 0.82 | Semantic: 0.88 | Temporal: 3/3 | Confounder Risk: Low
       │
       ▼
[ANALYST DECISION]      Verified by `analyst_id_402` at `2026-09-25T18:34:00Z` (Status: ACCEPT)
```

---

## 5. Evidence Package Data Contract (Export Schema)

When an analyst exports an investigation, TerraSeek generates a standardized JSON payload conforming to this schema:

```json
{
  "$schema": "https://terraseek.io/schemas/v1/evidence-package.json",
  "investigation_id": "inv_20260925_001",
  "created_at": "2026-09-25T18:34:00Z",
  "terraseek_version": "0.1.0",
  "query": {
    "raw_text": "Find newly built structures near a river between Jan 2023 and May 2024",
    "parsed_intent": "construction_near_waterbody",
    "spatial_extent_geojson": {
      "type": "Polygon",
      "coordinates": [[[-60.1, -3.2], [-60.1, -3.0], [-59.9, -3.0], [-59.9, -3.2], [-60.1, -3.2]]]
    },
    "temporal_range": {
      "start": "2023-01-01T00:00:00Z",
      "end": "2024-05-31T23:59:59Z"
    }
  },
  "selected_candidate": {
    "stac_item_id": "S2B_MSIL2A_20240412T142729_N0510_R097_T18UYP",
    "provider": "Copernicus",
    "collection": "sentinel-2-l2a",
    "acquisition_time": "2024-04-12T14:27:29Z",
    "cloud_cover_percentage": 2.1
  },
  "baseline_candidate": {
    "stac_item_id": "S2A_MSIL2A_20230210T142729_N0510_R097_T18UYP",
    "provider": "Copernicus",
    "collection": "sentinel-2-l2a",
    "acquisition_time": "2023-02-10T14:27:29Z",
    "cloud_cover_percentage": 1.2
  },
  "evidence_signals": {
    "spectral_change": {
      "metric": "NDBI_delta",
      "score": 0.42,
      "interpretation": "Strong built-up signal increase"
    },
    "semantic_match": {
      "model": "terraseek-geo-embed-v1",
      "cosine_similarity": 0.88,
      "interpretation": "High semantic match for construction pattern"
    },
    "temporal_persistence": {
      "supporting_scenes_count": 3,
      "total_scenes_evaluated": 3,
      "is_persistent": true
    },
    "confounders": {
      "cloud_shadow_risk": "low",
      "seasonality_risk": "low",
      "registration_offset_pixels": 0.25
    }
  },
  "analyst_verification": {
    "status": "ACCEPTED_GENUINE_CHANGE",
    "timestamp": "2026-09-25T18:34:00Z",
    "notes": "Earthmoving equipment confirmed along eastern bank."
  },
  "provenance_chain": {
    "processing_job_id": "job_884920",
    "pipeline_steps": [
      "COG_FETCH",
      "BAND_STACK",
      "GDAL_WARP_EPSG4326",
      "SPECTRAL_DIFF_CALC",
      "EMBEDDING_RERANK"
    ],
    "model_checksum": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  }
}
```

---

## Related Documents

- Product Direction → [PRODUCT_DIRECTION.md](PRODUCT_DIRECTION.md)
- Product Zero Spec → [PRODUCT_ZERO.md](PRODUCT_ZERO.md)
- Information Architecture → [INFORMATION_ARCHITECTURE.md](INFORMATION_ARCHITECTURE.md)
- Design Acceptance → [DESIGN_ACCEPTANCE.md](DESIGN_ACCEPTANCE.md)
