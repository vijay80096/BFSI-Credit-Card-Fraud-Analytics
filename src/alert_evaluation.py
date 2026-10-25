
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR / "data" / "processed" /
    "fraud_scored_train.parquet"
)

REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# 2. LOAD SCORED TRANSACTIONS
# ==========================================

df = pd.read_parquet(
    DATA_PATH,
    columns=["risk_score", "is_fraud", "amt"]
)

print("\n========== FRAUD ALERT EVALUATION ==========")
print("Total Transactions:", len(df))
print("Total Fraud:", df["is_fraud"].sum())

# ==========================================
# 3. COMPARE ALERT THRESHOLDS
# ==========================================

thresholds = [20, 40, 60, 80]

results = []

actual = df["is_fraud"] == 1
total_fraud_value = df.loc[actual, "amt"].sum()

for threshold in thresholds:

    predicted = df["risk_score"] >= threshold

    tp = int((predicted & actual).sum())
    fp = int((predicted & ~actual).sum())
    fn = int((~predicted & actual).sum())
    tn = int((~predicted & ~actual).sum())

    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    fpr = fp / (fp + tn) if fp + tn else 0

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0
    )

    alerts = tp + fp
    alert_rate = alerts / len(df)

    captured_value = df.loc[
        predicted & actual, "amt"
    ].sum()

    value_recall = (
        captured_value / total_fraud_value
        if total_fraud_value else 0
    )

    results.append({
        "threshold": threshold,
        "total_alerts": alerts,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn,
        "precision": precision,
        "recall": recall,
        "false_positive_rate": fpr,
        "f1_score": f1,
        "alert_rate": alert_rate,
        "fraud_value_recall": value_recall
    })

# ==========================================
# 4. SAVE RESULTS
# ==========================================

summary = pd.DataFrame(results)

print("\n========== THRESHOLD COMPARISON ==========")
print(summary.round(4).to_string(index=False))

summary.to_csv(
    REPORTS_DIR / "alert_threshold_comparison.csv",
    index=False
)

# ==========================================
# 5. PRECISION VS RECALL CHART
# ==========================================

plt.figure(figsize=(10, 6))

plt.plot(
    summary["threshold"],
    summary["precision"] * 100,
    marker="o",
    label="Precision"
)

plt.plot(
    summary["threshold"],
    summary["recall"] * 100,
    marker="s",
    label="Recall"
)

plt.xlabel("Risk Score Threshold")
plt.ylabel("Percentage (%)")
plt.title("Fraud Alert Precision vs Recall")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    REPORTS_DIR / "precision_recall_comparison.png",
    dpi=300
)
plt.close()

# ==========================================
# 6. FALSE POSITIVE CHART
# ==========================================

plt.figure(figsize=(10, 6))

plt.bar(
    summary["threshold"].astype(str),
    summary["false_positives"]
)

plt.xlabel("Risk Score Threshold")
plt.ylabel("False Positive Alerts")
plt.title("False Alerts by Risk Threshold")
plt.tight_layout()

plt.savefig(
    REPORTS_DIR / "false_positive_comparison.png",
    dpi=300
)
plt.close()

# ==========================================
# 7. F1 SCORE CHART
# ==========================================

plt.figure(figsize=(10, 6))

plt.plot(
    summary["threshold"],
    summary["f1_score"],
    marker="o"
)

plt.xlabel("Risk Score Threshold")
plt.ylabel("F1 Score")
plt.title("F1 Score by Alert Threshold")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    REPORTS_DIR / "f1_threshold_comparison.png",
    dpi=300
)
plt.close()

# ==========================================
# 8. BEST EXPLORATORY THRESHOLD
# ==========================================

best = summary.loc[
    summary["f1_score"].idxmax()
]

print("\n========== BEST THRESHOLD BY F1 ==========")
print("Threshold:", int(best["threshold"]))
print(f"Precision: {best['precision']:.2%}")
print(f"Recall: {best['recall']:.2%}")
print(f"F1 Score: {best['f1_score']:.4f}")
print(
    f"False Positive Rate: "
    f"{best['false_positive_rate']:.2%}"
)
print(
    f"Fraud Value Recall: "
    f"{best['fraud_value_recall']:.2%}"
)

print("\nAlert Evaluation Completed Successfully!")
print("All results saved in:", REPORTS_DIR)
