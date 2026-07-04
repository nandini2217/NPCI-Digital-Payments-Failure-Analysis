# Findings: NPCI Digital Payments Failure Analysis

## Summary
This analysis examined failure patterns in two NPCI-operated payment 
products — NFS (ATM network) and AEPS (Aadhaar-enabled payments) — across 
107 banks, from August 2021 to July 2023. Failures were split into 
Business Decline (BD, user/limit-related) and Technical Decline (TD, 
infrastructure-related).

## Key Findings

### 1. AEPS fails significantly more often than NFS, driven by technical issues
- AEPS: 23.37% total decline (6.31% TD, 17.06% BD)
- NFS: 18.05% total decline (1.72% TD, 16.34% BD)

AEPS's technical decline rate is over **3.6x higher** than NFS's. This is 
consistent with AEPS's dependence on biometric authentication over often 
lower-quality rural network infrastructure, versus NFS's more mature, 
wired ATM network.

### 2. Regional Rural Banks (RRBs) dominate technical failure rankings
The top technical-decline banks are almost entirely regional rural banks 
(Bangiya Gramin Vikash Bank, Jharkhand Rajya Gramin Bank, Madhyanchal 
Gramin Bank, Tripura Gramin Bank, Chhattisgarh Rajya Gramin Bank) rather 
than major national banks. This points to an infrastructure gap between 
large commercial banks and smaller rural-serving institutions.

### 3. Business decline is rising slightly; technical decline is falling
Comparing 2021 to 2023 monthly averages:
- BD: ~15.7% (late 2021) → ~17.3% (mid 2023)
- TD: ~4.3% (late 2021) → ~3.0-3.8% (mid 2023)

This suggests NPCI/banks have made real infrastructure improvements 
(fewer technical failures), but user-side friction — incorrect PINs, 
limit breaches, insufficient balance — has not improved and may be 
worsening slightly as transaction volumes grow.

### 4. Higher transaction volume does not guarantee lower failure rates
State Bank of India processes by far the highest volume (91.65 avg) but 
has a 20.07% decline rate — worse than several much smaller banks like 
Union Bank of India (26.47 volume, 15.65% decline). Scale alone doesn't 
predict reliability; some large banks (e.g. Bank of Baroda at 29.91% 
decline) perform notably worse than peers of similar size.

## Data Quality Issues Found and Resolved
- **Date encoding bug**: the source data stored the actual month number 
  in the "day" field, with the real month field fixed at 01 (e.g. 
  "2022-01-05" meant May 2022, not January 5th). Caught by validating 
  unique date counts before trusting any time-series result — an initial 
  pass showed only 3 distinct year-month combinations across 3 years, 
  which was the signal something was wrong.
- **Inconsistent bank name formatting**: several banks appeared as 
  multiple entries due to casing differences ("Bank of Baroda" vs 
  "Bank Of Baroda"), corrupted special characters, and inconsistent 
  punctuation ("Ltd." vs "Ltd"). Resolved via standardization rules plus 
  a small explicit alias map for cases regex couldn't generalize.
- A small number of edge-case duplicate bank entries may remain due to 
  source data quality; this was not fully exhaustive.

## Known Limitations
- Dataset covers NFS and AEPS only, not UPI (see `NOTES.md` for the full 
  data source investigation and why UPI-specific data wasn't available 
  for free without violating NPCI's scraping policy).
- One month (June 2023) is missing from the source data.
- Figures are percentages reported by NPCI/issuer banks, not raw 
  transaction counts, so absolute failure volumes cannot be derived from 
  this dataset alone.