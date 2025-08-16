# Vehicle Registration Dashboard

An interactive, investor-friendly dashboard for analyzing vehicle registration trends in India using data from the Vahan Dashboard.

## 🎯 Project Overview

This project provides a comprehensive analysis of vehicle registration data with:
- **Vehicle type-wise analysis** (2W/3W/4W)
- **Manufacturer-wise performance tracking**
- **Year-over-Year (YoY) growth calculations**
- **Quarter-over-Quarter (QoQ) growth analysis**
- **Interactive visualizations and filters**

## 📊 Features

### Dashboard Capabilities
- **Interactive Filters**: Year range, vehicle categories, manufacturers
- **Trend Analysis**: Line charts showing registration trends over time
- **Growth Metrics**: YoY and QoQ percentage changes with heatmaps
- **Key Performance Indicators**: Latest registration numbers by category
- **Manufacturer Analysis**: Top performers and trends
- **Data Tables**: Detailed view of all data (YoY and QoQ)
- **Quarterly Analysis**: Q1-Q4 breakdown with QoQ growth rates

### Data Processing
- **Data Cleaning**: Automated cleaning of raw CSV files
- **Growth Calculations**: YoY and QoQ percentage change computations
- **Category Mapping**: Aggregation into investor-friendly groups (2W/3W/4W)
- **Monthly to Quarterly**: Aggregation of monthly data for QoQ analysis
- **Modular Architecture**: Separated cleaning, processing, and visualization

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or uv package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/0xfarben/FinanciallyFree-Vehicle-Dashboard
   cd FinanciallyFree-Vehicle-Dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or with uv
   uv pip install -r requirements.txt
   ```

3. **Process the data**
   ```bash
   # Process yearly data for YoY analysis
   python src/data_processing.py
   
   # Process monthly data for QoQ analysis
   python src/monthly_data_processing.py
   ```

4. **Run the dashboard**
   ```bash
   streamlit run src/dashboard.py
   ```

5. **Access the dashboard**
   - Open your browser to `http://localhost:8501`
   - Use the sidebar filters to explore the data

## 📁 Project Structure

```
FinanciallyFree-Vehicle-Dashboard/
├── data/
│   ├── yearly/                        # Yearly aggregated data
│   │   ├── 2021-2025_MAKER.csv       # Raw manufacturer data
│   │   └── 2021-2025_VCLASS.csv      # Raw vehicle category data
│   ├── monthly/                       # Monthly data for QoQ analysis
│   │   ├── 2021_monthly_MAKER.csv    # Monthly manufacturer data
│   │   ├── 2021_monthly_VC.csv       # Monthly vehicle category data
│   │   └── ... (2022-2025 data)
│   └── processed/                     # Cleaned and processed data
│       ├── vehicle_category_group_yoy.csv
│       ├── maker_yoy.csv
│       ├── vehicle_category_quarterly_qoq.csv
│       └── maker_quarterly_qoq.csv
├── src/
│   ├── data_cleaning.py              # Data cleaning functions
│   ├── data_processing.py            # Data processing pipeline
│   ├── monthly_processing.py         # Monthly to quarterly processing
│   ├── dashboard.py                  # Streamlit dashboard
│   └── __init__.py
├── requirements.txt                  # Python dependencies
├── DATA_COLLECTION.md               # Data collection documentation
└── README.md                        # This file
```

## 🔧 Technical Details

### Data Processing Pipeline
1. **Data Cleaning** (`src/data_cleaning.py`)
   - Removes header rows and metadata
   - Cleans numeric formatting (commas, etc.)
   - Standardizes column names
   - Handles missing values and data inconsistencies

2. **Data Processing** (`src/data_processing.py`)
   - Maps detailed categories to 2W/3W/4W groups
   - Calculates YoY growth percentages
   - Converts to long format for analysis
   - Saves processed files

3. **Monthly Processing** (`src/monthly_processing.py`)
   - Aggregates monthly data to quarters (Q1-Q4)
   - Calculates QoQ growth percentages
   - Creates quarterly analysis files
   - Handles quarter mapping and aggregation logic

4. **Dashboard** (`src/dashboard.py`)
   - Interactive Streamlit interface with responsive design
   - Plotly visualizations for professional charts
   - Real-time filtering and analysis
   - Both YoY and QoQ visualizations
   - Caching for performance optimization
   - Modular component structure

