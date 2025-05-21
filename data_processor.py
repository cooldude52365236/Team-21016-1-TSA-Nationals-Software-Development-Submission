# This is Team No. 21016-1 submission for TSA Nationals 2025 Software Development. The website is https://ecoimpactnationalstsa2025.replit.app

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data.sample_data import get_environmental_data
import db

def load_data():
    """
    Load environmental data from the database.
    
    Returns:
        DataFrame: Environmental metrics data
    """
    
    return db.load_data_from_db()

def filter_data_by_date(data, start_date, end_date):
    """
    Filter data based on date range.
    
    Args:
        data: DataFrame with environmental metrics
        start_date: Start date for filtering
        end_date: End date for filtering
    
    Returns:
        DataFrame: Filtered data
    """
   
    if not isinstance(start_date, datetime):
        start_date = datetime.combine(start_date, datetime.min.time())
    if not isinstance(end_date, datetime):
        end_date = datetime.combine(end_date, datetime.max.time())
    
    
    mask = (data['date'] >= start_date) & (data['date'] <= end_date)
    filtered_data = data.loc[mask].copy()
    
    return filtered_data

def calculate_statistics(data):
    """
    Calculate various statistics from the environmental data.
    
    Args:
        data: DataFrame with environmental metrics
    
    Returns:
        dict: Dictionary with calculated statistics
    """
    stats = {}
    
    
    latest_record = data.iloc[-1]
    stats['current_temp'] = latest_record['temperature']
    stats['current_humidity'] = latest_record['humidity']
    stats['current_soil_moisture'] = latest_record['soil_moisture']
    
    
    stats['avg_temp'] = data['temperature'].mean()
    stats['avg_humidity'] = data['humidity'].mean()
    stats['avg_soil_moisture'] = data['soil_moisture'].mean()
    stats['avg_water_usage'] = data['water_usage'].mean()
    stats['avg_energy_consumption'] = data['energy_consumption'].mean()
    
    
    stats['temp_change'] = stats['current_temp'] - stats['avg_temp']
    stats['humidity_change'] = stats['current_humidity'] - stats['avg_humidity']
    stats['soil_moisture_change'] = stats['current_soil_moisture'] - stats['avg_soil_moisture']
    
    
    if 18 <= stats['current_temp'] <= 24:
        stats['temp_status'] = 'optimal'
    elif 15 <= stats['current_temp'] < 18 or 24 < stats['current_temp'] <= 28:
        stats['temp_status'] = 'warning'
    else:
        stats['temp_status'] = 'critical'
    
    
    if 50 <= stats['current_humidity'] <= 70:
        stats['humidity_status'] = 'optimal'
    elif 40 <= stats['current_humidity'] < 50 or 70 < stats['current_humidity'] <= 80:
        stats['humidity_status'] = 'warning'
    else:
        stats['humidity_status'] = 'critical'
    
    
    if 60 <= stats['current_soil_moisture'] <= 80:
        stats['soil_moisture_status'] = 'optimal'
    elif 40 <= stats['current_soil_moisture'] < 60 or 80 < stats['current_soil_moisture'] <= 90:
        stats['soil_moisture_status'] = 'warning'
    else:
        stats['soil_moisture_status'] = 'critical'
    
    
    if len(data) >= 7:
        week_data = data.iloc[-7:]
        stats['temp_trend'] = (week_data['temperature'].iloc[-1] - week_data['temperature'].iloc[0])
        stats['humidity_trend'] = (week_data['humidity'].iloc[-1] - week_data['humidity'].iloc[0])
        stats['soil_moisture_trend'] = (week_data['soil_moisture'].iloc[-1] - week_data['soil_moisture'].iloc[0])
    else:
        stats['temp_trend'] = 0
        stats['humidity_trend'] = 0
        stats['soil_moisture_trend'] = 0
    
    return stats

def calculate_resource_efficiency(data):
    """
    Calculate resource efficiency metrics.
    
    Args:
        data: DataFrame with environmental metrics
    
    Returns:
        dict: Dictionary with resource efficiency metrics
    """
    efficiency = {}
    
    
    water_per_moisture = data['water_usage'] / data['soil_moisture']
    efficiency['water_efficiency'] = water_per_moisture.mean()
    
    
    energy_per_temp = data['energy_consumption'] / (data['temperature'])
    efficiency['energy_efficiency'] = energy_per_temp.mean()
    
    
    water_baseline = 2.5
    efficiency['water_efficiency_vs_baseline'] = efficiency['water_efficiency'] / water_baseline
    
    
    energy_baseline = 1.2
    efficiency['energy_efficiency_vs_baseline'] = efficiency['energy_efficiency'] / energy_baseline
    
    
    efficiency['optimal_water_usage'] = data['soil_moisture'].mean() * (water_baseline * 0.7) 
    efficiency['optimal_energy_consumption'] = data['temperature'].mean() * (energy_baseline * 0.75)  
    
    
    current_water = data['water_usage'].mean()
    current_energy = data['energy_consumption'].mean()
    
    
    if current_water <= efficiency['optimal_water_usage']:
        efficiency['water_usage_efficiency_percent'] = 100.0
    else:
        efficiency['water_usage_efficiency_percent'] = (efficiency['optimal_water_usage'] / current_water) * 100
    
    if current_energy <= efficiency['optimal_energy_consumption']:
        efficiency['energy_consumption_efficiency_percent'] = 100.0
    else:
        efficiency['energy_consumption_efficiency_percent'] = (efficiency['optimal_energy_consumption'] / current_energy) * 100
    
    
    efficiency['current_water_usage'] = current_water
    efficiency['current_energy_consumption'] = current_energy
    
    
    efficiency['overall_score'] = (efficiency['water_usage_efficiency_percent'] + 
                                  efficiency['energy_consumption_efficiency_percent']) / 2
    
    return efficiency
