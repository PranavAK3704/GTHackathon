from pathlib import Path
from typing import Dict, Any, Tuple, List

import pandas as pd
from dateutil import parser as date_parser


def _read_csv(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Expected CSV not found at {path}")
    return pd.read_csv(path)


def load_all_data(cfg: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load all core datasets: customers, orders, stores, coupons.
    """
    data_cfg = cfg["data"]

    customers = _read_csv(data_cfg["customers"])
    orders = _read_csv(data_cfg["orders"])
    stores = _read_csv(data_cfg["stores"])
    coupons = _read_csv(data_cfg["coupons"])

    # parse datetimes for orders & coupon expiry if present
    if "created_at" in orders.columns:
        orders["created_at"] = orders["created_at"].apply(
            lambda x: date_parser.parse(str(x)) if pd.notna(x) else pd.NaT
        )

    if "expiry_date" in coupons.columns:
        coupons["expiry_date"] = coupons["expiry_date"].apply(
            lambda x: date_parser.parse(str(x)) if pd.notna(x) else pd.NaT
        )

    return customers, orders, stores, coupons


def get_customer(customers: pd.DataFrame, user_id: str) -> Dict[str, Any] | None:
    """
    Look up a single customer by ID.
    """
    row = customers.loc[customers["customer_id"] == user_id]
    if row.empty:
        return None
    return row.iloc[0].to_dict()


def get_recent_orders(orders: pd.DataFrame, user_id: str, n: int = 3) -> List[Dict[str, Any]]:
    """
    Return last N orders for a customer, most recent first.
    """
    if "created_at" in orders.columns:
        df = orders.sort_values("created_at", ascending=False)
    else:
        df = orders.copy()

    df = df.loc[df["customer_id"] == user_id]
    return df.head(n).to_dict(orient="records")


def get_active_coupons(coupons: pd.DataFrame, user_id: str) -> List[Dict[str, Any]]:
    """
    Fetch non-expired coupons for a customer, if expiry_date exists.
    """
    df = coupons.loc[coupons["customer_id"] == user_id].copy()

    if "expiry_date" in df.columns:
        df = df.loc[(df["expiry_date"].isna()) | (df["expiry_date"] >= pd.Timestamp.utcnow())]

    return df.to_dict(orient="records")
