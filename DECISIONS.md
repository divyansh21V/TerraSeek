# DECISIONS.md — Architectural Decision Log

> Last updated: 2026-09-25

---

## How to Use This Document

Record every non-trivial technical decision here.
Each decision follows this template:

```
### DEC-NNN: <Title>
- **Date**: YYYY-MM-DD
- **Status**: proposed | accepted | deprecated | superseded
- **Context**: Why this decision was needed
- **Decision**: What was decided
- **Alternatives**: What else was considered
- **Consequences**: What changes as a result
- **Decided by**: Who made the decision
```

---

## Pending Decisions

These decisions are **blocking or will block** implementation.

| ID | Decision Needed | Blocks | Status |
|---|---|---|---|
| DEC-001 | Python version (3.11 vs 3.12 vs 3.13) | All code | Proposed |
| DEC-002 | Web framework (FastAPI vs Django vs Flask) | API layer | Open |
| DEC-003 | Database (PostgreSQL+PostGIS vs SQLite+SpatiaLite) | Data layer | Open |
| DEC-004 | LLM provider(s) and framework | AI system | Open |
| DEC-005 | Authentication strategy | API, security | Open |
| DEC-006 | Deployment model (Docker vs K8s vs serverless) | DevOps | Open |
| DEC-007 | Vector database (pgvector vs Qdrant vs ChromaDB) | AI/search | Open |
| DEC-008 | Task queue (Celery vs ARQ vs Dramatiq) | Processing | Open |
| DEC-009 | Monorepo vs multi-repo | Project structure | Open |
| DEC-010 | STAC compliance (expose STAC API or internal only) | API contract | Open |
| DEC-011 | User interface scope for v1 (CLI-only vs CLI+API vs CLI+API+Web) | Frontend | Open |
| DEC-012 | Package manager (pip vs uv vs poetry vs pdm) | Build system | Open |
| DEC-013 | Spectral preprocessing grid and indices | Analysis pipeline | Accepted |

---

## Accepted Decisions

### DEC-000: Project License
- **Date**: 2026-09-25
- **Status**: accepted
- **Context**: Project needs an open-source license
- **Decision**: Apache License 2.0
- **Alternatives**: MIT, GPL-3.0, BSD-3-Clause
- **Consequences**: Permissive license allows commercial use; patent grant included
- **Decided by**: Repository creator

### DEC-A01: Primary Language
- **Date**: 2026-09-25
- **Status**: accepted
- **Context**: Need to choose primary implementation language
- **Decision**: Python — evidenced by .gitignore content
- **Alternatives**: TypeScript/Node, Rust, Go
- **Consequences**: Rich geospatial/ML ecosystem; performance-sensitive parts may need Rust/C extensions
- **Decided by**: Repository creator

### DEC-A02: Documentation-First Development
- **Date**: 2026-09-25
- **Status**: accepted
- **Context**: Starting from zero, need reliable AI-assisted development
- **Decision**: Establish complete documentation system before writing application code
- **Alternatives**: Start coding immediately, document later
- **Consequences**: Slower start, but agents can work with clear context; reduced rework
- **Decided by**: Project architect

### DEC-013: Spectral Preprocessing Grid and Indices
- **Date**: 2026-09-26
- **Status**: accepted
- **Context**: Need to define robust preprocessing steps for mixed-resolution Sentinel-2 assets before spectral change analysis.
- **Decision**: 
  1. Target Grid: Fixed to native 10m Sentinel-2 grid.
  2. Resampling: Continuous 20m bands (B11, B12) use Bilinear interpolation. Categorical 20m bands (SCL) use Nearest-Neighbour interpolation.
  3. Masking: Joint valid mask (`valid_T1 & valid_T2`) over valid SCL classes (4, 5, 6, 7). All indices use this joint mask to exclude clouds, water, etc.
  4. Indices: NDVI `(B08-B04)/(B08+B04)`, NDWI `(B03-B08)/(B03+B08)`, MNDWI `(B03-B11)/(B03+B11)`, NDBI `(B11-B08)/(B11+B08)`.
  5. Interpretation Constraint: Spectral difference (ΔIndex) is diagnostic only and NOT classified as confirmed change-detection or construction.
- **Alternatives**: Implicit resampling, using 20m target grid.
- **Consequences**: Safely comparable 10m indices ready for downstream threshold selection or connected components.
- **Decided by**: Project architect

### DEC-014: Change Detection V1 Methodology
- **Date**: 2026-09-26
- **Status**: accepted
- **Context**: Need a robust, explainable mechanism to detect change between two dates without relying on fragile global thresholds or black-box ML models.
- **Decision**: 
  1. Use robust, scene-relative Z-score standardization on temporal deltas, using Median Absolute Deviation (MAD) to absorb broad temporal variation (e.g. seasonal change).
  2. Implement Multi-Index Physical Evidence rules (e.g. Veg to Built requires NDVI drop AND NDBI rise).
  3. Apply Spatial Coherence filtering (minimum connected component size of 10 pixels / 1000m²).
  4. Output region-level explainable evidence rather than opaque classifications.
- **Alternatives**: Global fixed thresholds (too fragile to atmospheric differences), clipping to [-1, 1] (destroys data), deep learning models (black-box, too heavy for prototype).
- **Consequences**: Deterministic, transparent change detection that successfully suppresses noise and isolates valid geospatial anomalies. Thresholds (Z>3.0) and spatial parameters (10 pixels) are explicit but currently hardcoded.
- **Decided by**: Project architect

---

## Deprecated Decisions

_None yet._

---

## Related Documents

- Architecture → [ARCHITECTURE.md](ARCHITECTURE.md)
- AI System → [AI_SYSTEM.md](AI_SYSTEM.md)
- Roadmap → [ROADMAP.md](ROADMAP.md)
