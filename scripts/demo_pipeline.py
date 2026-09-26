import argparse
import sys
import json
import numpy as np
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import common reusable components from V1 detector and probe
from scripts.change_detection_v1 import calc_robust_z, extract_regions, save_visual, Z_THRESH, MIN_AREA_PIXELS
from scripts.spectral_analysis_probe import calculate_indices

DEMO_DIR = Path("examples/demo_output")

def generate_synthetic_data(shape=(500, 500), seed=42):
    """
    Generate deterministic synthetic raw bands for T1 and T2 to demonstrate the pipeline.
    This replaces Sentinel-2 ingestion for the synthetic demo.
    """
    np.random.seed(seed)
    h, w = shape
    
    def make_correlated_field(mean, std):
        noise = np.random.normal(0, 1, shape)
        smoothed = ndimage.gaussian_filter(noise, sigma=3)
        smoothed = (smoothed - np.mean(smoothed)) / np.std(smoothed)
        return (smoothed * std + mean).astype(np.float32)

    # Base backgrounds (e.g. Vegetation) with spatial smoothing
    b_blue = make_correlated_field(0.02, 0.005)
    b_green = make_correlated_field(0.04, 0.005)
    b_red = make_correlated_field(0.03, 0.005)
    b_nir = make_correlated_field(0.30, 0.02)
    b_swir = make_correlated_field(0.15, 0.01)
    
    data_t1 = {
        "blue": b_blue.copy(), "green": b_green.copy(), "red": b_red.copy(),
        "nir": b_nir.copy(), "swir16": b_swir.copy()
    }
    data_t2 = {
        "blue": b_blue.copy(), "green": b_green.copy(), "red": b_red.copy(),
        "nir": b_nir.copy(), "swir16": b_swir.copy()
    }
    
    # Introduce broad temporal variation (e.g., seasonal dimming)
    data_t2["nir"] *= 0.8
    data_t2["red"] *= 0.9
    
    # Add localized changes
    # 1. Veg to Water (Flooding): NIR drops heavily, Green slightly up, SWIR drops
    data_t2["nir"][50:150, 50:150] = np.random.normal(0.05, 0.01, (100, 100))
    data_t2["red"][50:150, 50:150] = np.random.normal(0.04, 0.01, (100, 100))
    data_t2["green"][50:150, 50:150] = np.random.normal(0.08, 0.01, (100, 100))
    data_t2["swir16"][50:150, 50:150] = np.random.normal(0.02, 0.01, (100, 100))
    
    # 2. Veg to Built (Construction): NIR drops, SWIR heavily increases, Red increases
    data_t2["nir"][300:400, 300:400] = np.random.normal(0.15, 0.01, (100, 100))
    data_t2["red"][300:400, 300:400] = np.random.normal(0.15, 0.01, (100, 100))
    data_t2["green"][300:400, 300:400] = np.random.normal(0.12, 0.01, (100, 100))
    data_t2["swir16"][300:400, 300:400] = np.random.normal(0.35, 0.02, (100, 100))
    
    # 3. Water to Land (Drying)
    # T1 is Water here
    data_t1["nir"][100:200, 350:450] = np.random.normal(0.05, 0.01, (100, 100))
    data_t1["swir16"][100:200, 350:450] = np.random.normal(0.02, 0.01, (100, 100))
    data_t1["green"][100:200, 350:450] = np.random.normal(0.08, 0.01, (100, 100))
    data_t1["red"][100:200, 350:450] = np.random.normal(0.04, 0.01, (100, 100))
    # T2 is Bare land (similar to built but less extreme)
    data_t2["nir"][100:200, 350:450] = np.random.normal(0.20, 0.02, (100, 100))
    data_t2["swir16"][100:200, 350:450] = np.random.normal(0.25, 0.02, (100, 100))
    data_t2["green"][100:200, 350:450] = np.random.normal(0.10, 0.01, (100, 100))
    data_t2["red"][100:200, 350:450] = np.random.normal(0.15, 0.01, (100, 100))
    
    # Valid mask (all True for simplicity, with a small cutout to simulate clouds)
    joint_mask = np.ones(shape, dtype=bool)
    joint_mask[450:480, 450:480] = False
    
    return data_t1, data_t2, joint_mask

