# INFORMATION_ARCHITECTURE.md — Information Architecture & Screen Design

> Last updated: 2026-09-25  
> Status: `[CONFIRMED]` Product Experience Lock  

---

## 1. Screen Hierarchy & Navigation Map

TerraSeek uses a linear, evidence-driven navigation hierarchy. Every screen maintains context of the active investigation:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        MAIN APP HEADER                                 │
│ [TerraSeek Logo]  [Active Investigation: Amazon Mining]  [Expert Mode] │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
       ┌───────────────────────────┴───────────────────────────┐
       ▼                                                       ▼
┌──────────────────────────────┐              ┌──────────────────────────────┐
│ SCREEN 1: LANDING            │              │ SCREEN 2: DISCOVERY          │
│ • Mission Statement (WHAT)   │ ──(Submit)─> │ • Parsed Query Constraints   │
│ • Value Prop (WHY)           │              │ • Candidate Cards (Left)     │
│ • NL Query Bar (DO)          │              │ • Interactive Map (Right)    │
│ • Realistic Example Prompts  │              │ • Ranking Evidence Tags      │
└──────────────────────────────┘              └──────────────┬───────────────┘
                                                             │
                                                     (Select Candidate)
                                                             │
                                                             ▼
                                              ┌──────────────────────────────┐
                                              │ SCREEN 3: EVIDENCE WORKBENCH │
                                              │ • Dual Before/After Viewport │
                                              │ • Swipe & Opacity Controls   │
                                              │ • Evidence Decomposition     │
                                              │ • Temporal Timeline Series   │
                                              └──────────────┬───────────────┘
                                                             │
                                                    (Toggle Panel/Drawer)
                                                             │
                                       ┌─────────────────────┴─────────────────────┐
                                       ▼                                           ▼
                        ┌──────────────────────────────┐            ┌──────────────────────────────┐
                        │ SCREEN 4: VERIFICATION DRAWER│            │ SCREEN 5: EXPORT & AUDIT     │
                        │ • Confounder Analysis        │            │ • Evidence Package Summary   │
                        │ • Quality Mask Inspection    │ ──(Export)─>│ • JSON Schema Preview        │
                        │ • Accept / Reject / Uncertain│            │ • Download Archive (.ZIP)    │
                        │ • Full Provenance Graph      │            │                              │
                        └──────────────────────────────┘            └──────────────────────────────┘
```

---

## 2. Screen Specifications

### Screen 1: Investigation Landing Screen

#### Purpose
Immediately communicate **WHAT** TerraSeek is, **WHY** it is distinct, and **DO** (guide the user to start an investigation).

#### UI Structure
1. **Header Zone**:
   - Title: `TERRASEEK // Earth-Observation Evidence Engine`
   - Subtitle: `Offline-capable, provenance-aware satellite imagery investigation & temporal change verification.`
2. **Primary Action Zone (DO)**:
   - Natural Language Query Input Box (Prompt Placeholder: *"Describe the location, timeframe, and activity to investigate..."*)
   - Constraint Quick-Pills: `[AOI Polygon / Bounding Box]` | `[Date Interval]` | `[Cloud Threshold]`
3. **Realistic Example Prompt Cards**:
   - Card A: *"Find newly built structures near a river in the Amazon Basin (Jan 2023 - May 2024)."*
   - Card B: *"Identify coastal land reclamation activity near South China Sea ports over the last 3 years."*
   - Card C: *"Show evidence of flood extent changes along the Indus River between July and September 2023."*
   - Card D: *"Find similar clearing activity to Site Alpha across the Gran Chaco region."*
4. **Anti-Pattern Exclusions `[CONSTRAINT]`**:
   - NO "Ask me anything" generic chatbot placeholders.
   - NO empty hero banners or decorative spinning 3D globes.

---

### Screen 2: Discovery & Search Results View

#### Purpose
Present candidate satellite observation scenes ranked by semantic, temporal, and spatial relevance.

#### UI Structure
- **Left Panel (35% Width)**:
  - Query Interpretation Header: Shows extracted intent, bbox, date range, and sensor constraints.
  - Filter Controls: Cloud cover slider, spatial resolution selector, constellation toggle.
  - Candidate Scene List: Cards containing thumbnail, acquisition date, sensor name, resolution, cloud %, and **Why This Result** badge.
