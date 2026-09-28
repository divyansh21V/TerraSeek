# TerraSeek Industry-Level Prototype Plan

> Status: `[ASSUMPTION]` Working plan based on the current repository and the locked Product Zero documents.

## Current audit verdict

TerraSeek has a differentiated thesis: an evidence path instead of a generic satellite chatbot. The repository already contains a deterministic change-detection engine, FastAPI services, a golden-path UI, and tests. The current prototype is not yet industry-ready because the frontend is fixture-driven, the backend and frontend contracts diverge, export formats are mislabeled, decisions are not persisted from the UI, and the product presents a single confidence score despite the product decision to use inspectable evidence channels.

## Prototype target

Make one complete analyst loop reliable and honest:

1. Describe an investigation in plain language.
2. Review structured constraints before search.
3. See ranked candidates with evidence tags and quality warnings.
4. Compare aligned before/after imagery.
5. Inspect temporal persistence and confounders.
6. Record a decision with a justification.
7. Export a reproducible JSON evidence package.

The prototype must clearly label demo/local data and must never imply that a fixture result is live satellite telemetry.

## Differentiating features worth building

### 1. Evidence ledger

Every finding gets an append-only ledger of source item, processing step, evidence channel, analyst action, and timestamp. This becomes the durable product advantage over a map viewer or LLM wrapper.

### 2. Counterfactual false-alarm review

For each candidate, show the most likely alternative explanation—cloud, seasonality, tide, shadow, registration error—and what evidence reduced or increased that risk.

### 3. Investigation replay

Exported packages should be replayable offline with the exact query, source identifiers, parameters, and detector version. A reviewer can reproduce the result without trusting a screenshot.

### 4. Quality-aware search budgeting

Let analysts choose a trade-off such as “fastest credible result” or “highest confidence”. The planner then explains whether it will use Sentinel-2, Sentinel-1, Landsat, or a wider temporal window.

### 5. Field-verification handoff

Turn a deferred finding into a compact field task: coordinates, map snapshot, observation window, uncertainty, and the specific question the field operator must answer.

### 6. Dataset and model cards

Expose sensor resolution, acquisition conditions, detector version, known failure modes, and validation coverage beside every evidence package.

## Delivery sequence

### Slice A — Trustworthy Product Zero

- Align frontend decision vocabulary with the API.
- Replace single “AI confidence” language with evidence-channel coverage and explicit risk.
- Make JSON the only honest export until PDF/GeoTIFF packaging exists.
- Persist decision and notes in the backend, not only in browser state.
- Add empty, loading, error, and insufficient-evidence states.
- Label local/demo data in the UI and export manifest.

### Slice B — Contract-backed discovery

- Make the browser call `/api/v1/investigate`.
- Add an adapter that maps API `CandidateDetail` into the workbench view model.
- Add provider metadata and STAC item IDs to the API contract.
- Replace in-memory stores with SQLite for local persistence, keeping the same service interface.

### Slice C — Evidence-grade analysis

- Add a formal evidence-channel schema: spectral, semantic, temporal, spatial, quality, confounder.
- Attach every derived raster and metric to a provenance node.
- Add temporal persistence checks and explicit “insufficient evidence” outcomes.
- Add golden fixtures for clouds, seasonality, registration offset, and missing bands.

### Slice D — Operational hardening

- Add authentication only after the local workflow is stable.
- Add background jobs for retrieval and raster processing.
- Add structured logging, request IDs, health/readiness checks, and metrics.
- Add CI for formatting, strict typing, tests, security checks, and frontend smoke tests.
- Package the app with Docker and document offline deployment.

## Acceptance gates

- A fresh user can complete the golden path without reading documentation.
- No UI label claims live data when local fixtures are active.
- A rejected or deferred finding exports its reason and evidence gaps.
- A decision cannot be recorded for a candidate outside the investigation.
- Every exported JSON package identifies source data, detector version, parameters, and limitations.
- The same fixture produces the same evidence package when replayed offline.

## Risks and open questions

- `[OPEN QUESTION]` Which first operational domain should anchor validation: infrastructure, environmental compliance, disaster response, or research?
- `[OPEN QUESTION]` Which STAC provider is the first production source, and what authentication limits apply?
- `[RISK]` A polished UI can overstate scientific validity unless validation coverage and uncertainty are visible at the point of decision.
- `[RISK]` In-memory session state makes the current API unsuitable for multi-user or restart-safe workflows.
