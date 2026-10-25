
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ====================================
# 1. FILE PATHS
# ====================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA = BASE_DIR / "data" / "processed" / "fraud_train_processed.parquet"

REPORTS = BASE_DIR / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

# ====================================
# 2. LOAD DATA
# ====================================

df = pd.read_parquet(DATA)

print("\n========== AMOUNT ANALYSIS ==========")

print("\nTotal Transactions:", len(df))
print("Fraud Transactions:", df["is_fraud"].sum())

# ====================================
# 3. AMOUNT STATISTICS
# ====================================

amount_stats = df.groupby("is_fraud")["amt"].agg(
    ["count", "mean", "median", "min", "max", "std"]
)

print("\nAmount Statistics:")
print(amount_stats.round(2))

amount_stats.to_csv(
    REPORTS / "amount_statistics.csv"
)

# ====================================
# 4. AMOUNT CATEGORIES
# ====================================

bins = [-np.inf, 50, 200, 1000, np.inf]

labels = [
    "Low (<=50)",
    "Medium (50-200)",
    "High (200-1000)",
    "Very High (>1000)"
]

df["amount_band"] = pd.cut(
    df["amt"],
    bins=bins,
    labels=labels
)

amount_summary = df.groupby(
    "amount_band", observed=True
).agg(
    total_transactions=("is_fraud", "size"),
    fraud_transactions=("is_fraud", "sum"),
    total_amount=("amt", "sum"),
    fraud_amount=(
        "amt",
        lambda x: x[df.loc[x.index, "is_fraud"] == 1].sum()
    )
).reset_index()

amount_summary["fraud_rate"] = (
    amount_summary["fraud_transactions"]
    / amount_summary["total_transactions"] * 100
)

print("\nFraud Rate by Amount Band:")
print(amount_summary.round(2).to_string(index=False))

amount_summary.to_csv(
    REPORTS / "amount_band_analysis.csv",
    index=False
)

# ====================================
# 5. FRAUD VALUE EXPOSURE
# ====================================

total_value = df["amt"].sum()
fraud_value = df.loc[df["is_fraud"] == 1, "amt"].sum()

print("\nTotal Transaction Value:", round(total_value, 2))
print("Fraud Transaction Value:", round(fraud_value, 2))

print(
    "Fraud Value Percentage:",
    round(fraud_value / total_value * 100, 3),
    "%"
)

# ====================================
# 6. VISUALIZATION
# ====================================

sns.set_theme(style="whitegrid")

# Chart 1: Amount distribution
plt.figure(figsize=(11, 6))

sample = df.sample(
    n=min(100000, len(df)),
    random_state=42
)

sns.histplot(
    data=sample,
    x="amt",
    hue="is_fraud",
    bins=60,
    log_scale=(True, False),
    common_norm=False,
    stat="density"
)

plt.title("Transaction Amount Distribution: Genuine vs Fraud")
plt.xlabel("Transaction Amount (USD)")
plt.ylabel("Density")
plt.tight_layout()

plt.savefig(
    REPORTS / "amount_distribution.png",
    dpi=300
)
plt.close()

# Chart 2: Fraud rate by amount band
plt.figure(figsize=(10, 6))

sns.barplot(
    data=amount_summary,
    x="amount_band",
    y="fraud_rate",
    color="steelblue"
)

plt.title("Fraud Rate by Transaction Amount Band")
plt.xlabel("Transaction Amount Category")
plt.ylabel("Fraud Rate (%)")
plt.xticks(rotation=15)
plt.tight_layout()

plt.savefig(
    REPORTS / "amount_band_fraud_rate.png",
    dpi=300
)
plt.close()

# Chart 3: Amount comparison
plt.figure(figsize=(9, 6))

sns.boxplot(
    data=sample,
    x="is_fraud",
    y="amt",
    showfliers=False
)

plt.title("Transaction Amount: Genuine vs Fraud")
plt.xlabel("Transaction Type (0 = Genuine, 1 = Fraud)")
plt.ylabel("Transaction Amount (USD)")
plt.tight_layout()

plt.savefig(
    REPORTS / "fraud_amount_boxplot.png",
    dpi=300
)
plt.close()

print("\nAnalysis Completed Successfully!")
print("Reports saved in:", REPORTS)
