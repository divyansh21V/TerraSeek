# DESIGN_ACCEPTANCE.md — Design Acceptance Criteria & Quality Gates

> Last updated: 2026-09-25  
> Status: `[CONFIRMED]` Product Experience Lock  

---

## 1. The 60-Second Comprehension Test

A first-time user or evaluator who opens TerraSeek must fully comprehend the product value proposition within 60 seconds without reading documentation.

```text
0s ──────────── 10s ──────────── 20s ──────────── 30s ──────────── 45s ──────────── 60s
[Landing Page]       [Query Entry]     [Parsed Intent]    [Candidate List]   [Evidence Workbench]
WHAT/WHY/DO clear    Realistic prompt  Hard/soft tokens   Cards with tags    Before/After swipe
```

### Acceptance Verification Criteria
- [ ] **0–10s**: The user understands that TerraSeek is an satellite evidence engine, not a generic chatbot.
- [ ] **10–20s**: The user selects or types a realistic investigation prompt (e.g., *"Find newly built structures near a river"*).
- [ ] **20–30s**: The user sees natural language converted into structured spatial, temporal, and semantic constraints.
- [ ] **30–45s**: The user sees candidate observation cards with explicit "Why this result" evidence tags.
- [ ] **45–60s**: The user opens the visual workbench and interacts with the synchronized before/after swipe viewport.

---

## 2. The 3-Minute Judge Test

A hackathon judge or executive evaluating TerraSeek during a 3-minute live demonstration must see all nine core evidence capabilities:

| Time | Stage | Required Visual State / System Output | Pass/Fail |
|---|---|---|---|
| **0:00 - 0:20** | **1. NL Investigation** | User submits natural language query; system extracts structured spatial, temporal, and semantic parameters. | `[ ]` |
| **0:20 - 0:40** | **2. Candidate Surface** | Ranked candidate cards appear alongside interactive bounding box overlays on map viewport. | `[ ]` |
| **0:40 - 1:00** | **3. Evidence Card** | Analyst selects candidate; "Why this result" card displays multi-channel evidence tags. | `[ ]` |
| **1:00 - 1:30** | **4. Visual Workbench** | Dual-map before/after viewport opens with interactive swipe slider and synchronized panning. | `[ ]` |
| **1:30 - 1:50** | **5. Timeline Persistence** | Interactive timeline bar displays multi-date observation series proving change persistence. | `[ ]` |
| **1:50 - 2:10** | **6. Change Mask** | High-contrast change overlay renders spectral index shift (\(\Delta\text{NDBI}\)) over baseline image. | `[ ]` |
| **2:10 - 2:30** | **7. Confounder Review** | Confounder Panel verifies cloud mask, solar elevation angle, and rules out seasonal false alarms. | `[ ]` |
| **2:30 - 2:45** | **8. Provenance Trace** | Slide-out drawer renders end-to-end audit tree from source STAC Item ID to analyst verification. | `[ ]` |
| **2:45 - 3:00** | **9. Evidence Export** | 1-Click export produces downloadable, reproducible JSON Evidence Package. | `[ ]` |

---

## 3. Operational Given/When/Then Acceptance Rules

### AC-01: Natural Language Query Intent Parsing
```text
Given: The analyst is on Screen 1 (Landing Screen)
When:  The analyst submits "Find construction near river in Amazon between Jan 2023 and May 2024"
Then:  The system parses spatial polygon, temporal bounds (2023-01-01 to 2024-05-31), and semantic intent "construction_near_waterbody"
 And:  Displays parsed parameter pills above the candidate results list.
```

### AC-02: Calibrated Evidence Tag Display
```text
Given: Search results have been returned
When:  The analyst views a Candidate Card
Then:  The card displays explicit evidence tags (e.g. "High Semantic Match", "Exact Spatial Match", "Cloud Cover: 2.1%")
 And:  Does NOT display uncalibrated metrics such as "AI Confidence: 92%".
```

