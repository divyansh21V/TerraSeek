import sys
from pathlib import Path
import json
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

# Import from the existing probe
from scripts.spectral_analysis_probe import (
    fetch_stac_item, build_target_grid, load_and_resample, 
    build_valid_mask, calculate_indices, T1_ID, T2_ID
)

PROBE_DIR = Path("data/probe/change_design")
PROBE_DIR.mkdir(parents=True, exist_ok=True)

def calc_robust_stats(delta, mask):
    valid = delta[mask]
    valid = valid[~np.isnan(valid)]
    
    count = valid.size
    if count == 0:
        return None
        
    mean = float(np.mean(valid))
    median = float(np.median(valid))
    std = float(np.std(valid))
    
    # MAD (Median Absolute Deviation)
    mad = float(np.median(np.abs(valid - median)))
    
    percentiles = [1, 2, 5, 10, 25, 50, 75, 90, 95, 98, 99]
    p_vals = np.percentile(valid, percentiles)
    p_dict = {f"p{p:02d}": float(v) for p, v in zip(percentiles, p_vals)}
    
    return {
        "mean": mean,
        "median": median,
        "std": std,
        "mad": mad,
        **p_dict
    }

def analyze_spatial_structure(delta, mask, p99_val, p01_val):
    # Analyze p99 tail
    mask_p99 = mask & (delta >= p99_val) & ~np.isnan(delta)
    labeled_p99, num_features_p99 = ndimage.label(mask_p99)
    if num_features_p99 > 0:
        sizes_p99 = ndimage.sum(mask_p99, labeled_p99, range(1, num_features_p99 + 1))
        max_size_p99 = float(np.max(sizes_p99))
        pct_in_largest_p99 = float(max_size_p99 / np.sum(mask_p99)) * 100
        mean_size_p99 = float(np.mean(sizes_p99))
    else:
        max_size_p99 = 0.0
        pct_in_largest_p99 = 0.0
        mean_size_p99 = 0.0

    # Analyze p01 tail
    mask_p01 = mask & (delta <= p01_val) & ~np.isnan(delta)
    labeled_p01, num_features_p01 = ndimage.label(mask_p01)
    if num_features_p01 > 0:
        sizes_p01 = ndimage.sum(mask_p01, labeled_p01, range(1, num_features_p01 + 1))
        max_size_p01 = float(np.max(sizes_p01))
        pct_in_largest_p01 = float(max_size_p01 / np.sum(mask_p01)) * 100
        mean_size_p01 = float(np.mean(sizes_p01))
    else:
        max_size_p01 = 0.0
        pct_in_largest_p01 = 0.0
        mean_size_p01 = 0.0

    return {
        "upper_99th_tail": {
            "num_components": int(num_features_p99),
            "max_component_size": int(max_size_p99),
            "mean_component_size": float(mean_size_p99),
            "pct_pixels_in_largest": float(pct_in_largest_p99)
        },
        "lower_1st_tail": {
            "num_components": int(num_features_p01),
            "max_component_size": int(max_size_p01),
            "mean_component_size": float(mean_size_p01),
            "pct_pixels_in_largest": float(pct_in_largest_p01)
        }
    }

def calculate_cross_index(delta_a, delta_b, mask, condition_a, condition_b):
    cross_mask = mask & condition_a(delta_a) & condition_b(delta_b)
    
    labeled, num_features = ndimage.label(cross_mask)
    count = int(np.sum(cross_mask))
    
    if num_features > 0:
        sizes = ndimage.sum(cross_mask, labeled, range(1, num_features + 1))
        max_size = float(np.max(sizes))
        pct_in_largest = float(max_size / count) * 100
        mean_size = float(np.mean(sizes))
    else:
        max_size = 0.0
        pct_in_largest = 0.0
        mean_size = 0.0
        
    return {
        "pixel_count": count,
        "pct_of_joint_valid": float(count / np.sum(mask)) * 100 if np.sum(mask) > 0 else 0,
        "spatial_components": {
            "num_components": int(num_features),
            "max_component_size": int(max_size),
            "mean_component_size": float(mean_size),
            "pct_pixels_in_largest": float(pct_in_largest)
        }
    }

