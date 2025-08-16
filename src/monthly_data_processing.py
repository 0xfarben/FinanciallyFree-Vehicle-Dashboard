import pandas as pd
import os
from data_cleaning import clean_numeric_columns


def load_monthly_csv(filepath):
    """Load a monthly CSV file."""
    df = pd.read_csv(filepath)
    return df


def aggregate_to_quarters(df, id_cols):
    """Aggregate monthly data to quarterly data."""
    # Define quarter mapping
    quarter_map = {
        'JAN': 'Q1', 'FEB': 'Q1', 'MAR': 'Q1',
        'APR': 'Q2', 'MAY': 'Q2', 'JUN': 'Q2',
        'JUL': 'Q3', 'AUG': 'Q3', 'SEP': 'Q3',
        'OCT': 'Q4', 'NOV': 'Q4', 'DEC': 'Q4'
    }
    
    # Get month columns (excluding TOTAL)
    month_cols = [col for col in df.columns if col in ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']]
    
    # Create quarterly data
    quarterly_data = []
    
    for _, row in df.iterrows():
        for year in range(2021, 2026):
            year_data = {}
            year_data.update({col: row[col] for col in id_cols})
            year_data['Year'] = year
            
            # Aggregate months to quarters
            for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
                quarter_months = [month for month, q in quarter_map.items() if q == quarter and month in month_cols]
                if quarter_months:
                    quarter_total = sum(row[month] for month in quarter_months if pd.notna(row[month]))
                    year_data[quarter] = quarter_total
            
            quarterly_data.append(year_data)
    
    return pd.DataFrame(quarterly_data)


def melt_quarters(df, id_cols):
    """Convert quarterly data to long format."""
    quarter_cols = ['Q1', 'Q2', 'Q3', 'Q4']
    available_quarters = [col for col in quarter_cols if col in df.columns]
    
    if not available_quarters:
        return pd.DataFrame()
    
    long_df = df.melt(
        id_vars=id_cols + ['Year'],
        value_vars=available_quarters,
        var_name='Quarter',
        value_name='Registrations'
    )
    
    # Create Year-Quarter column
    long_df['Year_Quarter'] = long_df['Year'].astype(str) + '-' + long_df['Quarter']
    
    # Sort by group and year-quarter
    long_df = long_df.sort_values(id_cols + ['Year_Quarter'])
    
    return long_df


def compute_qoq(long_df, group_col):
    """Compute Quarter-over-Quarter percentage change."""
    long_df = long_df.copy()
    
    # Calculate QoQ percentage change
    long_df['QoQ_pct'] = (
        long_df.groupby(group_col)['Registrations']
        .pct_change()
        .multiply(100)
        .round(2)
    )
    
    return long_df


def process_monthly_data(monthly_data_dir):
    """Process all monthly data and create quarterly analysis."""
    processed_dir = os.path.join(os.path.dirname(monthly_data_dir), "processed")
    os.makedirs(processed_dir, exist_ok=True)
    
    # Process vehicle category data
    print("Processing vehicle category monthly data...")
    vc_quarterly_data = []
    
    for year in range(2021, 2026):
        vc_file = os.path.join(monthly_data_dir, f"{year}_monthly_VC.csv")
        if os.path.exists(vc_file):
            print(f"  Processing {year} vehicle category data...")
            vc_df = load_monthly_csv(vc_file)
            
            # Aggregate to quarters
            quarterly_df = aggregate_to_quarters(vc_df, ['S No', 'Vehicle Category'])
            vc_quarterly_data.append(quarterly_df)
    
    # Combine all years
    if vc_quarterly_data:
        vc_combined = pd.concat(vc_quarterly_data, ignore_index=True)
        
        # Map to vehicle groups (2W/3W/4W)
        group_map = {
            "2W": ["TWO WHEELER"],
            "3W": ["THREE WHEELER"],
            "4W": [
                "FOUR WHEELER", "LIGHT MOTOR VEHICLE", "MEDIUM MOTOR VEHICLE",
                "HEAVY MOTOR VEHICLE", "LIGHT PASSENGER VEHICLE", "MEDIUM PASSENGER VEHICLE",
                "HEAVY PASSENGER VEHICLE", "LIGHT GOODS VEHICLE", "MEDIUM GOODS VEHICLE", "HEAVY GOODS VEHICLE"
            ]
        }
        
        vc_grouped_data = []
        for group, keywords in group_map.items():
            mask = vc_combined["Vehicle Category"].str.contains("|".join(keywords), case=False, na=False)
            subset = vc_combined.loc[mask]
            if not subset.empty:
                subset = subset.copy()
                subset['Group'] = group
                vc_grouped_data.append(subset)
        
        if vc_grouped_data:
            vc_final = pd.concat(vc_grouped_data, ignore_index=True)
            
            # Convert to long format and calculate QoQ
            vc_long = melt_quarters(vc_final, ['Group'])
            vc_long = compute_qoq(vc_long, 'Group')
            
            # Save vehicle category quarterly data
            vc_output_path = os.path.join(processed_dir, "vehicle_category_quarterly_qoq.csv")
            vc_long.to_csv(vc_output_path, index=False)
            print(f"  Saved: {vc_output_path}")
    
    # Process manufacturer data
    print("Processing manufacturer monthly data...")
    maker_quarterly_data = []
    
    for year in range(2021, 2026):
        maker_file = os.path.join(monthly_data_dir, f"{year}_monthly_MAKER.csv")
        if os.path.exists(maker_file):
            print(f"  Processing {year} manufacturer data...")
            maker_df = load_monthly_csv(maker_file)
            
            # Aggregate to quarters
            quarterly_df = aggregate_to_quarters(maker_df, ['S No', 'Maker'])
            maker_quarterly_data.append(quarterly_df)
    
    # Combine all years
    if maker_quarterly_data:
        maker_combined = pd.concat(maker_quarterly_data, ignore_index=True)
        
        # Convert to long format and calculate QoQ
        maker_long = melt_quarters(maker_combined, ['Maker'])
        maker_long = compute_qoq(maker_long, 'Maker')
        
        # Save manufacturer quarterly data
        maker_output_path = os.path.join(processed_dir, "maker_quarterly_qoq.csv")
        maker_long.to_csv(maker_output_path, index=False)
        print(f"  Saved: {maker_output_path}")
    
    return {
        'vc_quarterly_path': os.path.join(processed_dir, "vehicle_category_quarterly_qoq.csv"),
        'maker_quarterly_path': os.path.join(processed_dir, "maker_quarterly_qoq.csv")
    }


def main():
    """Main function to process monthly data."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    monthly_data_dir = os.path.join(project_root, "data", "monthly")
    
    print("Processing monthly data for quarterly analysis...")
    outputs = process_monthly_data(monthly_data_dir)
    
    print("\nProcessing complete!")
    print("Output files:")
    for key, path in outputs.items():
        if os.path.exists(path):
            print(f"  - {path}")


if __name__ == "__main__":
    main() 