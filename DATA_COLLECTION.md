# Data Collection Documentation

## Overview
This project analyzes vehicle registration data from the Vahan Dashboard (https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml).

## Data Collection Process

### 1. Data Source
- **Website**: Vahan Dashboard - Government of India's vehicle registration portal
- **Data Type**: Public vehicle registration statistics
- **Time Period**: 2021-2025 (5 years of data)
- **Granularity**: Monthly data available for quarterly analysis

### 2. Data Categories Collected

#### Vehicle Category Data
- **Yearly Files**: `data/yearly/2021-2025_VCLASS.csv`
- **Monthly Files**: `data/monthly/2021_monthly_VC.csv` through `2025_monthly_VC.csv`
- **Content**: Vehicle type-wise registration data
- **Categories**: 
  - TWO WHEELER (2W)
  - THREE WHEELER (3W) 
  - FOUR WHEELER (4W)
  - And other detailed categories

#### Manufacturer Data
- **Yearly Files**: `data/yearly/2021-2025_MAKER.csv`
- **Monthly Files**: `data/monthly/2021_monthly_MAKER.csv` through `2025_monthly_MAKER.csv`
- **Content**: Manufacturer-wise registration data
- **Scope**: All manufacturers with registration data

### 3. Collection Method
1. **Manual Download**: Data was downloaded as Excel files from the dashboard
2. **Format Conversion**: Excel files converted to CSV for processing
3. **Data Cleaning**: Removed headers, cleaned formatting, standardized column names
4. **Monthly Aggregation**: Monthly data processed for quarterly (QoQ) analysis

### 4. Data Collection Challenges
- **No API Access**: Vahan Dashboard is a Java-based web application without public APIs
- **Complex Interface**: Dashboard has complex navigation and data loading mechanisms
- **Manual Process**: Each data update requires manual navigation and download
- **Format Inconsistencies**: Data structure may change between updates
- **Limited Granularity**: Only national-level data available, no state-wise breakdown

### 4. Data Structure
- **Time Series**: Yearly data from 2021 to 2025
- **Monthly Data**: Available for quarterly aggregation
- **Format**: Wide format with years/months as columns
- **Processing**: Converted to long format for analysis

### 5. Data Processing Pipeline
- **Yearly Analysis**: Direct YoY calculations from yearly data
- **Quarterly Analysis**: Monthly data aggregated to quarters (Q1-Q4)
- **QoQ Calculations**: Quarter-over-Quarter percentage changes
- **Output Files**: Both YoY and QoQ processed data available

### 6. Data Quality
- **Completeness**: 5 years of data available (2021-2025)
- **Accuracy**: Government source data
- **Granularity**: Both yearly and monthly data available
- **QoQ Analysis**: Enabled through monthly data aggregation

## Files Structure

### Raw Data
- `data/yearly/2021-2025_MAKER.csv` - Raw manufacturer data
- `data/yearly/2021-2025_VCLASS.csv` - Raw vehicle category data
- `data/monthly/` - Monthly data files for quarterly analysis

### Processed Data
- `data/processed/vehicle_category_group_yoy.csv` - Vehicle category YoY data
- `data/processed/maker_yoy.csv` - Manufacturer YoY data
- `data/processed/vehicle_category_quarterly_qoq.csv` - Vehicle category QoQ data
- `data/processed/maker_quarterly_qoq.csv` - Manufacturer QoQ data

## Key Features Enabled

### YoY Analysis
- Year-over-Year growth calculations
- Vehicle category performance trends
- Manufacturer growth patterns

### QoQ Analysis
- Quarter-over-Quarter growth calculations
- Seasonal trend identification
- Monthly data aggregation to quarters
- Enhanced granularity for trend analysis

## Data Processing Scripts

### Monthly Processing
- `src/monthly_processing.py` - Converts monthly data to quarterly format
- Aggregates months to quarters (Q1, Q2, Q3, Q4)
- Calculates QoQ percentage changes
- Creates quarterly analysis files

### Data Processing
- `src/data_processing.py` - Processes yearly data for YoY analysis
- `src/data_cleaning.py` - Cleans and standardizes raw data

## Limitations and Considerations

### Data Availability
- **Real-time**: Data is static (2021-2025)
- **Geographic**: National-level data only
- **Categories**: Limited to available vehicle classifications

### Processing Considerations
- **Monthly Aggregation**: QoQ analysis depends on monthly data availability
- **Data Consistency**: Government data format may vary over time
- **Missing Values**: Handled through data cleaning processes