def main():
    print("Loading T1/T2 items...")
    item_t1 = fetch_stac_item(T1_ID)
    item_t2 = fetch_stac_item(T2_ID)

    print("Building target grids...")
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
    robust_stats = {}
    spatial_stats = {}
    
    for k in idx_t1.keys():
        deltas[k] = idx_t2[k] - idx_t1[k]
        robust_stats[k] = calc_robust_stats(deltas[k], joint)
        spatial_stats[k] = analyze_spatial_structure(
            deltas[k], joint, robust_stats[k]["p99"], robust_stats[k]["p01"]
        )
        
    print("Calculating centered deltas (Global Shift Analysis)...")
    centered_stats = {}
    for k in deltas.keys():
        med = robust_stats[k]["median"]
        delta_centered = deltas[k] - med
        centered_stats[k] = calc_robust_stats(delta_centered, joint)
        
    print("Calculating cross-index agreement...")
    def dec_ndvi(x): return x <= robust_stats["NDVI"]["p05"]
    def inc_ndbi(x): return x >= robust_stats["NDBI"]["p95"]
    def inc_mndwi(x): return x >= robust_stats["MNDWI"]["p95"]
    def inc_ndwi(x): return x >= robust_stats["NDWI"]["p95"]
    def dec_ndbi(x): return x <= robust_stats["NDBI"]["p05"]
    
    cross_index = {
        "NDVI_decrease_AND_NDBI_increase": calculate_cross_index(deltas["NDVI"], deltas["NDBI"], joint, dec_ndvi, inc_ndbi),
        "NDVI_decrease_AND_MNDWI_increase": calculate_cross_index(deltas["NDVI"], deltas["MNDWI"], joint, dec_ndvi, inc_mndwi),
        "NDVI_decrease_AND_NDWI_increase": calculate_cross_index(deltas["NDVI"], deltas["NDWI"], joint, dec_ndvi, inc_ndwi),
        "NDBI_increase_AND_NDVI_decrease": calculate_cross_index(deltas["NDBI"], deltas["NDVI"], joint, inc_ndbi, dec_ndvi),
        "MNDWI_increase_AND_NDVI_decrease": calculate_cross_index(deltas["MNDWI"], deltas["NDVI"], joint, inc_mndwi, dec_ndvi)
    }

    print("Investigating extreme pixels...")
    extreme_pixels = {}
    for k in ["NDVI", "NDBI"]:
        valid_indices = np.where(joint)
        vals = deltas[k][valid_indices]
        
        # Max positive extremes
        top_idx_pos = np.argsort(vals)[-5:]
        sample_pos = []
        for i in top_idx_pos:
            r, c = valid_indices[0][i], valid_indices[1][i]
            p_data = {
                "row": int(r), "col": int(c),
                f"Delta_{k}": float(deltas[k][r, c]),
                "T1": {b: float(data_t1[b][r, c]) for b in data_t1},
                "T2": {b: float(data_t2[b][r, c]) for b in data_t2}
            }
            sample_pos.append(p_data)
            
        # Max negative extremes
        top_idx_neg = np.argsort(vals)[:5]
        sample_neg = []
        for i in top_idx_neg:
            r, c = valid_indices[0][i], valid_indices[1][i]
            p_data = {
                "row": int(r), "col": int(c),
                f"Delta_{k}": float(deltas[k][r, c]),
                "T1": {b: float(data_t1[b][r, c]) for b in data_t1},
                "T2": {b: float(data_t2[b][r, c]) for b in data_t2}
            }
            sample_neg.append(p_data)
            
        extreme_pixels[f"max_positive_{k}"] = sample_pos
        extreme_pixels[f"max_negative_{k}"] = sample_neg

    report = {
        "robust_statistics": robust_stats,
        "centered_statistics": centered_stats,
        "spatial_structure": spatial_stats,
        "cross_index_agreement": cross_index,
        "extreme_pixels": extreme_pixels
    }
    
    with open(PROBE_DIR / "change_design_report.json", "w") as f:
        json.dump(report, f, indent=2)
        
    print("Generating diagnostic visualizations...")
    med = robust_stats["NDVI"]["median"]
    mad = robust_stats["NDVI"]["mad"]
    z_ndvi = (deltas["NDVI"] - med) / (1.4826 * mad)
    
    plt.figure(figsize=(8,8))
    plt.imshow(z_ndvi, cmap="seismic", vmin=-5, vmax=5)
    plt.colorbar(label="Robust Standardized Delta (MADs)")
    plt.title("Robust Standardized Delta NDVI")
    plt.axis("off")
    plt.savefig(PROBE_DIR / "z_robust_delta_ndvi.png", dpi=150, bbox_inches='tight')
    plt.close()

    print("Done")
    
if __name__ == "__main__":
    main()
