
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent.parent

# Load processed data
file_path = BASE_DIR / "data" / "processed" / "fraud_train_processed.parquet"
df = pd.read_parquet(file_path)

# Calculate hourly fraud statistics
hourly = df.groupby("hour").agg(
    total_transactions=("is_fraud", "size"),
    fraud_transactions=("is_fraud", "sum")
).reset_index()

hourly["fraud_rate"] = (
    hourly["fraud_transactions"]
    / hourly["total_transactions"] * 100
)

# Find hour with highest fraud rate
highest = hourly.loc[hourly["fraud_rate"].idxmax()]

print("\n========== HOURLY FRAUD ANALYSIS ==========")

print(hourly.to_string(index=False))

print("\nHighest Fraud Rate Hour:", int(highest["hour"]))
print("Fraud Rate:", round(highest["fraud_rate"], 3), "%")

# Create reports folder
reports_dir = BASE_DIR / "reports"
reports_dir.mkdir(exist_ok=True)

# Save analysis results
hourly.to_csv(
    reports_dir / "hourly_fraud_analysis.csv",
    index=False
)

# Visualization
sns.set_theme(style="whitegrid")

plt.figure(figsize=(12, 6))

sns.barplot(
    data=hourly,
    x="hour",
    y="fraud_rate",
    color="steelblue"
)

plt.title("Credit Card Fraud Rate by Transaction Hour")
plt.xlabel("Hour of Day (0-23)")
plt.ylabel("Fraud Rate (%)")

plt.tight_layout()

plt.savefig(
    reports_dir / "hourly_fraud_rate.png",
    dpi=300
)

plt.show()

print("\nAnalysis completed!")
print("Chart saved in reports folder.")
