# ARCHITECTURE.md — System Architecture

> Last updated: 2026-09-25
> Status: Draft — structural skeleton, pending requirements confirmation

---

## 1. Architecture Principles

`[ASSUMPTION]` Based on README and project nature.

1. **Modular**: Each subsystem is independently deployable and testable
2. **Provider-agnostic**: Data source adapters behind a common interface
3. **AI-native**: LLM integration is a first-class architectural concern, not a bolt-on
4. **Offline-capable**: Core processing works without internet after data retrieval
5. **Extensible**: Plugin system for new data sources, processors, and AI models

---

## 2. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        USER LAYER                            │
│  ┌─────────┐  ┌──────────────┐  ┌──────────┐  ┌───────────┐│
│  │   CLI   │  │  Web UI      │  │ REST API │  │ Python SDK││
│  └────┬────┘  └──────┬───────┘  └────┬─────┘  └─────┬─────┘│
└───────┼──────────────┼───────────────┼───────────────┼──────┘
        │              │               │               │
        └──────────────┴───────┬───────┴───────────────┘
                               │
┌──────────────────────────────┼──────────────────────────────┐
│                     ORCHESTRATION LAYER                      │
│                   ┌──────────┴──────────┐                   │
│                   │   AI Agent Engine   │                   │
│                   │  (Query → Plan →    │                   │
│                   │   Execute → Reason) │                   │
│                   └──────────┬──────────┘                   │
└──────────────────────────────┼──────────────────────────────┘
                               │
        ┌──────────┬───────────┼───────────┬──────────┐
        │          │           │           │          │
┌───────▼──┐ ┌────▼─────┐ ┌───▼────┐ ┌────▼────┐ ┌──▼───────┐
│ Discovery│ │Retrieval │ │Process │ │ Storage │ │ Reasoning│
│ Service  │ │ Service  │ │Service │ │ Service │ │ Service  │
└───────┬──┘ └────┬─────┘ └───┬────┘ └────┬────┘ └──┬───────┘
        │         │           │           │         │
┌───────▼─────────▼───────────▼───────────▼─────────▼────────┐
│                     ADAPTER LAYER                           │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐ │
│  │  STAC  │ │Sentinel│ │Landsat │ │  S3 /  │ │ LLM APIs │ │
│  │Catalogs│ │  Hub   │ │on AWS  │ │ MinIO  │ │(multiple)│ │
│  └────────┘ └────────┘ └────────┘ └────────┘ └──────────┘ │
└────────────────────────────────────────────────────────────┘
```

---

## 3. Component Descriptions

### 3.1 User Layer
`[OPEN QUESTION]` Which interfaces are in scope for v1?

| Component | Description | Status |
|---|---|---|
| CLI | Command-line interface for power users | `[ASSUMPTION]` In scope |
| Web UI | Browser-based dashboard with map view | `[OPEN QUESTION]` |
| REST API | HTTP API for programmatic access | `[ASSUMPTION]` In scope |
| Python SDK | Importable library for notebooks/scripts | `[OPEN QUESTION]` |

### 3.2 Orchestration Layer — AI Agent Engine
The central coordinator that:
1. Parses natural language queries
2. Creates execution plans (which data sources, what processing)
3. Dispatches to services
4. Aggregates results
5. Generates reasoning/explanations

`[OPEN QUESTION]` Agent framework choice — see `AI_SYSTEM.md` and `DECISIONS.md`.

### 3.3 Discovery Service
- Searches satellite data catalogs
- Translates queries into STAC/provider-specific searches
- Ranks and filters results

### 3.4 Retrieval Service
- Downloads/streams data assets
- Handles authentication per provider
- Manages download queue and retries
- Local caching layer

### 3.5 Processing Service
- Raster operations (GDAL/rasterio)
- Spectral index computation
- Compositing, mosaicking
- Time-series analysis

### 3.6 Storage Service
- Local file storage
- Object storage (S3-compatible) `[OPEN QUESTION]`
- Metadata database
- Vector store for embeddings `[OPEN QUESTION]`

### 3.7 Reasoning Service
- LLM-based analysis of processed data
- Report generation
- Explanation of methodology and findings

---

## 4. Technology Stack

`[ASSUMPTION]` — All choices need validation. See `DECISIONS.md`.

| Layer | Technology | Status |
|---|---|---|
| Language | Python 3.11+ | `[ASSUMPTION]` |
| Web framework | FastAPI | `[OPEN QUESTION]` |
| Task queue | Celery / ARQ / Dramatiq | `[OPEN QUESTION]` |
| Database | PostgreSQL + PostGIS | `[OPEN QUESTION]` |
| Object storage | S3-compatible (MinIO for dev) | `[OPEN QUESTION]` |
| Vector database | pgvector / Qdrant / ChromaDB | `[OPEN QUESTION]` |
| Geospatial | rasterio, GDAL, shapely, geopandas | `[ASSUMPTION]` |
| STAC client | pystac-client | `[ASSUMPTION]` |
| LLM framework | `[OPEN QUESTION]` | Not selected |
| Container runtime | Docker | `[ASSUMPTION]` |
| CI/CD | GitHub Actions | `[ASSUMPTION]` |

---

## 5. Data Flow

```
User Query (natural language)
  │
  ▼
AI Agent Engine
  │
  ├─ 1. Parse intent & extract parameters
  │     (location, time range, data type, analysis type)
  │
  ├─ 2. Search catalogs via Discovery Service
  │     └─ Returns ranked list of matching datasets
  │
  ├─ 3. Retrieve data via Retrieval Service
  │     └─ Downloads/caches selected assets
  │
  ├─ 4. Process data via Processing Service
  │     └─ Applies requested transformations
  │
  ├─ 5. Analyze via Reasoning Service
  │     └─ LLM interprets results, generates insights
  │
  └─ 6. Return structured response + artifacts
        (text explanation, processed imagery, metadata)
```

---

## 6. Deployment Architecture

`[OPEN QUESTION]` Deployment model not yet decided.

Options under consideration:
1. **Single process** — All-in-one for development/small scale
2. **Docker Compose** — Multi-container for self-hosted deployment
3. **Kubernetes** — Cloud-native for production scale
4. **Serverless** — Event-driven for cost optimization

---

## 7. Cross-Cutting Concerns

| Concern | Approach | Status |
|---|---|---|
| Configuration | Environment variables + YAML config files | `[ASSUMPTION]` |
| Logging | Structured JSON logging (structlog) | `[ASSUMPTION]` |
| Observability | OpenTelemetry traces + Prometheus metrics | `[OPEN QUESTION]` |
| Error handling | Result types, no silent failures | `[ASSUMPTION]` |
| Rate limiting | Per-provider rate limits in adapter layer | `[ASSUMPTION]` |
| Caching | Multi-tier: in-memory → disk → object storage | `[OPEN QUESTION]` |

---

## Related Documents

- Requirements → [PRD.md](PRD.md)
- Data model → [DATA_MODEL.md](DATA_MODEL.md)
- API contracts → [API_CONTRACT.md](API_CONTRACT.md)
- AI specifics → [AI_SYSTEM.md](AI_SYSTEM.md)
- Decisions → [DECISIONS.md](DECISIONS.md)
