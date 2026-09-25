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

---

## Deprecated Decisions

_None yet._

---

## Related Documents

- Architecture → [ARCHITECTURE.md](ARCHITECTURE.md)
- AI System → [AI_SYSTEM.md](AI_SYSTEM.md)
- Roadmap → [ROADMAP.md](ROADMAP.md)
