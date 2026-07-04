"""
Data Acquisition Script
------------------------
This project analyzes failure patterns (Business Decline vs Technical 
Decline) across NPCI's NFS (ATM network) and AEPS (Aadhaar-enabled 
payments) products.

Source: India Data Portal (free, no login required)
Dataset page: https://ckandev.indiadataportal.com/dataset/national-payments-corporation-of-india-npci/resource/f8c33592-34cd-4bdf-b4b8-d845d67b4eb4
Original publisher: National Payments Corporation of India (NPCI)

Coverage: 107 issuer banks, monthly, 2021-2023, products: NFS, AEPS
Columns: date, product, issuer_bank, total_volume, 
         approved_transaction_volume, business_decline_transactions, 
         technical_decline_transactions

Note: This dataset was originally investigated as a potential source of 
UPI-specific data, but profiling (see explore_data.py output and NOTES.md) 
confirmed it contains NFS and AEPS only. Project scope was adjusted 
accordingly.
"""

import os
import urllib.request

RAW_DATA_PATH = "data/raw/npci_declined_transactions.csv"
SOURCE_URL = "https://ckandev.indiadataportal.com/datastore/dump/f8c33592-34cd-4bdf-b4b8-d845d67b4eb4?bom=True"

def download_data():
    os.makedirs("data/raw", exist_ok=True)
    if os.path.exists(RAW_DATA_PATH):
        print(f"Data already exists at {RAW_DATA_PATH}")
        return
    print("Downloading NPCI declined transactions dataset (NFS, AEPS)...")
    urllib.request.urlretrieve(SOURCE_URL, RAW_DATA_PATH)
    print(f"Saved to {RAW_DATA_PATH}")

if __name__ == "__main__":
    download_data()