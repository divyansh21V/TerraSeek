"""
Sentinel-2 spectral-analysis probe.
Validates spectral index calculation over a common 10m grid.
"""

import json
import numpy as np
import rasterio
from rasterio.warp import transform_bounds, reproject, Resampling
from rasterio.windows import from_bounds
import matplotlib.pyplot as plt
from pathlib import Path
import httpx

# Define constants
T1_ID = "S2A_36RUU_20231129_0_L2A"
T2_ID = "S2B_36RUU_20231224_0_L2A"
AOI_SOUTH, AOI_WEST, AOI_NORTH, AOI_EAST = 29.90, 31.65, 30.15, 31.95

BANDS_10M = {"blue": "blue", "green": "green", "red": "red", "nir": "nir"}
BANDS_20M = {"swir16": "swir16", "swir22": "swir22", "scl": "scl"}
VALID_SCL_CLASSES = [4, 5, 6, 7]

PROBE_DIR = Path("data/probe/spectral")
PROBE_DIR.mkdir(parents=True, exist_ok=True)

def fetch_stac_item(item_id):
    url = f"https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a/items/{item_id}"
    resp = httpx.get(url, timeout=30.0)
    resp.raise_for_status()
    return resp.json()

def build_target_grid(item):
    """Derive the 10m target grid from the 'blue' 10m asset."""
    props = item["properties"]
    dst_crs = f"EPSG:{props.get('proj:epsg')}"
    left, bottom, right, top = transform_bounds(
        "EPSG:4326", dst_crs, AOI_WEST, AOI_SOUTH, AOI_EAST, AOI_NORTH
    )
    asset_url = item["assets"]["blue"]["href"]
    env = rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", AWS_NO_SIGN_REQUEST="YES")
    with env:
        with rasterio.open(asset_url) as src:
            window = from_bounds(left, bottom, right, top, src.transform).round_lengths().round_offsets()
            win_transform = src.window_transform(window)
            width = int(window.width)
            height = int(window.height)
            return {
                "crs": src.crs,
                "transform": win_transform,
                "width": width,
                "height": height,
                "bounds": rasterio.windows.bounds(window, src.transform)
            }

def load_and_resample(item, target_grid):
    """Load all assets and resample to the target grid."""
    assets_data = {}
    env = rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", AWS_NO_SIGN_REQUEST="YES")
    with env:
        # 10m bands
        for name, stac_key in BANDS_10M.items():
            url = item["assets"][stac_key]["href"]
            with rasterio.open(url) as src:
                window = from_bounds(*target_grid["bounds"], src.transform)
                data = src.read(1, window=window, out_shape=(target_grid["height"], target_grid["width"]))
                assets_data[name] = data.astype(np.float32)

        # 20m bands
        for name, stac_key in BANDS_20M.items():
            url = item["assets"][stac_key]["href"]
            with rasterio.open(url) as src:
                window = from_bounds(*target_grid["bounds"], src.transform)
                source_data = src.read(1, window=window)
                source_transform = src.window_transform(window)
                
                dest_data = np.zeros((target_grid["height"], target_grid["width"]), dtype=np.float32)
                resampling_alg = Resampling.nearest if name == "scl" else Resampling.bilinear
                
                reproject(
                    source=source_data,
                    destination=dest_data,
                    src_transform=source_transform,
                    src_crs=src.crs,
                    dst_transform=target_grid["transform"],
                    dst_crs=target_grid["crs"],
                    resampling=resampling_alg
                )
                assets_data[name] = dest_data

    return assets_data

def build_valid_mask(scl_data):
    return np.isin(scl_data, VALID_SCL_CLASSES)

def safe_index(b1, b2):
    """Calculates (b1 - b2) / (b1 + b2)."""
    num = b1 - b2
    den = b1 + b2
    return np.divide(num, den, out=np.full_like(num, np.nan), where=(den != 0))

def calculate_indices(data):
    b02 = data["blue"]
    b03 = data["green"]
    b04 = data["red"]
    b08 = data["nir"]
    b11 = data["swir16"]
    
    return {
        "NDVI": safe_index(b08, b04),
        "NDWI": safe_index(b03, b08),
        "MNDWI": safe_index(b03, b11),
        "NDBI": safe_index(b11, b08)
    }

def calculate_statistics(array, mask):
    valid_data = array[mask]
    valid_data = valid_data[~np.isnan(valid_data)]
    
    count = valid_data.size
    if count == 0:
        return {"valid_pixel_count": 0}
        
    return {
        "valid_pixel_count": int(count),
        "min": float(np.min(valid_data)),
        "max": float(np.max(valid_data)),
        "mean": float(np.mean(valid_data)),
        "median": float(np.median(valid_data)),
        "std": float(np.std(valid_data)),
        "p02": float(np.percentile(valid_data, 2)),
        "p05": float(np.percentile(valid_data, 5)),
        "p25": float(np.percentile(valid_data, 25)),
        "p75": float(np.percentile(valid_data, 75)),
        "p95": float(np.percentile(valid_data, 95)),
        "p98": float(np.percentile(valid_data, 98))
    }

def save_diagnostic_plot(data, out_path, title, cmap, vmin, vmax):
    plt.figure(figsize=(8, 8))
    vis_data = data.copy()
    current_cmap = plt.get_cmap(cmap).copy()
    current_cmap.set_bad(color='black')
    
    plt.imshow(vis_data, cmap=current_cmap, vmin=vmin, vmax=vmax)
    plt.colorbar(fraction=0.046, pad=0.04)
    plt.title(title)
    plt.axis('off')
    plt.savefig(out_path, bbox_inches='tight', dpi=150)
    plt.close()

