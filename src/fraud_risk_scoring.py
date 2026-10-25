
from pathlib import Path
import numpy as np
import pandas as pd

# ==========================================
# 1. PATHS
# ==========================================

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data" / "processed" / "fraud_train_processed.parquet"
REPORTS = BASE / "reports"
OUTPUT = BASE / "data" / "processed"

REPORTS.mkdir(exist_ok=True)
OUTPUT.mkdir(parents=True, exist_ok=True)

# ==========================================
# 2. LOAD DATA
# ==========================================

df = pd.read_parquet(DATA)

df["trans_date_trans_time"] = pd.to_datetime(
    df["trans_date_trans_time"]
)

# Keep transactions in chronological order
df = df.sort_values(
    ["cc_num", "trans_date_trans_time", "trans_num"]
).reset_index(drop=True)

# ==========================================
# 3. TRANSACTION VELOCITY
# ==========================================

# Count current and previous transactions
# within the last 10 minutes per card.

df["velocity_10min"] = (
    df.groupby("cc_num", group_keys=False)
      .rolling(
          "10min",
          on="trans_date_trans_time",
          closed="both"
      )["amt"]
      .count()
      .to_numpy()
)

# ==========================================
# 4. HISTORICAL SPENDING BASELINE
# ==========================================

# Previous 20 transactions only;
# current transaction is excluded.

df["previous_median_amt"] = (
    df.groupby("cc_num")["amt"]
      .transform(
          lambda s: s.shift(1).rolling(
              20, min_periods=5
          ).median()
      )
)

df["unusual_spending"] = (
    df["previous_median_amt"].notna()
    & (
        df["amt"]
        > 3 * df["previous_median_amt"]
    )
)

# ==========================================
# 5. FRAUD RISK RULES
# ==========================================

df["rule_night"] = df["hour"].between(0, 5) | (
    df["hour"] >= 22
)

df["rule_high_amount"] = df["amt"] > 1000

df["rule_distance"] = (
    df["merchant_distance_km"] > 100
)

df["rule_velocity"] = (
    df["velocity_10min"] >= 3
)

df["rule_spending"] = df["unusual_spending"]

# ==========================================
# 6. RISK SCORE
# ==========================================

df["risk_score"] = (
    df["rule_night"].astype(int) * 15
    + df["rule_high_amount"].astype(int) * 25
    + df["rule_distance"].astype(int) * 20
    + df["rule_velocity"].astype(int) * 25
    + df["rule_spending"].astype(int) * 15
)

df["risk_level"] = pd.cut(
    df["risk_score"],
    bins=[-1, 39, 69, 100],
    labels=["Low", "Medium", "High"]
)

# ==========================================
# 7. ANALYZE FRAUD BY RISK LEVEL
# ==========================================

summary = df.groupby(
    "risk_level", observed=True
).agg(
    total_transactions=("is_fraud", "size"),
    fraud_transactions=("is_fraud", "sum")
).reset_index()

summary["fraud_rate"] = (
    summary["fraud_transactions"]
    / summary["total_transactions"] * 100
)

print("\n========== FRAUD RISK SUMMARY ==========")
print(summary.to_string(index=False))

# ==========================================
# 8. EVALUATE ALERT THRESHOLD
# ==========================================

# Example: alert when score >= 40
df["alert"] = df["risk_score"] >= 40

tp = ((df["alert"]) & (df["is_fraud"] == 1)).sum()
fp = ((df["alert"]) & (df["is_fraud"] == 0)).sum()
fn = ((~df["alert"]) & (df["is_fraud"] == 1)).sum()
tn = ((~df["alert"]) & (df["is_fraud"] == 0)).sum()

precision = tp / (tp + fp) if tp + fp else 0
recall = tp / (tp + fn) if tp + fn else 0
fpr = fp / (fp + tn) if fp + tn else 0

print("\n========== ALERT PERFORMANCE ==========")
print("True Positives:", tp)
print("False Positives:", fp)
print("False Negatives:", fn)
print("True Negatives:", tn)
print(f"Precision: {precision:.2%}")
print(f"Recall: {recall:.2%}")
print(f"False Positive Rate: {fpr:.2%}")

# ==========================================
# 9. SAVE RESULTS
# ==========================================

summary.to_csv(
    REPORTS / "fraud_risk_summary.csv",
    index=False
)

df.to_parquet(
    OUTPUT / "fraud_scored_train.parquet",
    index=False
)

print("\nRisk Scoring Completed!")
print("Results saved successfully.")
