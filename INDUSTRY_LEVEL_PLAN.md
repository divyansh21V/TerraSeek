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

## SIH competitive edge

`[DECISION]` TerraSeek should be presented as an **evidence-to-action system for Indian field teams**, not as another satellite image viewer or generic AI chatbot. The winning demo should make one decision auditable from natural-language request to field-ready handoff.

### Signature features

| Feature | User value | Why it is distinct | Demo moment |
|---|---|---|---|
| Evidence Ledger | Every conclusion shows its source image, index, processing step, and analyst action | Turns AI output into an inspectable chain of custody | Open one finding and trace it back to the exact STAC item and detector version |
| Change Fingerprint | Summarizes a change using spectral, spatial, temporal, and quality signals | A compact, explainable alternative to a single opaque confidence score | Show “construction-like” change separated from seasonal vegetation or cloud noise |
| False-Alarm Copilot | Lists likely confounders and the test used to rule each one in or out | Makes uncertainty useful instead of hiding it | Toggle cloud, tide, shadow, and registration checks before accepting a finding |
| Field Mission Handoff | Converts a finding into a shareable verification brief with coordinates, evidence, and a question to answer | Connects remote sensing to action on the ground | Export a field task for a district officer or disaster-response team |
| Offline Evidence Pack | Downloads a self-contained, signed package that can be reviewed without network access | Fits low-connectivity government and field environments | Disable network and replay the same result from the exported package |
| India-first workflow presets | Ready-to-run investigations for encroachment, flood impact, crop stress, mining, and coastal change | Shows immediate public-sector relevance instead of a blank canvas | Select a district preset and complete the investigation in under two minutes |

### The judge-facing narrative

1. **Ask**: “Find new construction near this protected area between two dates.”
2. **Ground**: TerraSeek translates the request into AOI, dates, sensor, cloud threshold, and an explainable search plan.
3. **Prove**: The result shows aligned imagery, change fingerprint, source provenance, temporal persistence, and false-alarm checks.
4. **Decide**: The analyst accepts, rejects, or defers the finding with a reason.
5. **Act**: TerraSeek generates a signed evidence pack and field-verification handoff that another officer can replay offline.

### Prioritization for the hackathon

#### Must ship in the judging build

- Evidence Ledger UI with source IDs, processing steps, timestamps, and detector version.
- Change Fingerprint with channel-level scores for spectral, temporal, spatial, quality, and confounder evidence.
- False-Alarm Copilot with at least three deterministic checks: cloud/quality, seasonal persistence, and registration offset.
- Field Mission Handoff export containing coordinates, map snapshot, uncertainty, observation question, and evidence links.
- Three India-relevant presets: flood impact, illegal construction/encroachment, and crop or vegetation stress.
- Honest demo/live labels and a complete empty, loading, insufficient-evidence, and error state.

#### Strong differentiators if time remains

- Offline replay of an exported evidence package.
- Hindi and English query examples with terminology normalization for district, tehsil, village, and survey number.
- “Why this source?” comparison showing why Sentinel-1, Sentinel-2, or Landsat was selected.
- Human feedback loop: analyst corrections become evaluation cases for future detector versions.

#### Defer until after the hackathon

- Full multi-tenant authentication and organization administration.
- Large-scale distributed raster processing and provider billing orchestration.
- Custom model training, mobile apps, and real-time satellite tasking.

### Success measures for the final demo

`[ASSUMPTION]` Use measurable outcomes to make the pitch credible:

- Time from plain-language request to first ranked evidence: under 60 seconds on the demo fixture.
- Time from first result to a justified decision: under 3 minutes.
- Every accepted or deferred result has a visible evidence gap or supporting channel.
- A reviewer can reproduce the same result from the exported package without the original browser session.
- At least three confounder cases are correctly surfaced in the fixture evaluation set.

### Product guardrails

- Never call a fixture result “live telemetry.”
- Never collapse uncertainty into one AI-generated score without showing the contributing channels.
- Never export a finding without source identifiers, parameters, limitations, and detector version.
- Keep an analyst in the loop for any operational or enforcement decision.

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
