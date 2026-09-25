# TESTING.md — Testing Strategy

> Last updated: 2026-09-25
> Status: Draft — no test infrastructure exists yet

---

## 1. Testing Principles

1. No code merges without tests
2. Tests are documentation — they describe expected behavior
3. Fast feedback — unit tests run in seconds, not minutes
4. Realistic integration tests — use synthetic data, not mocks where possible
5. AI components get evaluation suites, not just unit tests

---

## 2. Test Pyramid

```
         ╱╲
        ╱  ╲        E2E Tests (few, slow, high confidence)
       ╱    ╲       Full query → result workflows
      ╱──────╲
     ╱        ╲     Integration Tests (medium count)
    ╱          ╲    Service interactions, DB queries, API calls
   ╱────────────╲
  ╱              ╲  Unit Tests (many, fast)
 ╱                ╲ Pure functions, parsers, validators
╱──────────────────╲
```

---

## 3. Test Categories

### 3.1 Unit Tests
- **Scope**: Single function/class, no external dependencies
- **Runner**: pytest
- **Location**: `tests/unit/`
- **Speed**: < 1 second each
- **Coverage target**: `[OPEN QUESTION]` — 80%? 90%?

What to unit test:
- Query parsing and intent extraction
- Coordinate/date validation
- Spectral index calculations
- Response formatting
- Error handling paths

### 3.2 Integration Tests
- **Scope**: Multiple components, may use DB/filesystem
- **Runner**: pytest with fixtures
- **Location**: `tests/integration/`
- **Speed**: < 30 seconds each
- **External deps**: Use testcontainers or in-memory alternatives

What to integration test:
- STAC catalog search and response handling
- Database CRUD for all entities
- Processing pipeline execution on synthetic data
- API endpoint request/response cycles

### 3.3 End-to-End Tests
- **Scope**: Full system, user-facing scenarios
- **Location**: `tests/e2e/`
- **Speed**: < 5 minutes per suite
- **External deps**: Full stack running (Docker Compose)

What to E2E test:
- "User asks question → gets analysis result"
- Multi-step query workflows
- Error recovery scenarios

### 3.4 AI Evaluation Tests
- **Scope**: LLM output quality and correctness
- **Location**: `tests/eval/`
- **Special**: May be non-deterministic; use statistical assertions

What to evaluate:
- Intent extraction accuracy on a golden dataset
- Tool selection correctness
- Analysis quality (human-evaluated baseline)
- Hallucination detection
- Prompt regression tests

---

## 4. Test Infrastructure

| Component | Tool | Status |
|---|---|---|
| Runner | pytest | `[ASSUMPTION]` |
| Coverage | pytest-cov | `[ASSUMPTION]` |
| Mocking | unittest.mock / pytest-mock | `[ASSUMPTION]` |
| Fixtures | pytest fixtures + conftest.py | `[ASSUMPTION]` |
| DB testing | testcontainers-python | `[OPEN QUESTION]` |
| API testing | httpx (async test client) | `[OPEN QUESTION]` |
| Geospatial fixtures | Synthetic GeoTIFFs (see SYNTHETIC_DATA.md) | `[ASSUMPTION]` |
| CI runner | GitHub Actions | `[ASSUMPTION]` |

---

## 5. CI/CD Pipeline

`[ASSUMPTION]` Pipeline stages:

```
PR opened/updated:
  1. Lint (ruff check)
  2. Type check (mypy --strict)
  3. Unit tests
  4. Integration tests
  5. Security scan (bandit, pip-audit)
  6. Coverage report

Merge to main:
  7. E2E tests
  8. Build container image
  9. Push to registry

Release tag:
  10. Deploy to staging
  11. Smoke tests
  12. Deploy to production
```

---

## 6. Testing External Services

Strategy for testing code that calls external APIs:

| Service | Test Strategy | Status |
|---|---|---|
| STAC catalogs | Record/replay with VCR.py or responses | `[ASSUMPTION]` |
| LLM providers | Mock responses + evaluation suite | `[ASSUMPTION]` |
| Object storage | MinIO testcontainer | `[OPEN QUESTION]` |
| Satellite data downloads | Pre-cached synthetic files | `[ASSUMPTION]` |

---

## 7. Test Data

See [SYNTHETIC_DATA.md](SYNTHETIC_DATA.md) for synthetic data generation.

Test fixtures should be:
- Deterministic (same input → same output)
- Small (minimal file sizes)
- Representative (cover edge cases)
- Version-controlled (checked into `tests/fixtures/`)

---

## Related Documents

- Synthetic data → [SYNTHETIC_DATA.md](SYNTHETIC_DATA.md)
- Security testing → [SECURITY.md](SECURITY.md)
- AI evaluation → [AI_SYSTEM.md](AI_SYSTEM.md)
