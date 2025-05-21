# This is Team No. 21016-1 submission for TSA Nationals 2025 Software Development. The website is https://ecoimpactnationalstsa2025.replit.app

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from utils import get_color_scale, display_metric_card, animated_progress_bar
from data_processor import load_data, filter_data_by_date, calculate_statistics, calculate_resource_efficiency
from recommendation_engine import generate_recommendations, calculate_potential_savings, calculate_environmental_impact
from eco_impact import calculate_regional_comparison, get_eco_impact_score, get_impact_recommendations, get_all_regions
import db

st.set_page_config(
    page_title="Agricultural Sustainability Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'data' not in st.session_state:
    st.session_state.data = load_data()

st.markdown("""
<div style="background-color:#e8f5e9; padding:10px; border-radius:10px; margin-bottom:10px">
    <h1 style="color:#2e7d32; text-align:center">Agricultural Sustainability Dashboard</h1>
    <p style="color:#444; text-align:center; font-size:18px">Track environmental metrics and optimize resource usage for sustainable farming</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="text-align:center; background-color:#2e7d32; padding:5px; border-radius:5px; margin-bottom:10px">
    <h3 style="color:white">Dashboard Controls</h3>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### Date Range")
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

col1, col2 = st.sidebar.columns(2)
with col1:
    selected_start_date = st.date_input("Start Date", start_date)
with col2:
    selected_end_date = st.date_input("End Date", end_date)

if selected_start_date > selected_end_date:
    st.sidebar.error("Error: End date must be after start date.")
    selected_start_date = start_date
    selected_end_date = end_date

quick_filters = st.sidebar.radio(
    "Quick Filter",
    ["Last 30 days", "Last 7 days", "Last 3 months", "All time"],
    horizontal=True
)

if quick_filters == "Last 7 days":
    selected_start_date = end_date - timedelta(days=7)
    selected_end_date = end_date
elif quick_filters == "Last 3 months":
    selected_start_date = end_date - timedelta(days=90)
    selected_end_date = end_date
elif quick_filters == "All time":
    selected_start_date = end_date - timedelta(days=365)
    selected_end_date = end_date
    
st.sidebar.markdown("---")
st.sidebar.markdown("### Region Selection")
selected_region = st.sidebar.selectbox(
    "Select Region for Eco-Impact Comparison", 
    get_all_regions(), 
    index=0,
    help="Choose a region to compare your resource usage against regional averages"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Add New Measurements")

with st.sidebar.form("new_measurements_form"):
    st.markdown("<p style='text-align:center; color:#2e7d32; font-weight:bold'>Enter today's environmental measurements</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        new_temperature = st.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0, value=22.0, step=0.1)
        new_humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0, step=0.1)
        new_soil_moisture = st.number_input("Soil Moisture (%)", min_value=0.0, max_value=100.0, value=70.0, step=0.1)
    
    with col2:
        new_water_usage = st.number_input("Water Usage (L)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
        new_energy_consumption = st.number_input("Energy Consumption (kWh)", min_value=0.0, max_value=100.0, value=15.0, step=0.1)
    
    submit_button = st.form_submit_button("Submit Measurements", use_container_width=True)
    
    if submit_button:
        success = db.add_metrics_record(
            temperature=new_temperature,
            humidity=new_humidity,
            soil_moisture=new_soil_moisture,
            water_usage=new_water_usage,
            energy_consumption=new_energy_consumption
        )
        
        if success:
            st.session_state.data = load_data()
            st.success("Measurements added successfully!")
            st.rerun()
        else:
            st.error("Failed to add measurements. Please try again.")

filtered_data = filter_data_by_date(st.session_state.data, selected_start_date, selected_end_date)
stats = calculate_statistics(filtered_data)

st.markdown("""
<div style="background-color:#e8f5e9; padding:10px; border-radius:10px; margin-bottom:10px; border-left:5px solid #2e7d32">
    <h2 style="color:#2e7d32; text-align:center">Current Environmental Metrics</h2>
    <p style="font-size:14px; text-align:center">Latest measurements for key environmental parameters</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    display_metric_card(
        "Temperature", 
        f"{stats['current_temp']:.1f}°C", 
        f"{stats['temp_change']:+.1f}°C from average",
        stats['temp_status']
    )

with col2:
    display_metric_card(
        "Humidity", 
        f"{stats['current_humidity']:.1f}%", 
        f"{stats['humidity_change']:+.1f}% from average",
        stats['humidity_status']
    )

with col3:
    display_metric_card(
        "Soil Moisture", 
        f"{stats['current_soil_moisture']:.1f}%", 
        f"{stats['soil_moisture_change']:+.1f}% from average",
        stats['soil_moisture_status']
    )

st.markdown("""
<div style="background-color:#e8f5e9; padding:10px; border-radius:10px; margin-bottom:10px; border-left:5px solid #2e7d32">
    <h2 style="color:#2e7d32; text-align:center">Data Visualization</h2>
    <p style="font-size:14px; text-align:center">Interactive charts to explore environmental metrics and their relationships</p>
</div>
""", unsafe_allow_html=True)

tab_labels = ["Time Series", "Correlations", "Resource Usage"]
tab1, tab2, tab3 = st.tabs(tab_labels)

with tab1:
    st.subheader("Environmental Metrics Over Time")
    
    metrics = st.multiselect(
        "Select metrics to display",
        ["Temperature", "Humidity", "Soil Moisture", "Water Usage", "Energy Consumption"],
        default=["Temperature", "Humidity", "Soil Moisture"]
    )
    
    if metrics:
        fig = go.Figure()
        
        if "Temperature" in metrics:
            fig.add_trace(go.Scatter(
                x=filtered_data['date'], 
                y=filtered_data['temperature'], 
                mode='lines+markers',
                name='Temperature (°C)'
            ))
            
        if "Humidity" in metrics:
            fig.add_trace(go.Scatter(
                x=filtered_data['date'], 
                y=filtered_data['humidity'], 
                mode='lines+markers',
                name='Humidity (%)'
            ))
            
        if "Soil Moisture" in metrics:
            fig.add_trace(go.Scatter(
                x=filtered_data['date'], 
                y=filtered_data['soil_moisture'], 
                mode='lines+markers',
                name='Soil Moisture (%)'
            ))
            
        if "Water Usage" in metrics:
            fig.add_trace(go.Scatter(
                x=filtered_data['date'], 
                y=filtered_data['water_usage'], 
                mode='lines+markers',
                name='Water Usage (L)'
            ))
            
        if "Energy Consumption" in metrics:
            fig.add_trace(go.Scatter(
                x=filtered_data['date'], 
                y=filtered_data['energy_consumption'], 
                mode='lines+markers',
                name='Energy (kWh)'
            ))
        
        fig.update_layout(
            height=500,
            xaxis_title='Date',
            yaxis_title='Value',
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please select at least one metric to display")

with tab2:
    st.subheader("Correlation Between Metrics")
    
    x_axis = st.selectbox(
        "X-axis",
        ["Temperature", "Humidity", "Soil Moisture", "Water Usage", "Energy Consumption"],
        index=0
    )
    
    y_axis = st.selectbox(
        "Y-axis",
        ["Temperature", "Humidity", "Soil Moisture", "Water Usage", "Energy Consumption"],
        index=1
    )
    
    metric_to_column = {
        "Temperature": "temperature",
        "Humidity": "humidity",
        "Soil Moisture": "soil_moisture",
        "Water Usage": "water_usage",
        "Energy Consumption": "energy_consumption"
    }
    
    if x_axis != y_axis:
        fig = px.scatter(
            filtered_data,
            x=metric_to_column[x_axis],
            y=metric_to_column[y_axis],
            trendline="ols",
            labels={
                metric_to_column[x_axis]: x_axis,
                metric_to_column[y_axis]: y_axis
            }
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        correlation = filtered_data[metric_to_column[x_axis]].corr(filtered_data[metric_to_column[y_axis]])
        st.info(f"Correlation coefficient: {correlation:.3f}")
        
        if abs(correlation) > 0.7:
            st.success(f"Strong correlation detected between {x_axis} and {y_axis}.")
        elif abs(correlation) > 0.3:
            st.info(f"Moderate correlation detected between {x_axis} and {y_axis}.")
        else:
            st.warning(f"Weak correlation detected between {x_axis} and {y_axis}.")
    else:
        st.warning("Please select different metrics for X and Y axes.")

with tab3:
    st.subheader("Resource Usage Analysis")
    
    resource_fig = go.Figure()
    
    resource_fig.add_trace(go.Bar(
        x=filtered_data['date'],
        y=filtered_data['water_usage'],
        name='Water Usage (L)',
        marker_color='blue'
    ))
    
    resource_fig.add_trace(go.Bar(
        x=filtered_data['date'],
        y=filtered_data['energy_consumption'],
        name='Energy (kWh)',
        marker_color='orange',
        yaxis='y2'
    ))
    
    resource_fig.update_layout(
        height=500,
        xaxis_title='Date',
        yaxis_title='Water Usage (L)',
        yaxis2=dict(
            title='Energy (kWh)',
            overlaying='y',
            side='right'
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(resource_fig, use_container_width=True)
    
    total_water = filtered_data['water_usage'].sum()
    total_energy = filtered_data['energy_consumption'].sum()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Water Usage", f"{total_water:.1f} L")
    
    with col2:
        st.metric("Total Energy Consumption", f"{total_energy:.1f} kWh")

st.markdown("""
<div style="background-color:#e8f5e9; padding:10px; border-radius:10px; margin-bottom:10px; border-left:5px solid #2e7d32">
    <h2 style="color:#2e7d32; text-align:center">Resource Efficiency Metrics</h2>
    <p style="font-size:14px; text-align:center">Animated progress bars showing water and energy efficiency relative to optimal targets</p>
</div>
""", unsafe_allow_html=True)

efficiency = calculate_resource_efficiency(filtered_data)
eff_col1, eff_col2 = st.columns(2)

with eff_col1:
    st.subheader("Water Usage Efficiency")
    animated_progress_bar(
        value=efficiency['current_water_usage'],
        target=efficiency['optimal_water_usage'],
        title="Current vs. Optimal Water Usage",
        unit="L",
        speed=0.01,
        color="#4CAF50"
    )
    
    st.markdown(f"""
    **Efficiency Score:** {efficiency['water_usage_efficiency_percent']:.1f}%
    
    **Target:** Reduce water usage to {efficiency['optimal_water_usage']:.1f}L or less while maintaining soil moisture.
    """)
    
    st.progress(min(1.0, 1.0 / efficiency['water_efficiency_vs_baseline']))
    st.caption(f"Performance vs. Industry Baseline: {100/efficiency['water_efficiency_vs_baseline']:.1f}% " + 
              ("(Better than baseline)" if efficiency['water_efficiency_vs_baseline'] < 1.0 else "(Needs improvement)"))

with eff_col2:
    st.subheader("Energy Consumption Efficiency")
    animated_progress_bar(
        value=efficiency['current_energy_consumption'],
        target=efficiency['optimal_energy_consumption'],
        title="Current vs. Optimal Energy Usage",
        unit="kWh",
        speed=0.01,
        color="#388E3C"
    )
    
    st.markdown(f"""
    **Efficiency Score:** {efficiency['energy_consumption_efficiency_percent']:.1f}%
    
    **Target:** Reduce energy consumption to {efficiency['optimal_energy_consumption']:.1f}kWh or less.
    """)
    
    st.progress(min(1.0, 1.0 / efficiency['energy_efficiency_vs_baseline']))
    st.caption(f"Performance vs. Industry Baseline: {100/efficiency['energy_efficiency_vs_baseline']:.1f}% " + 
              ("(Better than baseline)" if efficiency['energy_efficiency_vs_baseline'] < 1.0 else "(Needs improvement)"))

st.subheader("Overall Resource Efficiency Score")
score_color = "#2e7d32" if efficiency['overall_score'] >= 80 else "#4CAF50" if efficiency['overall_score'] >= 60 else "#81C784"
st.markdown(f"<h1 style='text-align: center; color: {score_color};'>{efficiency['overall_score']:.1f}%</h1>", unsafe_allow_html=True)

st.markdown("""
<div style="background-color:#e8f5e9; padding:10px; border-radius:10px; margin-bottom:10px; border-left:5px solid #2e7d32">
    <h2 style="color:#2e7d32; text-align:center">Resource Optimization Recommendations</h2>
    <p style="font-size:14px; text-align:center">Personalized recommendations to improve resource efficiency and sustainability</p>
</div>
""", unsafe_allow_html=True)

recommendations = generate_recommendations(filtered_data, stats)
savings = calculate_potential_savings(filtered_data)
col1, col2 = st.columns([2, 1])

with col1:
    for i, rec in enumerate(recommendations):
        priority_color = "#2e7d32" if rec['priority'] == "High" else "#4CAF50" if rec['priority'] == "Medium" else "#81C784"
        
        with st.container():
            st.markdown(f"""
            <div style="background-color:#e8f5e9; padding:10px; border-radius:10px; margin-bottom:10px; border:1px solid #c8e6c9">
                <div style="display:flex; justify-content:space-between; align-items:center">
                    <h4 style="color:#2e7d32; margin:0">{i+1}. {rec['title']}</h4>
                    <span style="background-color:{priority_color}; color:white; padding:3px 8px; border-radius:10px; font-size:12px">{rec['priority']} Priority</span>
                </div>
                <p style="margin-top:10px">{rec['description']}</p>
                <p style="font-style:italic; color:#555; margin-bottom:0"><strong>Expected impact:</strong> {rec['impact']}</p>
            </div>
            """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color:#e8f5e9; padding:10px; border-radius:10px; text-align:center; margin-bottom:10px">
        <h4 style="color:#2e7d32; margin-top:0">Potential Resource Savings</h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background-color:rgba(76, 175, 80, 0.1); padding:10px; border-radius:10px; margin-bottom:10px">
        <p style="font-size:14px; margin-bottom:0">Water Savings</p>
        <h3 style="margin:0; color:#4CAF50">{savings['water_savings']:.1f} L</h3>
        <p style="color:#2e7d32; margin:0">+{savings['water_savings_percent']:.1f}%</p>
        <p style="font-size:12px; color:#666; margin-top:5px">Estimated savings based on optimization</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background-color:rgba(76, 175, 80, 0.1); padding:10px; border-radius:10px; margin-bottom:10px">
        <p style="font-size:14px; margin-bottom:0">Energy Savings</p>
        <h3 style="margin:0; color:#4CAF50">{savings['energy_savings']:.1f} kWh</h3>
        <p style="color:#2e7d32; margin:0">+{savings['energy_savings_percent']:.1f}%</p>
        <p style="font-size:12px; color:#666; margin-top:5px">Estimated savings based on optimization</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background-color:rgba(76, 175, 80, 0.1); padding:10px; border-radius:10px; margin-bottom:10px">
        <p style="font-size:14px; margin-bottom:0">Cost Savings</p>
        <h3 style="margin:0; color:#4CAF50">${savings['cost_savings']:.2f}</h3>
        <p style="font-size:12px; color:#666; margin-top:5px">Estimated monthly cost reduction</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="background-color:#e8f5e9; padding:10px; border-radius:10px; margin-bottom:10px; border-left:5px solid #2e7d32">
    <h2 style="color:#2e7d32; text-align:center">Environmental Impact</h2>
    <p style="font-size:14px; text-align:center">Calculated impact of your agricultural operations on the environment</p>
</div>
""", unsafe_allow_html=True)

impact = calculate_environmental_impact(filtered_data, savings)

st.container().markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

carbon_score_color = "#2e7d32" if impact['carbon_reduction_percent'] > 10 else "#4CAF50" if impact['carbon_reduction_percent'] > 5 else "#81C784"
water_score_color = "#2e7d32" if impact['water_conservation_percent'] > 15 else "#4CAF50" if impact['water_conservation_percent'] > 7 else "#81C784"
sustain_score_color = "#2e7d32" if impact['sustainability_score'] > 80 else "#4CAF50" if impact['sustainability_score'] > 60 else "#81C784"

with col1:
    st.markdown(f"""
    <div style="background-color:rgba(76, 175, 80, 0.1); border:1px solid #c8e6c9; padding:10px; border-radius:10px; text-align:center; height:150px; display:flex; flex-direction:column; justify-content:space-between;">
        <div>
            <h4 style="color:#2e7d32; margin:5px 0">Carbon Footprint</h4>
        </div>
        <div>
            <h2 style="color:{carbon_score_color}; margin:5px 0">{impact['carbon_reduction']:.1f} kg</h2>
            <span style="color:#2e7d32;">↓ {impact['carbon_reduction_percent']:.1f}%</span>
        </div>
        <div>
            <p style="color:#666; font-size:12px; margin:5px 0">Reduction from recommendations</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background-color:rgba(76, 175, 80, 0.1); border:1px solid #c8e6c9; padding:10px; border-radius:10px; text-align:center; height:150px; display:flex; flex-direction:column; justify-content:space-between;">
        <div>
            <h4 style="color:#2e7d32; margin:5px 0">Water Conservation</h4>
        </div>
        <div>
            <h2 style="color:{water_score_color}; margin:5px 0">{impact['water_conservation']:.1f} L</h2>
            <span style="color:#2e7d32;">↓ {impact['water_conservation_percent']:.1f}%</span>
        </div>
        <div>
            <p style="color:#666; font-size:12px; margin:5px 0">Water savings from optimization</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background-color:rgba(76, 175, 80, 0.1); border:1px solid #c8e6c9; padding:10px; border-radius:10px; text-align:center; height:150px; display:flex; flex-direction:column; justify-content:space-between;">
        <div>
            <h4 style="color:#2e7d32; margin:5px 0">Sustainability Score</h4>
        </div>
        <div>
            <h2 style="color:{sustain_score_color}; margin:5px 0">{impact['sustainability_score']}/100</h2>
            <span style="color:{'#2e7d32' if impact['sustainability_score_change'] > 0 else '#c62828'};">{impact['sustainability_score_change']:+.1f} points</span>
        </div>
        <div>
            <p style="color:#666; font-size:12px; margin:5px 0">Overall sustainability rating</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div style="background-color:#e8f5e9; padding:10px; border-radius:10px; margin-bottom:10px; border-left:5px solid #2e7d32">
    <h2 style="color:#2e7d32; text-align:center">Location-based Eco-Impact Comparison</h2>
    <p style="font-size:14px; text-align:center">Comparing your resource usage with regional averages in the {selected_region} region</p>
</div>
""", unsafe_allow_html=True)

# Add spacing between sections
st.container().markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)

regional_comparison = calculate_regional_comparison(filtered_data, selected_region)
eco_impact_score = get_eco_impact_score(regional_comparison)

st.markdown(f"""
<div style="background-color:#e8f5e9; padding:10px; border-radius:10px; margin-bottom:20px">
    <h3 style="color:#2e7d32; text-align:center">Comparison with {regional_comparison['region_name']} Region</h3>
</div>
"""
, unsafe_allow_html=True)
st.markdown(f"""
Regional climate: Average temperature {regional_comparison['region_avg_temp']}°C, 
Humidity {regional_comparison['region_avg_humidity']}%, 
Annual rainfall {regional_comparison['region_avg_rainfall']} mm
""")

comp_col1, comp_col2, comp_col3 = st.columns(3)

with comp_col1:
    water_diff_color = "green" if regional_comparison["water_usage_diff_percent"] <= 0 else "red"
    water_diff_text = f"-{abs(regional_comparison['water_usage_diff_percent']):.1f}%" if regional_comparison["water_usage_diff_percent"] <= 0 else f"+{regional_comparison['water_usage_diff_percent']:.1f}%"
    
    st.metric(
        "Water Usage vs Region",
        f"{regional_comparison['water_usage_current']:.1f} L",
        water_diff_text,
        delta_color="normal" if regional_comparison["water_usage_diff_percent"] <= 0 else "inverse"
    )

with comp_col2:
    energy_diff_color = "green" if regional_comparison["energy_consumption_diff_percent"] <= 0 else "red"
    energy_diff_text = f"-{abs(regional_comparison['energy_consumption_diff_percent']):.1f}%" if regional_comparison["energy_consumption_diff_percent"] <= 0 else f"+{regional_comparison['energy_consumption_diff_percent']:.1f}%"
    
    st.metric(
        "Energy Usage vs Region",
        f"{regional_comparison['energy_consumption_current']:.1f} kWh",
        energy_diff_text,
        delta_color="normal" if regional_comparison["energy_consumption_diff_percent"] <= 0 else "inverse"
    )

with comp_col3:
    carbon_diff_color = "green" if regional_comparison["carbon_footprint_diff_percent"] <= 0 else "red"
    carbon_diff_text = f"-{abs(regional_comparison['carbon_footprint_diff_percent']):.1f}%" if regional_comparison["carbon_footprint_diff_percent"] <= 0 else f"+{regional_comparison['carbon_footprint_diff_percent']:.1f}%"
    
    st.metric(
        "Carbon Footprint vs Region",
        f"{regional_comparison['estimated_carbon_footprint']:.1f} kg CO₂",
        carbon_diff_text,
        delta_color="normal" if regional_comparison["carbon_footprint_diff_percent"] <= 0 else "inverse"
    )

st.subheader("Regional Eco-Impact Score")
score_color = "#2e7d32" if eco_impact_score["total_score"] >= 80 else "#4CAF50" if eco_impact_score["total_score"] >= 60 else "#81C784"
st.markdown(f"<h1 style='text-align: center; color: {score_color};'>{eco_impact_score['total_score']:.1f}/100</h1>", unsafe_allow_html=True)

score_col1, score_col2, score_col3 = st.columns(3)

with score_col1:
    st.markdown("##### Water Impact")
    st.progress(eco_impact_score["water_impact_score"] / 35)
    st.text(f"{eco_impact_score['water_impact_score']:.1f}/35")

with score_col2:
    st.markdown("##### Energy Impact")
    st.progress(eco_impact_score["energy_impact_score"] / 35)
    st.text(f"{eco_impact_score['energy_impact_score']:.1f}/35")

with score_col3:
    st.markdown("##### Carbon Impact")
    st.progress(eco_impact_score["carbon_impact_score"] / 30)
    st.text(f"{eco_impact_score['carbon_impact_score']:.1f}/30")
recommendations = get_impact_recommendations(regional_comparison)

with st.expander("View Regional Eco-Impact Recommendations"):
    for i, rec in enumerate(recommendations):
        st.markdown(f"**{rec['category']} ({rec['priority']} Priority)**")
        st.markdown(rec["recommendation"])
        if i < len(recommendations) - 1:
            st.markdown("---")

st.markdown("---")
st.markdown("### About This Dashboard")
st.markdown("""
It tracks environmental data such as temperature, humidity, soil
water use, and energy use to allow farmers to make
sustainable choices. The user can enter everyday measurements, see
trends, assess efficiency scores, and get individual recommendations
to maximize resources and decrease environmental footprint.
""")


st.markdown("---")
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("### Data Source")
    if db.check_connection():
        st.success(" Connected to SQLite database")
    else:
        st.error(" Database connection error")
        st.info("Using sample data for demonstration")
        
with col2:
    st.markdown("### Data Management")
    st.info("""
    This dashboard uses a local SQLite database to store environmental metrics.
    You can add new measurements using the form in the sidebar.
    Data will persist between sessions.
    """)

st.sidebar.markdown("---")
st.sidebar.info("Dashboard last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M"))
