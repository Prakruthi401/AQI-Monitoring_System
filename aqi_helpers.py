import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_aqi(pm25, pm10, no2=0, so2=0, co=0, o3=0):
    """
    Calculate AQI using EPA breakpoints
    Returns AQI value and category
    """
    def get_pm25_aqi(concentration):
        if concentration <= 12.0:
            return linear_scale(concentration, 0, 12.0, 0, 50)
        elif concentration <= 35.4:
            return linear_scale(concentration, 12.1, 35.4, 51, 100)
        elif concentration <= 55.4:
            return linear_scale(concentration, 35.5, 55.4, 101, 150)
        elif concentration <= 150.4:
            return linear_scale(concentration, 55.5, 150.4, 151, 200)
        elif concentration <= 250.4:
            return linear_scale(concentration, 150.5, 250.4, 201, 300)
        else:
            return linear_scale(concentration, 250.5, 500.4, 301, 500)

    def get_pm10_aqi(concentration):
        if concentration <= 54:
            return linear_scale(concentration, 0, 54, 0, 50)
        elif concentration <= 154:
            return linear_scale(concentration, 55, 154, 51, 100)
        elif concentration <= 254:
            return linear_scale(concentration, 155, 254, 101, 150)
        elif concentration <= 354:
            return linear_scale(concentration, 255, 354, 151, 200)
        elif concentration <= 424:
            return linear_scale(concentration, 355, 424, 201, 300)
        else:
            return linear_scale(concentration, 425, 604, 301, 500)

    def linear_scale(value, min_val, max_val, min_aqi, max_aqi):
        return ((max_aqi - min_aqi) / (max_val - min_val)) * (value - min_val) + min_aqi

    # Calculate individual AQIs
    aqi_values = []
    if pm25 > 0:
        aqi_values.append(get_pm25_aqi(pm25))
    if pm10 > 0:
        aqi_values.append(get_pm10_aqi(pm10))

    # Return the highest AQI
    final_aqi = max(aqi_values) if aqi_values else 0

    return int(final_aqi), get_aqi_category(final_aqi)

def get_aqi_category(aqi):
    """Get AQI category and color"""
    if aqi <= 50:
        return "Good", "#00e400", "Air quality is satisfactory"
    elif aqi <= 100:
        return "Moderate", "#ffff00", "Air quality is acceptable"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups", "#ff7e00", "Sensitive individuals may experience issues"
    elif aqi <= 200:
        return "Unhealthy", "#ff0000", "Everyone may experience health effects"
    elif aqi <= 300:
        return "Very Unhealthy", "#8f3f97", "Health alert for everyone"
    else:
        return "Hazardous", "#7e0023", "Emergency conditions"

def get_aqi_color_gradient(aqi):
    if aqi <= 50:
        return "linear-gradient(135deg, #10b981 0%, #34d399 100%)", "Good", "#10b981", "🟢"
    elif aqi <= 100:
        return "linear-gradient(135deg, #fbbf24 0%, #fde047 100%)", "Moderate", "#fbbf24", "🟡"
    elif aqi <= 150:
        return "linear-gradient(135deg, #f97316 0%, #fb923c 100%)", "Poor", "#f97316", "🟠"
    elif aqi <= 200:
        return "linear-gradient(135deg, #ef4444 0%, #f87171 100%)", "Unhealthy", "#ef4444", "🔴"
    elif aqi <= 300:
        return "linear-gradient(135deg, #a855f7 0%, #c084fc 100%)", "Severe", "#a855f7", "🟣"
    else:
        return "linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%)", "Hazardous", "#7f1d1d", "⚫"

def generate_calculated_data():
    """Generate calculated AQI data for testing"""
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='h')
    data = []

    for date in dates:
        base_aqi = 50 + np.random.normal(0, 20)  # Base AQI with some variation
        seasonal_factor = 10 * np.sin(2 * np.pi * date.dayofyear / 365)  # Seasonal variation
        daily_factor = 15 * np.sin(2 * np.pi * date.hour / 24)  # Daily variation

        aqi = max(0, base_aqi + seasonal_factor + daily_factor + np.random.normal(0, 10))

        data.append({
            'timestamp': date,
            'aqi': round(aqi, 1),
            'pm25': round(max(0, aqi * 0.3 + np.random.normal(0, 5)), 1),
            'pm10': round(max(0, aqi * 0.5 + np.random.normal(0, 8)), 1),
            'temperature': round(25 + np.random.normal(0, 5), 1),
            'humidity': round(60 + np.random.normal(0, 10), 1)
        })

    return pd.DataFrame(data)

def format_timestamp(timestamp):
    """Format timestamp for display"""
    if isinstance(timestamp, str):
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    else:
        dt = timestamp

    now = datetime.now()
    diff = now - dt.replace(tzinfo=None)

    if diff.days == 0:
        if diff.seconds < 3600:
            return f"{diff.seconds // 60} minutes ago"
        else:
            return f"{diff.seconds // 3600} hours ago"
    elif diff.days == 1:
        return "Yesterday"
    else:
        return dt.strftime("%b %d, %Y")

def calculate_trend(data, hours=24):
    """Calculate AQI trend over last N hours"""
    if len(data) < 2:
        return "stable"

    recent = data.tail(hours)
    if len(recent) < 2:
        return "stable"

    first_half = recent[:len(recent)//2]['aqi'].mean()
    second_half = recent[len(recent)//2:]['aqi'].mean()

    diff = second_half - first_half
    if abs(diff) < 5:
        return "stable"
    elif diff > 0:
        return "increasing"
    else:
        return "decreasing"

def get_health_recommendations(aqi):
    """Get health recommendations based on AQI"""
    if aqi <= 50:
        return {
            'level': 'Good',
            'message': 'Air quality is satisfactory. Enjoy outdoor activities!',
            'color': '#00e400'
        }
    elif aqi <= 100:
        return {
            'level': 'Moderate',
            'message': 'Air quality is acceptable. Sensitive individuals should consider limiting prolonged outdoor exertion.',
            'color': '#ffff00'
        }
    elif aqi <= 150:
        return {
            'level': 'Unhealthy for Sensitive Groups',
            'message': 'Members of sensitive groups may experience health effects. Consider reducing outdoor activities.',
            'color': '#ff7e00'
        }
    elif aqi <= 200:
        return {
            'level': 'Unhealthy',
            'message': 'Everyone may begin to experience health effects. Sensitive groups should avoid outdoor activities.',
            'color': '#ff0000'
        }
    elif aqi <= 300:
        return {
            'level': 'Very Unhealthy',
            'message': 'Health alert: everyone may experience more serious health effects. Avoid outdoor activities.',
            'color': '#8f3f97'
        }
    else:
        return {
            'level': 'Hazardous',
            'message': 'Health warning of emergency conditions. Everyone should avoid all outdoor activities.',
            'color': '#7e0023'
        }
