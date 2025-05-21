# This is Team No. 21016-1 submission for TSA Nationals 2025 Software Development. The website is https://ecoimpactnationalstsa2025.replit.app

import streamlit as st
import pandas as pd
import numpy as np
import time

def get_color_scale(value, thresholds):
    """
    Returns a color based on the value and specified thresholds.
    
    Args:
        value: The value to evaluate
        thresholds: Dictionary with min, max and optimal values
    
    Returns:
        String: Color value (red, yellow, or green)
    """
    min_val = thresholds['min']
    max_val = thresholds['max']
    optimal_low = thresholds['optimal_low']
    optimal_high = thresholds['optimal_high']
    
    if min_val <= value <= optimal_low or optimal_high <= value <= max_val:
        return "yellow"
    elif optimal_low < value < optimal_high:
        return "green"
    else:
        return "red"

def get_status_color(status):
    """
    Returns a color hex code based on status string.
    
    Args:
        status: Status string ('optimal', 'warning', 'critical')
    
    Returns:
        String: Hex color code
    """
    colors = {
        'optimal': '#28a745',  # Green
        'warning': '#ffc107',  # Yellow
        'critical': '#dc3545'  # Red
    }
    return colors.get(status, '#6c757d')  

def display_metric_card(title, value, delta, status):
    """
    Display a metric with custom styling based on status.
    
    Args:
        title: Title of the metric
        value: Current value as string
        delta: Change from average as string
        status: Status string ('optimal', 'warning', 'critical')
    """
    st.metric(
        label=title,
        value=value,
        delta=delta
    )
    

    status_color = get_status_color(status)
    st.markdown(f"""
        <div style="margin-top:-1rem;">
            <span style="color:{status_color};font-weight:bold;">●</span>
            <span style="color:{status_color};"> {status.capitalize()}</span>
        </div>
    """, unsafe_allow_html=True)

def calculate_moving_average(data, column, window=7):
    """
    Calculate moving average for a column in dataframe.
    
    Args:
        data: Pandas DataFrame
        column: Column name to calculate moving average
        window: Window size for moving average
    
    Returns:
        Series: Moving average values
    """
    return data[column].rolling(window=window, min_periods=1).mean()

def normalize_data(data, column, min_val=0, max_val=1):
    """
    Normalize data column to specified range.
    
    Args:
        data: Pandas DataFrame
        column: Column name to normalize
        min_val: Minimum value for normalization
        max_val: Maximum value for normalization
    
    Returns:
        Series: Normalized values
    """
    x = data[column].values
    x_norm = (x - np.min(x)) / (np.max(x) - np.min(x))
    return min_val + (max_val - min_val) * x_norm

def animated_progress_bar(value, target, title, unit="", speed=0.02, color="green"):
    """
    Display an animated progress bar with a specified value and target.
    
    Args:
        value: Current value
        target: Target value or maximum (100%)
        title: Title of the progress bar
        unit: Unit of measurement (e.g., "%", "kWh", "L")
        speed: Animation speed (lower is faster)
        color: Color of the progress bar
    
    Returns:
        None: Displays a progress bar widget
    """

    percent = min(100, max(0, (value / target) * 100))
    

    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    

    for i in range(0, int(percent) + 1, 2):
        progress_placeholder.progress(i / 100)
        status_text = f"{title}: {i:.0f}% ({value:.1f}{unit} of {target:.1f}{unit})"
        status_placeholder.markdown(
            f"<div style='color:{color};'>{status_text}</div>",
            unsafe_allow_html=True
        )
        time.sleep(speed)
    

    progress_placeholder.progress(percent / 100)
    status_text = f"{title}: {percent:.0f}% ({value:.1f}{unit} of {target:.1f}{unit})"
    status_placeholder.markdown(
        f"<div style='color:{color};'>{status_text}</div>",
        unsafe_allow_html=True
    )
