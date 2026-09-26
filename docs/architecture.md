# TerraSeek Architecture

## Core Pipeline

```text
AOI
 ↓
STAC / Sentinel-2 acquisition
 ↓
COG windowed read
 ↓
SCL quality masking
 ↓
Common 10m grid
 ↓
Spectral indices
 ↓
Temporal deltas
 ↓
Robust anomaly detection
 ↓
Multi-index evidence
 ↓
Spatial coherence
 ↓
Region extraction
 ↓
Explainability
 ↓
JSON / visualization outputs
```

## System State

### Real Sentinel-2 Validation
The current real scene pair validates:
* acquisition
* preprocessing
* grid harmonization
* spectral indices
* detector execution

### Synthetic Demonstration
The synthetic demo validates:
* reproducible execution
* pipeline integration
* region extraction
* explainability
* deterministic offline demonstration

Do NOT treat synthetic output as accuracy validation.

### Future
The following features are planned for future iterations and do not yet exist:
* automated multi-date monitoring
* production STAC ingestion
* scalable processing
* broader validation
* additional data sources
* UI/dashboard
* alerting
