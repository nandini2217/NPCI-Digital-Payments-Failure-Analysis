# UPI Transaction Failure Analysis

## Overview
An exploratory data analysis project investigating failure patterns in India's 
Unified Payments Interface (UPI) transactions. The goal is to understand *why* 
UPI transactions fail — separating technical infrastructure issues from 
business/user-side declines — and to identify which banks and time periods 
show reliability concerns.

## Business Questions
1. Which banks have chronically high **technical decline (TD)** rates 
   (infrastructure/reliability issue) vs high **business decline (BD)** rates 
   (user error / limits issue)?
2. Does the overall failure rate spike during high-volume periods 
   (festivals, month-end salary days)?
3. Do larger PSPs (SBI, HDFC, etc.) actually perform better than smaller 
   banks, or does market share mask worse reliability?
4. Has the technical decline rate improved over time while business decline 
   has stayed flat?

## Data Source
- Primary: [Dataful - UPI Payer/Payee PSP Performance](https://dataful.in/datasets/18242/) 
  — year-, month-, and bank-wise UPI transaction data with approval/BD/TD breakdown (2022–present)
- Secondary: [NPCI UPI Ecosystem Statistics](https://www.npci.org.in/what-we-do/upi/upi-ecosystem-statistics)

> Raw data files are not committed to this repo (see `.gitignore`). 
> Download instructions are in `src/download_data.py`.

## Tools
Python (pandas, matplotlib/seaborn), SQL (SQLite), Jupyter
