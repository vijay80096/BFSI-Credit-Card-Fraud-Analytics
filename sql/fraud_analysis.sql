CREATE DATABASE IF NOT EXISTS bfsi_fraud_analysis;

USE bfsi_fraud_analysis;

SELECT DATABASE();


USE bfsi_fraud_analysis;

CREATE TABLE IF NOT EXISTS credit_card_transactions (
    transaction_id VARCHAR(64) PRIMARY KEY,
    transaction_datetime DATETIME,
    card_id VARCHAR(32),
    merchant VARCHAR(255),
    category VARCHAR(100),
    amount DECIMAL(12,2),
    city VARCHAR(150),
    state VARCHAR(20),
    transaction_hour INT,
    is_weekend TINYINT,
    merchant_distance_km DECIMAL(10,2),
    risk_score INT,
    risk_level VARCHAR(20),
    is_fraud TINYINT
);

SHOW TABLES;


USE bfsi_fraud_analysis;

SELECT
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_transactions,
    COUNT(*) - SUM(is_fraud) AS genuine_transactions,
    ROUND(AVG(is_fraud) * 100, 4) AS fraud_rate_percent,
    ROUND(SUM(amount), 2) AS total_transaction_value,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END), 2)
        AS fraudulent_transaction_value
FROM credit_card_transactions;


SELECT
    risk_level,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_transactions,
    ROUND(AVG(is_fraud) * 100, 2) AS fraud_rate_percent
FROM credit_card_transactions
GROUP BY risk_level
ORDER BY fraud_rate_percent DESC;


SELECT
    transaction_hour,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_transactions,
    ROUND(AVG(is_fraud) * 100, 2) AS fraud_rate_percent
FROM credit_card_transactions
GROUP BY transaction_hour
ORDER BY transaction_hour;


SELECT
    state,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_transactions,
    ROUND(AVG(is_fraud) * 100, 2) AS fraud_rate_percent
FROM credit_card_transactions
GROUP BY state
HAVING COUNT(*) >= 1000
ORDER BY fraud_transactions DESC
LIMIT 10;



USE bfsi_fraud_analysis;

CREATE OR REPLACE VIEW vw_fraud_kpis AS
SELECT
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_transactions,
    COUNT(*) - SUM(is_fraud) AS genuine_transactions,
    ROUND(AVG(is_fraud) * 100, 4) AS fraud_rate_percent,
    ROUND(SUM(amount), 2) AS total_transaction_value,
    ROUND(
        SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END),
        2
    ) AS fraudulent_transaction_value
FROM credit_card_transactions;

CREATE OR REPLACE VIEW vw_fraud_by_risk AS
SELECT
    risk_level,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_transactions,
    ROUND(AVG(is_fraud) * 100, 2) AS fraud_rate_percent
FROM credit_card_transactions
GROUP BY risk_level;

CREATE OR REPLACE VIEW vw_fraud_by_hour AS
SELECT
    transaction_hour,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_transactions,
    ROUND(AVG(is_fraud) * 100, 2) AS fraud_rate_percent
FROM credit_card_transactions
GROUP BY transaction_hour;

CREATE OR REPLACE VIEW vw_fraud_by_state AS
SELECT
    state,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_transactions,
    ROUND(AVG(is_fraud) * 100, 2) AS fraud_rate_percent
FROM credit_card_transactions
GROUP BY state;

SHOW FULL TABLES
WHERE Table_type = 'VIEW';

SELECT * FROM vw_fraud_kpis;

SELECT *
FROM bfsi_fraud_analysis.vw_fraud_kpis;

SELECT *
FROM bfsi_fraud_analysis.vw_fraud_by_hour
ORDER BY transaction_hour;

SELECT *
FROM bfsi_fraud_analysis.vw_fraud_by_state
ORDER BY fraud_transactions DESC;

SELECT *
FROM bfsi_fraud_analysis.vw_fraud_by_risk
ORDER BY
    CASE risk_level
        WHEN 'Low' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'High' THEN 3
    END;