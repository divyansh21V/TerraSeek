# TerraSeek Methodology

## Data
Sentinel-2 Level-2A (L2A) surface reflectance imagery, atmospherically corrected to Bottom-of-Atmosphere (BOA) reflectance.

## Preprocessing
* **AOI Reprojection**: Target areas of interest are translated into the local UTM zone (e.g., EPSG:32636).
* **COG Windowed Reads**: Assets are read efficiently from Cloud Optimized GeoTIFFs to save bandwidth and memory.
* **SCL Quality Masking**: Uses Sentinel-2 Scene Classification (SCL) to mask clouds, shadows, and invalid pixels.
* **Common 10m Grid**: A strictly deterministic target grid is generated.
* **20m → 10m Resampling**: 20m bands (e.g., SWIR) are bilinearly resampled to the 10m grid.

## Spectral Indices
The detector leverages multiple distinct physical indices to form a composite view of change:
* **NDVI**: Normalized Difference Vegetation Index (Vegetation health)
* **NDWI**: Normalized Difference Water Index (Water content in leaves/water bodies)
* **MNDWI**: Modified Normalized Difference Water Index (Open water, suppressing built-up noise)
* **NDBI**: Normalized Difference Built-up Index (Urban/built surfaces)

## Change Detection
The core detection logic relies on a robust statistical approach rather than arbitrary universal thresholds:

```text
T2 - T1
↓
median-centering
↓
MAD-based robust standardization
↓
multi-index evidence
↓
spatial coherence
```

1. **Temporal Deltas:** Computes the raw difference between T2 and T1.
2. **Median-centering:** Shifts the distribution to center on the median (0), absorbing broad scene-wide temporal variation.
3. **MAD-based Robust Standardization:** Divides the centered delta by the Median Absolute Deviation (MAD) scaled by 1.4826 (for normality). Absolute robust Z-scores above 3.0 are treated as candidate local anomalies in the V1 detector.
4. **Multi-Index Evidence:** Requires physical agreement across indices (e.g., Veg $\rightarrow$ Built requires NDVI to drop AND NDBI to rise).
5. **Spatial Coherence:** Filters out fragmented noise by requiring connected components of at least 10 pixels (1,000 $m^2$).

## Explainability
The detector outputs **region-level evidence rather than opaque classification**. Each detected region is annotated with the list of supporting indices, a qualitative evidence summary, valid observation fraction, and a probabilistic interpretation (e.g., "Likely vegetation-to-built-surface transition").

## Limitations
* **Validation Scope:** V1 prototype validated on the current Sentinel-2 scene pair. Seasonality/generalization has not yet been established across biomes.
* **Masking Imperfections:** Heavy reliance on SCL limitations. Cloud/shadow misclassification risks exist.
* **Spatial Resolution:** Limited to Sentinel-2's 10m spatial resolution.
* **Fixed Thresholds:** The current V1 anomaly threshold ($Z > 3.0$) is fixed and may require tuning.
* **No Ground Truth:** There is no ground-truth accuracy assessment or production-scale benchmarking yet.
