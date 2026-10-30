import pandas as pd
from pathlib import Path

# --------------------------------
# 1. Load the dataset
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "orders_sample.csv"

df = pd.read_csv(DATA_PATH)

print("\n========== COD RISK ANALYSIS ==========")

print("\n1. DATASET INFORMATION")
print("--------------------------------------")
print("Total records:", len(df))
print("Total columns:", len(df.columns))
print("Columns:", list(df.columns))


# --------------------------------
# 2. Clean the data
# --------------------------------

df["final_status"] = (
    df["final_status"]
    .astype(str)
    .str.strip()
    .str.upper()
)

df["pincode"] = df["pincode"].astype("string").str.strip()

# Remove spaces and standardize status labels


# --------------------------------
# 3. Order status analysis
# --------------------------------

print("\n2. ORDER STATUS DISTRIBUTION")
print("--------------------------------------")

print(df["final_status"].value_counts())

completed_orders = df[
    df["final_status"].isin(["DELIVERED", "RTO"])
].copy()

total_orders = len(completed_orders)

rto_orders = (
    completed_orders["final_status"] == "RTO"
).sum()

delivered_orders = (
    completed_orders["final_status"] == "DELIVERED"
).sum()

rto_rate = (rto_orders / total_orders) * 100

print("\nTotal completed orders:", total_orders)
print("Delivered orders:", delivered_orders)
print("RTO orders:", rto_orders)
print(f"Overall RTO Rate: {rto_rate:.2f}%")


# --------------------------------
# 4. Previous RTO analysis
# --------------------------------

print("\n3. CUSTOMER PREVIOUS RTO ANALYSIS")
print("--------------------------------------")

prior_rto_analysis = (
    completed_orders
    .groupby("customer_prior_rto")
    .agg(
        total_orders=("order_id", "count"),
        rto_orders=("final_status",
                    lambda x: (x == "RTO").sum())
    )
)

prior_rto_analysis["rto_rate"] = (
    prior_rto_analysis["rto_orders"]
    / prior_rto_analysis["total_orders"]
    * 100
)

print(prior_rto_analysis.round(2))


# --------------------------------
# 5. City-wise RTO analysis
# --------------------------------

print("\n4. CITY-WISE RTO ANALYSIS")
print("--------------------------------------")

city_analysis = (
    completed_orders
    .groupby("city")
    .agg(
        total_orders=("order_id", "count"),
        rto_orders=("final_status",
                    lambda x: (x == "RTO").sum())
    )
)

city_analysis["rto_rate"] = (
    city_analysis["rto_orders"]
    / city_analysis["total_orders"]
    * 100
)

city_analysis = city_analysis.sort_values(
    by="rto_rate",
    ascending=False
)

print(city_analysis.round(2).head(10))


# --------------------------------
# 6. Marketing source analysis
# --------------------------------

print("\n5. MARKETING SOURCE ANALYSIS")
print("--------------------------------------")

source_analysis = (
    completed_orders
    .groupby("utm_source")
    .agg(
        total_orders=("order_id", "count"),
        rto_orders=("final_status",
                    lambda x: (x == "RTO").sum())
    )
)

source_analysis["rto_rate"] = (
    source_analysis["rto_orders"]
    / source_analysis["total_orders"]
    * 100
)

print(source_analysis.round(2))


# --------------------------------
# 7. Address quality analysis
# --------------------------------

print("\n6. ADDRESS QUALITY ANALYSIS")
print("--------------------------------------")

completed_orders["address"] = (
    completed_orders["address"]
    .fillna("")
    .astype(str)
    .str.strip()
)

incomplete_address = completed_orders[
    completed_orders["address"].isin(["", "."])
]

print("Orders with blank or dot addresses:",
      len(incomplete_address))

if len(incomplete_address) > 0:

    address_rto = (
        incomplete_address["final_status"] == "RTO"
    ).mean() * 100

    print(f"RTO rate for these orders: {address_rto:.2f}%")


# --------------------------------
# 8. Data quality checks
# --------------------------------

print("\n7. DATA QUALITY CHECKS")
print("--------------------------------------")

print("Duplicate order IDs:",
      df["order_id"].duplicated().sum())

print("Missing city values:",
      df["city"].isna().sum())

print("Missing pincode values:",
      df["pincode"].isna().sum())

print("\n========== ANALYSIS COMPLETED ==========")