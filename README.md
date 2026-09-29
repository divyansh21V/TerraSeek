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
- Sentinel-2 synthetic-data contract covering L2A-like provenance, band resolution, SCL-like quality, indices, ground truth, and validation gates

## Why judges remember TerraSeek

TerraSeek is not only a “find change” demo. It turns a satellite question into a reviewable decision:

| Differentiator | What is already real in the prototype |
|---|---|
| Evidence Ledger | Source, quality, timeline, evidence channels, analyst decision, and export are shown as one traceable path. |
| Change Fingerprint | Spectral, semantic, spatial, quality, persistence, and confounder signals are surfaced separately. |
| False-alarm review | Cloud, seasonality, registration, terrain, smoke, and other quality/confounder checks are visible before sign-off. |
| Human-in-the-loop action | An analyst can confirm, reject, or defer a candidate with a justification. |
| Evidence replay | Before/after imagery, a deterministic change mask, timeline, provenance graph, and JSON package support reproducibility. |
| Offline-first resilience | The core judging flow runs from local probe imagery and an explicit fixture fallback when the API or network is unavailable. |
| India/public-sector fit | The journey is designed for field verification, environmental monitoring, encroachment review, disaster response, and district-level workflows. |

The strongest 180-second story is: **ask → ground → prove → decide → act**. Do not pitch an opaque AI score; show how TerraSeek exposes enough evidence for a human to defend the decision.

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

The image includes the local probe assets used by the offline judging flow. For a persistent deployment, set `TERRASEEK_DB_PATH` to a mounted writable volume, plus long random values for `TERRASEEK_API_KEY` and `TERRASEEK_SIGNING_KEY`.

### Deploy on Render

The repository includes [`render.yaml`](render.yaml) for a Docker web service with a persistent SQLite disk and `/api/v1/health` health checks:

1. Push this repository to GitHub.
2. In Render, choose **New → Blueprint** and select the repository.
3. Set the two secret values requested by the blueprint: `TERRASEEK_API_KEY` and `TERRASEEK_SIGNING_KEY`.
4. Deploy and verify `/api/v1/health`, `/docs`, and the root UI URL.

This is a hackathon deployment profile. For production multi-user workloads, replace SQLite with PostgreSQL/PostGIS and the in-process job runner with a durable worker queue.

### Deploy the judging UI on Netlify

The repository includes [`netlify.toml`](netlify.toml) and a zero-dependency Node build script. Netlify copies `frontend/` plus the local probe assets into `dist/`, so the offline judging journey remains usable without a Python server:

```bash
netlify login
netlify init       # choose an existing site or create a new one
netlify deploy --prod
```

The Netlify site is the static demo surface. It uses the explicit local fixture fallback because FastAPI, SQLite, background jobs, and signing secrets are not available in a static deployment. Use the Render/Docker service when you need the live API path. After deployment, verify the query → discovery → workbench → decision → export journey and confirm that `/data/probe/` assets load.

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

The Sentinel-2 synthetic-data thesis is implemented as a project contract in [`docs/SENTINEL2_SYNTHETIC_DATA_SPEC.md`](docs/SENTINEL2_SYNTHETIC_DATA_SPEC.md).

## UI QA screenshots

The latest browser smoke pass covers login, query setup, discovery, and the workbench at desktop, tablet, and mobile widths. Accepted screenshots are stored in [`artifacts/ui-qa/`](artifacts/ui-qa/).

The most presentation-ready frame is [`desktop-workbench-ppt.png`](artifacts/ui-qa/desktop-workbench-ppt.png).

The latest visual refinement pass is captured in [`artifacts/ui-audit-after/`](artifacts/ui-audit-after/): query setup, discovery, workbench, change mask, export manifest, and a presentation-sized workbench frame. The flow was rechecked at 1440px, 768px, and 390px widths with no horizontal overflow.

## Current limitations

- Demo mode uses a local NASA MODIS/Worldview fixture dataset. Investigation and decision records persist to SQLite by default.
- MODIS resolution is approximately 250 m/pixel; it cannot confirm individual structures.
- The browser uses the FastAPI investigation, candidate detail, decision, and export endpoints when the API is available; it falls back to explicitly labelled local fixtures when the server is unavailable.
- The judging UI is offline-safe: probe imagery is served from `data/probe/`, while live provider URLs remain provenance metadata and are never required to render the core journey.
- The live STAC adapter is discovery-only; downstream COG retrieval and raster processing still need provider-specific implementation.
- A result is evidence for analyst review, not an autonomous determination of construction, deforestation, or legal compliance.

## Roadmap to production

1. Replace the intentionally small offline fallback with a versioned local evidence-pack adapter.
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
