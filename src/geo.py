from typing import Dict, Any, Optional

import math
import pandas as pd


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Approximate distance in meters between two lat/lon points.
    """
    R = 6371000  # Earth radius (m)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def find_nearest_open_store(
    stores: pd.DataFrame,
    lat: float,
    lon: float,
    current_hour: int,
) -> Optional[Dict[str, Any]]:
    """
    Given user location + current hour, return the nearest open store.

    Expected store columns: store_id, name, lat, lon, open_hour, close_hour
    """
    if stores.empty:
        return None

    open_stores = stores[
        (stores["open_hour"] <= current_hour) & (stores["close_hour"] >= current_hour)
    ].copy()

    if open_stores.empty:
        return None

    open_stores["distance_m"] = open_stores.apply(
        lambda r: haversine(lat, lon, float(r["lat"]), float(r["lon"])),
        axis=1,
    )

    best = open_stores.sort_values("distance_m").iloc[0]
    return best.to_dict()
