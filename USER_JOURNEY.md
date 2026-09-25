# USER_JOURNEY.md — Primary User Journey & Mental Model Mapping

> Last updated: 2026-09-25  
> Status: `[CONFIRMED]` Product Experience Lock  

---

## 1. User Mental Model vs. System Execution Mapping

The analyst must **never** be forced to think like the internal backend services. TerraSeek maps the analyst's natural investigative questions directly to precise internal processing stages:

```text
ANALYST MENTAL MODEL                     SYSTEM EXECUTION PIPELINE
┌───────────────────────────┐            ┌───────────────────────────┐
│ "Find me places like this"│ ─────────> │ Intent Extraction & STAC  │
│                           │            │ Semantic / Vector Rerank  │
└─────────────┬─────────────┘            └─────────────┬─────────────┘
              │                                        │
              ▼                                        ▼
┌───────────────────────────┐            ┌───────────────────────────┐
│ "Why did you show me this?"│ ─────────> │ Evidence Scoring Engine   │
│                           │            │ (Semantic, Spatial, Date) │
└─────────────┬─────────────┘            └─────────────┬─────────────┘
              │                                        │
              ▼                                        ▼
┌───────────────────────────┐            ┌───────────────────────────┐
│ "What changed?"           │ ─────────> │ COG Fetch & Alignment     │
│                           │            │ Spectral / Structural Diff│
└─────────────┬─────────────┘            └─────────────┬─────────────┘
              │                                        │
              ▼                                        ▼
┌───────────────────────────┐            ┌───────────────────────────┐
│ "Is this change real?"    │ ─────────> │ Confounder Analysis &     │
│                           │            │ Temporal Persistence Check│
└─────────────┬─────────────┘            └─────────────┬─────────────┘
              │                                        │
              ▼                                        ▼
┌───────────────────────────┐            ┌───────────────────────────┐
│ "Can I prove how you got  │ ─────────> │ Provenance Graph Build &  │
│  this result?"            │            │ Evidence Package Export   │
└───────────────────────────┘            └───────────────────────────┘
```

---

## 2. Step-by-Step Golden Path Journey

### Step 1: SEARCH (Investigation Initiation)
- **User Action**: The analyst lands on TerraSeek and enters a natural language query:
  > *"Find newly built structures near a river between Jan 2023 and May 2024."*
- **System Interpretation**:
  - *Semantic Intent*: New construction / earthmoving near riverbank.
  - *Hard Spatial Constraint*: Extracted river polygon / bounding box.
  - *Hard Temporal Constraint*: `2023-01-01` to `2024-05-31`.
  - *Hard Quality Constraint*: Cloud cover `< 15%`.
- **UI State**: Search bar populates parsed tokens: `[Construction near River]`, `[2023-01-01 - 2024-05-31]`, `[Cloud < 15%]`.

---

### Step 2: RESULTS (Candidate Surface)
- **User Action**: Analyst clicks "Investigate" or hits Enter.
- **System Processing**: System queries STAC catalogs, generates candidates, filters by spatial/temporal bounds, and computes semantic relevance scores.
- **UI Output**: Screen renders a split view:
  - **Left**: Ranked list of Candidate Cards showing acquisition date, sensor, thumbnail, and Evidence Tags (`High Semantic Match`, `Exact Spatial Match`, `Clean Imagery`).
  - **Right**: Overview Map displaying spatial bounding boxes of candidate scenes.

---

### Step 3: SELECT CANDIDATE (Focusing Investigation)
- **User Action**: Analyst clicks on Candidate `#1` (`Sentinel-2B, Acquired 2024-04-12, Location: Amazon Basin`).
- **System Processing**: System fetches scene STAC metadata, locates pre-event baseline scene (`Sentinel-2A, Acquired 2023-02-10`), and pre-computes raster alignment parameters.
- **UI Output**: Candidate Card expands; map centers on the selected scene frame.

---

### Step 4: EVIDENCE (Understanding Relevance)
- **User Action**: Analyst inspects the "Why This Result" panel on the selected candidate card.
- **System Output**: Multi-channel evidence tag matrix:
  ```text
  Semantic Match       High (0.88)
  Spatial Relationship Target river feature within 250m
  Temporal Span        14 months baseline-to-observation
  Scene Quality        Cloud Cover: 2.1% | Solar Angle: Optimal
  ```

---

