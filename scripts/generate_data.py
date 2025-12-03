import csv
import random
from pathlib import Path
from datetime import datetime, timedelta

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# --------------------------------------------------------------
# CITY COORDINATES (REAL LOCATIONS)
# --------------------------------------------------------------
CITY_COORDS = {
    "Bengaluru": (12.9716, 77.5946),
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.7041, 77.1025),
    "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Jaipur": (26.9124, 75.7873),
    "Ahmedabad": (23.0225, 72.5714),
    "Kochi": (9.9312, 76.2673),
}


# --------------------------------------------------------------
# 1. STORES
# --------------------------------------------------------------
def generate_stores(n_stores: int = 50):
    rows = []

    for i in range(1, n_stores + 1):
        city = random.choice(list(CITY_COORDS.keys()))
        base_lat, base_lon = CITY_COORDS[city]

        # store location within 1–2 km of center
        lat = round(base_lat + random.uniform(-0.02, 0.02), 6)
        lon = round(base_lon + random.uniform(-0.02, 0.02), 6)

        open_hour = random.choice(range(7, 10))
        close_hour = random.choice(range(20, 24))

        rows.append({
            "store_id": f"store_{i:03d}",
            "name": f"{city} Coffee #{i}",
            "city": city,
            "lat": lat,
            "lon": lon,
            "open_hour": open_hour,
            "close_hour": close_hour,
        })

    path = DATA_DIR / "stores.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "store_id", "name", "city",
                "lat", "lon", "open_hour", "close_hour"
            ]
        )
        writer.writeheader()
        writer.writerows(rows)


# --------------------------------------------------------------
# 2. CUSTOMERS
# --------------------------------------------------------------
def generate_customers(n_customers: int = 10000):
    first_names = [
        "Alex","Blake","Chitra","Dev","Esha","Farhan","Gia","Hari",
        "Isha","Kabir","Lena","Mira","Nikhil","Om","Priya","Rohan",
        "Sara","Tanvi","Uma","Vikram"
    ]

    last_names = [
        "Sharma","Patel","Rao","Iyer","Khan","Singh","Nair","Das",
        "Mehta","Kulkarni"
    ]

    tiers = ["Bronze", "Silver", "Gold", "Platinum"]

    rows = []

    for i in range(1, n_customers + 1):
        city = random.choice(list(CITY_COORDS.keys()))
        base_lat, base_lon = CITY_COORDS[city]

        # customer lives within 2 km of the city
        lat = round(base_lat + random.uniform(-0.03, 0.03), 6)
        lon = round(base_lon + random.uniform(-0.03, 0.03), 6)

        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        tier = np.random.choice(tiers, p=[0.5, 0.3, 0.15, 0.05])

        rows.append({
            "customer_id": f"cust_{i:05d}",
            "name": name,
            "city": city,
            "lat": lat,
            "lon": lon,
            "loyalty_tier": tier,
        })

    path = DATA_DIR / "customers.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["customer_id", "name", "city", "lat", "lon", "loyalty_tier"]
        )
        writer.writeheader()
        writer.writerows(rows)


# --------------------------------------------------------------
# 3. ORDERS
# --------------------------------------------------------------
def generate_orders(n_orders: int = 100000):
    customers_path = DATA_DIR / "customers.csv"
    stores_path = DATA_DIR / "stores.csv"

    customers = [row["customer_id"] for row in csv.DictReader(customers_path.open())]
    stores = [row["store_id"] for row in csv.DictReader(stores_path.open())]

    drinks = ["Latte", "Cappuccino", "Espresso", "Hot Cocoa", "Cold Brew", "Mocha"]

    start_date = datetime(2025, 1, 1)
    rows = []

    for i in range(1, n_orders + 1):
        cust = random.choice(customers)
        store = random.choice(stores)

        created_at = start_date + timedelta(
            days=random.randint(0, 180),
            hours=random.randint(7, 22),
            minutes=random.randint(0, 59),
        )

        item = random.choice(drinks)
        quantity = np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1])
        total_amount = round(quantity * np.random.uniform(2.5, 6.0), 2)

        status = np.random.choice(
            ["placed", "preparing", "ready", "delivered"],
            p=[0.1, 0.2, 0.2, 0.5],
        )

        rows.append({
            "order_id": f"ord_{i:06d}",
            "customer_id": cust,
            "store_id": store,
            "status": status,
            "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "item": item,
            "quantity": quantity,
            "total_amount": total_amount,
        })

    path = DATA_DIR / "orders.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "order_id", "customer_id", "store_id", "status",
                "created_at", "item", "quantity", "total_amount"
            ]
        )
        writer.writeheader()
        writer.writerows(rows)


# --------------------------------------------------------------
# 4. COUPONS
# --------------------------------------------------------------
def generate_coupons(max_coupons: int = 40000):
    customers_path = DATA_DIR / "customers.csv"
    stores_path = DATA_DIR / "stores.csv"

    customers = [row["customer_id"] for row in csv.DictReader(customers_path.open())]
    stores = [row["store_id"] for row in csv.DictReader(stores_path.open())]

    rows = []
    coupon_id = 1

    for cust in customers:
        n = np.random.choice([0, 1, 2, 3], p=[0.5, 0.3, 0.15, 0.05])
        for _ in range(n):
            if coupon_id > max_coupons:
                break

            store = random.choice(stores)
            discount = np.random.choice([5, 10, 15, 20], p=[0.4, 0.3, 0.2, 0.1])

            valid_from = datetime(2025, 6, 1) + timedelta(days=random.randint(0, 30))
            valid_to = valid_from + timedelta(days=random.randint(7, 30))

            rows.append({
                "coupon_id": f"cpn_{coupon_id:06d}",
                "customer_id": cust,
                "store_id": store,
                "discount_percent": discount,
                "valid_from": valid_from.strftime("%Y-%m-%d"),
                "valid_to": valid_to.strftime("%Y-%m-%d"),
            })
            coupon_id += 1

        if coupon_id > max_coupons:
            break

    path = DATA_DIR / "coupons.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "coupon_id", "customer_id", "store_id",
                "discount_percent", "valid_from", "valid_to"
            ]
        )
        writer.writeheader()
        writer.writerows(rows)


# --------------------------------------------------------------
# MAIN
# --------------------------------------------------------------
def main():
    print("Generating stores...")
    generate_stores()

    print("Generating customers...")
    generate_customers()

    print("Generating orders...")
    generate_orders()

    print("Generating coupons...")
    generate_coupons()

    print("\nDone! CSV files ready in /data 🎉")


if __name__ == "__main__":
    main()
