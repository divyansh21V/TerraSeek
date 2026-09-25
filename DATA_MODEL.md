# DATA_MODEL.md — Data Model Definition

> Last updated: 2026-09-25
> Status: Draft — entities inferred from domain, not validated

---

## 1. Entity Overview

`[ASSUMPTION]` All entities below are inferred from the product domain.
None are confirmed requirements.

```
┌──────────┐     ┌───────────┐     ┌──────────────┐
│  Query   │────▶│ SearchJob │────▶│ SearchResult │
└──────────┘     └───────────┘     └──────┬───────┘
                                          │
                                   ┌──────▼───────┐
                                   │   Dataset    │
                                   └──────┬───────┘
                                          │
                              ┌───────────┼───────────┐
                              │           │           │
                        ┌─────▼───┐ ┌─────▼───┐ ┌────▼─────┐
                        │  Asset  │ │Processing│ │ Analysis │
                        │  (file) │ │   Job    │ │  Result  │
                        └─────────┘ └─────────┘ └──────────┘
```

---

## 2. Core Entities

### 2.1 Query
A user's natural language request.

| Field | Type | Description | Status |
|---|---|---|---|
| id | UUID | Primary key | `[ASSUMPTION]` |
| raw_text | string | Original user input | `[ASSUMPTION]` |
| parsed_intent | JSON | Structured extraction from NL | `[ASSUMPTION]` |
| spatial_extent | GeoJSON | Bounding box or polygon | `[ASSUMPTION]` |
| temporal_range | DateRange | Start and end date | `[ASSUMPTION]` |
| data_type | enum | Optical, SAR, DEM, etc. | `[OPEN QUESTION]` |
| created_at | timestamp | When query was submitted | `[ASSUMPTION]` |
| user_id | UUID? | Optional user reference | `[OPEN QUESTION]` |

### 2.2 SearchJob
An execution of a query against one or more catalogs.

| Field | Type | Description | Status |
|---|---|---|---|
| id | UUID | Primary key | `[ASSUMPTION]` |
| query_id | UUID | FK → Query | `[ASSUMPTION]` |
| status | enum | pending, running, completed, failed | `[ASSUMPTION]` |
| catalogs_searched | string[] | Which providers were queried | `[ASSUMPTION]` |
| started_at | timestamp | | `[ASSUMPTION]` |
| completed_at | timestamp? | | `[ASSUMPTION]` |
| error | string? | Error message if failed | `[ASSUMPTION]` |

### 2.3 SearchResult
A single matching item from a catalog search.

| Field | Type | Description | Status |
|---|---|---|---|
| id | UUID | Primary key | `[ASSUMPTION]` |
| search_job_id | UUID | FK → SearchJob | `[ASSUMPTION]` |
| dataset_id | UUID | FK → Dataset | `[ASSUMPTION]` |
| relevance_score | float | Ranking score | `[ASSUMPTION]` |
| stac_item | JSON | Raw STAC item if applicable | `[ASSUMPTION]` |

### 2.4 Dataset
A discovered satellite data product.

| Field | Type | Description | Status |
|---|---|---|---|
| id | UUID | Primary key | `[ASSUMPTION]` |
| external_id | string | Provider's identifier | `[ASSUMPTION]` |
| provider | string | Source provider name | `[ASSUMPTION]` |
| collection | string | Collection/constellation name | `[ASSUMPTION]` |
| spatial_extent | GeoJSON | Coverage geometry | `[ASSUMPTION]` |
| temporal_extent | DateRange | Acquisition time range | `[ASSUMPTION]` |
| cloud_cover | float? | Percent cloud cover | `[ASSUMPTION]` |
| resolution | float? | Spatial resolution in meters | `[ASSUMPTION]` |
| bands | string[] | Available spectral bands | `[ASSUMPTION]` |
| metadata | JSON | Provider-specific metadata | `[ASSUMPTION]` |

### 2.5 Asset
A downloadable file belonging to a dataset.

| Field | Type | Description | Status |
|---|---|---|---|
| id | UUID | Primary key | `[ASSUMPTION]` |
| dataset_id | UUID | FK → Dataset | `[ASSUMPTION]` |
| url | string | Download URL | `[ASSUMPTION]` |
| media_type | string | MIME type | `[ASSUMPTION]` |
| role | string | thumbnail, data, metadata, etc. | `[ASSUMPTION]` |
| file_size | int? | Size in bytes | `[ASSUMPTION]` |
| local_path | string? | Cached local path | `[ASSUMPTION]` |
| checksum | string? | Hash for integrity | `[ASSUMPTION]` |

### 2.6 ProcessingJob
A data processing task applied to one or more assets.

| Field | Type | Description | Status |
|---|---|---|---|
| id | UUID | Primary key | `[ASSUMPTION]` |
| query_id | UUID | FK → Query | `[ASSUMPTION]` |
| input_assets | UUID[] | Assets being processed | `[ASSUMPTION]` |
| operation | string | ndvi, composite, clip, etc. | `[ASSUMPTION]` |
| parameters | JSON | Operation-specific params | `[ASSUMPTION]` |
| status | enum | pending, running, completed, failed | `[ASSUMPTION]` |
| output_path | string? | Path to result | `[ASSUMPTION]` |
| started_at | timestamp | | `[ASSUMPTION]` |
| completed_at | timestamp? | | `[ASSUMPTION]` |

### 2.7 AnalysisResult
AI-generated analysis of processed data.

| Field | Type | Description | Status |
|---|---|---|---|
| id | UUID | Primary key | `[ASSUMPTION]` |
| query_id | UUID | FK → Query | `[ASSUMPTION]` |
| processing_job_id | UUID? | FK → ProcessingJob | `[ASSUMPTION]` |
| summary | text | Natural language summary | `[ASSUMPTION]` |
| findings | JSON | Structured findings | `[ASSUMPTION]` |
| confidence | float? | AI confidence score | `[OPEN QUESTION]` |
| model_used | string | Which LLM/model produced this | `[ASSUMPTION]` |
| created_at | timestamp | | `[ASSUMPTION]` |

---

## 3. Enumerations

`[OPEN QUESTION]` All enums need domain expert validation.

### DataType
```
optical | sar | dem | lidar | hyperspectral | thermal | [OPEN QUESTION]
```

### JobStatus
```
pending | running | completed | failed | cancelled
```

### Provider
```
[OPEN QUESTION] — Which providers will be supported in v1?
Candidates: sentinel_hub | usgs_landsat | copernicus | nasa_earthdata | ...
```

---

## 4. Database Selection

`[OPEN QUESTION]` See `DECISIONS.md`.

Requirements for the database:
- Spatial query support (PostGIS or equivalent)
- JSON column support
- Full-text search (for metadata)
- Vector similarity search (for embeddings) — same DB or separate?

---

## Related Documents

- Architecture → [ARCHITECTURE.md](ARCHITECTURE.md)
- API contracts → [API_CONTRACT.md](API_CONTRACT.md)
- Synthetic data → [SYNTHETIC_DATA.md](SYNTHETIC_DATA.md)
