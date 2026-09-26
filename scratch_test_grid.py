import rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds
from scripts.spectral_analysis_probe import fetch_stac_item, T1_ID, T2_ID, AOI_WEST, AOI_SOUTH, AOI_EAST, AOI_NORTH

item1 = fetch_stac_item(T1_ID)
props = item1['properties']
dst_crs = f"EPSG:{props.get('proj:epsg')}"
left, bottom, right, top = transform_bounds('EPSG:4326', dst_crs, AOI_WEST, AOI_SOUTH, AOI_EAST, AOI_NORTH)
asset_url = item1['assets']['blue']['href']

with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", AWS_NO_SIGN_REQUEST="YES"):
    with rasterio.open(asset_url) as src:
        window = from_bounds(left, bottom, right, top, src.transform)
        print("Raw window:", window)
        print("Rounded width, height:", round(window.width), round(window.height))
        
        w_rounded = window.round_lengths().round_offsets()
        print("Rounded window:", w_rounded)
        print("Rounded window width, height:", w_rounded.width, w_rounded.height)
