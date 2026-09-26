import sys
from pathlib import Path
import json
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

# Import from existing probe
from scripts.spectral_analysis_probe import (
    fetch_stac_item, build_target_grid, load_and_resample, 
    build_valid_mask, calculate_indices, T1_ID, T2_ID
)

PROBE_DIR = Path("data/probe/change_detection")
PROBE_DIR.mkdir(parents=True, exist_ok=True)

# Defensible diagnostic thresholds
Z_THRESH = 3.0
MIN_AREA_PIXELS = 10  # 10 pixels * 100m^2 = 1000m^2

def calc_robust_z(delta, mask):
    valid = delta[mask]
    valid = valid[~np.isnan(valid)]
    if valid.size == 0:
        return np.zeros_like(delta), 0, 0
    median = float(np.median(valid))
    mad = float(np.median(np.abs(valid - median)))
    if mad == 0:
        mad = 1e-6
    z = (delta - median) / (1.4826 * mad)
    # Mask out invalid pixels in Z
    z_safe = np.copy(z)
    z_safe[~mask] = np.nan
    return z_safe, median, mad

def extract_regions(boolean_mask, z_scores, deltas, evidence_label, joint_mask):
    labeled_array, num_features = ndimage.label(boolean_mask)
    regions = []
    
    if num_features == 0:
        return regions, np.zeros_like(boolean_mask)
        
    sizes = ndimage.sum(boolean_mask, labeled_array, range(1, num_features + 1))
    
    # Filter by size
    valid_labels = np.where(sizes >= MIN_AREA_PIXELS)[0] + 1
    
    filtered_mask = np.isin(labeled_array, valid_labels)
    filtered_labeled, num_filtered = ndimage.label(filtered_mask)
    
    # Extract properties
    for i in range(1, num_filtered + 1):
        region_mask = (filtered_labeled == i)
        pixel_count = int(np.sum(region_mask))
        area_m2 = pixel_count * 100  # 10m x 10m pixels
        
        # Calculate magnitudes for supporting indices
        supporting_indices = []
        for idx_name, z_array in z_scores.items():
            mean_z = float(np.nanmean(z_array[region_mask]))
            if abs(mean_z) >= Z_THRESH:
                supporting_indices.append(idx_name)
                
        # Primary magnitude from NDVI/NDBI or highest absolute Z
        magnitudes = [abs(float(np.nanmean(z[region_mask]))) for z in z_scores.values()]
        primary_mag = max(magnitudes) if magnitudes else 0
        
        confidence = "strong evidence" if primary_mag > 5.0 else "moderate evidence"
        
        # Explainability
        if "Veg_to_Built" in evidence_label:
            interp = "Likely vegetation-to-built-surface transition."
            ev = ["Strong NDVI decrease", "Strong NDBI increase"]
        elif "Veg_to_Water" in evidence_label:
            interp = "Likely vegetation-to-water/flooding transition."
            ev = ["Strong NDVI decrease", "Strong NDWI/MNDWI increase"]
        elif "Water_to_Land" in evidence_label:
            interp = "Likely water-to-land/drying transition."
            ev = ["Strong MNDWI decrease", "Strong NDVI/NDBI increase"]
        else:
            interp = "Unclassified anomalous spectral change."
            ev = supporting_indices
            
        region = {
            "region_id": f"{evidence_label}_R{i}",
            "area_m2": area_m2,
            "pixel_count": pixel_count,
            "change_magnitude": primary_mag,
            "supporting_indices": supporting_indices,
            "evidence": ev,
            "valid_observation_fraction": 1.0, # Pixels inside the region are all valid by definition
            "spatial_coherence": pixel_count, # Simple proxy for coherence
            "interpretation": interp,
            "confidence": confidence
        }
        regions.append(region)
        
    return regions, filtered_mask

def save_visual(data, out_path, title, cmap, vmin=None, vmax=None):
    plt.figure(figsize=(10, 10))
    current_cmap = plt.get_cmap(cmap).copy()
    current_cmap.set_bad(color='black')
    plt.imshow(data, cmap=current_cmap, vmin=vmin, vmax=vmax)
    plt.colorbar(fraction=0.046, pad=0.04)
    plt.title(title)
    plt.axis('off')
    plt.savefig(out_path, bbox_inches='tight', dpi=150)
    plt.close()

