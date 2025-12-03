from typing import Dict, Any, Optional
import math
import pandas as pd


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000  # meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def find_nearest_open_store(
    stores: pd.DataFrame,
    lat: float,
    lon: float,
    current_hour: int,
) -> Optional[Dict[str, Any]]:
    """
    Return nearest open store; if none open, return nearest store overall.
    """

    if stores.empty:
        return None

    # All stores, compute distance
    stores = stores.copy()
    stores["distance_m"] = stores.apply(
        lambda r: haversine(lat, lon, float(r["lat"]), float(r["lon"])),
        axis=1,
    )

    # Filter open stores
    open_stores = stores[
        (stores["open_hour"] <= current_hour) & (stores["close_hour"] >= current_hour)
    ]

    # If at least one store is open, pick nearest open store
    if not open_stores.empty:
        best = open_stores.sort_values("distance_m").iloc[0]
        return best.to_dict()

    # If NO store is open → return nearest store overall
    best_any = stores.sort_values("distance_m").iloc[0]
    return best_any.to_dict()
