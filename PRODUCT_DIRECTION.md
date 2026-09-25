# PRODUCT_DIRECTION.md — TerraSeek Product Direction & Strategy

> Last updated: 2026-09-25  
> Status: `[CONFIRMED]` Product Experience Lock  

---

## 1. Executive Summary & One-Liner

**TerraSeek** is an offline-capable, provenance-aware Earth-observation (EO) evidence engine. It enables defense, environmental, and infrastructure analysts to discover relevant satellite imagery by semantic meaning, compare observations across time, suppress predictable false alarms, and inspect every step of the analytical pipeline.

---

## 2. Product Thesis vs. Anti-Positioning

### 2.1 The Core Thesis `[CONFIRMED]`
> **TerraSeek is an offline, provenance-aware Earth-observation evidence engine that helps analysts discover relevant satellite imagery by meaning, compare observations across time, suppress predictable false alarms, and inspect why a result was surfaced.**

The core conceptual unit of TerraSeek is the **EVIDENCE PATH**:
```text
Source Observation 
  └──> Preprocessing & Calibration
        └──> Hard Constraints & Retrieval
              └──> Semantic & Spatial Ranking
                    └──> Temporal Comparison
                          └──> Multi-Channel Evidence Signals
                                └──> Analyst Verification & Decision
```

### 2.2 What TerraSeek Is NOT (Anti-Positioning) `[CONSTRAINT]`
To maintain clarity and operational utility, TerraSeek explicitly rejects the following positioning:
- ❌ **NOT a Generic AI Chatbot**: It is not a conversational "ask me anything" box. Text input is an intent parser for geospatial parameters.
- ❌ **NOT a Satellite Marketplace**: It does not focus on buying imagery, credit billing, or commercial vendor negotiations.
- ❌ **NOT a Generic GIS Dashboard**: It is not a cluttered cockpit of 50 layer toggles, GIS widgets, and raw vector layers.
- ❌ **NOT a Vector Database UI**: It does not expose raw embedding vectors, distance matrices, or uncalibrated similarity math to the analyst by default.
- ❌ **NOT a Simple Image-Difference Tool**: It does not equate raw pixel subtraction (\(I_2 - I_1\)) with real-world activity or change.
- ❌ **NOT "ChatGPT for Satellites"**: It does not generate unverified text narratives or hallucinated summaries detached from underlying raster assets.

---

## 3. Primary User Persona

### 3.1 The EO-Capable Analyst / Researcher `[CONFIRMED]`
- **Domain Understanding**: Understands real-world investigation objectives (e.g., tracking illegal riverbank mining, verifying facility construction, monitoring flood extents, observing port activity).
- **Technical Literacy**: Understands basic geospatial concepts (AOI, acquisition date, cloud cover, spatial resolution, sensor types), but does **not** want to write manual Python scripts, configure STAC API parameters, or manage GDAL reprojections just to start an investigation.
- **Core Job-to-Be-Done**:
  > *"Help me find relevant observations and determine whether the apparent change is meaningful, while letting me inspect the evidence and prove how the conclusion was reached."*

### 3.2 Secondary Personas (Out of Scope for Product Zero UX) `[CONSTRAINT]`
- Developers & Data Engineers (Serviced via SDK/REST API, not Product Zero UI).
- Administrators & Executives (Serviced via exported evidence reports).

---

## 4. Problem & Solution Paradigm

| Legacy Analyst Workflow | TerraSeek Evidence Engine Workflow |
|---|---|
| Manual STAC catalog queries with rigid spatial/temporal bounds | Natural language query converted to structured hard + soft constraints |
| Browsing hundreds of scenes with high cloud cover or seasonal noise | Semantic retrieval combined with automatic quality & contextual filtering |
| Calculating manual pixel differences in desktop GIS tools | Automated multi-channel evidence decomposition (Spectral + Semantic + Object + Temporal) |
| High false-alarm rate caused by clouds, shadows, and seasonal shifts | Explicit confounder analysis (illumination, view angle, registration, seasonality) |
| Opaque "black box" automated detection outputs | Step-by-step inspectable evidence path with full data provenance |
| Screenshots pasted into static slide decks | Exportable, reproducible evidence objects with audit trails |

---

## 5. System Boundaries & Operating Constraints

