
from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent

input_file = BASE_DIR / "data" / "raw" / "fraudTrain.csv"
output_dir = BASE_DIR / "data" / "processed"

output_dir.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(input_file, low_memory=False)

# Convert transaction date
df["trans_date_trans_time"] = pd.to_datetime(
    df["trans_date_trans_time"],
    errors="coerce"
)

# 1. Time-based features
df["hour"] = df["trans_date_trans_time"].dt.hour
df["day_of_week"] = df["trans_date_trans_time"].dt.day_name()
df["month"] = df["trans_date_trans_time"].dt.month

# 2. Weekend flag
df["is_weekend"] = (
    df["trans_date_trans_time"].dt.dayofweek >= 5
).astype(int)

# 3. Night flag (10 PM to 6 AM)
df["is_night"] = (
    (df["hour"] >= 22) | (df["hour"] < 6)
).astype(int)

# 4. Transaction amount categories
df["amount_category"] = pd.cut(
    df["amt"],
    bins=[-np.inf, 50, 200, 1000, np.inf],
    labels=["Low", "Medium", "High", "Very High"]
)

# 5. Haversine distance calculation
# Distance between customer home and merchant
lat1 = np.radians(df["lat"])
lon1 = np.radians(df["long"])
lat2 = np.radians(df["merch_lat"])
lon2 = np.radians(df["merch_long"])

dlat = lat2 - lat1
dlon = lon2 - lon1

a = (
    np.sin(dlat / 2) ** 2
    + np.cos(lat1) * np.cos(lat2)
    * np.sin(dlon / 2) ** 2
)

a = np.clip(a, 0, 1)

df["merchant_distance_km"] = (
    6371 * 2 * np.arcsin(np.sqrt(a))
)

# Save processed dataset
output_file = output_dir / "fraud_train_processed.parquet"
df.to_parquet(output_file, index=False)

print("Feature Engineering Completed!")

print("\nDataset Shape:", df.shape)

print("\nNew Features Preview:")
print(df[[
    "hour",
    "day_of_week",
    "month",
    "is_weekend",
    "is_night",
    "amount_category",
    "merchant_distance_km",
    "is_fraud"
]].head())

print("\nProcessed file saved at:")
print(output_file)