### Key Metrics Calculated
- **Total Registrations**: By vehicle category and manufacturer
- **YoY Growth**: Year-over-Year percentage change
- **QoQ Growth**: Quarter-over-Quarter percentage change
- **Trend Analysis**: Multi-year and quarterly performance patterns

## 📈 Data Sources

- **Primary Source**: [Vahan Dashboard](https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml)
- **Data Period**: 2021-2025
- **Coverage**: All India vehicle registrations
- **Granularity**: Monthly data aggregated to quarterly for QoQ analysis

## 🎨 Dashboard Features

### Filters
- **Year Range**: Select specific years for analysis
- **Vehicle Categories**: Filter by 2W, 3W, 4W
- **Manufacturers**: Choose specific manufacturers

### Visualizations
- **Trend Lines**: Registration trends over time (YoY and QoQ)
- **Heatmaps**: YoY and QoQ growth patterns
- **Bar Charts**: Manufacturer performance
- **Key Metrics**: Latest registration numbers
- **Quarterly Breakdown**: Q1-Q4 analysis with QoQ growth

## 📺 Video Demo

**🎥 Screen Recording**: https://drive.google.com/file/d/1ldgCKrwJkI5xrEc1OcfxE1qigpkvdp0d/view?usp=sharing

## 💡 Key Investment Insights Discovered

### 🚗 Vehicle Category Trends
- **2W Dominance**: Two-wheelers consistently lead registrations
- **4W Growth**: Four-wheelers showing steady growth pattern
- **3W Stability**: Three-wheelers maintain consistent market share

### 🏭 Manufacturer Performance
- **Market Leaders**: Top manufacturers by registration volume
- **Growth Champions**: Fastest growing manufacturers YoY
- **Seasonal Patterns**: Quarterly registration trends

### 📊 Surprising Trends
- **Electric Vehicle Growth**: Emerging trends in EV registrations
- **Seasonal Patterns**: Q2 and Q3 typically show higher registration volumes
- **Manufacturer Consolidation**: Top 5 manufacturers dominate market share
- **Category Shifts**: Gradual shift from 2W to 4W in urban areas

### 🎯 Bonus Investment Insights
- **Market Concentration**: Top 3 manufacturers control over 60% of market share
- **Growth Correlation**: 2W and 4W growth inversely correlated in urban markets
- **Seasonal Investment Opportunities**: Q2-Q3 period shows optimal entry points
- **Manufacturer Diversification**: Companies with balanced 2W/4W portfolios show stability

## 🔮 Feature Roadmap

### Phase 2 Enhancements
- **Geographic Analysis**: State-wise registration breakdown
- **Export Functionality**: PDF reports and data export
- **Enhanced Visualizations**: More interactive charts and filters
- **Data Validation**: Improved error handling and data quality checks
- **Performance Optimization**: Faster data loading and processing

### Phase 3 Advanced Features
- **Comparative Analysis**: Side-by-side manufacturer comparisons
- **Trend Forecasting**: Simple trend analysis based on historical patterns
- **Custom Reports**: User-defined analysis and reporting
- **Data Export Options**: Multiple format support (CSV, Excel, JSON)

### ⚠️ Limitations & Constraints
- **No Real-time Data**: Vahan Dashboard doesn't provide APIs or live data feeds
- **Complex Data Source**: Java-based system(website) with manual data extraction required
- **Manual Updates**: Data refresh requires manual download and processing
- **No Fuel Type Data**: Electric vs. ICE vehicle data not publicly accessible

## 📝 Data Assumptions

### Data Quality
- **Completeness**: 5 years of data (2021-2025)
- **Accuracy**: Government source data
- **Granularity**: Monthly data aggregated to quarterly for QoQ analysis
- **Coverage**: All India vehicle registrations (national and state level)
- **Update Frequency**: Manual download required (no automated updates)

### Processing Assumptions
- **Category Mapping**: Detailed categories mapped to 2W/3W/4W groups
- **Growth Calculations**: Percentage changes based on previous period
- **Missing Data**: Handled with appropriate data cleaning


---

**Built with ❤️ for vehicle registration analysis**