### Step 5: BEFORE / AFTER (Visual Comparison)
- **User Action**: Analyst clicks "Open Visual Workbench".
- **System Processing**: Streams dual Cloud-Optimized GeoTIFFs (COG) for T1 (Before) and T2 (After) into viewport.
- **UI Output**: Synchronized dual-map viewport opens with interactive Swipe Divider, allowing the analyst to slide back and forth across the exact same spatial coordinates.

---

### Step 6: TIMELINE (Temporal Persistence Verification)
- **User Action**: Analyst clicks "View Temporal Series".
- **System Output**: Interactive timeline bar rendering all available scene observations between 2023 and 2024:
  ```text
  2023-02-10 ─── [Baseline: Forest cover intact]
  2023-07-15 ─── [Unchanged: Cloud free]
  2023-11-20 ─── [Weak Signal: Initial clearing detected]
  2024-04-12 ─── [Strong Signal: Structure & earthmoving visible]
  2024-05-18 ─── [Persistent: Clearing expands]
  ```

---

### Step 7: CHANGE MASK (Inspecting Spectral & Structural Diff)
- **User Action**: Analyst toggles "Render Change Overlay".
- **System Output**: Highlights change region in high-contrast emerald green (spectral index diff + building index change), masking out unchanged forest canopy.

---

### Step 8: VERIFICATION (Confounder Review & Analyst Sign-off)
- **User Action**: Analyst expands the "Confounder & False Alarm Review" tab.
- **System Check**:
  - *Cloud/Shadow Artifact*: Low risk (0.02)
  - *Seasonal Sun Angle Shift*: Reviewed (Minor illumination diff)
  - *Registration Offset*: < 0.3 pixels (Excellent)
- **Analyst Action**: Analyst selects `VERIFIED: Genuine Activity` and enters optional note: *"Earthmoving equipment confirmed along eastern bank."*

---

### Step 9: PROVENANCE (Audit Trail Inspection)
- **User Action**: Analyst clicks "Inspect Provenance".
- **System Output**: Opens slide-out drawer showing complete end-to-end chain:
  `Source STAC Item ID` → `Sensor Calibration Metadata` → `GDAL Reprojection Log` → `Vector Index Commit ID` → `Analyst Verification Event ID`.

---

### Step 10: EXPORT (Reproducible Evidence Object)
- **User Action**: Analyst clicks "Export Evidence Package".
- **System Processing**: Bundles JSON evidence payload containing raw coordinates, STAC links, evidence scores, before/after thumbnails, confounder status, and signed analyst verification into a zip archive.
- **UI Output**: Download initiates (`terraseek_evidence_investigation_20240525.json`).

---

## 3. Edge Case Journeys

### Edge Case A: High Cloud Cover Contamination
- **Trigger**: Spatial query intersects a scene with 45% cloud cover.
- **User Experience**: System renders yellow warning tag on Candidate Card: `⚠️ High Cloud Noise`. When opened, cloud mask overlay highlights affected regions in semi-transparent amber and suppresses change calculations in cloud-contaminated pixels.

### Edge Case B: Seasonal False Alarm (False Positive)
- **Trigger**: Dry-season riverbed shrinkage flagged by raw spectral diff.
- **User Experience**: Confounder Panel automatically displays alert: `⚠️ High Seasonality Risk`. System explicitly notes: *"Spectral change correlates with historical dry-season water level reduction (2021-2023 data). Recommended status: REJECT or UNCERTAIN."*

---

## 4. Expert Mode Progressive Disclosure

For advanced remote sensing specialists who want deeper inspection:
- **Default View**: Clean intent box, candidate cards, before/after swipe, simple evidence tags.
- **Expert Toggle**: Clicking "Expert View" in the header expands:
  - Raw STAC Item JSON editor
  - Band combination selector (e.g., Sentinel-2 B8/B11/B4 False Color, NDVI, NDWI)
  - Raw embedding similarity metrics & distance scores
  - Custom GDAL/Rasterio pipeline configuration parameters

---

## Related Documents

- Product Direction → [PRODUCT_DIRECTION.md](PRODUCT_DIRECTION.md)
- Product Zero Spec → [PRODUCT_ZERO.md](PRODUCT_ZERO.md)
- Information Architecture → [INFORMATION_ARCHITECTURE.md](INFORMATION_ARCHITECTURE.md)
- Evidence Model → [EVIDENCE_MODEL.md](EVIDENCE_MODEL.md)
