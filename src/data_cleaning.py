import os
import pandas as pd


def clean_numeric_columns(df, columns):
    """
    Remove commas and non-digit characters from numbers and convert to nullable integers.
    """
    for col in columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace(r"[^0-9\-]", "", regex=True)
            .replace({"": None, "-": None})
        )
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    return df

def load_and_clean_vehicle_category_csv(filepath):
    """Load and clean vehicle category CSV file."""
    # File has 3 header rows; the 4th row contains years, with first two and last empty → Unnamed
    raw_df = pd.read_csv(filepath, skiprows=3)

    # Rename Unnamed columns to meaningful names
    rename_map = {
        col: name
        for col, name in zip(raw_df.columns, ["S No", "Vehicle Category", "2025", "2024", "2023", "2022", "2021", "TOTAL"])  # type: ignore
    }
    df = raw_df.rename(columns=rename_map)

    # Keep only rows that have a numeric S No
    df = df[pd.to_numeric(df["S No"], errors="coerce").notna()].copy()
    df["S No"] = df["S No"].astype(int)

    # Clean numeric year columns
    year_cols = ["2025", "2024", "2023", "2022", "2021", "TOTAL"]
    df = clean_numeric_columns(df, year_cols)

    return df


def load_and_clean_maker_csv(filepath):
    """Load and clean manufacturer CSV file."""
    # Similar multi-row header structure: skip 3 header rows
    df = pd.read_csv(filepath, skiprows=3, header=None)
    df.columns = ["S No", "Maker", "2025", "2024", "2023", "2022", "2021", "TOTAL"]

    # Drop any residual header row (NaN in S No / Maker)
    df = df[pd.to_numeric(df["S No"], errors="coerce").notna()].copy()
    df["S No"] = df["S No"].astype(int)

    # Clean numeric columns
    year_cols = ["2025", "2024", "2023", "2022", "2021", "TOTAL"]
    df = clean_numeric_columns(df, year_cols)

    # Trim maker names
    df["Maker"] = df["Maker"].astype(str).str.strip()

    return df 