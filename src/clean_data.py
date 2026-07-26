"""
Data Cleaning Script
----------------------
Transforms the raw NPCI declined-transactions data into an analysis-ready
format:
- Drops redundant index columns (_id, id)
- Parses date and extracts year/month
  NOTE: NPCI's export has a quirk where the real month number is stored
  in the "day" slot, with the actual month field fixed at 01. E.g.
  "2022-01-05" actually means May 2022, not Jan 5th. Verified via
  src/check_dates.py (day values run 01-12 across years, consistent with
  month numbers, not real calendar days).
- Renames columns to short, consistent names
- Standardizes bank names:
    - Fixes inconsistent spacing and corrupted special characters that
      were fragmenting the same bank into multiple entries
      (e.g. "Yes Bank - Prepaid - YP2" vs "Yes Bank ? Prepaid ? YP2")
    - Normalizes casing (e.g. "Bank Of India" vs "bank of india" vs
      "Bank of India" were being treated as different banks)
    - Normalizes "Limited" -> "Ltd" and removes parentheses, since these
      were also fragmenting entries (e.g. "Equitas Small Finance Bank
      Limited" vs "...Ltd", "Karnataka Gramin Bank (Erstwhile...)" vs
      "Karnataka Gramin Bank Erstwhile...")
    - Applies explicit alias mapping for known duplicates that formatting
      rules alone can't catch, including spelling variants
      (e.g. "Vikash" vs "Vikas") found via systematic fuzzy-matching in
      src/check_duplicate_banks.py, not just manual inspection
- Confirms approved/BD/TD are percentages (see explore_data.py validation)
- Adds a derived total_decline_pct column
"""

import re
import pandas as pd

RAW_PATH = "data/raw/npci_declined_transactions.csv"
PROCESSED_PATH = "data/processed/npci_declined_cleaned.csv"

# Explicit fixes for known duplicate entities that regex/casing rules
# can't catch on their own (inconsistent formatting or spelling in the
# raw source, not a pattern we can generalize). Keys are
# post-standardization names -> canonical name to merge into.
# Found via src/check_duplicate_banks.py fuzzy-matching.
BANK_ALIASES = {
    "Yes Bank Prepaid Yp2": "Yes Bank - Prepaid - Yp2",
    "Andhra Pradesh Grameena Vikash Bank": "Andhra Pradesh Grameena Vikas Bank",
    "Paytm Payments Bank": "Paytm Payments Bank Ltd",
    "Fincare Small Finance Bank": "Fincare Small Finance Bank Ltd",
}

def standardize_bank_name(name):
    name = name.strip()
    name = re.sub(r"\s+", " ", name)          # collapse multiple/double spaces
    name = name.replace("?", "-")              # fix corrupted special chars
    name = re.sub(r"\s*-\s*", " - ", name)     # consistent spacing around hyphens
    name = name.rstrip(".")                    # remove trailing period (Ltd. vs Ltd)
    name = re.sub(r"\bLimited\b", "Ltd", name) # normalize Limited -> Ltd
    name = re.sub(r"[()]", "", name)           # remove parentheses (keep content)
    name = re.sub(r"\s+", " ", name).strip()   # re-collapse spaces after removals
    name = name.title()                        # normalize casing
    return name

def apply_bank_aliases(name):
    return BANK_ALIASES.get(name, name)

def clean_data():
    df = pd.read_csv(RAW_PATH)

    # Drop redundant index columns from the source database
    df = df.drop(columns=["_id", "id"])

    # Parse date and extract year/month (see date-quirk note in docstring)
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.day  # day slot actually holds the real month

    # Rename columns to short, consistent names
    df = df.rename(columns={
        "issuer_bank": "bank",
        "total_volume": "total_volume",
        "approved_transaction_volume": "approved_pct",
        "business_decline_transactions": "bd_pct",
        "technical_decline_transactions": "td_pct",
    })

    # Standardize bank name formatting, then resolve known duplicates
    df["bank"] = df["bank"].apply(standardize_bank_name)
    df["bank"] = df["bank"].apply(apply_bank_aliases)

    # Derived column: total decline percentage
    df["total_decline_pct"] = df["bd_pct"] + df["td_pct"]

    # Flag rows where approved+BD+TD is far from 100%, indicating
    # unreliable/incomplete reporting for that bank-month rather than
    # a real decline pattern. Investigation (see src/explore_data.py)
    # found 47 of 55 such rows cluster on a single AEPS reporting period
    # (Dec 2022), suggesting a systemic NPCI reporting gap that month
    # rather than scattered random noise.
    checksum = df["approved_pct"] + df["bd_pct"] + df["td_pct"]
    df["data_quality_flag"] = (checksum < 95) | (checksum > 105)
    n_flagged = df["data_quality_flag"].sum()
    print(f"Flagged {n_flagged} rows with unreliable checksum (outside 95-105%)")
  
    # Reorder columns for readability
    df = df[["date", "year", "month", "product", "bank", "total_volume",
              "approved_pct", "bd_pct", "td_pct", "total_decline_pct",
              "data_quality_flag"]]

    df.to_csv(PROCESSED_PATH, index=False)
    print(f"Cleaned data saved to {PROCESSED_PATH}")
    print(f"Shape: {df.shape}")
    print(df.head())

if __name__ == "__main__":
    clean_data()