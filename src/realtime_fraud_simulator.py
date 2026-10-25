
import time
import pandas as pd
from pathlib import Path

# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    BASE_DIR / "data" / "processed" /
    "fraud_scored_train.parquet"
)

OUTPUT_FILE = (
    BASE_DIR / "reports" /
    "simulated_fraud_alerts.csv"
)

# ==========================================
# 2. LOAD DATASET
# ==========================================

df = pd.read_parquet(INPUT_FILE)

required = ["risk_score", "risk_level", "is_fraud"]

missing = [col for col in required if col not in df.columns]

if missing:
    raise ValueError(f"Missing columns: {missing}")

# Support common dataset column names
date_col = next(
    (
        col for col in [
            "trans_date_trans_time",
            "transaction_datetime"
        ]
        if col in df.columns
    ),
    None
)

amount_col = next(
    (
        col for col in ["amt", "amount"]
        if col in df.columns
    ),
    None
)

merchant_col = (
    "merchant" if "merchant" in df.columns else None
)

# ==========================================
# 3. SELECT SAMPLE TRANSACTIONS
# ==========================================

samples = []

for level in ["Low", "Medium", "High"]:

    group = df[df["risk_level"] == level]

    if not group.empty:

        selected = group.sample(
            n=min(10, len(group)),
            random_state=42
        )

        samples.append(selected)

if not samples:
    raise ValueError("No transactions available for simulation.")

sample = pd.concat(samples, ignore_index=True)

# Shuffle transactions
sample = sample.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# ==========================================
# 4. FRAUD ALERT SIMULATION
# ==========================================

alerts = []

print("\n==========================================")
print("       BFSI FRAUD ALERT SIMULATOR")
print("==========================================\n")

for i, (_, row) in enumerate(sample.iterrows(), start=1):

    score = int(row["risk_score"])
    level = str(row["risk_level"])

    transaction_time = (
        str(row[date_col])
        if date_col else "N/A"
    )

    merchant = (
        str(row[merchant_col])
        if merchant_col else "N/A"
    )

    amount = (
        float(row[amount_col])
        if amount_col else 0.0
    )

    # Determine alert severity
    if score >= 70:
        status = "HIGH RISK ALERT"
        priority = "CRITICAL"

    elif score >= 40:
        status = "MEDIUM RISK ALERT"
        priority = "WARNING"

    else:
        status = "LOW RISK"
        priority = "NORMAL"

    # Display transaction details
    print(f"Transaction #{i:02d}")
    print(f"Date/Time : {transaction_time}")
    print(f"Merchant  : {merchant}")
    print(f"Amount    : ${amount:.2f}")
    print(f"Risk Score: {score}")
    print(f"Risk Level: {level}")
    print(f"Status    : {status}")
    print(f"Priority  : {priority}")
    print("-" * 45)

    # Save medium and high risk alerts
    if score >= 40:

        alerts.append({
            "transaction_number": i,
            "transaction_datetime": transaction_time,
            "merchant": merchant,
            "amount_usd": round(amount, 2),
            "risk_score": score,
            "risk_level": level,
            "alert_status": status,
            "priority": priority,
            "actual_is_fraud": int(row["is_fraud"])
        })

    # Simulated streaming delay
    time.sleep(0.2)

# ==========================================
# 5. EXPORT FRAUD ALERTS
# ==========================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

alert_columns = [
    "transaction_number",
    "transaction_datetime",
    "merchant",
    "amount_usd",
    "risk_score",
    "risk_level",
    "alert_status",
    "priority",
    "actual_is_fraud"
]

alerts_df = pd.DataFrame(
    alerts,
    columns=alert_columns
)

alerts_df.to_csv(
    OUTPUT_FILE,
    index=False
)

# ==========================================
# 6. FINAL SUMMARY
# ==========================================

print("\n==========================================")
print("          SIMULATION SUMMARY")
print("==========================================")

print(f"Transactions Processed : {len(sample)}")
print(f"Alerts Generated       : {len(alerts_df)}")

print(
    "High Risk Alerts       :",
    (alerts_df["risk_score"] >= 70).sum()
)

print(
    "Medium Risk Alerts     :",
    (
        (alerts_df["risk_score"] >= 40) &
        (alerts_df["risk_score"] < 70)
    ).sum()
)

print(f"\nAlerts saved to:\n{OUTPUT_FILE}")

print("\nSimulation completed successfully!")
