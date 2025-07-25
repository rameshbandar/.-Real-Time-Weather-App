import streamlit as st
import requests
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
import pandas as pd
import os

# Set page config
st.set_page_config(page_title="Weather Forecast App", page_icon="⛅", layout="wide")

# Improved API key handling with multiple fallback options
def get_api_key():
    # 1. First try Streamlit secrets
    try:
        return st.secrets["OPENWEATHER_API_KEY"]
    except (KeyError, FileNotFoundError):
        pass
    
    # 2. Then try environment variable
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if api_key:
        return api_key
    
    # 3. Finally, prompt user to enter key (for local testing)
    st.warning("API key not found in secrets or environment variables")
    return None

API_KEY = get_api_key()
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
ICON_URL = "https://openweathermap.org/img/wn/{icon}@2x.png"

def get_weather_data(city_name, units="metric"):
    """Fetch current weather data for a given city"""
    if not API_KEY:
        st.error("Please configure your OpenWeatherMap API key")
        return None
        
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": units
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

# ... [rest of your functions remain the same] ...

def main():
    """Main app function"""
    st.title("🌤️ Real-Time Weather App")
    
    if not API_KEY:
        api_key_input = st.text_input("Enter your OpenWeatherMap API key", type="password")
        if api_key_input:
            global API_KEY
            API_KEY = api_key_input
            st.rerun()
        return
    
    # Rest of your main function
    with st.sidebar:
        st.header("Settings")
        city = st.text_input("Enter city name", "London")
        units = st.radio("Select units", ["metric", "imperial"], index=0)
        st.markdown("---")
        st.markdown("### Sample Cities")
        sample_cities = ["New York", "Tokyo", "Sydney", "Paris"]
        for sample_city in sample_cities:
            if st.button(sample_city):
                city = sample_city
    
    if city:
        with st.spinner("Fetching weather data..."):
            weather_data = get_weather_data(city, units)
            forecast_data = get_forecast_data(city, units)
        
        if weather_data and forecast_data:
            display_current_weather(weather_data, units)
            st.markdown("---")
            display_forecast_chart(forecast_data, units)
        else:
            st.error("Failed to fetch weather data. Please check the city name and try again.")

if __name__ == "__main__":
    main()