def rgb_visual(data, out_path, title):
    # Normalize RGB for simple visualization
    rgb = np.dstack([data["red"], data["green"], data["blue"]])
    rgb = np.clip(rgb / 0.3, 0, 1)
    
    plt.figure(figsize=(8, 8))
    plt.imshow(rgb)
    plt.title(title + " (DEMO / SYNTHETIC DATA)")
    plt.axis('off')
    plt.savefig(out_path, bbox_inches='tight', dpi=150)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="TerraSeek V1 Detector Demo")
    parser.add_argument("--mode", choices=["synthetic"], required=True, help="Run mode (must be synthetic for demo)")
    args = parser.parse_args()
    
    if args.mode != "synthetic":
        print("Only 'synthetic' mode is supported in the demo pipeline.")
        sys.exit(1)
        
    print("Initializing synthetic demo pipeline (Deterministic Mode)...")
    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Provide synthetic data
    data_t1, data_t2, joint_mask = generate_synthetic_data()
    
    # Save base visuals
    rgb_visual(data_t1, DEMO_DIR / "before.png", "T1 RGB")
    rgb_visual(data_t2, DEMO_DIR / "after.png", "T2 RGB")
    
    print("Calculating indices...")
    # 2. Use the SAME spectral index representation
    idx_t1 = calculate_indices(data_t1)
    idx_t2 = calculate_indices(data_t2)
    
    print("Running common change detector (MAD + Multi-Index)...")
    deltas = {}
    z_scores = {}
    robust_params = {}
    
    # 3. Same change detector robust statistics
    for k in idx_t1.keys():
        deltas[k] = idx_t2[k] - idx_t1[k]
        z_safe, med, mad = calc_robust_z(deltas[k], joint_mask)
        z_scores[k] = z_safe
        robust_params[k] = {"median": med, "mad": mad}
        
    # Multi-index rules (same logic)
    mask_veg_to_built = joint_mask & (z_scores["NDVI"] <= -Z_THRESH) & (z_scores["NDBI"] >= Z_THRESH)
    mask_veg_to_water = joint_mask & (z_scores["NDVI"] <= -Z_THRESH) & (z_scores["MNDWI"] >= Z_THRESH)
    mask_water_to_land = joint_mask & (z_scores["MNDWI"] <= -Z_THRESH) & ((z_scores["NDBI"] >= Z_THRESH) | (z_scores["NDVI"] >= Z_THRESH))
    
    print("Extracting and explaining regions...")
    # 4. Same region extraction & explainability
    regions_vb, fmask_vb = extract_regions(mask_veg_to_built, z_scores, deltas, "Veg_to_Built", joint_mask)
    regions_vw, fmask_vw = extract_regions(mask_veg_to_water, z_scores, deltas, "Veg_to_Water", joint_mask)
    regions_wl, fmask_wl = extract_regions(mask_water_to_land, z_scores, deltas, "Water_to_Land", joint_mask)
    
    all_regions = regions_vb + regions_vw + regions_wl
    all_regions = sorted(all_regions, key=lambda x: x["area_m2"], reverse=True)
    
    # 5. Output formats
    final_change_mask = np.zeros(joint_mask.shape, dtype=np.float32)
    final_change_mask[fmask_vb] = 1
    final_change_mask[fmask_vw] = 2
    final_change_mask[fmask_wl] = 3
    final_change_mask[~joint_mask] = np.nan
    
    save_visual(final_change_mask, DEMO_DIR / "change_map.png", "Change Map (1=Built, 2=Water, 3=Land) (DEMO / SYNTHETIC DATA)", "viridis")
    save_visual(deltas["NDVI"], DEMO_DIR / "ndvi_delta.png", "NDVI Delta (DEMO / SYNTHETIC DATA)", "seismic", -0.5, 0.5)
    save_visual(deltas["NDWI"], DEMO_DIR / "ndwi_delta.png", "NDWI Delta (DEMO / SYNTHETIC DATA)", "seismic", -0.5, 0.5)
    
    report = {
        "metadata": {
            "mode": "synthetic",
            "disclaimer": "DEMO / SYNTHETIC DATA. NOT ACTUAL SATELLITE DERIVED."
        },
        "summary": {
            "total_pixels": int(np.prod(joint_mask.shape)),
            "joint_valid_pixels": int(np.sum(joint_mask)),
            "detected_regions_count": len(all_regions),
            "total_changed_area_m2": sum(r["area_m2"] for r in all_regions)
        },
        "regions": all_regions
    }
    
    with open(DEMO_DIR / "summary.json", "w") as f:
        json.dump(report["summary"], f, indent=2)
        
    with open(DEMO_DIR / "regions.json", "w") as f:
        json.dump(report["regions"], f, indent=2)
        
    print("Demo execution complete. Check examples/demo_output/ for results.")

if __name__ == "__main__":
    main()
