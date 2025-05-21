# This is Team No. 21016-1 submission for TSA Nationals 2025 Software Development. The website is https://ecoimpactnationalstsa2025.replit.app

import pandas as pd
import numpy as np

def get_region_data():
    regions = [
        {"name": "Northeast", "avg_temp": 11.2, "avg_humidity": 68.5, "avg_rainfall": 1050, 
         "water_usage": 18.5, "energy_consumption": 22.3, "carbon_footprint": 15.2},
        
        {"name": "Southeast", "avg_temp": 18.7, "avg_humidity": 75.2, "avg_rainfall": 1270, 
         "water_usage": 22.1, "energy_consumption": 19.8, "carbon_footprint": 14.5},
        
        {"name": "Midwest", "avg_temp": 13.4, "avg_humidity": 65.8, "avg_rainfall": 920, 
         "water_usage": 16.2, "energy_consumption": 21.7, "carbon_footprint": 16.8},
        
        {"name": "Southwest", "avg_temp": 24.3, "avg_humidity": 45.2, "avg_rainfall": 380, 
         "water_usage": 28.4, "energy_consumption": 27.5, "carbon_footprint": 19.3},
        
        {"name": "West", "avg_temp": 16.2, "avg_humidity": 58.6, "avg_rainfall": 760, 
         "water_usage": 24.7, "energy_consumption": 18.9, "carbon_footprint": 13.4},
        
        {"name": "Pacific Northwest", "avg_temp": 12.8, "avg_humidity": 73.2, "avg_rainfall": 1150, 
         "water_usage": 12.9, "energy_consumption": 16.4, "carbon_footprint": 11.8}
    ]
    
    return pd.DataFrame(regions)

def calculate_regional_comparison(current_data, selected_region):
    regions_df = get_region_data()
    region_data = regions_df[regions_df["name"] == selected_region].iloc[0]
    
    current_water = current_data["water_usage"].mean()
    current_energy = current_data["energy_consumption"].mean()
    
    comparison = {
        "region_name": region_data["name"],
        "region_avg_temp": region_data["avg_temp"],
        "region_avg_humidity": region_data["avg_humidity"],
        "region_avg_rainfall": region_data["avg_rainfall"],
        
        "water_usage_current": current_water,
        "water_usage_region": region_data["water_usage"],
        "water_usage_diff_percent": ((current_water - region_data["water_usage"]) / region_data["water_usage"]) * 100,
        
        "energy_consumption_current": current_energy,
        "energy_consumption_region": region_data["energy_consumption"],
        "energy_consumption_diff_percent": ((current_energy - region_data["energy_consumption"]) / region_data["energy_consumption"]) * 100,
        
        "estimated_carbon_footprint": (current_water * 0.005) + (current_energy * 0.4),
        "region_carbon_footprint": region_data["carbon_footprint"],
        "carbon_footprint_diff_percent": (((current_water * 0.005 + current_energy * 0.4) - region_data["carbon_footprint"]) / region_data["carbon_footprint"]) * 100
    }
    
    return comparison

def get_eco_impact_score(comparison):
    water_impact = 35 - abs(comparison["water_usage_diff_percent"]) * 0.3 if comparison["water_usage_diff_percent"] <= 0 else 35 - comparison["water_usage_diff_percent"] * 0.5
    energy_impact = 35 - abs(comparison["energy_consumption_diff_percent"]) * 0.3 if comparison["energy_consumption_diff_percent"] <= 0 else 35 - comparison["energy_consumption_diff_percent"] * 0.5
    carbon_impact = 30 - abs(comparison["carbon_footprint_diff_percent"]) * 0.3 if comparison["carbon_footprint_diff_percent"] <= 0 else 30 - comparison["carbon_footprint_diff_percent"] * 0.5
    
    total_score = max(0, min(100, water_impact + energy_impact + carbon_impact))
    
    return {
        "total_score": total_score,
        "water_impact_score": max(0, min(35, water_impact)),
        "energy_impact_score": max(0, min(35, energy_impact)),
        "carbon_impact_score": max(0, min(30, carbon_impact)),
    }

def get_impact_recommendations(comparison):
    recommendations = []
    
    if comparison["water_usage_diff_percent"] > 10:
        recommendations.append({
            "category": "Water Usage",
            "recommendation": f"Your water usage is {comparison['water_usage_diff_percent']:.1f}% higher than the regional average. Consider implementing water conservation techniques appropriate for your region's climate.",
            "priority": "High" if comparison["water_usage_diff_percent"] > 25 else "Medium"
        })
    
    if comparison["energy_consumption_diff_percent"] > 10:
        recommendations.append({
            "category": "Energy Consumption",
            "recommendation": f"Your energy consumption is {comparison['energy_consumption_diff_percent']:.1f}% higher than the regional average. Consider energy efficiency improvements tailored to your region's climate conditions.",
            "priority": "High" if comparison["energy_consumption_diff_percent"] > 25 else "Medium"
        })
    
    if comparison["carbon_footprint_diff_percent"] > 10:
        recommendations.append({
            "category": "Carbon Footprint",
            "recommendation": f"Your carbon footprint is {comparison['carbon_footprint_diff_percent']:.1f}% higher than the regional average. Consider renewable energy sources and carbon offset programs.",
            "priority": "High" if comparison["carbon_footprint_diff_percent"] > 25 else "Medium"
        })
    
    if len(recommendations) == 0:
        recommendations.append({
            "category": "Overall Impact",
            "recommendation": "Your environmental metrics are close to or better than regional averages. Continue your sustainable practices.",
            "priority": "Low"
        })
    
    return recommendations

def get_all_regions():
    regions_df = get_region_data()
    return regions_df["name"].tolist()
