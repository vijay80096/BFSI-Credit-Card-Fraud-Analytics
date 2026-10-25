
from pathlib import Path
import pandas as pd

# 1. Load dataset
BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "data" / "raw" / "fraudTrain.csv"

df = pd.read_csv(file_path, low_memory=False)

print("========== DATA QUALITY REPORT ==========")

# 2. Dataset size
print("\n1. Dataset Shape:")
print(df.shape)

# 3. Data types
print("\n2. Data Types:")
print(df.dtypes)

# 4. Missing values
print("\n3. Missing Values:")
print(df.isnull().sum())

# 5. Duplicate transaction IDs
print("\n4. Duplicate Transaction IDs:")
print(df["trans_num"].duplicated().sum())

# 6. Fraud distribution
print("\n5. Fraud Distribution:")
print(df["is_fraud"].value_counts())

# 7. Fraud percentage
fraud_rate = df["is_fraud"].mean() * 100

print("\n6. Fraud Rate:")
print(f"{fraud_rate:.3f}%")

# 8. Convert date column
df["trans_date_trans_time"] = pd.to_datetime(
    df["trans_date_trans_time"],
    errors="coerce"
)

print("\n7. Invalid Dates:")
print(df["trans_date_trans_time"].isna().sum())

# 9. Check negative transaction amounts
print("\n8. Negative Amounts:")
print((df["amt"] < 0).sum())

print("\n========== REPORT COMPLETE ==========")
