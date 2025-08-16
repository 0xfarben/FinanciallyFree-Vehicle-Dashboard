import pandas as pd
import os
from data_cleaning import clean_numeric_columns


def load_and_clean_monthly_vehicle_category(filepath):
    """Load and clean monthly vehicle category Excel file."""
    # Read Excel file, skip header rows
    raw_df = pd.read_excel(filepath, skiprows=3)
    
    # Print column names for debugging
    print(f"Columns in {os.path.basename(filepath)}: {list(raw_df.columns)}")
    
    # Rename columns to standard format - handle different column structures
    expected_columns = ["S No", "Vehicle Category", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "TOTAL"]
    
    # Only rename if we have the expected number of columns
    if len(raw_df.columns) == len(expected_columns):
        rename_map = {col: name for col, name in zip(raw_df.columns, expected_columns)}
        df = raw_df.rename(columns=rename_map)
    else:
        # Use the first two columns as S No and Vehicle Category, rest as months
        df = raw_df.copy()
        df.columns = expected_columns[:len(df.columns)]
    
    # Keep only rows that have a numeric S No
    df = df[pd.to_numeric(df["S No"], errors="coerce").notna()].copy()
    df["S No"] = df["S No"].astype(int)
    
    # Clean numeric month columns - only those that exist
    month_cols = [col for col in ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "TOTAL"] if col in df.columns]
    df = clean_numeric_columns(df, month_cols)
    
    return df


def load_and_clean_monthly_maker(filepath):
    """Load and clean monthly manufacturer Excel file."""
    # Read Excel file, skip header rows
    df = pd.read_excel(filepath, skiprows=3, header=None)
    
    # Print column count for debugging
    print(f"Columns in {os.path.basename(filepath)}: {len(df.columns)}")
    
    # Set column names based on actual number of columns
    expected_columns = ["S No", "Maker", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "TOTAL"]
    
    if len(df.columns) == len(expected_columns):
        df.columns = expected_columns
    else:
        # Use available columns
        available_columns = expected_columns[:len(df.columns)]
        df.columns = available_columns
    
    # Drop any residual header row (NaN in S No / Maker)
    df = df[pd.to_numeric(df["S No"], errors="coerce").notna()].copy()
    df["S No"] = df["S No"].astype(int)
    
    # Clean numeric columns - only those that exist
    month_cols = [col for col in ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "TOTAL"] if col in df.columns]
    df = clean_numeric_columns(df, month_cols)
    
    # Trim maker names
    df["Maker"] = df["Maker"].astype(str).str.strip()
    
    return df


def process_all_monthly_files(monthly_data_dir):
    """Process all monthly Excel files and convert to cleaned CSVs."""
    processed_files = []
    
    # Process vehicle category files
    for year in range(2021, 2026):
        vc_file = os.path.join(monthly_data_dir, f"{year}_monthly_VC.xlsx")
        if os.path.exists(vc_file):
            print(f"Processing {year} vehicle category data...")
            vc_df = load_and_clean_monthly_vehicle_category(vc_file)
            
            # Save as CSV
            csv_file = os.path.join(monthly_data_dir, f"{year}_monthly_VC.csv")
            vc_df.to_csv(csv_file, index=False)
            processed_files.append(csv_file)
            print(f"Saved: {csv_file}")
    
    # Process maker files
    for year in range(2021, 2026):
        maker_file = os.path.join(monthly_data_dir, f"{year}_monthly_MAKER.xlsx")
        if os.path.exists(maker_file):
            print(f"Processing {year} maker data...")
            maker_df = load_and_clean_monthly_maker(maker_file)
            
            # Save as CSV
            csv_file = os.path.join(monthly_data_dir, f"{year}_monthly_MAKER.csv")
            maker_df.to_csv(csv_file, index=False)
            processed_files.append(csv_file)
            print(f"Saved: {csv_file}")
    
    return processed_files


def main():
    """Main function to process all monthly data files."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    monthly_data_dir = os.path.join(project_root, "data", "monthly")
    
    print("Processing monthly data files...")
    processed_files = process_all_monthly_files(monthly_data_dir)
    
    print(f"\nProcessed {len(processed_files)} files:")
    for file in processed_files:
        print(f"  - {os.path.basename(file)}")


if __name__ == "__main__":
    main() 