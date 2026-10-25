# BFSI Credit Card Fraud Detection & Risk Analytics

## Executive Summary

This project analyzes 1,296,675 synthetic credit card transactions to identify fraud patterns, evaluate transaction risk, and explore fraud alert strategies using Python, MySQL, Power BI, and Streamlit.

The training dataset contains 7,506 fraudulent transactions, representing approximately 0.58% of all transactions. The total value of transactions labeled as fraudulent is approximately $3.99 million.

## Key Findings

**1. Fraud is relatively rare.** Only 0.58% of transactions are labeled as fraudulent, highlighting the importance of evaluating fraud detection systems with metrics beyond accuracy.

**2. High-risk transactions show stronger fraud concentration.** The observed fraud rate is approximately 50.72% in the High Risk category, compared with 8.11% in Medium Risk and 0.44% in Low Risk.

**3. Fraud remains present in low-risk transactions.** A large share of fraudulent transactions is classified as Low Risk, demonstrating the limitations of the current rule-based scoring approach.

**4. Alert thresholds create operational trade-offs.** Lower thresholds generally increase fraud coverage but can also increase false alerts and investigation workload.

**5. Fraudulent transaction value represents potential exposure.** Approximately $3.99 million in transaction value is labeled as fraudulent. This does not establish actual financial losses.

## Business Recommendations

- Prioritize high-risk transactions for investigation while considering transaction value and operational capacity.
- Apply proportionate verification to medium-risk transactions.
- Improve fraud detection rules to identify fraudulent transactions currently classified as low risk.
- Evaluate alert thresholds using precision, recall, false positive rate, fraud value recall, and investigation costs.
- Validate the risk scoring approach on held-out test data before considering operational deployment.

## Project Limitations

The dataset is synthetic, and the risk scores are generated using manually defined rules. Reported risk-level performance comes from the training dataset.

The Streamlit dashboard replays historical scored transactions and does not connect to a live payment processing system.

The demonstration sample is deliberately stratified across risk levels. Its 40% alert precision must not be interpreted as the system's overall or production precision.

## Conclusion

The analysis demonstrates how transaction data, rule-based risk scoring, SQL analytics, interactive dashboards, and simulated fraud monitoring can support fraud investigation and risk management decisions.

Further work should focus on held-out validation, stronger fraud detection methods, threshold optimization, and operational impact assessment.