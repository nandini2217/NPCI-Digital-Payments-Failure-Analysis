"""
Load to SQLite
----------------
Loads the cleaned NPCI declined-transactions data into a local SQLite 
database, so we can answer the project's business questions using SQL 
rather than only pandas.
"""

import sqlite3
import pandas as pd

PROCESSED_PATH = "data/processed/npci_declined_cleaned.csv"
DB_PATH = "data/npci.db"
TABLE_NAME = "declined_transactions"

def load_to_sql():
    df = pd.read_csv(PROCESSED_PATH, parse_dates=["date"])

    conn = sqlite3.connect(DB_PATH)
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)

    # Quick sanity check: row count matches what we loaded
    result = conn.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()
    print(f"Loaded {result[0]} rows into '{TABLE_NAME}' table in {DB_PATH}")

    # Preview
    preview = pd.read_sql(f"SELECT * FROM {TABLE_NAME} LIMIT 5", conn)
    print(preview)

    conn.close()

if __name__ == "__main__":
    load_to_sql()