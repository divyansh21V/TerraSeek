# TODO.md — Current Task Tracker

> Last updated: 2026-09-25
> Phase: 0 (Foundation)

---

## How to Use

- Tasks are grouped by phase
- Check off items as they're completed: `[x]`
- Add new tasks discovered during work
- Reference decision IDs and document sections where relevant

---

## Phase 0: Foundation

### Documentation & Product Experience Lock (Complete)
- [x] Create AGENTS.md
- [x] Create PRODUCT.md
- [x] Create PRD.md
- [x] Create ARCHITECTURE.md
- [x] Create DATA_MODEL.md
- [x] Create API_CONTRACT.md
- [x] Create AI_SYSTEM.md
- [x] Create SECURITY.md
- [x] Create TESTING.md
- [x] Create SYNTHETIC_DATA.md
- [x] Create DECISIONS.md
- [x] Create ROADMAP.md
- [x] Create TODO.md
- [x] Create PRODUCT_DIRECTION.md (Product Experience Lock)
- [x] Create PRODUCT_ZERO.md (MVP Scope & 10-Step Golden Path)
- [x] Create USER_JOURNEY.md (Primary Analyst Journey & Mental Model)
- [x] Create INFORMATION_ARCHITECTURE.md (Screens & Progressive Disclosure)
- [x] Create EVIDENCE_MODEL.md (Evidence Taxonomy & Provenance Schema)
- [x] Create DESIGN_ACCEPTANCE.md (UX Acceptance & Quality Gates)
- [x] Create DEMO_GOLDEN_PATH.md (3-Minute Judge Demonstration Script)
- [x] Create PRODUCT_DECISIONS.md (PDEC-001 through PDEC-008 Locked Decisions)

### Blocking Decisions (Required Before Code)
- [ ] DEC-001: Python version → `[OPEN QUESTION]`
- [ ] DEC-002: Web framework → `[OPEN QUESTION]`
- [ ] DEC-003: Database → `[OPEN QUESTION]`
- [ ] DEC-004: LLM provider and framework → `[OPEN QUESTION]`
- [ ] DEC-005: Authentication strategy → `[OPEN QUESTION]`
- [ ] DEC-006: Deployment model → `[OPEN QUESTION]`
- [ ] DEC-007: Vector database → `[OPEN QUESTION]`
- [ ] DEC-008: Task queue → `[OPEN QUESTION]`
- [ ] DEC-009: Monorepo vs multi-repo → `[OPEN QUESTION]`
- [ ] DEC-010: STAC API compliance → `[OPEN QUESTION]`
- [x] DEC-011 / PDEC-001: Product Zero Experience Lock → `[CONFIRMED]` Evidence Engine UX (Product Zero locked)
- [ ] DEC-012: Package manager → `[OPEN QUESTION]`

### Project Scaffolding
- [ ] Create pyproject.toml with dependencies
- [ ] Configure ruff (linting + formatting)
- [ ] Configure mypy
- [ ] Create directory structure per AGENTS.md
- [ ] Create .env.example with all expected env vars
- [ ] Create Dockerfile (dev)
- [ ] Create docker-compose.yml (dev stack)
- [ ] Set up GitHub Actions CI pipeline
- [ ] Create CONTRIBUTING.md

### Synthetic Data
- [ ] Write raster fixture generator script
- [ ] Write STAC response fixture generator
- [ ] Create initial AI evaluation dataset (10-20 queries)
- [ ] Document fixtures in tests/fixtures/README.md

### Stakeholder Input Needed
- [ ] Validate target user personas (PRODUCT.md §2)
- [ ] Confirm v1 feature scope (PRD.md §2)
- [ ] Define success metrics (PRODUCT.md §5)
- [ ] Confirm supported satellite providers (PRD.md §3)
- [ ] Define non-functional requirements (PRD.md §3)

---

## Phase 1: Search & Discovery
_Not started. Blocked by Phase 0 completion._

- [ ] Implement STAC catalog client
- [ ] Implement provider adapter interface
- [ ] Add first provider adapter (Sentinel/STAC)
- [ ] Implement search API endpoint
- [ ] Implement CLI search command
- [ ] Write integration tests

---

## Phase 2–7: Future
_See [ROADMAP.md](ROADMAP.md) for full phase breakdown._

---

## Discovered During Work
_Add items here as they emerge during development._

(none yet)
