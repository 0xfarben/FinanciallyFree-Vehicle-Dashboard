import pandas as pd
import os
from data_cleaning import load_and_clean_vehicle_category_csv, load_and_clean_maker_csv


def melt_years(df: pd.DataFrame, id_cols: list, value_name: str) -> pd.DataFrame:
    """Convert wide year columns into long format with integer years and values."""
    year_cols = [c for c in df.columns if c.isdigit()]
    long_df = df.melt(id_vars=id_cols, value_vars=year_cols, var_name="Year", value_name=value_name)
    long_df["Year"] = long_df["Year"].astype(int)
    long_df[value_name] = pd.to_numeric(long_df[value_name], errors="coerce").astype("Int64")
    return long_df.dropna(subset=[value_name])


def compute_yoy(long_df: pd.DataFrame, group_col: str, value_col: str = "Registrations") -> pd.DataFrame:
    """Compute YoY percentage change per group."""
    long_df = long_df.sort_values([group_col, "Year"]).copy()
    long_df["YoY_pct"] = (
        long_df.groupby(group_col)[value_col]
        .pct_change()
        .multiply(100)
        .round(2)
    )
    return long_df


def clean_final_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean final dataframe by handling NaN values and formatting."""
    # Replace NaN YoY_pct with empty string for better CSV readability
    df["YoY_pct"] = df["YoY_pct"].astype(str).replace("nan", "").replace("<NA>", "")
    
    # Ensure Registrations is properly formatted
    df["Registrations"] = df["Registrations"].fillna(0).astype(int)
    
    return df


def map_vehicle_groups(vc_df: pd.DataFrame) -> pd.DataFrame:
    """Map detailed vehicle categories to investor-friendly groups 2W/3W/4W."""
    group_map = {
        "2W": ["TWO WHEELER"],
        "3W": ["THREE WHEELER"],
        "4W": [
            "FOUR WHEELER",
            "LIGHT MOTOR VEHICLE",
            "MEDIUM MOTOR VEHICLE",
            "HEAVY MOTOR VEHICLE",
            "LIGHT PASSENGER VEHICLE",
            "MEDIUM PASSENGER VEHICLE",
            "HEAVY PASSENGER VEHICLE",
            "LIGHT GOODS VEHICLE",
            "MEDIUM GOODS VEHICLE",
            "HEAVY GOODS VEHICLE",
        ],
    }

    year_cols = [c for c in vc_df.columns if c.isdigit()]
    rows = []
    for group, keywords in group_map.items():
        mask = vc_df["Vehicle Category"].str.contains("|".join(keywords), case=False, na=False)
        subset = vc_df.loc[mask, ["Vehicle Category"] + year_cols]
        # Sum across matched categories per year
        totals = subset[year_cols].sum(axis=0)
        for year in year_cols:
            rows.append({"Group": group, "Year": int(year), "Registrations": int(totals[year]) if pd.notna(totals[year]) else None})

    grouped_df = pd.DataFrame(rows)
    grouped_df["Registrations"] = grouped_df["Registrations"].astype("Int64")
    return grouped_df


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def run_pipeline(data_dir: str) -> dict:
    vc_path = os.path.join(data_dir, "yearly", "2021-2025_VCLASS.csv")
    maker_path = os.path.join(data_dir, "yearly", "2021-2025_MAKER.csv")

    vc_df = load_and_clean_vehicle_category_csv(vc_path)
    maker_df = load_and_clean_maker_csv(maker_path)

    # Vehicle category groups (2W/3W/4W) in long format with YoY
    vc_group_long = map_vehicle_groups(vc_df)
    vc_group_long = compute_yoy(vc_group_long, group_col="Group", value_col="Registrations")
    vc_group_long = clean_final_data(vc_group_long)

    # Maker long with YoY
    maker_long = melt_years(maker_df[["Maker", "2025", "2024", "2023", "2022", "2021"]], ["Maker"], "Registrations")
    maker_long = compute_yoy(maker_long, group_col="Maker", value_col="Registrations")
    maker_long = clean_final_data(maker_long)

    # Save processed outputs
    processed_dir = os.path.join(data_dir, "processed")
    ensure_dir(processed_dir)
    vc_group_path = os.path.join(processed_dir, "vehicle_category_group_yoy.csv")
    maker_yoy_path = os.path.join(processed_dir, "maker_yoy.csv")
    vc_group_long.to_csv(vc_group_path, index=False)
    maker_long.to_csv(maker_yoy_path, index=False)

    return {
        "vc_group_long": vc_group_long,
        "maker_long": maker_long,
        "vc_path": vc_group_path,
        "maker_path": maker_yoy_path,
    }


def main():
    project_root = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(project_root, "data")

    print("Running pipeline...")
    outputs = run_pipeline(data_dir)

    print("\nVehicle category group YoY (head):")
    print(outputs["vc_group_long"].head())

    print("\nMaker YoY (head):")
    print(outputs["maker_long"].head())

    print("\nSaved processed files:")
    print(outputs["vc_path"])
    print(outputs["maker_path"])


if __name__ == "__main__":
    main() 

