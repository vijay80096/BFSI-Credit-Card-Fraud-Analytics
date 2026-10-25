
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. FILE PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA = BASE_DIR / "data" / "processed" / "fraud_train_processed.parquet"

REPORTS = BASE_DIR / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

# ==========================================
# 2. LOAD DATA
# ==========================================

df = pd.read_parquet(DATA)

print("\n========== GEOGRAPHIC FRAUD ANALYSIS ==========")

print("\nTotal Transactions:", len(df))
print("Fraud Transactions:", df["is_fraud"].sum())

# ==========================================
# 3. REUSABLE FRAUD SUMMARY
# ==========================================

def fraud_summary(columns):
    result = df.groupby(
        columns, observed=True
    ).agg(
        total_transactions=("is_fraud", "size"),
        fraud_transactions=("is_fraud", "sum")
    ).reset_index()

    result["fraud_rate"] = (
        result["fraud_transactions"]
        / result["total_transactions"] * 100
    )

    return result

# ==========================================
# 4. STATE-WISE FRAUD ANALYSIS
# ==========================================

state_summary = fraud_summary(["state"])

state_summary = state_summary.sort_values(
    "fraud_rate", ascending=False
)

# Filter states with sufficient transactions
state_reliable = state_summary[
    state_summary["total_transactions"] >= 1000
].copy()

print("\nTop 10 States by Fraud Rate:")
print(state_reliable.head(10).to_string(index=False))

state_summary.to_csv(
    REPORTS / "state_fraud_analysis.csv",
    index=False
)

# ==========================================
# 5. CITY-WISE FRAUD ANALYSIS
# ==========================================

city_summary = fraud_summary(["state", "city"])

city_reliable = city_summary[
    city_summary["total_transactions"] >= 100
].sort_values(
    "fraud_rate", ascending=False
)

print("\nTop 10 Cities by Fraud Rate:")
print(city_reliable.head(10).to_string(index=False))

city_summary.to_csv(
    REPORTS / "city_fraud_analysis.csv",
    index=False
)

# ==========================================
# 6. MERCHANT DISTANCE ANALYSIS
# ==========================================

# Distance already calculated in feature engineering
df["distance_band"] = pd.cut(
    df["merchant_distance_km"],
    bins=[-np.inf, 25, 50, 100, 200, np.inf],
    labels=[
        "0-25 km",
        "25-50 km",
        "50-100 km",
        "100-200 km",
        "200+ km"
    ]
)

distance_summary = fraud_summary(["distance_band"])

print("\nFraud Rate by Merchant Distance:")
print(distance_summary.to_string(index=False))

distance_summary.to_csv(
    REPORTS / "distance_fraud_analysis.csv",
    index=False
)

# ==========================================
# 7. GEOGRAPHIC ANOMALY INDICATORS
# ==========================================

# Descriptive flag, not confirmed fraud
df["long_distance_flag"] = (
    df["merchant_distance_km"] > 100
).astype(int)

long_distance_summary = fraud_summary(["long_distance_flag"])

print("\nLong-Distance Flag Analysis:")
print(long_distance_summary.to_string(index=False))

long_distance_summary.to_csv(
    REPORTS / "long_distance_fraud_analysis.csv",
    index=False
)

# ==========================================
# 8. VISUALIZATIONS
# ==========================================

sns.set_theme(style="whitegrid")

# Chart 1: Top states
plt.figure(figsize=(12, 6))

sns.barplot(
    data=state_reliable.head(10),
    x="fraud_rate",
    y="state",
    color="steelblue"
)

plt.title("Top 10 States by Fraud Rate")
plt.xlabel("Fraud Rate (%)")
plt.ylabel("State")

plt.tight_layout()
plt.savefig(
    REPORTS / "state_fraud_rate.png",
    dpi=300
)
plt.close()

# Chart 2: Top cities
plt.figure(figsize=(12, 6))

sns.barplot(
    data=city_reliable.head(10),
    x="fraud_rate",
    y="city",
    color="teal"
)

plt.title("Top 10 Cities by Fraud Rate")
plt.xlabel("Fraud Rate (%)")
plt.ylabel("City")

plt.tight_layout()
plt.savefig(
    REPORTS / "city_fraud_rate.png",
    dpi=300
)
plt.close()

# Chart 3: Distance fraud rate
plt.figure(figsize=(11, 6))

sns.barplot(
    data=distance_summary,
    x="distance_band",
    y="fraud_rate",
    color="coral"
)

plt.title("Fraud Rate by Merchant Distance")
plt.xlabel("Distance from Cardholder Home")
plt.ylabel("Fraud Rate (%)")

plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    REPORTS / "distance_fraud_rate.png",
    dpi=300
)
plt.close()

# Chart 4: Geographic scatter plot
fraud_sample = df[df["is_fraud"] == 1].sample(
    n=min(3000, (df["is_fraud"] == 1).sum()),
    random_state=42
)

plt.figure(figsize=(12, 7))

plt.scatter(
    fraud_sample["merch_long"],
    fraud_sample["merch_lat"],
    alpha=0.35,
    s=12,
    color="crimson"
)

plt.title("Geographic Distribution of Fraudulent Merchant Transactions")
plt.xlabel("Merchant Longitude")
plt.ylabel("Merchant Latitude")
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(
    REPORTS / "fraud_geographic_scatter.png",
    dpi=300
)
plt.close()

print("\nGeographic Analysis Completed Successfully!")
print("All CSV reports and charts saved in:", REPORTS)
