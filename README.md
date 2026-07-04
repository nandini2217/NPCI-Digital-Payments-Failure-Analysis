# NPCI Digital Payments Failure Analysis

## Overview
An exploratory data analysis project investigating failure patterns in 
India's NPCI-operated digital payment products — specifically NFS 
(National Financial Switch, the ATM network) and AEPS (Aadhaar-enabled 
Payment System). The goal is to understand *why* transactions fail — 
separating technical infrastructure issues from business/user-side 
declines — and to identify which banks and time periods show reliability 
concerns.

Note: This project originally targeted UPI-specific failure data. After 
investigating multiple sources (see `NOTES.md` for the full decision log), 
the scope was adjusted to NFS/AEPS, which offer the same Business 
Decline / Technical Decline structure with genuinely free, unrestricted 
data — and are themselves under-analyzed compared to UPI.

## Business Questions
1. Which banks have chronically high **technical decline (TD)** rates 
   (infrastructure/reliability issue) vs high **business decline (BD)** 
   rates (user error / limits issue)?
2. Does NFS (ATM) failure behavior differ from AEPS (Aadhaar-based) 
   failure behavior — are the failure causes fundamentally different 
   between the two products?
3. Do larger banks (SBI, HDFC, etc.) actually perform better than smaller 
   banks, or does market share mask worse reliability?
4. Has technical decline improved over the 2021–2023 period while 
   business decline stayed flat?

## Data Source
- [India Data Portal - NPCI Product Wise Declined Transactions](https://ckandev.indiadataportal.com/dataset/national-payments-corporation-of-india-npci/resource/f8c33592-34cd-4bdf-b4b8-d845d67b4eb4) 
  (free, no login required)
- Original publisher: National Payments Corporation of India (NPCI)
- Coverage: 107 banks, monthly, 2021–2023, NFS and AEPS products

## Project Structure
upi-failure-analysis/
├── data/
│   ├── raw/          # raw downloaded CSVs (not tracked)
│   └── processed/    # cleaned data (not tracked)
├── notebooks/        # EDA notebooks
├── sql/               # SQL queries for business questions
├── src/               # data acquisition, exploration & cleaning scripts
├── NOTES.md           # data source exploration & decision log
├── requirements.txt
└── README.md

## Tools
Python (pandas, matplotlib/seaborn), SQL (SQLite), Jupyter

## Status
🚧 In progress — data cleaning stage

## Findings
_(To be added as analysis progresses — see `FINDINGS.md`)