# PRODUCT_DECISIONS.md — Product Architecture & UX Decision Record

> Last updated: 2026-09-25  
> Status: `[CONFIRMED]` Product Experience Lock  

---

## 1. Decision Log Format

Every product and experience decision follows this strict template:

```text
### PDEC-NNN: <Title>
- **Date**: YYYY-MM-DD
- **Status**: accepted | superseded | deprecated
- **Context**: Problem or trade-off being resolved
- **Decision**: What experience or architectural choice was made
- **Alternatives Rejected**: What options were evaluated and rejected
- **Consequences**: Impact on UX, system scope, and implementation
- **Decided by**: Product Architect & Engineering Team
```

---

## 2. Locked Product Decisions

### PDEC-001: Evidence Engine Positioning over Generic AI Chatbot
- **Date**: 2026-09-25
- **Status**: accepted `[CONFIRMED]`
- **Context**: Market saturation of generic LLM wrapper chatbots ("ChatGPT for X") creates user skepticism and fails to meet operational requirements for defensible geospatial analysis.
- **Decision**: Position TerraSeek strictly as an **offline, provenance-aware Earth-observation evidence engine**. NL input is used solely as an intent parser for geospatial constraints.
- **Alternatives Rejected**: Conversational multi-turn chatbot interface, satellite data marketplace portal, raw vector database viewer.
- **Consequences**: UI focuses on structured candidate cards, evidence tags, synchronized before/after maps, and provenance traces.
- **Decided by**: Product Architect

---

### PDEC-002: Primary User Focus on EO-Capable Analyst / Researcher
- **Date**: 2026-09-25
- **Status**: accepted `[CONFIRMED]`
- **Context**: Attempting to design an interface that caters equally to developers, executives, data engineers, and non-technical consumers dilutes UX clarity and increases feature bloat.
- **Decision**: Optimize Product Zero UX exclusively for the **EO-capable analyst / researcher** who understands investigation goals and geospatial concepts but wants to avoid manual scripting overhead.
- **Alternatives Rejected**: Consumer-focused "satellite discovery" app, developer-first API-only interface, enterprise executive dashboard.
- **Consequences**: UI features domain-relevant evidence tags, spectral indices, and confounder reviews without exposing raw Python code by default.
- **Decided by**: Product Architect

---

### PDEC-003: Multi-Channel Evidence Decomposition over Single AI Confidence Percentage
- **Date**: 2026-09-25
- **Status**: accepted `[CONFIRMED]`
- **Context**: Displaying uncalibrated probability scores (e.g., `"AI Confidence: 92%"`) is dangerous in high-stakes domain investigations because it creates false trust and provides no operational explanation.
- **Decision**: Decompose all change findings into six inspectable evidence channels: **Spectral Signal**, **Semantic Match**, **Temporal Persistence**, **Spatial Match**, **Image Quality**, and **Confounder Risk**.
- **Alternatives Rejected**: Single percentage confidence badge, black-box text narrative summary.
- **Consequences**: Analyst can inspect why a result was surfaced and verify each signal independently.
- **Decided by**: Product Architect & AI Lead

---

### PDEC-004: 3-Tier Progressive Disclosure Model
- **Date**: 2026-09-25
- **Status**: accepted `[CONFIRMED]`
- **Context**: Analysts need rapid high-level clarity but also require deep technical details when verifying edge cases. Exposing all data simultaneously causes severe visual clutter.
- **Decision**: Implement a strict 3-tier information hierarchy: **Primary** (Immediate intent & before/after swipe), **Secondary** (Evidence table & temporal series), **Tertiary** (Raw STAC JSON & GDAL parameters via Expert Mode toggle).
- **Alternatives Rejected**: Single-page GIS cockpit with dozens of open panels, hidden multi-page wizard navigation.
- **Consequences**: Cleaner initial interface (60-second comprehension) with zero loss of technical depth for power users.
- **Decided by**: UX Designer & Product Architect

---

### PDEC-005: Offline-First Execution with Deterministic Fallback
- **Date**: 2026-09-25
- **Status**: accepted `[CONFIRMED]`
- **Context**: Defense, field, and sensitive environmental deployments often operate in air-gapped or low-bandwidth environments where external LLM cloud APIs are unavailable.
- **Decision**: Core STAC retrieval, raster processing, spectral indexing, and evidence visualizers must execute 100% offline from local disk caches. If AI models fail or go offline, the engine degrades gracefully to deterministic keyword and spatial filtering.
- **Alternatives Rejected**: Cloud-only LLM agent dependence, blocking application startup when AI models fail.
- **Consequences**: System remains reliable and operational regardless of external API state.
- **Decided by**: Lead Systems Architect

---

### PDEC-006: 10-Step Evidence Path Golden Workflow
- **Date**: 2026-09-25
- **Status**: accepted `[CONFIRMED]`
- **Context**: Unstructured user flows lead to fragmented analyst actions and incomplete audit histories.
- **Decision**: Enforce a unified 10-step Golden Path sequence: **SEARCH → RESULTS → SELECT CANDIDATE → EVIDENCE → BEFORE/AFTER → TIMELINE → CHANGE MASK → VERIFICATION → PROVENANCE → EXPORT**.
- **Alternatives Rejected**: Free-form unguided canvas, multi-tab fragmented dashboard.
- **Consequences**: Linear, predictable user journey that ensures every exported finding has undergone complete verification and provenance collection.
- **Decided by**: Product Architect

---

### PDEC-007: Explicit Confounder & False-Alarm Surface
- **Date**: 2026-09-25
- **Status**: accepted `[CONFIRMED]`
- **Context**: Environmental factors like cloud shadows, seasonal vegetation shifts, and solar angle variations frequently trigger false-positive change detections in satellite imagery.
- **Decision**: Implement a dedicated **Confounder Analysis Panel** that automatically evaluates cloud/shadow masks, seasonal historical baselines, solar elevation deltas, and registration offsets.
- **Alternatives Rejected**: Hiding potential false alarms, relying solely on visual inspection.
- **Consequences**: Drastically reduces false-alarm rates and equips analysts with defensible verification tools.
- **Decided by**: Remote Sensing Specialist & Product Architect

---

### PDEC-008: Reproducible Evidence Package JSON Export Specification
- **Date**: 2026-09-25
- **Status**: accepted `[CONFIRMED]`
- **Context**: Findings must be portable and verifiable outside of the TerraSeek application for official reports and downstream auditing.
- **Decision**: Export investigations as self-contained **Evidence Packages** (JSON schema + zip archive) containing raw coordinates, STAC IDs, evidence channel scores, baseline/observation metadata, confounder status, signed analyst verification, and model checksums.
- **Alternatives Rejected**: Static PDF report-only export, screenshot exports.
- **Consequences**: Exported packages can be re-imported or verified programmatically by third-party systems.
- **Decided by**: Lead Data Architect

---

## Related Documents

- Product Direction → [PRODUCT_DIRECTION.md](PRODUCT_DIRECTION.md)
- Product Zero Spec → [PRODUCT_ZERO.md](PRODUCT_ZERO.md)
- Evidence Model → [EVIDENCE_MODEL.md](EVIDENCE_MODEL.md)
- Design Acceptance → [DESIGN_ACCEPTANCE.md](DESIGN_ACCEPTANCE.md)
