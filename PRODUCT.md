# PRODUCT.md — TerraSeek Product Definition

> Last updated: 2026-09-25

## What Is TerraSeek?

**TerraSeek** is an open-source, AI-powered system for discovering, retrieving,
processing, and reasoning over Earth observation (EO) satellite data.

It combines modern AI (LLMs, embeddings, agents) with geospatial technologies
to make satellite data accessible to researchers, developers, and analysts
who are not necessarily remote sensing experts.

---

## Problem Statement

`[OPEN QUESTION]` The specific user pain points need stakeholder validation.

Likely problems TerraSeek addresses:
1. Satellite data is scattered across dozens of providers and catalogs
2. Querying requires expert knowledge of band combinations, projections, and metadata schemas
3. No unified way to search across providers using natural language
4. Processing pipelines are fragmented and hard to compose
5. Reasoning over results requires manual interpretation

---

## Target Users

`[OPEN QUESTION]` User personas need definition and validation.

| Persona | Description | Priority |
|---|---|---|
| Researcher | Academic/gov scientist analyzing land use, climate, etc. | `[OPEN QUESTION]` |
| Developer | Building apps on top of EO data | `[OPEN QUESTION]` |
| Analyst | Non-technical user who needs insights from satellite imagery | `[OPEN QUESTION]` |
| Data Engineer | Managing EO data pipelines at scale | `[OPEN QUESTION]` |

---

## Core Value Proposition

`[ASSUMPTION]` Based on README description:

> A single system that lets you **ask questions in natural language**,
> and TerraSeek **discovers** the right satellite data, **retrieves** it,
> **processes** it, and **reasons** over the results — all automatically.

---

## Competitive Landscape

`[OPEN QUESTION]` Needs research.

| Competitor / Alternative | Differentiation |
|---|---|
| Google Earth Engine | `[OPEN QUESTION]` |
| Microsoft Planetary Computer | `[OPEN QUESTION]` |
| Sentinel Hub | `[OPEN QUESTION]` |
| STAC ecosystem (manual) | `[OPEN QUESTION]` |

---

## Success Metrics

`[OPEN QUESTION]` All metrics need stakeholder definition.

| Metric | Target | Status |
|---|---|---|
| Time to first query result | `[OPEN QUESTION]` | Not defined |
| Number of supported data sources | `[OPEN QUESTION]` | Not defined |
| Query accuracy (natural language → correct data) | `[OPEN QUESTION]` | Not defined |
| Processing pipeline reliability | `[OPEN QUESTION]` | Not defined |
| Community adoption (stars, forks, contributors) | `[OPEN QUESTION]` | Not defined |

---

## License & Distribution

- **License**: Apache 2.0 `[CONFIRMED]`
- **Distribution**: Open source `[CONFIRMED]`
- **Monetization model**: `[OPEN QUESTION]` — OSS-first, commercial add-ons?

---

## Related Documents

- Requirements → [PRD.md](PRD.md)
- Architecture → [ARCHITECTURE.md](ARCHITECTURE.md)
- AI System → [AI_SYSTEM.md](AI_SYSTEM.md)
