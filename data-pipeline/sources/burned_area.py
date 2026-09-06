"""
Real risk ground truth via MODIS MCD64A1 monthly burned-area (v6.1).

Public, anonymous access via Microsoft Planetary Computer's STAC API —
verified working: no account needed, `planetary_computer.sign_inplace`
issues an anonymous SAS token per request.

MCD64A1's "Burn Date" band (per the product user guide) is a 500m raster,
gridded into MODIS sinusoidal tiles (h/v), one monthly granule per tile:
    0        = not burned this month
    1-366    = day of year burned
    -1       = not processed / no data (commonly water or missing input)
    -2       = water mask

This module answers, for one hotspot (lat, lon, date): did a burned-area
pixel appear at this location within `window_days` following the
detection? That becomes the real basis for `risk_level` — replacing the
FRP-threshold bucket the original dataset used — instead of asking "is
FRP above X" it asks "did this actually burn".
"""

from datetime import date, timedelta

import planetary_computer
import pystac_client
import rasterio

STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
COLLECTION = "modis-64A1-061"

_catalog = None


def _get_catalog():
    global _catalog
    if _catalog is None:
        _catalog = pystac_client.Client.open(STAC_URL, modifier=planetary_computer.sign_inplace)
    return _catalog


def burned_outcome_for(
    lat: float,
    lon: float,
    detected_on: date,
    window_days: int = 30,
    neighborhood_px: int = 5,
) -> dict:
    """
    Look up whether a hotspot at (lat, lon) detected on `detected_on`
    corresponds to a mapped burn within the following `window_days`.

    Also counts burned pixels in a `neighborhood_px` x `neighborhood_px`
    window around the point (500m pixels, so 5x5 ~= 2.5km x 2.5km) as a
    cheap size proxy for Medium vs High risk severity — a real, sourced
    number, but a simplification of true fire-perimeter delineation
    (contiguous burned-area polygons), which would need connected-
    component analysis across tile boundaries. Documented as a follow-up
    refinement once this is producing real labels end-to-end.

    Returns:
        {
            "burned": bool,
            "burn_day_of_year": int | None,
            "neighborhood_burned_pixels": int,
            "confidence": "found" | "no_data",
        }
    """
    end = detected_on + timedelta(days=window_days)
    bbox = [lon - 0.05, lat - 0.05, lon + 0.05, lat + 0.05]

    catalog = _get_catalog()
    search = catalog.search(
        collections=[COLLECTION],
        bbox=bbox,
        datetime=f"{detected_on.isoformat()}/{end.isoformat()}",
    )
    items = list(search.items())

    if not items:
        return {
            "burned": False,
            "burn_day_of_year": None,
            "neighborhood_burned_pixels": 0,
            "confidence": "no_data",
        }

    best_day = None
    max_neighbors = 0

    for item in items:
        asset = item.assets.get("Burn_Date")
        if asset is None:
            continue

        with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"):
            with rasterio.open(asset.href) as src:
                # MCD64A1 is in MODIS sinusoidal projection; reproject the
                # point rather than the raster to keep this a cheap lookup.
                from rasterio.warp import transform as warp_transform

                xs, ys = warp_transform("EPSG:4326", src.crs, [lon], [lat])
                row, col = src.index(xs[0], ys[0])

                half = neighborhood_px // 2
                r0, r1 = max(row - half, 0), row + half + 1
                c0, c1 = max(col - half, 0), col + half + 1

                try:
                    block = src.read(1, window=((r0, r1), (c0, c1)))
                except IndexError:
                    continue

        neighbor_count = int((block > 0).sum())
        if neighbor_count > max_neighbors:
            max_neighbors = neighbor_count

        r_local, c_local = row - r0, col - c0
        if 0 <= r_local < block.shape[0] and 0 <= c_local < block.shape[1]:
            center_value = int(block[r_local, c_local])
            if center_value > 0 and best_day is None:
                best_day = center_value

    return {
        "burned": best_day is not None,
        "burn_day_of_year": best_day,
        "neighborhood_burned_pixels": max_neighbors,
        "confidence": "found",
    }
