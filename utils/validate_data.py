import pandas as pd

def validate():
    df = pd.read_csv("data/processed/shl_clean.csv")

    print("Total records:", len(df))
    print("Missing names:", df["name"].isnull().sum())
    print("Missing descriptions:", df["description"].isnull().sum())
    print("Missing duration:", df["duration_minutes"].isnull().sum())

    print("Validation complete.")