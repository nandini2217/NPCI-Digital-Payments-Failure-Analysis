"""
Fuzzy Bank Name Duplicate Checker
------------------------------------
Systematically checks all bank names for near-duplicates (formatting
variants of the same bank) rather than relying on manually noticing them
in top-N rankings. Flags any pair with high similarity for manual review.
"""

import pandas as pd
from rapidfuzz import fuzz

PROCESSED_PATH = "data/processed/npci_declined_cleaned.csv"
SIMILARITY_THRESHOLD = 90  # 0-100 scale

def find_potential_duplicates():
    df = pd.read_csv(PROCESSED_PATH)
    banks = sorted(df["bank"].unique())

    print(f"Checking {len(banks)} unique bank names for potential duplicates...\n")
    flagged = []

    for i in range(len(banks)):
        for j in range(i + 1, len(banks)):
            score = fuzz.ratio(banks[i], banks[j])
            if score >= SIMILARITY_THRESHOLD:
                flagged.append((banks[i], banks[j], round(score, 1)))

    if not flagged:
        print("No potential duplicates found above threshold.")
    else:
        print(f"Found {len(flagged)} potential duplicate pairs:\n")
        for a, b, score in flagged:
            print(f"  {score}%  |  '{a}'  <->  '{b}'")

    return flagged

if __name__ == "__main__":
    find_potential_duplicates()