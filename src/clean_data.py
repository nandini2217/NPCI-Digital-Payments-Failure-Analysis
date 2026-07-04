"""
Data Cleaning Script
----------------------
Transforms the raw NPCI declined-transactions data into an analysis-ready
format:
- Drops redundant index columns (_id, id)
- Parses date into year/month for easier grouping
- Renames columns to short, consistent names
- Confirms approved/BD/TD are percentages (see explore_data.py validation)
- Adds a derived total_decline_pct column
"""

import pandas as pd

RAW_PATH = "data/raw/npci_declined_transactions.csv"
PROCESSED_PATH = "data/processed/npci_declined_cleaned.csv"

def clean_data():
    df = pd.read_csv(RAW_PATH)

    # Drop redundant index columns from the source database
    df = df.drop(columns=["_id", "id"])

    # Parse date and extract year/month
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    # Rename columns to short, consistent names
    df = df.rename(columns={
        "issuer_bank": "bank",
        "total_volume": "total_volume",
        "approved_transaction_volume": "approved_pct",
        "business_decline_transactions": "bd_pct",
        "technical_decline_transactions": "td_pct",
    })

    # Standardize bank name formatting (strip whitespace, consistent casing)
    df["bank"] = df["bank"].str.strip()

    # Derived column: total decline percentage
    df["total_decline_pct"] = df["bd_pct"] + df["td_pct"]

    # Reorder columns for readability
    df = df[["date", "year", "month", "product", "bank", "total_volume",
              "approved_pct", "bd_pct", "td_pct", "total_decline_pct"]]

    df.to_csv(PROCESSED_PATH, index=False)
    print(f"Cleaned data saved to {PROCESSED_PATH}")
    print(f"Shape: {df.shape}")
    print(df.head())

if __name__ == "__main__":
    clean_data()