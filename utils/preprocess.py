import pandas as pd

def load_and_prepare_data(path):
    df = pd.read_excel(path, engine="openpyxl")

    # Normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    # Use query text for matching
    df["combined_text"] = df["query"].fillna("")

    return df