
# 🏦 BFSI | Credit Card Fraud Detection & Risk Analytics

### End-to-End Fraud Analytics | Python • Pandas • MySQL • Power BI • Streamlit • Plotly

An end-to-end **Banking, Financial Services & Insurance (BFSI)** analytics project focused on identifying suspicious credit card transactions, analyzing fraud patterns, evaluating transaction risk, and assessing fraud alert performance.

The project combines Python-based data processing, SQL analytics, rule-based risk scoring, Power BI dashboards, and interactive fraud alert monitoring using Streamlit.

## 📊 Project Overview

Credit card fraud detection is a major challenge for financial institutions. This project explores transaction behavior and fraud patterns using a synthetic credit card transaction dataset.

**Key Objectives:**

- Analyze fraudulent and genuine transactions.
- Identify fraud trends by transaction hour, geographic location, and risk level.
- Develop a rule-based transaction risk scoring approach.
- Evaluate alert thresholds using precision, recall, F1 score, and fraud value recall.
- Present actionable insights through Power BI and Streamlit.

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
| Python | Data preprocessing, feature engineering, fraud analysis and risk scoring |
| Pandas | Data cleaning, transformation and aggregation |
| MySQL | Transaction storage and SQL-based fraud analysis |
| SQL | Fraud KPIs, risk segmentation and analytical queries |
| Power BI | Three-page business intelligence dashboard |
| Streamlit | Interactive historical fraud alert monitoring application |
| Plotly | Interactive charts in the Streamlit dashboard |
| Git & GitHub | Version control and project documentation |

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

## 📁 Project Structure

```text
BFSI CREDIT CARD FROUD ANALYSIS/
├── data/                   # Local datasets (not uploaded)
├── notebooks/              # Exploratory analysis
├── powerbi/                # Power BI summary datasets
├── reports/                # Analysis outputs and Power BI PDF
│   └── BFSI_Credit_Card_Fraud_Analytics.pdf
├── sql/
│   └── fraud_analysis.sql  # MySQL analysis queries
├── src/                    # Python analysis scripts
├── app.py                  # Streamlit fraud alert dashboard
├── .gitignore
└── README.md
```

*Large datasets and local development files are excluded from version control.*

## 📄 Power BI Report

The Power BI report contains three analytical pages.

### Page 1 — Executive Overview

Provides a high-level view of transaction volume, fraud rate, fraudulent transaction value, geographic fraud concentration, hourly fraud activity, and risk distribution.

### Page 2 — Fraud Patterns & Risk Analysis

Explores geographic fraud rates, fraud transactions by risk level, transaction volume versus fraud rate, and hourly fraud patterns.

### Page 3 — Fraud Alert & Risk Performance

Evaluates fraud alert thresholds using:

- Total fraud alerts
- Fraud value recall
- Precision and recall
- F1 score
- False-positive rate

**[📊 View Complete 3-Page Power BI Report](reports/BFSI_Credit_Card_Fraud_Analytics.pdf)**

## 🗄️ SQL Analysis

This project uses MySQL for credit card transaction analysis, fraud patterns, risk segmentation, and reporting.

The SQL script includes database schema creation and analytical queries for transaction risk levels, hourly trends, geographic analysis, and fraud-related KPIs.

**[🗄️ View Complete SQL Analysis](sql/fraud_analysis.sql)**

## 🐍 Python Source Code

Explore the Python implementation of this project, including:

- Data cleaning and preprocessing
- Feature engineering
- Rule-based fraud risk scoring
- Geographic and time-based fraud analysis
- Fraud alert evaluation and performance analysis

**[🐍 View Python Source Code](src/)**

## 🚨 Streamlit Fraud Alert Monitoring

An interactive Streamlit application complements the Power BI report by allowing users to explore historical simulated fraud alerts.

**Dashboard Features:**

- Total alerts, high-risk alerts and actual fraud KPIs
- Alerts by risk level
- Fraud alert outcomes
- Searchable and filterable transaction details
- Downloadable fraud alerts CSV

The dashboard uses historical transaction simulation and is not a live banking fraud monitoring system. Results from its deliberately selected demonstration sample should not be interpreted as production performance.

**[💻 View Streamlit Dashboard Source Code](app.py)**

*Live dashboard link can be added after deployment.*

## 🔍 Key Business Insights

- The overall fraud rate is approximately **0.58%**, highlighting class imbalance in the dataset.
- Fraud risk differs substantially across transaction risk categories.
- Fraud patterns vary by transaction hour and geographic location.
- Lower alert thresholds capture more fraudulent transaction value but generate more alerts.
- Among the tested thresholds, **40 achieved the highest observed F1 score (approximately 0.13)**.
- Threshold 40 is a candidate for further validation, not a production-ready recommendation.

## ⚠️ Dataset & Project Disclaimer~~

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

**Developed as a data analytics and fraud intelligence portfolio project.**