def validate_alignment(grid1, grid2):
    assert grid1["crs"] == grid2["crs"], "CRS mismatch!"
    assert grid1["width"] == grid2["width"], "Width mismatch!"
    assert grid1["height"] == grid2["height"], "Height mismatch!"
    assert grid1["transform"] == grid2["transform"], "Transform mismatch!"

def main():
    print("Loading metadata...")
    item_t1 = fetch_stac_item(T1_ID)
    item_t2 = fetch_stac_item(T2_ID)
    
    print("Building target grids...")
    grid_t1 = build_target_grid(item_t1)
    grid_t2 = build_target_grid(item_t2)
    
    validate_alignment(grid_t1, grid_t2)
    target_grid = grid_t1
    
    print("Loading and resampling assets...")
    data_t1 = load_and_resample(item_t1, target_grid)
    data_t2 = load_and_resample(item_t2, target_grid)
    
    h, w = target_grid["height"], target_grid["width"]
    for k in data_t1:
        assert data_t1[k].shape == (h, w), f"T1 shape mismatch for {k}"
        assert data_t2[k].shape == (h, w), f"T2 shape mismatch for {k}"
        
    print("Building masks...")
    mask_t1 = build_valid_mask(data_t1["scl"])
    mask_t2 = build_valid_mask(data_t2["scl"])
    joint_mask = mask_t1 & mask_t2
    
    total_pixels = h * w
    print(f"Total pixels: {total_pixels}")
    pct_valid_t1 = (np.sum(mask_t1) / total_pixels) * 100
    pct_valid_t2 = (np.sum(mask_t2) / total_pixels) * 100
    pct_valid_joint = (np.sum(joint_mask) / total_pixels) * 100
    
    print(f"T1 Valid: {pct_valid_t1:.2f}% | Masked: {100-pct_valid_t1:.2f}%")
    print(f"T2 Valid: {pct_valid_t2:.2f}% | Masked: {100-pct_valid_t2:.2f}%")
    print(f"Joint Valid: {pct_valid_joint:.2f}% | Masked: {100-pct_valid_joint:.2f}%")
    
    assert joint_mask.shape == (h, w), "Joint mask shape mismatch"
    
    print("Calculating indices...")
    idx_t1 = calculate_indices(data_t1)
    idx_t2 = calculate_indices(data_t2)
    
    delta = {}
    report_stats = {}
    
    print("Calculating changes and statistics...")
    for k in idx_t1.keys():
        idx_t1[k][~joint_mask] = np.nan
        idx_t2[k][~joint_mask] = np.nan
        delta[k] = idx_t2[k] - idx_t1[k]
        
        # Explicitly validate raw indices in [-1, 1]
        for arr, name in [(idx_t1[k], "T1"), (idx_t2[k], "T2")]:
            valid_arr = arr[joint_mask]
            valid_arr = valid_arr[~np.isnan(valid_arr)]
            if valid_arr.size > 0:
                assert np.min(valid_arr) >= -1.0 - 1e-5, f"{name} {k} min < -1"
                assert np.max(valid_arr) <= 1.0 + 1e-5, f"{name} {k} max > 1"
                
        # Explicitly validate temporal deltas in [-2, 2]
        delta_arr = delta[k][joint_mask]
        delta_arr = delta_arr[~np.isnan(delta_arr)]
        if delta_arr.size > 0:
            assert np.min(delta_arr) >= -2.0 - 1e-5, f"Delta {k} min < -2"
            assert np.max(delta_arr) <= 2.0 + 1e-5, f"Delta {k} max > 2"
        
        report_stats[f"{k}_T1"] = calculate_statistics(idx_t1[k], joint_mask)
        report_stats[f"{k}_T2"] = calculate_statistics(idx_t2[k], joint_mask)
        report_stats[f"{k}_Delta"] = calculate_statistics(delta[k], joint_mask)
        
        print(f"Saving diagnostic plots for {k}...")
        save_diagnostic_plot(idx_t1[k], PROBE_DIR / f"{k}_T1.png", f"T1 {k}", "RdYlGn" if k=="NDVI" else "RdBu", -1, 1)
        save_diagnostic_plot(idx_t2[k], PROBE_DIR / f"{k}_T2.png", f"T2 {k}", "RdYlGn" if k=="NDVI" else "RdBu", -1, 1)
        save_diagnostic_plot(delta[k], PROBE_DIR / f"{k}_Delta.png", f"Delta {k}", "seismic", -0.5, 0.5)
        
    report = {
        "grid": {
            "crs": str(target_grid["crs"]),
            "width": target_grid["width"],
            "height": target_grid["height"],
            "transform": [float(x) for x in target_grid["transform"]]
        },
        "resampling": {
            "B11": "bilinear",
            "B12": "bilinear",
            "SCL": "nearest"
        },
        "masks": {
            "total_pixels": int(total_pixels),
            "T1_valid_pct": float(pct_valid_t1),
            "T2_valid_pct": float(pct_valid_t2),
            "joint_valid_pct": float(pct_valid_joint)
        },
        "statistics": report_stats
    }
    
    with open(PROBE_DIR / "spectral_report.json", "w") as f:
        json.dump(report, f, indent=2)
        
    print("Spectral analysis probe completed successfully.")

if __name__ == "__main__":
    main()