1. **Offline-Capable `[CONSTRAINT]`**: The core engine must run locally without cloud dependencies once data assets are retrieved or pre-indexed.
2. **Deterministic Fallback `[CONSTRAINT]`**: If LLM or embedding services fail or are offline, hard geospatial, temporal, and spectral filtering remains fully functional.
3. **Calibrated Evidence `[CONSTRAINT]`**: The system shall never present uncalibrated "AI Confidence: 92%" scores. All findings are broken down into inspectable evidence channels.
4. **No Fabricated Evidence `[CONSTRAINT]`**: If imagery is ambiguous, cloud-covered, or missing, TerraSeek explicitly flags "Insufficient Evidence" rather than generating speculative conclusions.

---

## 6. Design Aesthetics & Visual Tone `[CONFIRMED]`

- **Tone**: Scientific, operational, precise, calm, spatial, trustworthy.
- **Visual Palette**: Dark mode by default (slate gray `#0F172A`, deep navy `#020617`, muted silver `#94A3B8`, precise accent cyan `#0EA5E9`, emerald status green `#10B981`, amber warning `#F59E0B`).
- **Typography**: Clean, highly readable sans-serif (Inter / Roboto) paired with monospace (JetBrains Mono / Fira Code) for coordinates, timestamps, and STAC IDs.
- **Forbidden Aesthetics**: No neon cyberpunk, no generic AI blue/purple gradients, no glassmorphism blur, no decorative 3D spinning globes, no giant empty hero banners.

---

## 7. Answers to the 14 Critical Self-Interrogations

1. **Solving a user problem or exposing architecture?**  
   *Solving a user problem.* The architecture is hidden behind an operational workflow and only revealed when the analyst explicitly opens the Provenance Drawer.

2. **What would the analyst do manually without TerraSeek?**  
   *Manually query STAC catalogs, download full GeoTIFFs, load them into QGIS/ArcGIS, manually align bands, run band math, and visually inspect for false alarms.*

3. **Which step does TerraSeek remove?**  
   *Removes manual STAC query formulation, band combination setup, and preliminary false-alarm screening.*

4. **Which step does TerraSeek merely automate?**  
   *Automates image registration, spectral index calculation, temporal alignment, and multi-scene comparison.*

5. **What could TerraSeek confidently get wrong?**  
   *Mistaking extreme seasonal shifts (e.g., snowmelt or dry-season riverbeds) or off-nadir sensor registration offsets for man-made changes.*

6. **How does the analyst discover that it is wrong?**  
   *Via the explicit Confounder Analysis panel, which flags seasonality, illumination, and view-angle differences alongside the raw before/after observations.*

7. **Why would the user trust a result?**  
   *Because every result provides a complete evidence breakdown, raw synchronized before/after imagery, and a 1-click provenance trace back to the source provider scene.*

8. **Can every important result be traced backward?**  
   *Yes. Result -> Change Evidence -> Processing Job -> Source STAC Item -> Provider.*

9. **Can a technically sophisticated user inspect the pipeline?**  
   *Yes. Opening Expert Mode reveals raw STAC JSON, model versions, index parameters, and raw band statistics.*

10. **Can a judge understand the innovation without remote sensing knowledge?**  
    *Yes. The 60-second comprehension flow demonstrates natural language inquiry turning directly into a clean before/after comparison with clear "Why this result" evidence tags.*

11. **What is the smallest end-to-end experience that proves the thesis?**  
    *Product Zero: A single NL query -> candidate selection -> before/after swipe -> evidence decomposition -> verification -> JSON export.*

12. **If we removed AI branding, would the workflow still be valuable?**  
    *Extremely valuable. The structured evidence path, temporal alignment, false-positive breakdown, and provenance tracking solve major operational headaches regardless of AI.*

13. **If another team copied our UI, what advantage remains?**  
    *Our multi-channel evidence model, deterministic fallback architecture, and provenance graph structure.*

14. **Are we building a search engine, an analysis tool, or an evidence system?**  
    *An evidence system. Search and analysis are sub-components in service of building a defensible evidence path.*

---

## Related Documents

- MVP Specification → [PRODUCT_ZERO.md](PRODUCT_ZERO.md)
- Primary User Journey → [USER_JOURNEY.md](USER_JOURNEY.md)
- Information Architecture → [INFORMATION_ARCHITECTURE.md](INFORMATION_ARCHITECTURE.md)
- Evidence Model → [EVIDENCE_MODEL.md](EVIDENCE_MODEL.md)
