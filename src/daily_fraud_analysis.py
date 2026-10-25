
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA = BASE_DIR / "data" / "processed" / "fraud_train_processed.parquet"
REPORTS = BASE_DIR / "reports"
REPORTS.mkdir(exist_ok=True)

# Load processed dataset
df = pd.read_parquet(DATA)

# Ensure datetime and derive calendar features
df["trans_date_trans_time"] = pd.to_datetime(
    df["trans_date_trans_time"]
)

df["day_num"] = df["trans_date_trans_time"].dt.dayofweek
df["day_name"] = df["trans_date_trans_time"].dt.day_name()
df["year_month"] = df["trans_date_trans_time"].dt.to_period("M").astype(str)
df["weekend_type"] = df["day_num"].map(
    lambda x: "Weekend" if x >= 5 else "Weekday"
)

# Reusable fraud summary
def fraud_summary(group_columns):
    result = df.groupby(group_columns).agg(
        total_transactions=("is_fraud", "size"),
        fraud_transactions=("is_fraud", "sum")
    ).reset_index()

    result["fraud_rate"] = (
        result["fraud_transactions"]
        / result["total_transactions"] * 100
    )

    return result

# 1. Day-wise fraud
daily = fraud_summary(["day_num", "day_name"])
daily = daily.sort_values("day_num")

print("\n========== DAY-WISE FRAUD ==========")
print(daily.to_string(index=False))

daily.to_csv(REPORTS / "daily_fraud_analysis.csv", index=False)

# 2. Weekend vs weekday
weekend = fraud_summary(["weekend_type"])

print("\n========== WEEKEND VS WEEKDAY ==========")
print(weekend.to_string(index=False))

weekend.to_csv(REPORTS / "weekend_fraud_analysis.csv", index=False)

# 3. Monthly fraud
monthly = fraud_summary(["year_month"])

print("\n========== MONTHLY FRAUD ==========")
print(monthly.to_string(index=False))

monthly.to_csv(REPORTS / "monthly_fraud_analysis.csv", index=False)

# 4. Monthly consistency by weekday
consistency = fraud_summary(["year_month", "day_name"])

pivot = consistency.pivot(
    index="year_month",
    columns="day_name",
    values="fraud_rate"
)

days = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

pivot = pivot.reindex(columns=days)

# Save monthly consistency table
pivot.to_csv(REPORTS / "monthly_weekday_fraud_rates.csv")

sns.set_theme(style="whitegrid")

# Chart 1: Day-wise fraud rate
plt.figure(figsize=(11, 5))
sns.barplot(data=daily, x="day_name", y="fraud_rate",
            color="steelblue")
plt.title("Fraud Rate by Day of Week")
plt.xlabel("Day")
plt.ylabel("Fraud Rate (%)")
plt.xticks(rotation=25)
plt.tight_layout()
plt.savefig(REPORTS / "daily_fraud_rate.png", dpi=300)
plt.close()

# Chart 2: Weekend vs weekday
plt.figure(figsize=(7, 5))
sns.barplot(data=weekend, x="weekend_type",
            y="fraud_rate", color="teal")
plt.title("Weekend vs Weekday Fraud Rate")
plt.xlabel("Day Type")
plt.ylabel("Fraud Rate (%)")
plt.tight_layout()
plt.savefig(REPORTS / "weekend_fraud_rate.png", dpi=300)
plt.close()

# Chart 3: Monthly trend
plt.figure(figsize=(12, 5))
sns.lineplot(data=monthly, x="year_month",
             y="fraud_rate", marker="o")
plt.title("Monthly Credit Card Fraud Rate")
plt.xlabel("Month")
plt.ylabel("Fraud Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(REPORTS / "monthly_fraud_trend.png", dpi=300)
plt.close()

# Chart 4: Monthly weekday heatmap
plt.figure(figsize=(12, 7))
sns.heatmap(pivot, cmap="YlOrRd", annot=True,
            fmt=".2f", cbar_kws={"label": "Fraud Rate (%)"})
plt.title("Monthly Fraud Rate by Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Month")
plt.tight_layout()
plt.savefig(REPORTS / "monthly_weekday_heatmap.png", dpi=300)
plt.close()

print("\nAnalysis completed successfully!")
print("CSV reports and 4 charts saved in reports folder.")
