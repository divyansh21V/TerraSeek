import rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds
from scripts.spectral_analysis_probe import fetch_stac_item, T1_ID, T2_ID, AOI_WEST, AOI_SOUTH, AOI_EAST, AOI_NORTH

item2 = fetch_stac_item(T2_ID)
props = item2['properties']
dst_crs = f"EPSG:{props.get('proj:epsg')}"
left, bottom, right, top = transform_bounds('EPSG:4326', dst_crs, AOI_WEST, AOI_SOUTH, AOI_EAST, AOI_NORTH)
asset_url2 = item2['assets']['blue']['href']

with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", AWS_NO_SIGN_REQUEST="YES"):
    with rasterio.open(asset_url2) as src:
        window2 = from_bounds(left, bottom, right, top, src.transform)
        print('T2 window:', window2)
        print('T2 height:', window2.height)
