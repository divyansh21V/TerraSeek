# PRD.md — Product Requirements Document

> Last updated: 2026-09-25
> Status: Draft — awaiting stakeholder input

---

## 1. Overview

TerraSeek is an AI-powered satellite data retrieval and analysis system.
This document defines **what** the system must do. For **how**, see `ARCHITECTURE.md`.

---

## 2. Functional Requirements

### FR-1: Data Discovery
`[ASSUMPTION]` Inferred from README.

| ID | Requirement | Priority | Status |
|---|---|---|---|
| FR-1.1 | System shall search satellite data catalogs using natural language queries | `[OPEN QUESTION]` | Not specified |
| FR-1.2 | System shall support STAC (SpatioTemporal Asset Catalog) API | `[OPEN QUESTION]` | Not specified |
| FR-1.3 | System shall search across multiple data providers simultaneously | `[OPEN QUESTION]` | Not specified |
| FR-1.4 | System shall filter results by spatial extent, temporal range, and data type | `[OPEN QUESTION]` | Not specified |

### FR-2: Data Retrieval
`[ASSUMPTION]` Inferred from README.

| ID | Requirement | Priority | Status |
|---|---|---|---|
| FR-2.1 | System shall download satellite imagery from discovered sources | `[OPEN QUESTION]` | Not specified |
| FR-2.2 | System shall support COG (Cloud-Optimized GeoTIFF) format | `[OPEN QUESTION]` | Not specified |
| FR-2.3 | System shall cache retrieved data locally | `[OPEN QUESTION]` | Not specified |
| FR-2.4 | System shall handle authentication with data providers | `[OPEN QUESTION]` | Not specified |

### FR-3: Data Processing
`[ASSUMPTION]` Inferred from README.

| ID | Requirement | Priority | Status |
|---|---|---|---|
| FR-3.1 | System shall compute common spectral indices (NDVI, NDWI, etc.) | `[OPEN QUESTION]` | Not specified |
| FR-3.2 | System shall support raster operations (clip, reproject, resample) | `[OPEN QUESTION]` | Not specified |
| FR-3.3 | System shall generate composites and mosaics | `[OPEN QUESTION]` | Not specified |
| FR-3.4 | System shall support time-series analysis | `[OPEN QUESTION]` | Not specified |

### FR-4: AI Reasoning
`[ASSUMPTION]` Inferred from README.

| ID | Requirement | Priority | Status |
|---|---|---|---|
| FR-4.1 | System shall interpret natural language queries into data requests | `[OPEN QUESTION]` | Not specified |
| FR-4.2 | System shall generate textual analysis of retrieved data | `[OPEN QUESTION]` | Not specified |
| FR-4.3 | System shall support multi-step reasoning workflows (agents) | `[OPEN QUESTION]` | Not specified |
| FR-4.4 | System shall explain its reasoning and data selection to users | `[OPEN QUESTION]` | Not specified |

### FR-5: User Interface
`[OPEN QUESTION]` No UI requirements exist yet.

| ID | Requirement | Priority | Status |
|---|---|---|---|
| FR-5.1 | CLI interface | `[OPEN QUESTION]` | Not specified |
| FR-5.2 | Web dashboard | `[OPEN QUESTION]` | Not specified |
| FR-5.3 | REST API | `[OPEN QUESTION]` | Not specified |
| FR-5.4 | Python SDK | `[OPEN QUESTION]` | Not specified |

---

## 3. Non-Functional Requirements

| ID | Requirement | Target | Status |
|---|---|---|---|
| NFR-1 | Response time for search queries | `[OPEN QUESTION]` | Not specified |
| NFR-2 | Maximum concurrent users | `[OPEN QUESTION]` | Not specified |
| NFR-3 | Data storage limits | `[OPEN QUESTION]` | Not specified |
| NFR-4 | Availability SLA | `[OPEN QUESTION]` | Not specified |
| NFR-5 | Supported satellite constellations | `[OPEN QUESTION]` | Not specified |
| NFR-6 | Python version compatibility | 3.11+ `[ASSUMPTION]` | Draft |
| NFR-7 | Deployment model (self-hosted, cloud, hybrid) | `[OPEN QUESTION]` | Not specified |

---

## 4. Constraints

| ID | Constraint | Source |
|---|---|---|
| C-1 | Open source, Apache 2.0 | `[CONFIRMED]` — LICENSE file |
| C-2 | Python as primary language | `[CONFIRMED]` — .gitignore |
| C-3 | Must work with public satellite data APIs | `[ASSUMPTION]` |

---

## 5. Out of Scope (Initial Release)

`[OPEN QUESTION]` Needs stakeholder confirmation.

- Real-time streaming satellite feeds
- Custom satellite tasking
- Paid data provider integration
- Mobile application

---

## 6. Acceptance Criteria Template

Each feature requirement should eventually define:
```
Given: <precondition>
When:  <action>
Then:  <expected result>
```

No acceptance criteria have been written yet.
All requirements above need stakeholder validation before implementation.

---

## Related Documents

- Product context → [PRODUCT.md](PRODUCT.md)
- Architecture → [ARCHITECTURE.md](ARCHITECTURE.md)
- Data model → [DATA_MODEL.md](DATA_MODEL.md)
- API contracts → [API_CONTRACT.md](API_CONTRACT.md)
