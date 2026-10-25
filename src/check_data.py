
from pathlib import Path
import pandas as pd

# Project folder path
BASE_DIR = Path(__file__).resolve().parent.parent

# Load training dataset
file_path = BASE_DIR / "data" / "raw" / "fraudTrain.csv"

df = pd.read_csv(file_path)

# Dataset information
print("Dataset Shape:", df.shape)

print("\nFirst 5 Transactions:")
print(df.head())

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFraud Distribution:")
print(df["is_fraud"].value_counts())

print("\nMissing Values:")
print(df.isnull().sum())
