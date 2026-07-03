"""
Data Exploration Script

Quick profiling of the raw dataset before writing cleaning logic.
Run this first whenever a new raw file is added, to catch schema 
surprises (mixed products, percentage vs absolute values, nulls, 
inconsistent bank naming) before they leak into the cleaning pipeline.
"""

import pandas as pd

RAW_DATA_PATH = "data/raw/upi_declined_transactions.csv"

def explore():
    df = pd.read_csv(RAW_DATA_PATH)

    print("=" * 50)
    print("SHAPE:", df.shape)

    print("\n" + "=" * 50)
    print("UNIQUE PRODUCTS:")
    print(df["product"].unique())

    print("\n" + "=" * 50)
    print("UPI ROW COUNT:", (df["product"] == "UPI").sum())

    print("\n" + "=" * 50)
    print("NULL COUNTS:")
    print(df.isnull().sum())

    print("\n" + "=" * 50)
    print("DATE RANGE:", df["date"].min(), "to", df["date"].max())

    print("\n" + "=" * 50)
    print("UNIQUE BANKS:", df["issuer_bank"].nunique())
    print(df["issuer_bank"].unique()[:15])  # sample

if __name__ == "__main__":
    explore()