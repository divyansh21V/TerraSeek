# TerraSeek Synthetic Sentinel-2-like Data Contract

Status: `[DECISION]` v1 implementation contract derived from the Sentinel-2 research thesis supplied to the project on 2026-09-29.

This document turns the research findings into rules the generator, API, UI, and evaluation suite can share. Synthetic records must never be presented as real Copernicus acquisitions.

## Product identity and provenance

The canonical synthetic product is:

```text
product: TerraSeek Synthetic Sentinel-2-like Dataset
version: terraseek-s2-v1
data_origin: synthetic
sensor: Sentinel-2-like
processing_level: L2A-like
synthetic_profile: terraseek_s2_v1
coordinate_status: fictional_simulation_reference
```

Level-2A-like surface reflectance is the primary analytical product. Level-1C-like top-of-atmosphere data may be represented separately for cirrus or product-lineage demonstrations. Synthetic product IDs, coordinates, acquisition dates, catalog links, and SCL fields must be clearly labelled as simulated.

## Sentinel-2 band contract

The canonical L2A-like table contains these twelve analytical bands:

| Band | Native resolution | TerraSeek role |
|---|---:|---|
| B01 | 60 m | Coastal aerosol and atmospheric context |
| B02 | 10 m | Blue, RGB, haze and water context |
| B03 | 10 m | Green, RGB and water indices |
| B04 | 10 m | Red and NDVI |
| B05 | 20 m | Red-edge vegetation stress |
| B06 | 20 m | Red-edge vegetation condition |
| B07 | 20 m | Red-edge vegetation structure |
| B08 | 10 m | Broad NIR, NDVI and vegetation structure |
| B8A | 20 m | Narrow NIR and vegetation reference |
| B09 | 60 m | Water vapour context |
| B11 | 20 m | SWIR moisture, NDBI and flood/burn context |
| B12 | 20 m | SWIR disturbance and NBR |

B10 is excluded from the canonical L2A-like surface-reflectance table. It belongs only in an optional L1C-like/cirrus representation.

Reflectance is stored internally as `float32` in the physical range 0–1. The source-product relationship `DN = 10000 × reflectance` may be retained as `dn_value`; 0.4 is a typical optical threshold, not a hard maximum.

## Spatial and observation model

Use three normalized analytical levels:

1. AOI: scenario, geometry, coordinate status, and stable identity.
2. Observation: acquisition time, processing level, quality summaries, and provenance.
3. Cell: spatial grid identity, land-cover state, spectral values, quality, indices, and ground truth.

The canonical analytical grain is one row per `observation_id × cell_id × band_group`. Parquet is authoritative; CSV is for samples and inspection only.

The canonical analysis grid is 10 m:

- 10 m bands are generated at 10 m.
- 20 m bands are generated at native resolution and resampled with bilinear-like interpolation for the analysis grid.
- 60 m bands are generated at native resolution and resampled for API/map convenience.
- SCL-like classes are generated at 20 m and resampled with nearest-neighbour logic.
- `native_resolution_m` and `analysis_resolution_m` must remain visible in metadata.

## Required dataset outputs

```text
aoi_metadata.parquet / .csv
observation_metadata.parquet
spatial_cells.geojson / .parquet
spectral_observations.parquet
quality_observations.parquet
derived_indices.parquet
change_ground_truth.parquet
event_catalog.parquet
anomaly_cases.parquet
```

Required provenance and quality fields include `observation_id`, `aoi_id`, `cell_id`, `acquisition_datetime`, `processing_level`, `cloud_cover_percent`, `clear_fraction`, `invalid_fraction`, `haze_score`, `observation_status`, `generator_version`, `data_origin`, `native_resolution_note`, and `band_missing_mask`.

## Quality and SCL-like data

Synthetic quality data must be named `scl_synthetic` or `SCL-like`; it must not be described as ESA Sen2Cor output. The supported vocabulary is:

```text
0 no_data
1 saturated_or_defective
2 dark_area
3 cloud_shadow
4 vegetation
5 bare_or_built
6 water
7 unclassified
8 cloud_medium_probability
9 cloud_high_probability
10 thin_cirrus
11 snow_or_ice
```

Quality must exist at cell level. Tile/AOI cloud percentage is only a summary and must not substitute for event-area masking. Records should distinguish `usable`, `degraded`, `reject`, and missing-data states.

## Derived indices

Indices are computed from generated bands after quality masking; they are never independently randomized:

```text
NDVI = (B08 - B04) / (B08 + B04)
NDWI = (B03 - B08) / (B03 + B08)
MNDWI = (B03 - B11) / (B03 + B11)
NDBI = (B11 - B08) / (B11 + B08)
EVI = 2.5 × (B08 - B04) / (B08 + 6B04 - 7.5B02 + 1)
SAVI = 1.5 × (B08 - B04) / (B08 + B04 + 0.5)
NBR = (B08 - B12) / (B08 + B12)
```

Use an epsilon-safe denominator and retain `index_valid` and `index_quality`.

## Synthetic generation rules

Generate spectra from latent state, not independent per-band noise. A cell should combine base land cover, vegetation, moisture, water, built-up fraction, disturbance, season, and observation quality. Apply correlated noise after the latent mixture. Include sub-pixel fractions and spatially correlated patches; a 10 m cell may contain mixed crops, soil, roads, roofs, or water edges.

The generator should cover at least ten heterogeneous fictional scenarios, including agricultural seasonality, stable urban core, urban expansion, forest change, water variation, mixed rural land, industrial expansion, drought stress, flood/recovery, and land clearing.

Ground truth must distinguish:

```text
no_change, seasonal_change, vegetation_loss, vegetation_recovery,
urban_expansion, water_expansion, water_loss, flood, drought_stress,
land_clearing, construction, burn_disturbance, cloud_artifact
```

Keep model inputs separate from labels. Do not expose `change_type`, `confidence_reference`, or event labels as training features.

## Validation gates

The synthetic release is acceptable only when it verifies:

- all records are explicitly synthetic;
- bands stay within physical bounds and use warning thresholds for unusual values;
- vegetation, water, soil, and built-up spectra are statistically distinguishable;
- indices mathematically match the source bands;
- spatial neighbours have positive correlation;
- non-event time series remain smooth except for quality effects;
- clouds are spatially structured and high-cloud cells are rarely index-usable;
- rejected observations are not used for indices;
- seasonal change is represented separately from meaningful change;
- event polygons and false-positive-like cases exist;
- native and analysis resolutions are documented;
- API responses distinguish `null` from zero and preserve provenance.

Recommended tests include reflectance bounds, index consistency, vegetation/water relationships, neighbour correlation, temporal continuity, quality masking, ground-truth directionality, missing-data propagation, duplicate keys, foreign-key integrity, and outlier detection.

## Known limitations

This is a physically informed synthetic generator, not a radiative-transfer simulation. It does not reproduce exact atmospheric effects, bidirectional reflectance, adjacency effects, illumination geometry, sensor response functions, or Sen2Cor decisions. Upsampling does not create new spatial information. The UI and API must communicate these limits rather than implying empirical satellite truth.

## Implementation mapping

The intended generator package is `terraseek_synth/` with modules for configuration, scenarios, geometry, temporal state, land cover, spectra, atmosphere, indices, quality, events, ground truth, validation, and CLI output. Until that package is implemented, the existing probe assets remain demo fixtures and must keep their explicit offline/demo labels.

Research references supplied with the thesis include the Sentinel-2 User Handbook, Copernicus Data Space Sentinel-2 L2A documentation, and the ESA Sen2Cor configuration manual.