def main():
    print("Loading T1/T2 items...")
    item_t1 = fetch_stac_item(T1_ID)
    item_t2 = fetch_stac_item(T2_ID)

    print("Building authoritative target grid...")
    grid = build_target_grid(item_t1)
    
    print("Loading and resampling assets...")
    data_t1 = load_and_resample(item_t1, grid)
    data_t2 = load_and_resample(item_t2, grid)

    print("Building masks...")
    mask_t1 = build_valid_mask(data_t1["scl"])
    mask_t2 = build_valid_mask(data_t2["scl"])
    joint = mask_t1 & mask_t2
    
    print("Calculating indices...")
    idx_t1 = calculate_indices(data_t1)
    idx_t2 = calculate_indices(data_t2)
    
    deltas = {}
    z_scores = {}
    robust_params = {}
    
    for k in idx_t1.keys():
        deltas[k] = idx_t2[k] - idx_t1[k]
        z_safe, med, mad = calc_robust_z(deltas[k], joint)
        z_scores[k] = z_safe
        robust_params[k] = {"median": med, "mad": mad}
        
    print("Evaluating multi-index evidence rules...")
    
    # Rule 1: Veg -> Built (NDVI drops, NDBI rises)
    mask_veg_to_built = joint & (z_scores["NDVI"] <= -Z_THRESH) & (z_scores["NDBI"] >= Z_THRESH)
    
    # Rule 2: Veg -> Water (NDVI drops, NDWI/MNDWI rises)
    mask_veg_to_water = joint & (z_scores["NDVI"] <= -Z_THRESH) & (z_scores["MNDWI"] >= Z_THRESH)
    
    # Rule 3: Water -> Land (MNDWI drops, NDBI or NDVI rises)
    mask_water_to_land = joint & (z_scores["MNDWI"] <= -Z_THRESH) & ((z_scores["NDBI"] >= Z_THRESH) | (z_scores["NDVI"] >= Z_THRESH))
    
    print("Applying spatial coherence filtering and extracting regions...")
    
    regions_vb, fmask_vb = extract_regions(mask_veg_to_built, z_scores, deltas, "Veg_to_Built", joint)
    regions_vw, fmask_vw = extract_regions(mask_veg_to_water, z_scores, deltas, "Veg_to_Water", joint)
    regions_wl, fmask_wl = extract_regions(mask_water_to_land, z_scores, deltas, "Water_to_Land", joint)
    
    all_regions = regions_vb + regions_vw + regions_wl
    
    # Combine masks for visual
    final_change_mask = np.zeros(joint.shape, dtype=np.uint8)
    final_change_mask[fmask_vb] = 1
    final_change_mask[fmask_vw] = 2
    final_change_mask[fmask_wl] = 3
    # 0 = No change/masked
    
    # Mask out invalid pixels for visualization
    final_change_mask_vis = final_change_mask.astype(float)
    final_change_mask_vis[~joint] = np.nan
    
    report = {
        "grid": {
            "crs": str(grid["crs"]),
            "width": grid["width"],
            "height": grid["height"],
            "transform": [float(x) for x in grid["transform"]]
        },
        "detector_parameters": {
            "robust_z_threshold": Z_THRESH,
            "min_component_pixels": MIN_AREA_PIXELS,
            "min_area_m2": MIN_AREA_PIXELS * 100
        },
        "robust_standardization": robust_params,
        "summary": {
            "total_pixels": int(grid["width"] * grid["height"]),
            "joint_valid_pixels": int(np.sum(joint)),
            "detected_regions_count": len(all_regions),
            "total_changed_area_m2": sum(r["area_m2"] for r in all_regions)
        },
        "regions": sorted(all_regions, key=lambda x: x["area_m2"], reverse=True)
    }
    
    print("Saving detector report...")
    with open(PROBE_DIR / "detector_report.json", "w") as f:
        json.dump(report, f, indent=2)
        
    print("Saving visualizations...")
    save_visual(final_change_mask_vis, PROBE_DIR / "final_change_mask.png", "Change Detection V1 Mask (1=Built, 2=Water, 3=Land)", "viridis")
    save_visual(z_scores["NDVI"], PROBE_DIR / "z_ndvi.png", "Robust Z-Score (NDVI)", "seismic", -5, 5)
    save_visual(z_scores["NDBI"], PROBE_DIR / "z_ndbi.png", "Robust Z-Score (NDBI)", "seismic", -5, 5)
    
    print("V1 Detector completed.")

if __name__ == "__main__":
    main()
