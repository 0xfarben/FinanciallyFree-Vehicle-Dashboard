import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Page configuration
st.set_page_config(
    page_title="Vehicle Registration Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    /* Custom tooltip styles */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 280px;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 10px 15px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -140px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 1rem;
        line-height: 1.5;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .tooltip .tooltiptext::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #333 transparent transparent transparent;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load processed data files."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(project_root, "data", "processed")
    
    # Load yearly data
    vc_data = pd.read_csv(os.path.join(data_dir, "vehicle_category_group_yoy.csv"))
    maker_data = pd.read_csv(os.path.join(data_dir, "maker_yoy.csv"))
    
    # Load quarterly data
    vc_qoq_data = pd.read_csv(os.path.join(data_dir, "vehicle_category_quarterly_qoq.csv"))
    maker_qoq_data = pd.read_csv(os.path.join(data_dir, "maker_quarterly_qoq.csv"))
    
    # Convert empty strings back to NaN for calculations
    vc_data['YoY_pct'] = pd.to_numeric(vc_data['YoY_pct'], errors='coerce')
    maker_data['YoY_pct'] = pd.to_numeric(maker_data['YoY_pct'], errors='coerce')
    vc_qoq_data['QoQ_pct'] = pd.to_numeric(vc_qoq_data['QoQ_pct'], errors='coerce')
    maker_qoq_data['QoQ_pct'] = pd.to_numeric(maker_qoq_data['QoQ_pct'], errors='coerce')
    
    return vc_data, maker_data, vc_qoq_data, maker_qoq_data

def main():
    # Header
    st.markdown('<h1 class="main-header">🚗 Vehicle 🏍️ Registration 🛺 Dashboard</h1>', unsafe_allow_html=True)
    
    # Add animated LED sign GIF
    # st.image("https://prodimages.everythingneon.com/350/l102-0938-auto-registration-animated-led-sign.gif", 
    #         width=200)
    
    # Load data
    vc_data, maker_data, vc_qoq_data, maker_qoq_data = load_data()
    
    # Sidebar filters
    st.sidebar.header("📊 Filters")
    
    # Year range filter
    years = sorted(vc_data['Year'].unique())
    selected_years = st.sidebar.multiselect(
        "Select Years:",
        years,
        default=years[-3:],  # Default to last 3 years
        help="Choose years to analyze"
    )
    
    # Vehicle category filter
    categories = sorted(vc_data['Group'].unique())
    selected_categories = st.sidebar.multiselect(
        "Vehicle Categories:",
        categories,
        default=categories,
        help="Select vehicle types to analyze"
    )
    
    # Manufacturer filter
    st.sidebar.subheader("🏭 Manufacturer Selection")
    
    # Top manufacturers by performance
    top_makers = maker_data.groupby('Maker')['Registrations'].sum().sort_values(ascending=False).head(20).index.tolist()
    
    # Simple manufacturer selection
    selected_makers = st.sidebar.multiselect(
        "Select Manufacturers:",
        top_makers,
        default=top_makers[:5] if len(top_makers) >= 5 else top_makers,
        help="Select manufacturers to analyze"
    )
    
    # Filter data based on selections
    if selected_years:
        vc_filtered = vc_data[vc_data['Year'].isin(selected_years)]
        maker_filtered = maker_data[maker_data['Year'].isin(selected_years)]
    else:
        vc_filtered = vc_data
        maker_filtered = maker_data
    
    if selected_categories:
        vc_filtered = vc_filtered[vc_filtered['Group'].isin(selected_categories)]
    
    if selected_makers:
        maker_filtered = maker_filtered[maker_filtered['Maker'].isin(selected_makers)]
    
    # Section 1: Overview & Key Metrics
    st.subheader("📊 Overview & Key Metrics")
    

    
    # Key metrics in a clean row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not vc_filtered.empty:
            total_reg = vc_filtered['Registrations'].sum()
            st.markdown(f"""
            <div style="
                background-color: #1f1f1f;
                padding: 1rem;
                border-radius: 0.5rem;
                border-left: 4px solid #1f77b4;
                text-align: center;
            ">
                <h4 style="color: #ffffff; margin: 0; font-size: 1rem;">
                    <span class="tooltip">📊 Total Registrations <span style="color: #1f77b4; font-size: 0.8rem; margin-left: 0.3rem;">ℹ️</span>
                        <span class="tooltiptext">Total Registrations shows the sum of all vehicle registrations across 2W, 3W, and 4W categories for the selected time period. This gives you a complete picture of market size and overall industry performance.</span>
                    </span>
                </h4>
                <h3 style="color: #1f77b4; margin: 0.5rem 0; font-size: 1.8rem; font-weight: bold;">{total_reg:,}</h3>
                <p style="color: #cccccc; margin: 0; font-size: 0.9rem;">Selected Period</p>
                <p style="color: #999999; margin: 0.2rem 0 0 0; font-size: 0.7rem; font-style: italic;">Sum of all vehicle types</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if not vc_filtered.empty:
            latest_year = vc_filtered['Year'].max()
            latest_data = vc_filtered[vc_filtered['Year'] == latest_year]
            if not latest_data.empty:
                best_performer = latest_data.loc[latest_data['YoY_pct'].idxmax()]
                st.markdown(f"""
                <div style="
                    background-color: #1f1f1f;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    border-left: 4px solid #28a745;
                    text-align: center;
                ">
                    <h4 style="color: #ffffff; margin: 0; font-size: 1rem;">
                        <span class="tooltip">🏆 Best Performer <span style="color: #28a745; font-size: 0.8rem; margin-left: 0.3rem;">ℹ️</span>
                            <span class="tooltiptext">Best Performer identifies the vehicle category (2W, 3W, or 4W) with the highest Year-over-Year growth rate. This helps identify the most promising sector for opportunities.</span>
                        </span>
                    </h4>
                    <h3 style="color: #28a745; margin: 0.5rem 0; font-size: 1.5rem; font-weight: bold;">{best_performer['Group']}</h3>
                    <p style="color: #cccccc; margin: 0; font-size: 0.9rem;">{best_performer['YoY_pct']:.1f}% YoY</p>
                    <p style="color: #999999; margin: 0.2rem 0 0 0; font-size: 0.7rem; font-style: italic;">Highest growth rate</p>
                </div>
                """, unsafe_allow_html=True)
    
    with col3:
        if not vc_filtered.empty:
            if not latest_data.empty:
                worst_performer = latest_data.loc[latest_data['YoY_pct'].idxmin()]
                st.markdown(f"""
                <div style="
                    background-color: #1f1f1f;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    border-left: 4px solid #dc3545;
                    text-align: center;
                ">
                                    <h4 style="color: #ffffff; margin: 0; font-size: 1rem;">
                                        <span class="tooltip">📉 Needs Attention <span style="color: #dc3545; font-size: 0.8rem; margin-left: 0.3rem;">ℹ️</span>
                                            <span class="tooltiptext">Needs Attention highlights the vehicle category with the lowest Year-over-Year growth rate. This helps identify potential risks and areas that may require attention.</span>
                                        </span>
                                    </h4>
                <h3 style="color: #dc3545; margin: 0.5rem 0; font-size: 1.5rem; font-weight: bold;">{worst_performer['Group']}</h3>
                <p style="color: #cccccc; margin: 0; font-size: 0.9rem;">{worst_performer['YoY_pct']:.1f}% YoY</p>
                <p style="color: #999999; margin: 0.2rem 0 0 0; font-size: 0.7rem; font-style: italic;">Lowest growth rate</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.write("")  # Add spacing
    
    # Section 2: Main Trends
    st.subheader("📈 Registration Trends")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Main trend chart
        fig_vc = px.line(
            vc_filtered,
            x='Year',
            y='Registrations',
            color='Group',
            title='Vehicle Registration Trends Over Time',
            labels={'Registrations': 'Total Registrations', 'Year': 'Year'},
            markers=True
        )
        fig_vc.update_layout(height=400)
        st.plotly_chart(fig_vc, use_container_width=True)
    
    with col2:
        # Latest year breakdown
        if not vc_filtered.empty:
            latest_year = vc_filtered['Year'].max()
            latest_data = vc_filtered[vc_filtered['Year'] == latest_year]
            
            for _, row in latest_data.iterrows():
                # Different colors for different vehicle types
                color_map = {'2W': '#1f77b4', '3W': '#ff7f0e', '4W': '#2ca02c'}
                card_color = color_map.get(row['Group'], '#1f77b4')
                
                # Create a container for each metric card
                with st.container():
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {card_color}15 0%, {card_color}08 100%); padding: 0.8rem; border-radius: 12px; margin: 0.1rem 0; border: 1px solid {card_color}30; box-shadow: 0 8px 25px rgba(0,0,0,0.15), 0 4px 10px rgba(0,0,0,0.1); position: relative; overflow: hidden; min-height: 80px; display: flex; flex-direction: column; justify-content: space-between;">
                        <div style="position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: linear-gradient(180deg, {card_color} 0%, {card_color}80 100%); border-radius: 2px;"></div>
                        <div style="display: flex; align-items: center; margin-bottom: 0.3rem; padding-left: 0.5rem;">
                            <span style="font-size: 1rem; margin-right: 0.4rem; color: {card_color};">🚗</span>
                            <h4 style="color: #ffffff; margin: 0; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">{row['Group']}</h4>
                        </div>
                        <h3 style="color: {card_color}; margin: 0.2rem 0; font-size: 1.2rem; font-weight: 800; text-shadow: 0 2px 4px rgba(0,0,0,0.3); padding-left: 0.5rem;">{row['Registrations']:,}</h3>
                        <div style="display: inline-block; margin-top: auto; padding: 0.2rem 0.5rem; background: rgba(255,255,255,0.1); border-radius: 12px; border: 1px solid rgba(255,255,255,0.2); margin-left: 0.5rem; align-self: flex-start;">
                            <span style="color: #ffffff; font-size: 0.6rem; font-weight: 500;">{latest_year}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Section 3: Growth Analysis
    st.subheader("📊 Growth Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # YoY growth chart
        if not vc_filtered.empty:
            fig_yoy_bars = px.bar(
                vc_filtered,
                x='Year',
                y='YoY_pct',
                color='Group',
                title='Year-over-Year [YoY] Growth by Vehicle Category',
                barmode='group',
                labels={'YoY_pct': 'YoY Growth (%)', 'Year': 'Year'},
                color_discrete_map={'2W': '#1f77b4', '3W': '#ff7f0e', '4W': '#2ca02c'}
            )
            fig_yoy_bars.update_layout(height=400, xaxis_tickangle=0)
            fig_yoy_bars.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
            st.plotly_chart(fig_yoy_bars, use_container_width=True)
    
    with col2:
            # QoQ growth chart
            if not vc_qoq_data.empty:
                # Filter QoQ data based on selections
                if selected_years:
                    vc_qoq_filtered = vc_qoq_data[vc_qoq_data['Year'].isin(selected_years)]
                else:
                    vc_qoq_filtered = vc_qoq_data
                
                if selected_categories:
                    vc_qoq_filtered = vc_qoq_filtered[vc_qoq_filtered['Group'].isin(selected_categories)]
                
                if not vc_qoq_filtered.empty:
                    fig_qoq_line = px.line(
                        vc_qoq_filtered,
                        x='Year_Quarter',
                        y='QoQ_pct',
                        color='Group',
                        title='Quarter-over-Quarter [QoQ] Growth Trends',
                        labels={'QoQ_pct': 'QoQ Growth (%)', 'Year_Quarter': 'Year-Quarter'},
                        markers=True,
                        color_discrete_map={'2W': '#1f77b4', '3W': '#ff7f0e', '4W': '#2ca02c'}
                    )
                    fig_qoq_line.update_layout(height=400, xaxis_tickangle=-45)
                    fig_qoq_line.update_traces(mode='lines+markers', marker_size=8)
                    st.plotly_chart(fig_qoq_line, use_container_width=True)
    
    # Section 4: Manufacturer Analysis
    st.subheader("🏭 Manufacturer Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top manufacturers
        if not maker_filtered.empty:
            top_makers_summary = maker_filtered.groupby('Maker')['Registrations'].sum().sort_values(ascending=False).head(10)
            fig_makers = px.bar(
                x=top_makers_summary.values,
                y=top_makers_summary.index,
                orientation='h',
                title='Top 10 Manufacturers by Total Registrations',
                labels={'x': 'Total Registrations', 'y': 'Manufacturer'}
            )
            fig_makers.update_layout(height=400)
            st.plotly_chart(fig_makers, use_container_width=True)
    
    with col2:
        # Manufacturer trends
        if not maker_filtered.empty:
            fig_maker_trends = px.line(
                maker_filtered,
                x='Year',
                y='Registrations',
                color='Maker',
                title='Manufacturer Registration Trends',
                labels={'Registrations': 'Total Registrations', 'Year': 'Year'}
            )
            fig_maker_trends.update_layout(height=400)
            st.plotly_chart(fig_maker_trends, use_container_width=True)
    
    # Section 5: Summary Visualizations
    st.subheader(f"📊 Summary Visualizations - {vc_filtered['Year'].max()}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top performing vehicle categories
        if not vc_filtered.empty:
            latest_year = vc_filtered['Year'].max()
            latest_vc = vc_filtered[vc_filtered['Year'] == latest_year]
            # Sort by registrations in descending order
            latest_vc_sorted = latest_vc.sort_values('Registrations', ascending=False)
            fig_top_vc = px.bar(
                latest_vc_sorted,
                x='Group',
                y='Registrations',
                title=f'{latest_year} Registrations by Vehicle Category',
                color='Group',
                text='Registrations',
                color_discrete_map={'2W': '#1f77b4', '3W': '#ff7f0e', '4W': '#2ca02c'}
            )
            fig_top_vc.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig_top_vc.update_layout(height=400)
            st.plotly_chart(fig_top_vc, use_container_width=True)
    
    with col2:
        # Top performing manufacturers
        if not maker_filtered.empty:
            latest_year = maker_filtered['Year'].max()
            latest_maker = maker_filtered[maker_filtered['Year'] == latest_year]
            top_10_makers = latest_maker.nlargest(10, 'Registrations')
            fig_top_makers = px.bar(
                top_10_makers,
                x='Registrations',
                y='Maker',
                orientation='h',
                title=f'Top 10 Manufacturers ({latest_year})',
                color='Registrations',
                color_continuous_scale='Blues'
            )
            fig_top_makers.update_layout(height=400)
            st.plotly_chart(fig_top_makers, use_container_width=True)
    
    # Section 6: Data Tables (Collapsible)
    with st.expander("📋 Detailed Data Tables", expanded=False):
        tab1, tab2, tab3, tab4 = st.tabs(["Vehicle Categories (YoY)", "Manufacturers (YoY)", "Vehicle Categories (QoQ)", "Manufacturers (QoQ)"])
        
        with tab1:
            st.dataframe(
                vc_filtered.sort_values(['Group', 'Year']),
                use_container_width=True,
                hide_index=True
            )
        
        with tab2:
            st.dataframe(
                maker_filtered.sort_values(['Maker', 'Year']),
                use_container_width=True,
                hide_index=True
            )
        
        with tab3:
            if 'vc_qoq_filtered' in locals() and not vc_qoq_filtered.empty:
                st.dataframe(
                    vc_qoq_filtered.sort_values(['Group', 'Year_Quarter']),
                    use_container_width=True,
                    hide_index=True
                )
        
        with tab4:
            if selected_makers and not maker_qoq_data.empty:
                maker_qoq_filtered = maker_qoq_data[maker_qoq_data['Maker'].isin(selected_makers)]
                if selected_years:
                    maker_qoq_filtered = maker_qoq_filtered[maker_qoq_filtered['Year'].isin(selected_years)]
                st.dataframe(
                    maker_qoq_filtered.sort_values(['Maker', 'Year_Quarter']),
                    use_container_width=True,
                    hide_index=True
                )

if __name__ == "__main__":
    main() 