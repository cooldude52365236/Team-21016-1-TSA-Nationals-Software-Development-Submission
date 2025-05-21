# This is Team No. 21016-1 submission for TSA Nationals 2025 Software Development. The website is https://ecoimpactnationalstsa2025.replit.app

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_recommendations(data, stats):
    recommendations = []

    if stats['current_soil_moisture'] > 80:
        recommendations.append({
            'title': 'Reduce irrigation frequency',
            'description':
            'Soil moisture levels are above optimal range. Consider reducing irrigation frequency by 25% for the next 3 days and monitor soil moisture levels.',
            'impact':
            'Potential water savings of 20-30% while maintaining optimal soil moisture.',
            'priority': 'High'
        })
    elif stats['current_soil_moisture'] < 50:
        recommendations.append({
            'title': 'Optimize irrigation schedule',
            'description':
            'Soil moisture levels are below optimal range. Implement a drip irrigation system to deliver water directly to plant roots and reduce evaporation loss.',
            'impact':
            'Increase water efficiency by 30-40% while improving plant health.',
            'priority': 'High'
        })
    else:
        recommendations.append({
            'title': 'Maintain current irrigation schedule',
            'description':
            'Soil moisture levels are within optimal range. Continue current irrigation practices but monitor for changing weather conditions.',
            'impact': 'Sustained optimal water usage efficiency.',
            'priority': 'Medium'
        })

    if stats['temp_status'] == 'critical':
        if stats['current_temp'] > 28:
            recommendations.append({
                'title': 'Implement heat mitigation strategies',
                'description':
                'Current temperatures exceed optimal growing conditions. Consider installing shade cloths, increasing ventilation, or using evaporative cooling systems during peak heat hours.',
                'impact':
                'Reduce heat stress on plants and decrease water requirements by 15-20%.',
                'priority': 'High'
            })
        elif stats['current_temp'] < 15:
            recommendations.append({
                'title': 'Optimize greenhouse heating',
                'description':
                'Temperatures are below optimal growing range. Implement energy-efficient heating solutions like thermal curtains or heat retention systems.',
                'impact':
                'Reduce energy consumption for heating by 20-25% while maintaining optimal growing temperatures.',
                'priority': 'High'
            })

    avg_daily_energy = data['energy_consumption'].mean()
    if avg_daily_energy > 15:
        recommendations.append({
            'title': 'Implement energy efficiency measures',
            'description':
            'Energy consumption is above optimal levels. Consider upgrading to LED lighting, installing energy-efficient pumps, and implementing automated controls for environmental systems.',
            'impact':
            'Potential energy savings of 30-40% with minimal impact on production.',
            'priority': 'Medium'
        })

    if stats['humidity_status'] == 'critical':
        if stats['current_humidity'] > 80:
            recommendations.append({
                'title': 'Reduce greenhouse humidity',
                'description':
                'Current humidity levels are too high, increasing risk of fungal diseases. Improve ventilation and consider dehumidification during high-humidity periods.',
                'impact':
                'Decrease disease pressure and potentially reduce fungicide applications by 20-30%.',
                'priority': 'High'
            })
        elif stats['current_humidity'] < 40:
            recommendations.append({
                'title': 'Increase humidity levels',
                'description':
                'Humidity is below optimal range. Consider using misting systems during dry periods to increase local humidity without excessive water usage.',
                'impact':
                'Improve plant vigor and reduce water stress with minimal water input.',
                'priority': 'Medium'
            })

    recommendations.append({
        'title': 'Implement rainwater harvesting',
        'description':
        'Install rainwater collection systems to capture and store rainfall for irrigation purposes. This reduces reliance on municipal water supplies or groundwater.',
        'impact':
        'Potential to offset 30-60% of irrigation water needs, depending on local rainfall patterns.',
        'priority': 'Medium'
    })

    recommendations.append({
        'title': 'Consider solar power integration',
        'description':
        'Evaluate the potential for solar panel installation to offset energy usage for pumps, lighting, and climate control systems.',
        'impact':
        'Potential to reduce grid electricity consumption by 40-70% with a 3-7 year return on investment.',
        'priority': 'Medium'
    })

    return recommendations


def calculate_potential_savings(data):
    savings = {}

    total_water_usage = data['water_usage'].sum()
    avg_water_daily = data['water_usage'].mean()

    savings['water_savings'] = total_water_usage * 0.25
    savings['water_savings_percent'] = 25.0

    total_energy_usage = data['energy_consumption'].sum()
    avg_energy_daily = data['energy_consumption'].mean()

    savings['energy_savings'] = total_energy_usage * 0.30
    savings['energy_savings_percent'] = 30.0

    water_cost_per_liter = 0.002
    energy_cost_per_kwh = 0.15

    savings[
        'water_cost_savings'] = savings['water_savings'] * water_cost_per_liter
    savings['energy_cost_savings'] = savings[
        'energy_savings'] * energy_cost_per_kwh
    savings['cost_savings'] = savings['water_cost_savings'] + savings[
        'energy_cost_savings']

    return savings


def calculate_environmental_impact(data, savings):
    impact = {}

    carbon_per_kwh = 0.5
    carbon_per_liter = 0.003

    total_carbon_current = (data['energy_consumption'].sum() * carbon_per_kwh +
                            data['water_usage'].sum() * carbon_per_liter)

    carbon_savings = (savings['energy_savings'] * carbon_per_kwh +
                      savings['water_savings'] * carbon_per_liter)

    impact['carbon_reduction'] = carbon_savings
    impact['carbon_reduction_percent'] = (carbon_savings /
                                          total_carbon_current) * 100

    impact['water_conservation'] = savings['water_savings']
    impact['water_conservation_percent'] = savings['water_savings_percent']

    base_score = 60

    efficiency_factor = min(
        20, data['soil_moisture'].mean() / data['water_usage'].mean() * 100)
    resource_optimization_factor = min(
        15, (1 - (data['energy_consumption'].std() /
                  data['energy_consumption'].mean())) * 30)

    impact['sustainability_score'] = min(
        100, base_score + efficiency_factor + resource_optimization_factor)

    impact['sustainability_score_change'] = min(
        25,
        (savings['water_savings_percent'] + savings['energy_savings_percent'])
        / 4)

    return impact
