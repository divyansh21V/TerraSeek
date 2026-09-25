# AGENTS.md — TerraSeek AI Agent Operating Manual

> Last updated: 2026-09-25

## Purpose

This file is the **entry point** for any AI coding agent working on TerraSeek.
Read this file first. Then read only the documents relevant to your task.

---

## Project Identity

- **Name**: TerraSeek
- **One-liner**: Open-source AI-powered satellite data retrieval and analysis system
- **License**: Apache 2.0
- **Language**: Python (primary)
- **Status**: Pre-implementation (documentation phase)

---

## Document Map — Read Only What You Need

| Task | Read These |
|---|---|
| Understand the product | `PRODUCT.md` |
| Understand requirements | `PRD.md` |
| Design a feature | `ARCHITECTURE.md`, `DATA_MODEL.md`, `API_CONTRACT.md` |
| Work on AI/ML components | `AI_SYSTEM.md` |
| Implement security | `SECURITY.md` |
| Write or run tests | `TESTING.md` |
| Generate test data | `SYNTHETIC_DATA.md` |
| Understand past decisions | `DECISIONS.md` |
| Find what to build next | `ROADMAP.md`, `TODO.md` |
| Check project workflow | This file (`AGENTS.md`) |

---

## Development Workflow

Every feature moves through these phases **in order**.
Do not skip phases. Mark phase completion in `TODO.md`.

```
DISCOVER   → Identify user need, research domain, gather constraints
SPECIFY    → Write requirements in PRD.md, define acceptance criteria
DESIGN     → Define data model, API contracts, UI wireframes
ARCHITECT  → Select patterns, define component boundaries, update ARCHITECTURE.md
IMPLEMENT  → Write code, follow coding standards below
TEST       → Unit tests, integration tests, see TESTING.md
ATTACK     → Security review, adversarial testing, see SECURITY.md
VERIFY     → End-to-end validation, performance benchmarks
DEPLOY     → Containerize, CI/CD, staging verification
MEASURE    → Observability, metrics, user feedback loops
```

---

## Coding Standards

### Python
- **Version**: 3.11+ (exact version TBD in DECISIONS.md)
- **Formatter**: `ruff format`
- **Linter**: `ruff check`
- **Type checking**: `mypy --strict`
- **Imports**: `isort` (via ruff)
- **Docstrings**: Google style
- **Tests**: `pytest`

### General Rules
1. No code without tests
2. No API endpoint without contract in `API_CONTRACT.md`
3. No data entity without definition in `DATA_MODEL.md`
4. No architectural decision without entry in `DECISIONS.md`
5. All secrets via environment variables — never hardcoded
6. All external API calls go through a service abstraction layer

### File Organization (Planned)
```
terraseek/
├── core/           # Domain logic, models, services
├── api/            # REST/GraphQL endpoints
├── ai/             # LLM integration, agents, embeddings
├── ingest/         # Satellite data ingestion pipelines
├── search/         # Search and discovery engine
├── processing/     # Raster/vector processing
├── storage/        # Database and object storage adapters
├── config/         # Configuration management
└── cli/            # Command-line interface
tests/
├── unit/
├── integration/
├── e2e/
└── fixtures/
```

---

## Conventions

### Branching
- `main` — stable, deployable
- `dev` — integration branch
- `feature/<name>` — feature branches
- `fix/<name>` — bug fixes

### Commit Messages
```
<type>(<scope>): <description>

Types: feat, fix, docs, test, refactor, perf, ci, chore
Scope: core, api, ai, ingest, search, processing, storage, cli
```

### Status Markers in Documentation
Throughout all project documents, these markers distinguish knowledge status:

- `[CONFIRMED]` — Validated by stakeholder or evidence
- `[ASSUMPTION]` — Reasonable guess, needs validation
- `[OPEN QUESTION]` — Unknown, blocks or risks decisions
- `[DECISION]` — Deliberate choice, rationale recorded
- `[CONSTRAINT]` — Non-negotiable boundary
- `[RISK]` — Identified threat to project success

---

## Agent Behavior Rules

1. **Read before writing.** Always check existing docs before creating new patterns.
2. **Minimal context loading.** Use the Document Map above — don't load everything.
3. **Mark uncertainty.** Use `[ASSUMPTION]` and `[OPEN QUESTION]` markers.
4. **Record decisions.** Any non-trivial choice goes in `DECISIONS.md`.
5. **Update TODO.md.** Check off completed items. Add new items discovered during work.
6. **Don't invent requirements.** If unclear, add to `[OPEN QUESTION]` and ask.
7. **Preserve documentation.** Don't delete existing comments or docs unrelated to your change.