- **Right Panel (65% Width)**:
  - Map Viewport: Leaflet/Mapbox vector map rendering AOI footprint, candidate scene bounding boxes, and river/coastline vector overlays.
  - Hover Sync: Hovering over a card highlights its footprint on the map.

---

### Screen 3: Candidate Inspection & Evidence Workbench

#### Purpose
Perform detailed visual comparison, inspect change signals, and review the multi-channel evidence decomposition.

#### UI Structure
- **Top Control Bar**:
  - Baseline Scene (T1): `Sentinel-2A | 2023-02-10 | Cloud: 1.2%`
  - Observation Scene (T2): `Sentinel-2B | 2024-04-12 | Cloud: 2.1%`
  - Display Modes: `[Side-by-Side]` | `[Interactive Swipe]` | `[Opacity Blend]` | `[Change Overlay]`
- **Main Viewport (Dual-Map)**:
  - Synchronous pan & zoom across T1 and T2 images.
- **Bottom Panel (Evidence & Timeline Drawer)**:
  - **Evidence Decomposition Table**: Displays Spectral Diff, Semantic Match, Spatial Relationship, and Quality score cards.
  - **Temporal Timeline**: Interactive multi-date series bar displaying persistence of change.

---

### Screen 4: Verification & Provenance Drawer

#### Purpose
Provide a dedicated space to evaluate false alarms, review confounders, set verification status, and audit data lineage.

#### UI Structure (Slide-out Drawer from Right)
1. **Confounder & Risk Assessment Panel**:
   - Cloud / Shadow Mask Status (`CLEAR`)
   - Sun Elevation / Illumination Angle Diff (`3.2° - Low Risk`)
   - Seasonal Vegetation Shift Check (`No seasonal anomaly pattern matched`)
   - Spatial Registration Offset (`0.25 pixels - High Precision`)
2. **Analyst Decision Interface**:
   - Buttons: `[ VERIFY: Genuine Activity ]` | `[ REJECT: False Alarm ]` | `[ MARK UNCERTAIN ]`
   - Analyst Notes Text Area.
3. **Provenance Graph Visualizer**:
   - Tree node display showing: `Provider (Copernicus)` → `STAC Item ID` → `COG Asset URL` → `GDAL Resampling` → `Embedding Model` → `Analyst Decision`.

---

### Screen 5: Export & Evidence Object Builder

#### Purpose
Package all findings into a reproducible, audit-ready Evidence Package.

#### UI Structure
- **Summary Preview**: Overview of investigation query, selected candidate, before/after thumbnails, evidence breakdown, and verification status.
- **Data Format Selector**: `[JSON Evidence Package (.json)]` | `[Summary Report (.pdf)]` | `[GeoTIFF Change Mask Archive (.zip)]`
- **Action Button**: `[ Generate & Download Evidence Package ]`

---

## 3. Progressive Disclosure Rules

To prevent cognitive overload, TerraSeek enforces a strict 3-tier progressive disclosure model:

| Level | Target Audience | Exposed Information |
|---|---|---|
| **Tier 1: Primary (Default)** | All Analysts | NL query input, candidate card thumbnails, "Why this result" high-level tags, before/after swipe viewport, verify decision buttons. |
| **Tier 2: Secondary (1-Click)** | Investigative Analysts | Multi-channel evidence decomposition table, temporal persistence timeline, confounder risk checks, analyst notes area. |
| **Tier 3: Tertiary (Expert Toggle)** | Remote Sensing Experts & Engineers | Raw STAC JSON metadata, GDAL pipeline parameters, vector distance matrices, raw spectral band statistics, full provenance tree. |

---

## Related Documents

- Product Direction → [PRODUCT_DIRECTION.md](PRODUCT_DIRECTION.md)
- Product Zero Spec → [PRODUCT_ZERO.md](PRODUCT_ZERO.md)
- Primary User Journey → [USER_JOURNEY.md](USER_JOURNEY.md)
- Evidence Model → [EVIDENCE_MODEL.md](EVIDENCE_MODEL.md)
