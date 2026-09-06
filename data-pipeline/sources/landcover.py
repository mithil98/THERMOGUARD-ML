"""
Real fire-source ground truth via ESA WorldCover 10m land cover.

Public, anonymous S3 access (no account needed) — verified working:
    s3://esa-worldcover/v200/2021/map/ESA_WorldCover_10m_2021_v200_<TILE>_Map.tif

Tiles are named by the 3x3-degree cell they cover, e.g. "N18E072" for the
cell starting at 18N, 72E. WorldCover legend (v100/v200, ESA WorldCover
product user manual):

    10  Tree cover              50  Built-up
    20  Shrubland               60  Bare / sparse vegetation
    30  Grassland               70  Snow and ice
    40  Cropland                80  Permanent water bodies
    90  Herbaceous wetland      95  Mangroves
    100 Moss and lichen
"""

import math

import rasterio

WORLDCOVER_BUCKET = "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map"

# Maps WorldCover's 11 classes onto ThermoGuard's fire-source categories.
# This replaces reliance on FIRMS's own `type` field (0=vegetation fire,
# 1=volcano, 2=other static land source, 3=offshore), which is close to an
# answer key for the categories the old fire-source model predicted.
CLASS_TO_FIRE_SOURCE = {
    10: "Vegetation Fire",   # Tree cover
    20: "Vegetation Fire",   # Shrubland
    30: "Vegetation Fire",   # Grassland
    40: "Vegetation Fire",   # Cropland
    50: "Other Land Source",  # Built-up / urban-industrial
    60: "Other Land Source",  # Bare / sparse vegetation
    70: "Other Land Source",  # Snow and ice
    80: "Offshore",           # Permanent water bodies
    90: "Vegetation Fire",   # Herbaceous wetland
    95: "Vegetation Fire",   # Mangroves
    100: "Other Land Source",  # Moss and lichen
}


def tile_name_for(lat: float, lon: float) -> str:
    """WorldCover tiles are 3x3 degrees, named by their lower-left corner."""
    lat0 = int(math.floor(lat / 3) * 3)
    lon0 = int(math.floor(lon / 3) * 3)
    ns = f"N{lat0:02d}" if lat0 >= 0 else f"S{abs(lat0):02d}"
    ew = f"E{lon0:03d}" if lon0 >= 0 else f"W{abs(lon0):03d}"
    return f"{ns}{ew}"


_tile_cache: dict[str, rasterio.io.DatasetReader] = {}


def _get_tile(tile: str) -> rasterio.io.DatasetReader | None:
    if tile in _tile_cache:
        return _tile_cache[tile]

    url = f"{WORLDCOVER_BUCKET}/ESA_WorldCover_10m_2021_v200_{tile}_Map.tif"
    try:
        with rasterio.Env(AWS_NO_SIGN_REQUEST="YES", AWS_REGION="eu-central-1"):
            ds = rasterio.open(url)
    except rasterio.errors.RasterioIOError:
        # No WorldCover tile at this cell (e.g. open ocean far from coast).
        _tile_cache[tile] = None
        return None

    _tile_cache[tile] = ds
    return ds


def fire_source_for(lat: float, lon: float) -> str:
    """Real land-cover-derived fire source category for one hotspot."""
    tile = tile_name_for(lat, lon)
    ds = _get_tile(tile)
    if ds is None:
        return "Unknown"

    with rasterio.Env(AWS_NO_SIGN_REQUEST="YES", AWS_REGION="eu-central-1"):
        row, col = ds.index(lon, lat)
        try:
            value = int(ds.read(1, window=((row, row + 1), (col, col + 1)))[0, 0])
        except IndexError:
            return "Unknown"

    return CLASS_TO_FIRE_SOURCE.get(value, "Unknown")
