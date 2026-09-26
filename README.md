<div align="center">
  <h1>🌍 TerraSeek</h1>
  <p><b>Explainable, AI-Powered Satellite Data Retrieval & Change Detection Engine</b></p>
  
  [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
  [![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)
  [![Status](https://img.shields.io/badge/Status-V1_Technical_Prototype-success)](#)
</div>

---

## 🚀 The Vision
Detecting meaningful physical changes (unauthorized construction, flood inundation, deforestation) in satellite imagery is notoriously difficult due to seasonal variations, sensor noise, and atmospheric conditions. 

While the industry defaults to opaque "Black Box" Deep Learning models that require massive GPU clusters and cannot explain their reasoning, **TerraSeek takes a different path.** 

TerraSeek is an **Explainable AI (XAI) engine**. It relies on robust statistical methods and multi-spectral physical evidence to isolate genuine localized changes from broad temporal variation—producing results that are deterministic, mathematically defensible, and computationally lightweight.

---

## 🧠 Core Philosophy: Explainability > Blackbox AI
Governments and enterprises cannot act on "The AI said so." They need evidence. 
When TerraSeek detects a change, it doesn't just output a mask. It outputs a **probabilistic, evidence-based interpretation**:
> *"Region R66 flagged as Vegetation-to-Built transition. Evidence: 10,000 m² contiguous area. NDVI dropped by 3.2σ (MAD) while NDBI increased by 4.1σ (MAD)."*

---

## 🏗️ Technical Architecture
TerraSeek is designed as a highly scalable backend processing engine. 

```text
STAC / Sentinel-2 Acquisition ──> COG Windowed Reads ──> SCL Quality Masking
                                                              │
                                                              ▼
Multi-Index Evidence ⟵ MAD-Based Robust Z-Score ⟵ Deterministic 10m Grid 
      │
      ▼
Spatial Coherence Filter ──> Region Extraction ──> 📊 Explainable JSON / Visual Maps
```
*(For a deep dive into the methodology, see [`docs/methodology.md`](docs/methodology.md) and [`docs/architecture.md`](docs/architecture.md)).*

---

## 🔬 V1 Technical Prototype: What's Inside?

### ✅ Real Sentinel-2 Validation (The Core Engine)
The core mathematical pipeline has been successfully validated on real Sentinel-2 scene pairs. It natively handles:
- **Cloud-Optimized GeoTIFF (COG)** windowed reads (zero massive downloads).
- **Scene Classification (SCL)** masking (removing clouds/shadows).
- **Multi-Index computation** (NDVI, NDWI, MNDWI, NDBI).
- **Robust Anomaly Detection** using scene-relative Median Absolute Deviation (MAD).

### 🧪 Synthetic Demonstration (The Hackathon Fixture)
To ensure **100% deterministic, offline reproducibility** for hackathon judges, we have bundled a synthetic demo pipeline. It exercises the *exact same* production detector logic without requiring live Sentinel-2 API calls or internet access.
* **Validates:** Pipeline integration, region extraction, and explainability algorithms.
* *Note: Do NOT treat synthetic output as empirical accuracy validation. It is a functional demonstration of the software architecture.*

---

## 💻 Quick Start (Run it in 5 seconds)

Want to see the engine in action? Run the deterministic demo locally:

```bash
# 1. Install requirements
pip install -r requirements.txt

# 2. Run the pipeline in synthetic mode
python -m scripts.demo_pipeline --mode synthetic
```

### 📂 Demo Outputs
Check the `examples/demo_output/` folder for the results:
- 🗺️ **`change_map.png`**: Multi-class map of detected regions (Built vs. Water vs. Land).
- 📈 **`regions.json`**: The core XAI output (human-readable statistical evidence for every region).
- 📊 **`summary.json`**: Top-level analytics (pixels analyzed, total area changed).
- 🔴 **`ndvi_delta.png` / `ndwi_delta.png`**: Raw temporal variation heatmaps.

---

## 🗺️ Roadmap to Production

TerraSeek is intentionally decoupled. By perfecting the core algorithmic engine first, we ensure the foundation is flawless before wrapping it in a UI.

- [x] **Phase 1: The Core Engine (Current)** - Robust statistics, index fusion, spatial coherence, and explainability.
- [ ] **Phase 2: API & Cloud Infrastructure** - Wrapping the engine in FastAPI, deploying serverless functions, and setting up PostgreSQL/PostGIS for region tracking.
- [ ] **Phase 3: Web Dashboard (Frontend)** - A React-based interactive map visualization for end-users to click on regions and read the AI's evidence reports.
- [ ] **Phase 4: ML Noise Filtering** - Using lightweight ML models strictly to filter out edge-case false positives (like cloud-shadow leaks), while keeping the core detection physical and explainable.

---

## ⚠️ Limitations & Honesty
We believe in scientific rigor. The V1 prototype is validated on a limited Sentinel-2 scene pair. Seasonality generalization is not yet established. The system is heavily reliant on the quality of Sentinel-2's SCL mask, and resolution is hard-capped at 10m. This is a V1, not a finished commercial product.

---
<div align="center">
  <i>Built with ❤️ for the Smart India Hackathon</i>
</div>
