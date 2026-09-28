# TerraSeek

**Explainable, provenance-aware Earth-observation evidence engine.**

TerraSeek helps an analyst move from a geospatial question to a defensible change finding: discover candidate observations, compare time-separated imagery, inspect evidence channels and false-alarm risks, record a decision, and export a reproducible evidence package.

> Current status: **Product Zero / technical prototype**. The default dataset is deterministic local demo data. It is not a live satellite intelligence service and must not be used as empirical validation or operational truth.

## Why TerraSeek is different

TerraSeek is intentionally not “ChatGPT for satellites” and not a generic GIS dashboard. Its core unit is an **evidence path**:

```text
question → constraints → candidate ranking → temporal comparison
         → six evidence channels → confounder review → analyst decision
         → reproducible export
```

Every result exposes six inspectable channels instead of relying on an uncalibrated single AI-confidence number:

1. Spectral signal
2. Semantic match
3. Temporal persistence
4. Spatial/contextual match
5. Quality assurance
6. Confounder risk

## What works today

- Deterministic investigation service with AOI, date-range, and ranking filters
- FastAPI API under `/api/v1`
- Candidate detail with timeline, quality checks, warnings, and evidence channels
- Analyst decisions scoped to the investigation that produced the candidate
- JSON evidence-package export with demo-mode disclosure and limitations
- Browser Product Zero flow with candidate cards, map view, before/after workbench, decision modal, and export screen
- Offline synthetic/demo pipeline and existing raster-analysis fixtures
- Live public STAC Item Search adapter with configurable catalog URL
- SQLite persistence for investigations and analyst decisions
- Background investigation jobs with status polling
- Optional API-key protection and HMAC-signed evidence packages
- Docker entry point and GitHub Actions for Python and JavaScript checks

## Quick start

### Python API and UI

Python 3.11+ is required.

```bash
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
uvicorn terraseek.main:app --reload
```

Open `http://localhost:8000`. API documentation is available at `http://localhost:8000/docs`.

### Static browser prototype

```bash
node server.js
```

Open `http://localhost:3000`.

### Docker

```bash
docker build -t terraseek .
docker run --rm -p 8000:8000 terraseek
```

### Tests and checks

```bash
pytest -q
ruff check .
ruff format --check .
node --check frontend/js/app.js
node --check server.js
```

## API surface

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/health` | Runtime status, mode, and capabilities |
| GET | `/api/v1/aois` | Available demo areas of interest |
| POST | `/api/v1/investigate` | Run a ranked investigation |
| POST | `/api/v1/jobs/investigate` | Queue an investigation |
| GET | `/api/v1/jobs/{job_id}` | Poll a background job |
| POST | `/api/v1/catalog/search` | Search a live STAC catalog |
| GET | `/api/v1/candidates/{id}` | Retrieve evidence detail |
| POST | `/api/v1/decisions` | Record an analyst decision |
| GET | `/api/v1/export/{investigation_id}` | Export the evidence package |

All timestamps are ISO 8601 UTC. Secrets belong in environment variables; see `.env.example`. Set `TERRASEEK_API_KEY` to protect mutating/live endpoints and `TERRASEEK_SIGNING_KEY` to sign exported packages.

## Product journey

The intended analyst journey is documented in [`USER_JOURNEY.md`](USER_JOURNEY.md):

`SEARCH → RESULTS → SELECT → EVIDENCE → BEFORE/AFTER → TIMELINE → CHANGE MASK → VERIFICATION → PROVENANCE → EXPORT`

The industry-level delivery plan, unique feature backlog, risks, and acceptance gates are in [`INDUSTRY_LEVEL_PLAN.md`](INDUSTRY_LEVEL_PLAN.md).

## Current limitations

- Demo mode uses a local NASA MODIS/Worldview fixture dataset. Investigation and decision records persist to SQLite by default.
- MODIS resolution is approximately 250 m/pixel; it cannot confirm individual structures.
- The browser currently contains Product Zero fixture data and is not yet fully wired to the FastAPI service.
- The live STAC adapter is discovery-only; downstream COG retrieval and raster processing still need provider-specific implementation.
- A result is evidence for analyst review, not an autonomous determination of construction, deforestation, or legal compliance.

## Roadmap to production

1. Wire the browser to the API and remove duplicated fixture models.
2. Add COG asset retrieval, SCL/cloud masking, and provider retry/circuit-breaker policies.
3. Replace SQLite with PostgreSQL/PostGIS for multi-user deployments.
4. Add durable queue workers, object storage, rate limits, structured logs, and metrics.
5. Validate against labelled scenes and publish dataset/model cards before operational claims.

## Repository layout

```text
terraseek/       FastAPI routes, services, models, ranking, providers
frontend/        Product Zero browser prototype
scripts/         Offline demos and raster probes
tests/           Unit and integration tests
docs/            Methodology and architecture notes
```

## License

Apache License 2.0. See [`LICENSE`](LICENSE).
