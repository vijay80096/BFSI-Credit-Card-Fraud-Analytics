
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

ALERT_FILE = BASE_DIR / "reports" / "simulated_fraud_alerts.csv"
SUMMARY_FILE = BASE_DIR / "reports" / "fraud_alert_summary.csv"

if not ALERT_FILE.exists():
    raise FileNotFoundError(
        "Alert file not found. Run realtime_fraud_simulator.py first."
    )

df = pd.read_csv(ALERT_FILE)

if df.empty:
    print("No alerts generated in this simulation.")
else:
    total_alerts = len(df)
    actual_frauds = int(df["actual_is_fraud"].sum())
    false_alerts = total_alerts - actual_frauds

    high_alerts = int((df["risk_level"] == "High").sum())
    medium_alerts = int((df["risk_level"] == "Medium").sum())

    precision = actual_frauds / total_alerts * 100

    print("\n=== FRAUD ALERT MONITORING ===")
    print(f"Total Alerts      : {total_alerts}")
    print(f"High Risk Alerts  : {high_alerts}")
    print(f"Medium Risk Alerts: {medium_alerts}")
    print(f"Actual Fraud      : {actual_frauds}")
    print(f"False Alerts      : {false_alerts}")
    print(f"Alert Precision   : {precision:.2f}%")

    summary = pd.DataFrame([{
        "total_alerts": total_alerts,
        "high_risk_alerts": high_alerts,
        "medium_risk_alerts": medium_alerts,
        "actual_fraud_alerts": actual_frauds,
        "false_alerts": false_alerts,
        "alert_precision_percent": round(precision, 2)
    }])

    summary.to_csv(SUMMARY_FILE, index=False)
    print(f"\nSummary saved to: {SUMMARY_FILE}")
