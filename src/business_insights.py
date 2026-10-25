
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    BASE_DIR / "data" / "processed" /
    "fraud_scored_train.parquet"
)

OUTPUT_FILE = (
    BASE_DIR / "reports" /
    "business_insights_summary.csv"
)

# Load dataset
df = pd.read_parquet(INPUT_FILE)

# Identify amount column
amount_col = "amt" if "amt" in df.columns else "amount"

required = ["is_fraud", "risk_level", amount_col]
missing = [c for c in required if c not in df.columns]

if missing:
    raise ValueError(f"Missing columns: {missing}")

# Overall metrics
total_transactions = len(df)
fraud_transactions = int(df["is_fraud"].sum())

fraud_rate = (
    fraud_transactions / total_transactions * 100
)

total_transaction_value = df[amount_col].sum()

fraud_transaction_value = df.loc[
    df["is_fraud"] == 1, amount_col
].sum()

# Risk level analysis
risk_summary = (
    df.groupby("risk_level")
    .agg(
        total_transactions=("is_fraud", "size"),
        fraud_transactions=("is_fraud", "sum")
    )
    .reset_index()
)

risk_summary["fraud_rate_percent"] = (
    risk_summary["fraud_transactions"] /
    risk_summary["total_transactions"] * 100
).round(2)

# Print business insights
print("\n====================================")
print("BFSI FRAUD BUSINESS INSIGHTS")
print("====================================")

print(f"Total Transactions : {total_transactions:,}")
print(f"Fraud Transactions : {fraud_transactions:,}")
print(f"Fraud Rate         : {fraud_rate:.2f}%")

print(
    f"Total Transaction Value : "
    f"${total_transaction_value:,.2f}"
)

print(
    f"Fraud Transaction Value : "
    f"${fraud_transaction_value:,.2f}"
)

print("\nRisk Level Analysis:")
print(risk_summary.to_string(index=False))

# Save results
OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

risk_summary.to_csv(OUTPUT_FILE, index=False)

print(f"\nReport saved to:\n{OUTPUT_FILE}")
