-- ============================================================
-- NPCI Digital Payments Failure Analysis - Core SQL Queries
-- ============================================================
-- NOTE: data_quality_flag = 1 marks rows with unreliable checksums
-- (approved+BD+TD far from 100%), mostly from a Dec 2022 AEPS 
-- reporting anomaly (see FINDINGS.md). Queries below exclude flagged 
-- rows so results match the notebook's "flagged rows excluded" charts.
--
-- These queries are also embedded directly in run_query.py for 
-- execution — keep both in sync if modified here.
-- ============================================================

-- 1. Which banks have the highest TECHNICAL decline rates (infra issue)?
SELECT bank, ROUND(AVG(td_pct), 2) AS avg_td_pct
FROM declined_transactions
WHERE data_quality_flag = 0
GROUP BY bank
ORDER BY avg_td_pct DESC
LIMIT 10;

-- 2. Which banks have the highest BUSINESS decline rates (user/UX issue)?
SELECT bank, ROUND(AVG(bd_pct), 2) AS avg_bd_pct
FROM declined_transactions
WHERE data_quality_flag = 0
GROUP BY bank
ORDER BY avg_bd_pct DESC
LIMIT 10;

-- 3. Does failure behavior differ between NFS (ATM) and AEPS (Aadhaar)?
SELECT product,
       ROUND(AVG(bd_pct), 2) AS avg_bd_pct,
       ROUND(AVG(td_pct), 2) AS avg_td_pct,
       ROUND(AVG(total_decline_pct), 2) AS avg_total_decline_pct
FROM declined_transactions
WHERE data_quality_flag = 0
GROUP BY product;

-- 4. Monthly trend of total decline rate (are things improving over time?)
SELECT year, month, ROUND(AVG(total_decline_pct), 2) AS avg_total_decline_pct
FROM declined_transactions
WHERE data_quality_flag = 0
GROUP BY year, month
ORDER BY year, month;

-- 5. Big banks vs small banks: does higher volume correlate with lower failure?
SELECT bank,
       ROUND(AVG(total_volume), 2) AS avg_volume,
       ROUND(AVG(total_decline_pct), 2) AS avg_total_decline_pct
FROM declined_transactions
WHERE data_quality_flag = 0
GROUP BY bank
ORDER BY avg_volume DESC
LIMIT 15;

-- 6. Has technical decline improved over time while business decline stayed flat?
SELECT year, month,
       ROUND(AVG(bd_pct), 2) AS avg_bd_pct,
       ROUND(AVG(td_pct), 2) AS avg_td_pct
FROM declined_transactions
WHERE data_quality_flag = 0
GROUP BY year, month
ORDER BY year, month; 



