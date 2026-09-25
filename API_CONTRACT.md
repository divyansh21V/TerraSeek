# API_CONTRACT.md — API Contract Specification

> Last updated: 2026-09-25
> Status: Draft — no endpoints confirmed, all are proposed

---

## 1. API Design Principles

`[ASSUMPTION]` Pending stakeholder validation.

1. REST-first with JSON payloads
2. Versioned via URL prefix (`/api/v1/`)
3. Standard HTTP status codes
4. Pagination via cursor-based tokens
5. Rate limiting headers on all responses
6. All timestamps in ISO 8601 UTC

---

## 2. Base Configuration

```
Base URL:      [OPEN QUESTION] — not yet deployed
API Version:   v1
Content-Type:  application/json
Auth:          [OPEN QUESTION] — API key? OAuth2? None for OSS?
```

---

## 3. Proposed Endpoints

### 3.1 Queries

#### `POST /api/v1/queries`
Submit a natural language query.

```json
// Request
{
  "query": "Show me deforestation in the Amazon from Jan 2024 to Jun 2024",
  "options": {
    "max_results": 10,
    "providers": ["sentinel", "landsat"]  // optional filter
  }
}

// Response 202 Accepted
{
  "id": "uuid",
  "status": "pending",
  "created_at": "2026-09-25T00:00:00Z",
  "links": {
    "self": "/api/v1/queries/{id}",
    "results": "/api/v1/queries/{id}/results"
  }
}
```

#### `GET /api/v1/queries/{id}`
Get query status and parsed intent.

#### `GET /api/v1/queries/{id}/results`
Get search results, processing outputs, and analysis.

---

### 3.2 Datasets

#### `GET /api/v1/datasets`
Search datasets directly (structured query, not NL).

```
Query params:
  bbox        — bounding box (west,south,east,north)
  datetime    — temporal range (ISO 8601 interval)
  collections — comma-separated collection IDs
  limit       — max results (default 20)
  cursor      — pagination cursor
```

#### `GET /api/v1/datasets/{id}`
Get dataset details and available assets.

---

### 3.3 Processing

#### `POST /api/v1/processing/jobs`
Submit a processing job.

```json
// Request
{
  "operation": "ndvi",
  "input_datasets": ["uuid1", "uuid2"],
  "parameters": {
    "output_format": "geotiff",
    "clip_to": { "type": "Polygon", "coordinates": [...] }
  }
}

// Response 202 Accepted
{
  "id": "uuid",
  "status": "pending"
}
```

#### `GET /api/v1/processing/jobs/{id}`
Get processing job status and output location.

---

### 3.4 Analysis

#### `GET /api/v1/queries/{id}/analysis`
Get AI-generated analysis for a completed query.

```json
// Response 200
{
  "id": "uuid",
  "query_id": "uuid",
  "summary": "Analysis detected a 12% decrease in forest cover...",
  "findings": [...],
  "model_used": "gpt-4o",
  "created_at": "2026-09-25T00:00:00Z"
}
```

---

### 3.5 Health

#### `GET /api/v1/health`
System health check.

```json
// Response 200
{
  "status": "healthy",
  "version": "0.1.0",
  "services": {
    "database": "up",
    "object_storage": "up",
    "llm_provider": "up"
  }
}
```

---

## 4. Error Format

All errors follow a consistent structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      { "field": "bbox", "issue": "Invalid bounding box format" }
    ],
    "request_id": "uuid"
  }
}
```

Standard error codes: `[OPEN QUESTION]` — to be enumerated.

---

## 5. Pagination

```json
{
  "data": [...],
  "pagination": {
    "cursor": "abc123",
    "has_more": true,
    "total": 142
  }
}
```

---

## 6. Rate Limiting Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1695648000
```

`[OPEN QUESTION]` Rate limit values not defined.

---

## 7. Authentication

`[OPEN QUESTION]` Authentication strategy not decided.

Options:
1. No auth (fully open OSS)
2. API key in header (`X-API-Key`)
3. OAuth2 / OIDC
4. Multiple strategies (public + authenticated tiers)

---

## 8. STAC Compatibility

`[OPEN QUESTION]` Should TerraSeek expose a STAC-compatible API
in addition to its native API?

If yes, the datasets endpoint should conform to:
- STAC API 1.0 specification
- OGC API — Features Part 1

---

## Related Documents

- Data model → [DATA_MODEL.md](DATA_MODEL.md)
- Architecture → [ARCHITECTURE.md](ARCHITECTURE.md)
- Security → [SECURITY.md](SECURITY.md)
