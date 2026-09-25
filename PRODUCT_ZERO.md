# PRODUCT_ZERO.md — Product Zero (MVP) Specification

> Last updated: 2026-09-25  
> Status: `[CONFIRMED]` Product Experience Lock  

---

## 1. Product Zero Scope & Objective

**Product Zero** is the minimum end-to-end implementation of TerraSeek that completely proves the product thesis:

> *"Semantic investigation + evidence-backed change analysis."*

It delivers a complete, inspectable **Evidence Path** for a single high-priority operational workflow without requiring external cloud services, proprietary APIs, or bloated secondary features.

---

## 2. The 10-Step Golden Path

Every interaction in Product Zero strictly follows this 10-step sequence:

```text
[1. SEARCH]         Analyst enters natural language investigation intent & optional spatial/temporal bounds.
       │
[2. RESULTS]        System parses intent into hard/soft constraints & returns ranked candidate cards.
       │
[3. CANDIDATE]      Analyst selects a candidate observation scene for detailed inspection.
       │
[4. EVIDENCE]       System loads evidence summary explaining WHY this result was surfaced.
       │
[5. BEFORE/AFTER]   Analyst opens synchronized split/swipe visual comparison of T1 and T2 observations.
       │
[6. TIMELINE]       Analyst inspects multi-date observation persistence across the temporal series.
       │
[7. CHANGE MASK]    System renders inspectable change overlay (spectral + semantic diff).
       │
[8. VERIFY]         Analyst evaluates potential confounders (clouds, seasons) & sets verification status.
       │
[9. PROVENANCE]     Analyst expands provenance trace to inspect source STAC IDs, sensor, & processing.
       │
[10. EXPORT]        Analyst exports a self-contained, reproducible Evidence Package (JSON/PDF).
```

---

## 3. Feature-by-Feature Scope Matrix

| Feature Domain | IN Product Zero `[CONFIRMED]` | OUT of Product Zero `[CONSTRAINT]` |
|---|---|---|
| **Query & Search** | • NL intent parsing<br>• Structured spatial/temporal constraint extraction<br>• Multi-collection candidate generation (Sentinel-2, Landsat)<br>• Semantic + spatial reranking | • Conversational multi-turn chatbot<br>• Voice search<br>• Automated daily alert subscriptions |
| **Data Ingest & Storage** | • STAC API adapter (Local/Public STAC)<br>• Cloud-Optimized GeoTIFF (COG) reader<br>• Local disk asset caching<br>• Offline synthetic/cached dataset fallback | • Live real-time satellite stream ingestion<br>• Commercial satellite tasking APIs<br>• Proprietary vendor paywalls |
| **Visual Comparison** | • Synchronized dual-map viewport<br>• Interactive swipe / split divider<br>• Opacity slider overlay<br>• RGB & Spectral index rendering (NDVI, NDWI) | • Decorative 3D globe visualization<br>• VR/AR visualization modes<br>• Arbitrary canvas annotation painting |
| **Evidence & Analytics** | • Multi-channel evidence decomposition table<br>• Temporal persistence timeline (multi-date series)<br>• Explicit confounder check (clouds, seasonality, registration)<br>• Inspectable change mask overlay | • Uncalibrated "92% AI Confidence" badge<br>• Black-box LLM narrative generation<br>• Predictive future activity forecasting |
| **Verification & Provenance** | • Analyst decision recording (Accept / Reject / Uncertain)<br>• Interactive Provenance Drawer (Scene ID, Processing, Model)<br>• Reproducible JSON Evidence Package export | • Blockchain verification ledgers<br>• Multi-user team live collaborative cursor editing |

---

## 4. Failure State Handling Rules

### 4.1 No Relevant Results `[CONFIRMED]`
- **System Behavior**: Do not show a blank screen or vague error.
- **UI Output**: Display explicit diagnostic breakdown:
  - *No imagery matching cloud threshold (< 15%) in temporal window.*
  - *Suggested Action*: Expand temporal window by 30 days or increase cloud tolerance to 25%.

### 4.2 Cloud / Artifact Contamination `[CONFIRMED]`
- **System Behavior**: Detect quality mask flags in STAC metadata.
- **UI Output**: Display prominent Warning Banner:
  - ⚠️ *"High cloud cover detected (38%). Spectral change analysis in affected pixels marked unreliable."*

### 4.3 Weak Change Evidence `[CONFIRMED]`
- **System Behavior**: When spectral and semantic signals conflict.
- **UI Output**: Render status as `INSUFFICIENT EVIDENCE`:
  - *"Apparent change signal is weak and matches seasonal vegetation variation. Flagged for analyst verification."*

### 4.4 Model / LLM Offline `[CONFIRMED]`
- **System Behavior**: Fall back gracefully to local deterministic search.
- **UI Output**: Display fallback indicator:
  - ℹ️ *"AI semantic engine offline. Running in Deterministic Mode (STAC Metadata + NDVI difference)."*

---

## 5. Offline-First & Deterministic Fallback Specification

```text
                     ┌───────────────────────────┐
                     │ User Inquiry / Search Intent │
                     └─────────────┬─────────────┘
                                   │
                     Is LLM / Vector Store Online?
                                  ╱ ╲
                                 ╱   ╲
                           YES  ╱     ╲  NO
                               ╱       ╲
                              ▼         ▼
                    ┌─────────────────┐ ┌───────────────────┐
                    │ AI Agent Engine │ │ Deterministic     │
                    │ Semantic Search │ │ STAC Metadata +   │
                    │ & Vector Rerank │ │ BBOX / Date Filter│
                    └────────┬────────┘ └─────────┬─────────┘
                             │                    │
                             └──────────┬─────────┘
                                        │
                                        ▼
                             ┌─────────────────────┐
                             │ Evidence Rendering  │
                             │ & Multi-Channel UI  │
                             └─────────────────────┘
```

1. **Local Storage**: All raster assets, STAC metadata, and index structures are cached on local disk (`.terraseek_cache/`).
2. **Deterministic Guarantee**: The user can perform complete investigations, before/after comparisons, and evidence exports even when disconnected from the internet.

---

## 6. Verification & Analyst Audit Protocol

Analyst decisions are **immutable provenance events**:
1. When an analyst clicks **Accept**, **Reject**, or **Mark Uncertain**, the system generates a signed audit record:
   ```json
   {
     "event_id": "evt_987654",
     "timestamp": "2026-09-25T18:34:00Z",
     "analyst_action": "VERIFIED_GENUINE_CHANGE",
     "candidate_id": "STAC_S2B_20240515_T18UYP",
     "confounders_reviewed": ["seasonality", "cloud_mask"],
     "analyst_notes": "Earthmoving equipment visible along riverbank."
   }
   ```
2. The audit record is attached directly to the exported **Evidence Package**.

---

## Related Documents

- Product Direction → [PRODUCT_DIRECTION.md](PRODUCT_DIRECTION.md)
- Primary User Journey → [USER_JOURNEY.md](USER_JOURNEY.md)
- Evidence Model → [EVIDENCE_MODEL.md](EVIDENCE_MODEL.md)
- Export Specification → [EVIDENCE_MODEL.md#5-evidence-package-data-contract](EVIDENCE_MODEL.md#5-evidence-package-data-contract)
