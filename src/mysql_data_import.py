
from pathlib import Path
import hashlib
import getpass
import pandas as pd
import mysql.connector

# Project paths
BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data" / "processed" / "fraud_scored_train.parquet"

# MySQL connection
password = getpass.getpass("Enter MySQL password: ")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="bfsi_fraud_analysis"
)

cursor = conn.cursor()
print("MySQL connected successfully!")

# Read processed data
columns = [
    "trans_num", "trans_date_trans_time",
    "cc_num", "merchant", "category",
    "amt", "city", "state", "hour",
    "is_weekend", "merchant_distance_km",
    "risk_score", "risk_level", "is_fraud"
]

df = pd.read_parquet(DATA, columns=columns)

# Pseudonymous card ID
df["card_id"] = df["cc_num"].astype(str).map(
    lambda x: hashlib.sha256(x.encode()).hexdigest()[:32]
)

df["trans_date_trans_time"] = pd.to_datetime(
    df["trans_date_trans_time"]
)

df["risk_level"] = df["risk_level"].astype(str)

print("Total transactions:", len(df))

# SQL insert query
query = """
INSERT INTO credit_card_transactions (
    transaction_id, transaction_datetime,
    card_id, merchant, category, amount,
    city, state, transaction_hour,
    is_weekend, merchant_distance_km,
    risk_score, risk_level, is_fraud
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s
)
"""

# Batch import
batch_size = 5000

for start in range(0, len(df), batch_size):
    batch = df.iloc[start:start + batch_size]

    records = [
        (
            str(row.trans_num),
            row.trans_date_trans_time.to_pydatetime(),
            row.card_id,
            row.merchant,
            row.category,
            float(row.amt),
            row.city,
            row.state,
            int(row.hour),
            int(row.is_weekend),
            float(row.merchant_distance_km),
            int(row.risk_score),
            row.risk_level,
            int(row.is_fraud)
        )
        for row in batch.itertuples(index=False)
    ]

    cursor.executemany(query, records)
    conn.commit()

    print(
        f"Imported {min(start + batch_size, len(df)):,}"
        f" / {len(df):,}"
    )

# Verify
cursor.execute(
    "SELECT COUNT(*) FROM credit_card_transactions"
)

print("\nTotal rows in MySQL:", cursor.fetchone()[0])

cursor.close()
conn.close()

print("Data Import Completed Successfully!")
