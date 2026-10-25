# 🏦 BFSI | Credit Card Fraud Detection & Risk Analytics

### End-to-End Fraud Analytics | Python • SQL • Power BI • Streamlit

An end-to-end **Banking, Financial Services & Insurance (BFSI)** analytics project focused on identifying suspicious credit card transactions, analyzing fraud patterns, evaluating transaction risk, and assessing fraud alert performance.

The project combines data processing, SQL-based analysis, rule-based risk scoring, interactive dashboards, and threshold performance evaluation to support data-driven fraud monitoring.

## 📊 Project Overview

Credit card fraud detection is a major challenge for financial institutions. This project explores transaction behavior and fraud patterns using a synthetic transaction dataset.

**Key objectives:**
- Analyze fraudulent and genuine transactions.
- Identify fraud trends by transaction hour, geographic location, and risk level.
- Develop a rule-based transaction risk scoring approach.
- Evaluate alert thresholds using precision, recall, F1 score, and fraud value recall.
- Present actionable insights through Power BI and Streamlit dashboards.

## 📈 Key Project Metrics

| Metric | Result |
|---|---|
| Total Transactions | 1,296,675 |
| Fraud Transactions | 7,506 |
| Fraud Rate | 0.58% |
| Fraudulent Transaction Value | Approximately $3.99M |
| Risk Categories | Low, Medium, High |
| Power BI Dashboard Pages | 3 |

*Fraudulent transaction value represents the total amount of labeled fraudulent transactions, not verified financial losses.*

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data preprocessing and analytics |
| Pandas | Data transformation and analysis |
| MySQL | Transaction storage and SQL analytics |
| Power BI | Business intelligence dashboards |
| Streamlit | Interactive fraud monitoring application |
| Git & GitHub | Version control and portfolio presentation |

## 🧠 Fraud Risk Scoring

A rule-based risk scoring framework evaluates suspicious transaction characteristics, including:

- Late-night transaction activity
- High transaction amounts
- Unusual merchant distance
- High transaction frequency within a short period
- Spending significantly above recent transaction behavior

Transactions are classified into three risk levels:

| Risk Level | Score Range |
|---|---|
| Low | 0–39 |
| Medium | 40–69 |
| High | 70–100 |

This scoring system is a heuristic risk assessment approach, not a trained machine-learning fraud classifier.

## 📊 Power BI Dashboard

The Power BI report contains three analytical pages.

### 1. Executive Overview

Provides a high-level view of transaction volume, fraud rate, fraudulent transaction value, geographic fraud concentration, hourly fraud activity, and risk distribution.

### 2. Fraud Patterns & Risk Analysis

Explores geographic fraud rates, fraud transactions by risk level, transaction volume versus fraud rate, and hourly fraud patterns.

### 3. Fraud Alert & Risk Performance

Evaluates fraud alert thresholds using:

- Total fraud alerts
- Fraud value recall
- Precision and recall
- F1 score
- False-positive rate

## 🔍 Key Business Insights

- The overall fraud rate is approximately **0.58%**, highlighting the class imbalance in the transaction dataset.
- Fraud risk differs substantially across transaction risk categories.
- Fraud patterns vary by transaction hour and geographic location.
- Lower alert thresholds capture more fraudulent transaction value but generate more alerts.
- Among the tested thresholds, **40 achieved the highest observed F1 score (approximately 0.13)**.
- Threshold 40 is a candidate for further validation, not a production-ready recommendation.

## 📁 Project Structure

```text
BFSI CREDIT CARD FRAUD ANALYSIS/
├── data/
├── notebooks/
├── powerbi/
├── reports/
│   └── BFSI_Credit_Card_Fraud_Analytics.pdf
├── src/
├── app.py
└── README.md
```

## 📄 Dashboard Report

The complete three-page Power BI report is available here:

[View Power BI Analytics Report](reports/BFSI_Credit_Card_Fraud_Analytics.pdf)

## 🗄️ SQL Analysis

This project uses MySQL for credit card transaction analysis, fraud detection, risk segmentation, and reporting.

The SQL script includes database schema creation and analytical queries for fraud patterns, transaction risk levels, hourly trends, and geographic analysis.

**[View Complete SQL Analysis](sql/fraud_analysis.sql)**



## 🐍 Python Source Code

Explore the complete Python implementation of this project, including:

- Data cleaning and preprocessing
- Feature engineering
- Fraud risk scoring
- Geographic and time-based fraud analysis
- Fraud alert monitoring and evaluation

**[View Python Source Code](src/)**

**[View Streamlit Dashboard Code](app.py)**


## ⚠️ Dataset & Project Disclaimer

This project uses a synthetic credit card transaction dataset for educational, analytical, and portfolio purposes.

Risk scores and alert thresholds are exploratory and should not be used for real financial decisions without additional validation, monitoring, and appropriate governance.

## 🚀 Future Improvements

- Machine-learning fraud classification
- Model performance comparison
- Explainable fraud risk scoring
- Automated monitoring and alert workflows
- Evaluation on unseen transaction data

---

**Project Category:** BFSI Analytics | Fraud Detection | Risk Analytics | Business Intelligence

**Developed as a data analytics and fraud intelligence portfolio project.**# BFSI-Credit-Card-Fraud-Analytics
Interactive Credit Card Fraud Detection &amp; Risk Analytics Dashboard using Python, SQL, Plotly and Power BI.