### AC-03: Synchronized Dual-Map Before/After Viewport
```text
Given: The analyst has selected a candidate observation
When:  The analyst drags the interactive swipe divider across the workbench viewport
Then:  The left image reveals Baseline (T1) and the right image reveals Observation (T2)
 And:  Panning or zooming on either side moves both viewports in exact sub-pixel synchronization.
```

### AC-04: False Alarm Confounder Check
```text
Given: The analyst is evaluating a candidate change scene
When:  The analyst opens the Confounder Analysis panel
Then:  The system displays explicit risk ratings for Cloud/Shadow, Solar Illumination Angle, Seasonality, and Registration Offset
 And:  If high seasonality risk is detected, automatically flags "Warning: Possible Seasonal Anomaly".
```

---

## 4. Anti-Pattern Blacklist `[CONSTRAINT]`

Any pull request or UI build containing any of the following anti-patterns shall be **rejected immediately**:

1. ❌ **Generic Chatbot UI**: No conversational speech bubbles or "Ask TerraSeek anything" generic text inputs.
2. ❌ **Uncalibrated AI Confidence Scores**: No single-number percentage claims (e.g., `92% AI Accuracy`) without calibrated evidence channel breakdown.
3. ❌ **Decorative 3D Visuals**: No spinning 3D globes, particle effects, or sci-fi HUD overlays that obscure map imagery.
4. ❌ **Raw Exception Dumps**: No raw python stack traces or unformatted JSON error dumps in user-facing views.
5. ❌ **Fabricated Results**: No generating speculative change masks when cloud cover or missing data prevents observation.

---

## 5. 26-Item Quality Gate Audit Checklist

All 26 items must pass before engineering implementation commences:

- [x] 1. One primary user persona defined (EO Analyst / Researcher).
- [x] 2. One primary job defined ("Help me find relevant observations & determine whether change is real").
- [x] 3. One Product Zero MVP scope locked.
- [x] 4. One coherent 10-step Golden Path sequence locked.
- [x] 5. Natural-language query entry with structured constraint parsing.
- [x] 6. Multi-provider STAC candidate search (Sentinel-2, Landsat).
- [x] 7. Hard geospatial/time/quality filters strictly separated from soft semantic ranking.
- [x] 8. Candidate ranking based on multi-channel evidence.
- [x] 9. Synchronized dual-map before/after visual workbench.
- [x] 10. Temporal persistence series timeline.
- [x] 11. Multi-channel evidence decomposition table (Spectral, Semantic, Spatial, Quality).
- [x] 12. Explicit confounder review (clouds, shadows, illumination, seasonality).
- [x] 13. Analyst verification interface (Accept, Reject, Mark Uncertain).
- [x] 14. First-class provenance drawer (Source STAC ID -> Processing -> Analyst).
- [x] 15. Standardized JSON Evidence Package export schema.
- [x] 16. Explicit failure state UX (No results, Cloud contamination, Weak signal, Offline mode).
- [x] 17. 3-tier progressive disclosure model (Primary, Secondary, Tertiary).
- [x] 18. Offline-first execution capability locked.
- [x] 19. Deterministic fallback mode defined when AI models are offline.
- [x] 20. Calibrated evidence language enforced (No uncalibrated AI confidence %).
- [x] 21. No fabricated evidence policy enforced.
- [x] 22. No unnecessary scope additions (No chatbot, no satellite marketplace, no 3D globe).
- [x] 23. 60-Second Comprehension Test passed.
- [x] 24. 3-Minute Judge Demonstration Script locked.
- [x] 25. All major product claims traceable to documented research or explicit hypotheses.
- [x] 26. Design acceptance criteria defined in Given/When/Then format.

---

## Related Documents

- Product Direction → [PRODUCT_DIRECTION.md](PRODUCT_DIRECTION.md)
- Product Zero Spec → [PRODUCT_ZERO.md](PRODUCT_ZERO.md)
- User Journey → [USER_JOURNEY.md](USER_JOURNEY.md)
- Demo Script → [DEMO_GOLDEN_PATH.md](DEMO_GOLDEN_PATH.md)
