# ROADMAP.md — Development Roadmap

> Last updated: 2026-09-25
> Status: Draft — phases are structural, not time-bound

---

## Roadmap Philosophy

Each phase delivers a **usable increment**.
No phase starts until the previous phase's core functionality works end-to-end.

---

## Phase 0: Foundation ← CURRENT
**Goal**: Project infrastructure and documentation

| Milestone | Description | Status |
|---|---|---|
| M0.1 | Documentation system (AGENTS.md, PRD, ARCHITECTURE, etc.) | ✅ Done |
| M0.2 | Resolve blocking decisions (DEC-001 through DEC-012) | ⬜ Not started |
| M0.3 | Project scaffolding (pyproject.toml, CI, linting) | ⬜ Not started |
| M0.4 | Synthetic data generation scripts | ⬜ Not started |
| M0.5 | Development environment setup (Docker, .env.example) | ⬜ Not started |

**Exit criteria**: All blocking decisions made. Project builds and lints. CI green.

---

## Phase 1: Search & Discovery
**Goal**: Query satellite catalogs and return structured results

| Milestone | Description | Status |
|---|---|---|
| M1.1 | STAC catalog client (search, filter, paginate) | ⬜ Not started |
| M1.2 | Multi-provider adapter layer | ⬜ Not started |
| M1.3 | Structured search API endpoint | ⬜ Not started |
| M1.4 | Basic CLI for search | ⬜ Not started |
| M1.5 | Integration tests with synthetic STAC responses | ⬜ Not started |

**Exit criteria**: User can search for satellite data via CLI and get structured results.

---

## Phase 2: Retrieval & Storage
**Goal**: Download and cache satellite data

| Milestone | Description | Status |
|---|---|---|
| M2.1 | Asset download manager (queue, retry, progress) | ⬜ Not started |
| M2.2 | Local cache with eviction policy | ⬜ Not started |
| M2.3 | Provider authentication management | ⬜ Not started |
| M2.4 | Metadata database (store datasets, assets) | ⬜ Not started |
| M2.5 | CLI download commands | ⬜ Not started |

**Exit criteria**: User can download satellite imagery to local storage.

---

## Phase 3: Processing
**Goal**: Transform raw satellite data into analysis-ready products

| Milestone | Description | Status |
|---|---|---|
| M3.1 | Raster operations (clip, reproject, resample) | ⬜ Not started |
| M3.2 | Spectral index computation (NDVI, NDWI, etc.) | ⬜ Not started |
| M3.3 | Compositing and mosaicking | ⬜ Not started |
| M3.4 | Processing job queue and status tracking | ⬜ Not started |
| M3.5 | Processing API endpoints | ⬜ Not started |

**Exit criteria**: User can process downloaded data and get derived products.

---

## Phase 4: AI Integration
**Goal**: Natural language interface and intelligent reasoning

| Milestone | Description | Status |
|---|---|---|
| M4.1 | LLM abstraction layer (multi-provider) | ⬜ Not started |
| M4.2 | NL query parsing → structured intent | ⬜ Not started |
| M4.3 | AI agent with tool calling (search + retrieve + process) | ⬜ Not started |
| M4.4 | Result analysis and explanation generation | ⬜ Not started |
| M4.5 | AI evaluation suite | ⬜ Not started |
| M4.6 | Prompt management and versioning | ⬜ Not started |

**Exit criteria**: User can ask natural language questions and get data + analysis.

---

## Phase 5: API & Integration
**Goal**: Production-ready API for external consumers

| Milestone | Description | Status |
|---|---|---|
| M5.1 | REST API (FastAPI) with all endpoints | ⬜ Not started |
| M5.2 | Authentication and rate limiting | ⬜ Not started |
| M5.3 | API documentation (OpenAPI spec) | ⬜ Not started |
| M5.4 | Python SDK | ⬜ Not started |
| M5.5 | Webhook/streaming support for long jobs | ⬜ Not started |

**Exit criteria**: External developers can integrate TerraSeek via API.

---

## Phase 6: Web Interface
`[OPEN QUESTION]` — Is a web UI in scope?

| Milestone | Description | Status |
|---|---|---|
| M6.1 | Map-based query interface | ⬜ Not started |
| M6.2 | Results visualization | ⬜ Not started |
| M6.3 | Analysis dashboard | ⬜ Not started |

---

## Phase 7: Production Hardening
**Goal**: Reliability, observability, security

| Milestone | Description | Status |
|---|---|---|
| M7.1 | Structured logging and tracing | ⬜ Not started |
| M7.2 | Health checks and monitoring | ⬜ Not started |
| M7.3 | Security hardening (SECURITY.md implementation) | ⬜ Not started |
| M7.4 | Performance benchmarks | ⬜ Not started |
| M7.5 | Documentation for self-hosting | ⬜ Not started |

**Exit criteria**: System runs reliably in production with observability.

---

## Timeline

`[OPEN QUESTION]` No timeline commitments exist.
Phases are ordered by dependency, not by calendar.

---

## Related Documents

- Current tasks → [TODO.md](TODO.md)
- Decisions needed → [DECISIONS.md](DECISIONS.md)
- Requirements → [PRD.md](PRD.md)
