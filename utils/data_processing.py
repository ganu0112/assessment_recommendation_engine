import pandas as pd
import os

def clean_and_process():
    os.makedirs("data/processed", exist_ok=True)

    df = pd.read_json("data/raw/shl_raw.json")

    df["name"] = df["name"].str.strip()
    df["description"] = df["description"].fillna("")
    df["duration_minutes"] = df["duration"].str.extract(r'(\d+)')
    df["duration_minutes"] = pd.to_numeric(df["duration_minutes"], errors="coerce")

    df["combined_text"] = (
        df["name"] + " " +
        df["description"] + " " +
        df["test_type"].fillna("")
    )

    df.to_csv("data/processed/shl_clean.csv", index=False)

    print("Stage 2 Complete: Clean data saved.")
    print("Total records:", len(df))