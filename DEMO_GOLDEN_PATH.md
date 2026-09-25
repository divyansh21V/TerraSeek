# DEMO_GOLDEN_PATH.md — 3-Minute Demonstration Script & Golden Path

> Last updated: 2026-09-25  
> Status: `[CONFIRMED]` Product Experience Lock  

---

## 1. Demo Overview & Narrative Arc

### The Goal
Demonstrate to judges or stakeholders in exactly **180 seconds** that TerraSeek is an **offline, provenance-aware Earth-observation evidence engine** that transforms a natural language inquiry into a defensible evidence path.

### The Demonstration Scenario
- **Investigative Scenario**: Unflagged earthmoving & illegal mining activity along the Tapajós River, Amazon Basin.
- **Dataset**: Pre-indexed Sentinel-2 L2A time-series (Baseline: Feb 2023 | Observation: April 2024).

---

## 2. Minute-by-Minute Script & UI Walkthrough

```text
0:00 ───────────── 0:40 ───────────── 1:20 ───────────── 2:00 ───────────── 2:40 ───────────── 3:00
[NARRATIVE LOCK]   [CANDIDATE DISCOVERY] [BEFORE/AFTER SWIPE] [EVIDENCE & CONFO] [PROVENANCE & EXPORT]
Thesis & Problem   STAC Intent Parsing   Synchronized GeoTIFF Multi-Channel Dec  JSON Package Download
```

---

### Minute 1: The Thesis & Semantic Search (0:00 – 1:00)

#### 0:00 – 0:20: Opening & Thesis Lock
- **Presenter Voiceover**:
  > *"Most satellite tools fall into two traps: they are either complex GIS software requiring expert manual script writing, or generic AI chatbots that output unverified summaries. TerraSeek is different: it is an offline, provenance-aware evidence engine for Earth observation."*
- **Visual State**: Screen 1 (Landing Screen) displaying TerraSeek header, clear mission statement, and realistic prompt cards.

#### 0:20 – 0:40: Natural Language Query Submission
- **Presenter Action**: Clicks realistic example card: *"Find newly built structures near a river in the Amazon Basin (Jan 2023 - May 2024)."*
- **Presenter Voiceover**:
  > *"Instead of writing manual STAC API syntax, the analyst states their investigative intent in natural language."*
- **Visual State**: Query input populates; system parses intent into structured constraint pills: `[Semantic: construction_near_waterbody]`, `[BBOX: Amazon Basin]`, `[Date: 2023-01-01 to 2024-05-31]`, `[Cloud < 15%]`.

#### 0:40 – 1:00: Candidate Discovery & Evidence Card
- **Presenter Action**: Hits Enter / clicks "Investigate".
- **Presenter Voiceover**:
  > *"TerraSeek executes hard spatial and temporal constraints first, then ranks candidates using semantic vector similarity. Notice that every candidate card answers one fundamental question: 'Why is this result here?'"*
- **Visual State**: Screen 2 loads candidate list on left, vector map on right. Candidate #1 displays evidence tags: `High Semantic Match (0.88)`, `Exact Spatial Match (Riverbank)`, `Cloud Cover: 2.1%`.

---

### Minute 2: Visual Workbench & Multi-Channel Evidence (1:00 – 2:00)

#### 1:00 – 1:30: Synchronized Before/After Swipe Workbench
- **Presenter Action**: Clicks "Open Visual Workbench" on Candidate #1.
- **Presenter Voiceover**:
  > *"Selecting a candidate opens the Visual Workbench. Here we have synchronized dual Cloud-Optimized GeoTIFFs: Feb 10, 2023 on the left, and April 12, 2024 on the right. Dragging the interactive swipe reveals clear forest clearing and earthmoving along the riverbank."*
- **Visual State**: Screen 3 renders synchronized dual-map viewport with interactive swipe divider sliding smoothly across the spatial change area.

#### 1:30 – 2:00: Multi-Channel Evidence & Timeline Persistence
- **Presenter Action**: Toggles "Render Change Mask" and points to Evidence Decomposition drawer at bottom.
- **Presenter Voiceover**:
  > *"TerraSeek never outputs a black-box '92% AI confidence' badge. Instead, it decomposes evidence into inspectable channels: a +0.42 NDBI spectral shift, high semantic match, and multi-date temporal persistence across 3 consecutive post-event observations."*
- **Visual State**: High-contrast green change mask overlays viewport; Evidence Decomposition table displays Spectral, Semantic, Temporal, and Spatial score breakdown.

---

### Minute 3: Verification, Provenance & Export (2:00 – 3:00)

#### 2:00 – 2:30: False-Alarm Confounder Review & Analyst Verification
- **Presenter Action**: Clicks "Review Confounders" in right drawer, then clicks `[VERIFY: Genuine Activity]`.
- **Presenter Voiceover**:
  > *"Crucially, TerraSeek helps analysts rule out false alarms. The Confounder Panel automatically verifies that this change is not a seasonal water level shift or cloud shadow artifact. The analyst explicitly verifies the result, creating an immutable audit event."*
- **Visual State**: Screen 4 drawer opens. Confounder panel shows low risk ratings; analyst clicks Verify button; status converts to green `VERIFIED`.

#### 2:30 – 3:00: Provenance Drawer & Evidence Package Export
- **Presenter Action**: Clicks "Inspect Provenance" tree node, then clicks "Export Evidence Package".
- **Presenter Voiceover**:
  > *"Finally, every result is fully inspectable back to source provider STAC IDs, GDAL reprojection parameters, and model versions. In one click, the analyst exports a reproducible JSON Evidence Package."*
- **Visual State**: Provenance tree renders complete audit trail; JSON download triggers (`terraseek_evidence_package.json`).

---

## 3. Pre-Conditions & Demo Dataset Setup

To guarantee a flawless live demonstration:
1. **Pre-Cached Datasets `[CONFIRMED]`**: Sentinel-2 L2A scenes for Amazon Basin (`T18UYP`) cached locally in `.terraseek_cache/` to eliminate network dependencies.
2. **Pre-Computed Vectors**: Pre-calculated embeddings for the candidate scenes stored in local sqlite/vector store.
3. **Deterministic Mode Ready**: If LLM API fails during live demo, system automatically switches to local deterministic keyword + STAC filter mode without breaking the UI flow.

---

## 4. Live Demo Contingency Plan

| Failure Mode | Detection | Automated Recovery / Presenter Action |
|---|---|---|
| **Network Interruption** | API call timeout (> 2s) | System operates 100% offline from local `.terraseek_cache/`. Presenter highlights: *"As you can see, TerraSeek runs completely offline."* |
| **LLM Provider Rate Limit** | HTTP 429 from LLM API | Fallback engine uses local keyword intent parser. UI displays `Deterministic Intent Mode`. |
| **GPU/Model Memory Spike** | Model inference delay | System serves pre-calculated embedding similarity scores from local cache. |

---

## Related Documents

- Product Direction → [PRODUCT_DIRECTION.md](PRODUCT_DIRECTION.md)
- Product Zero Spec → [PRODUCT_ZERO.md](PRODUCT_ZERO.md)
- Information Architecture → [INFORMATION_ARCHITECTURE.md](INFORMATION_ARCHITECTURE.md)
- Design Acceptance → [DESIGN_ACCEPTANCE.md](DESIGN_ACCEPTANCE.md)
