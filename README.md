# TerraSeek

TerraSeek is an open-source, AI-powered satellite data retrieval and change detection system designed to track physical footprint changes over time.

## Problem
Detecting meaningful physical changes (construction, flooding, deforestation) in satellite imagery is difficult due to atmospheric variations, seasonal changes, sensor noise, and cloud cover. Naive thresholding fails, and complex ML models are often black boxes.

## Solution
TerraSeek implements a transparent, scene-relative change-detection approach. By computing robust statistics (MAD) on multi-spectral indices (NDVI, NDWI, MNDWI, NDBI) and requiring multi-index physical evidence plus spatial coherence, it isolates genuine localized changes from broad temporal variation.

## Technical Architecture
The system acquires Sentinel-2 L2A COGs, standardizes them to a deterministic 10m grid, computes spectral indices, and runs a robust Z-score anomaly detector. See `docs/architecture.md` for full details.

## Current V1 Detector
The current implementation demonstrates a transparent, scene-relative change-detection approach. It relies on robust median absolute deviation (MAD) to identify candidate local anomalies across multiple indices, outputting evidence-based interpretation for each region.

## Quick Start
```bash
pip install -r requirements.txt
python -m scripts.demo_pipeline --mode synthetic
```

## Demo Outputs
Running the synthetic demo will populate the `examples/demo_output/` folder with the following outputs:
* `before.png`: RGB representation of the T1 image.
* `after.png`: RGB representation of the T2 image.
* `change_map.png`: Multi-class map of detected change regions.
* `ndvi_delta.png`: Raw delta values for NDVI.
* `ndwi_delta.png`: Raw delta values for NDWI.
* `regions.json`: Detailed, explainable region-level evidence output.
* `summary.json`: Top-level summary of pixels analyzed and regions detected.

## Repository Structure
* `scripts/`: Detector pipeline and probes.
* `docs/`: Architecture and methodology.
* `data/`: Validation data and probe outputs (ignored in git).
* `examples/`: Synthetic demo outputs.

## Real Sentinel-2 Validation
The current real scene pair validates:
* acquisition
* preprocessing
* grid harmonization
* spectral indices
* detector execution

## Synthetic Demonstration
The synthetic demo validates:
* reproducible execution
* pipeline integration
* region extraction
* explainability
* deterministic offline demonstration

Do NOT treat synthetic output as accuracy validation.

## Future
The following features are planned for future iterations and do not yet exist:
* automated multi-date monitoring
* production STAC ingestion
* scalable processing
* broader validation across biomes
* additional data sources
* UI/dashboard
* alerting

## Limitations
The V1 prototype is validated on the current Sentinel-2 scene pair. Seasonality/generalization has not been established. It depends on SCL quality and is limited to 10m resolution. Interpretations are probabilistic ("Likely vegetation-to-built-surface transition") and are not guaranteed to be universally accurate.

## References
* `docs/methodology.md`
* `docs/architecture.md`
* `DECISIONS.md`
