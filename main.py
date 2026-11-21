import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
from folium.plugins import LocateControl
import random
import matplotlib.pyplot as plt
import os
import json
import glob
import joblib

from openaq_fetcher import OpenAQFetcher
from location_search import LocationSearch
from aqi_helpers import calculate_aqi, get_aqi_category, get_aqi_color_gradient, generate_calculated_data, format_timestamp, calculate_trend, get_health_recommendations
from bangalore_locations import BANGALORE_STATIONS, get_station_by_id, get_stations_by_type, BANGALORE_AREAS
from aqi_fallback import AQIFallbackService

# Optional AI predictor import
try:
    from aqi_predictor import predictor
    PREDICTOR_AVAILABLE = True
except ImportError:
    PREDICTOR_AVAILABLE = False
    predictor = None
    print("AI predictor not available - forecasting features will be disabled")

openaq_fetcher = OpenAQFetcher(api_key=None)  # No hardcoded API key
location_search = LocationSearch()
aqi_fallback_service = AQIFallbackService()

st.set_page_config(
    page_title="AQI Monitor - Air Quality Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# FIXED FRONTEND CSS WITH PERFORMANCE AND ACCESSIBILITY IMPROVEMENTS
st.markdown("""
    <style>
/* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global styles */
    * {
        font-family: 'Poppins', sans-serif;
    }

    /* Animated dark gradient background with GPU acceleration */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .main {
        background: linear-gradient(-45deg, rgba(10, 10, 15, 0.95), rgba(15, 10, 20, 0.95), rgba(10, 15, 25, 0.95), rgba(20, 15, 30, 0.95));
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
        will-change: background-position;
    }

    .stApp {
        background: linear-gradient(-45deg, rgba(10, 10, 15, 0.95), rgba(15, 10, 20, 0.95), rgba(10, 15, 25, 0.95), rgba(20, 15, 30, 0.95));
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(-45deg, rgba(10, 10, 15, 0.98), rgba(15, 10, 20, 0.98), rgba(10, 15, 25, 0.98), rgba(20, 15, 30, 0.98));
        padding: 1rem;
    }

    /* Floating animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    /* Pulse animation */
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.9; }
    }

    /* Glow animation */
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(139, 0, 0, 0.5); }
        50% { box-shadow: 0 0 40px rgba(139, 0, 0, 0.8); }
    }

    /* Slide in from left */
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    /* Slide in from right */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    /* Fade in up */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Scale in */
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    /* Shimmer effect */
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }

    /* ACCESSIBILITY: Reduce motion for users who prefer it */
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation: none !important;
            transition: none !important;
        }
    }

    /* Navigation bar */
    .nav-container {
        background: linear-gradient(135deg, rgba(8, 8, 12, 0.92) 0%, rgba(18, 8, 16, 0.92) 100%);
        backdrop-filter: blur(20px);
        padding: 1.2rem 3rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 0 20px rgba(139, 0, 0, 0.15);
        position: sticky;
        top: 0;
        z-index: 1000;
        margin: 0 0 2rem 0;
        animation: slideInLeft 0.8s ease-out;
        border-bottom: 2px solid rgba(139, 0, 0, 0.3);
    }

    /* RESPONSIVE: Stack nav on mobile */
    @media (max-width: 768px) {
        .nav-container {
            padding: 0.8rem 1rem;
            flex-direction: column;
        }
        .stColumns > div {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
    }

    .logo-container {
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }

    .logo-icon {
        font-size: 32px;
        animation: float 3s ease-in-out infinite;
        filter: drop-shadow(0 0 10px rgba(139, 0, 0, 0.6));
    }

    .logo-text {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(135deg, #8B0000 0%, #DC143C 50%, #FF6B6B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
        filter: drop-shadow(0 0 10px rgba(139, 0, 0, 0.4));
    }

    /* Content wrapper */
    .content-wrapper {
        max-width: 1400px;
        margin: 0 auto;
        padding: 3rem 4rem;
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }

    /* RESPONSIVE: Reduce padding on mobile */
    @media (max-width: 768px) {
        .content-wrapper {
            padding: 1.5rem 1rem;
        }
    }

    /* Hero section with GPU acceleration */
    .hero-section {
        background: linear-gradient(135deg, rgba(8, 8, 12, 0.88) 0%, rgba(18, 8, 16, 0.88) 50%, rgba(10, 18, 28, 0.88) 100%);
        border-radius: 30px;
        padding: 3rem;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 40px rgba(139, 0, 0, 0.2);
        animation: fadeInUp 1s ease-out;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(139, 0, 0, 0.3);
    }

    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(139, 0, 0, 0.2), transparent);
        animation: shimmer 3s infinite;
        will-change: transform;
    }

    .hero-title {
        font-size: 52px;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B6B 0%, #DC143C 50%, #8B0000 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-align: center;
        letter-spacing: -1px;
        animation: scaleIn 1s ease-out;
        filter: drop-shadow(0 0 20px rgba(139, 0, 0, 0.5));
    }

    /* RESPONSIVE: Reduce title size on mobile */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 32px;
        }
    }

    .hero-subtitle {
        font-size: 18px;
        color: #c0c0c0;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }

    /* Card styles with GPU acceleration */
    .card {
        background: linear-gradient(135deg, rgba(12, 12, 18, 0.88) 0%, rgba(18, 12, 22, 0.88) 50%, rgba(10, 18, 28, 0.88) 100%);
        border-radius: 24px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5), 0 0 30px rgba(139, 0, 0, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: fadeInUp 1s ease-out;
        border: 1px solid rgba(139, 0, 0, 0.3);
        transform: translateZ(0);
        backface-visibility: hidden;
    }

    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7), 0 0 50px rgba(139, 0, 0, 0.3);
        border-color: rgba(220, 20, 60, 0.5);
    }

    .card-title {
        font-size: 26px;
        font-weight: 700;
        background: linear-gradient(135deg, #FF6B6B 0%, #DC143C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        position: relative;
        margin-top: 0;
        padding-top: 0;
        text-align: center;
        width: 100%;
    }

    /* Metric cards with dark theme and GPU acceleration */
    .metric-card {
        background: linear-gradient(135deg, rgba(15, 15, 20, 0.85) 0%, rgba(22, 15, 25, 0.85) 100%);
        border-radius: 20px;
        padding: 1.8rem;
        text-align: center;
        border: 2px solid rgba(139, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        animation: scaleIn 0.6s ease-out;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        transform: translateZ(0);
        backface-visibility: hidden;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(139, 0, 0, 0.2) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px) scale(1.03);
        border-color: rgba(220, 20, 60, 0.6);
        box-shadow: 0 12px 30px rgba(139, 0, 0, 0.4);
        animation: glow 2s infinite;
    }

    .metric-card:hover::before {
        opacity: 1;
    }

    .metric-label {
        font-size: 13px;
        color: #b0b0b0;
        font-weight: 600;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-value {
        font-size: 40px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.5rem;
        transition: transform 0.3s ease;
        text-shadow: 0 0 20px rgba(139, 0, 0, 0.5);
    }

    .metric-card:hover .metric-value {
        transform: scale(1.1);
    }

    .metric-status {
        font-size: 13px;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: 600;
        animation: pulse 2s infinite;
    }

    .metric-unit {
        font-size: 13px;
        color: #999999;
        font-weight: 500;
    }

    /* AQI Level cards with dark theme */
    .aqi-level-card {
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.2rem;
        color: white;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        animation: slideInRight 0.8s ease-out;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }

    .aqi-level-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.6s ease;
    }

    .aqi-level-card:hover {
        transform: translateX(12px) scale(1.02);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6);
    }

    .aqi-level-card:hover::before {
        left: 100%;
    }

    .aqi-level-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .aqi-level-range {
        font-size: 15px;
        opacity: 0.95;
        margin-bottom: 0.8rem;
        font-weight: 500;
    }

    .aqi-level-desc {
        font-size: 14px;
        opacity: 0.95;
        line-height: 1.7;
    }

    /* Button styles with dark theme and focus indicators */
    .stButton > button {
        background: #470000;
        color: white;
        border: none;
        border-radius: 16px;
        padding: 0.85rem 2rem;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 8px 20px rgba(71, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(71, 0, 0, 0.5);
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 30px rgba(71, 0, 0, 0.8);
        background: #5a0000;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    /* ACCESSIBILITY: Focus indicators */
    .stButton > button:focus-visible {
        outline: 3px solid #DC143C;
        outline-offset: 2px;
    }

    .stButton > button:active {
        transform: translateY(-1px) scale(0.98);
    }

    /* Radio buttons */
    .stRadio > label {
        display: none;
    }

    .stRadio > div {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .stRadio > div > label {
        background: linear-gradient(135deg, rgba(20, 20, 20, 0.9) 0%, rgba(30, 15, 20, 0.9) 100%);
        padding: 0.85rem 1.8rem;
        border-radius: 16px;
        border: 2px solid rgba(139, 0, 0, 0.3);
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        color: #d0d0d0;
    }

    .stRadio > div > label:hover {
        border-color: #DC143C;
        color: #FF6B6B;
        background: linear-gradient(135deg, rgba(30, 20, 20, 0.9) 0%, rgba(40, 20, 25, 0.9) 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(139, 0, 0, 0.3);
    }

    /* Selectbox with dark theme */
    .stSelectbox > div > div {
        border-radius: 16px;
        border: 2px solid rgba(139, 0, 0, 0.3);
        transition: all 0.3s ease;
        background-color: rgba(20, 20, 20, 0.9);
        color: white;
    }

    .stSelectbox > div > div:hover {
        border-color: #DC143C;
        box-shadow: 0 4px 12px rgba(139, 0, 0, 0.3);
    }

    /* ACCESSIBILITY: Focus indicators for form elements */
    .stSelectbox > div > div:focus-within {
        outline: 2px solid #DC143C;
        outline-offset: 2px;
    }

    /* Hide Streamlit elements */
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Info boxes with dark theme */
    .info-box {
        background: linear-gradient(135deg, rgba(0, 51, 102, 0.3) 0%, rgba(0, 76, 153, 0.3) 100%);
        border-left: 5px solid #3b82f6;
        padding: 1.8rem;
        border-radius: 16px;
        margin: 1rem 0;
        animation: slideInLeft 0.8s ease-out;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }

    .info-box:hover {
        transform: translateX(8px);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
    }

    .warning-box {
        background: linear-gradient(135deg, rgba(102, 51, 0, 0.3) 0%, rgba(153, 76, 0, 0.3) 100%);
        border-left: 5px solid #f59e0b;
        padding: 1.8rem;
        border-radius: 16px;
        margin: 1rem 0;
        animation: slideInLeft 0.8s ease-out;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }

    .warning-box:hover {
        transform: translateX(8px);
        box-shadow: 0 8px 20px rgba(245, 158, 11, 0.3);
    }

    .danger-box {
        background: linear-gradient(135deg, rgba(102, 0, 0, 0.3) 0%, rgba(153, 0, 0, 0.3) 100%);
        border-left: 5px solid #ef4444;
        padding: 1.8rem;
        border-radius: 16px;
        margin: 1rem 0;
        animation: slideInLeft 0.8s ease-out;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }

    .danger-box:hover {
        transform: translateX(8px);
        box-shadow: 0 8px 20px rgba(239, 68, 68, 0.3);
    }

    /* News card with dark theme */
    .news-card {
        background: linear-gradient(135deg, rgba(12, 12, 16, 0.85) 0%, rgba(18, 12, 20, 0.85) 100%);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(139, 0, 0, 0.2);
        animation: fadeInUp 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }

    .news-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%);
        transform: scaleY(0);
        transition: transform 0.3s ease;
    }

    .news-card:hover {
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.7), 0 0 30px rgba(139, 0, 0, 0.3);
        transform: translateY(-5px);
        border-color: rgba(220, 20, 60, 0.5);
    }

    .news-card:hover::before {
        transform: scaleY(1);
    }

    .news-title {
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.8rem;
        transition: color 0.3s ease;
    }

    .news-card:hover .news-title {
        color: #FF6B6B;
    }

    .news-date {
        font-size: 13px;
        color: #a0a0a0;
        margin-bottom: 1rem;
        font-weight: 500;
    }

    .news-summary {
        font-size: 15px;
        color: #c0c0c0;
        line-height: 1.7;
    }

    .news-badge {
        display: inline-block;
        background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* Status indicator with pulse */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 0.5rem;
        animation: pulse 2s infinite;
    }

    .status-good {
        background-color: #10b981;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
    }

    .status-moderate {
        background-color: #f59e0b;
        box-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
    }

    .status-bad {
        background-color: #ef4444;
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
    }

    /* Date input styling */
    .stDateInput > div > div {
        background-color: rgba(20, 20, 20, 0.9);
        border: 2px solid rgba(139, 0, 0, 0.3);
        border-radius: 16px;
        color: white;
    }

    /* Text color overrides with improved contrast */
    p, span, div {
        color: #d0d0d0;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }

    /* Extra frontend padding and spacing fixes */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }

    .stButton > button {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }

    .card {
        margin-bottom: 2rem !important;
    }

    /* Text input styling */
    .stTextInput > div > div > input {
        background-color: rgba(20, 20, 20, 0.9);
        border: 2px solid rgba(139, 0, 0, 0.3);
        border-radius: 16px;
        color: white;
        padding: 0.75rem 1rem;
    }

    .stTextInput > div > div > input:focus {
        border-color: #DC143C;
        outline: 2px solid #DC143C;
        outline-offset: 2px;
    }

    /* Loading spinner */
    .stSpinner > div {
        border-color: #DC143C;
    }

    </style>
    """, unsafe_allow_html=True)

st.markdown("""<style>
[data-testid="stButton"] button {padding: .65rem .3rem !important; font-size: 14px !important;}
[data-testid="stButton"] button p {white-space: nowrap !important; word-break: normal !important; font-size: 14px !important;}
</style>""", unsafe_allow_html=True)

# Initialize session state
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = 'Dashboard'
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = 'Delhi'
if 'selected_forecast_station' not in st.session_state:
    st.session_state.selected_forecast_station = 'BTM Layout'
if 'openaq_api_key' not in st.session_state:
    st.session_state.openaq_api_key = ''

# API Key Input in Sidebar
st.warning("Learning demo: charts, history, fallback AQI values, and alert cards can use simulated data. Do not use this app for health or outdoor-activity decisions. OpenAQ integration is experimental and not verified here.")
st.sidebar.markdown("---")
st.sidebar.markdown("### API Configuration")
st.sidebar.markdown("Enter your OpenAQ API key to access OpenAQ data:")
st.sidebar.markdown("[Get your free API key here](https://openaq.org/#/signup)", unsafe_allow_html=True)
api_key_input = st.sidebar.text_input(
    "OpenAQ API Key",
    type="password",
    placeholder="Enter your API key from https://openaq.org",
    value=st.session_state.openaq_api_key,
    help="Get your free API key from https://openaq.org/#/signup"
)

if api_key_input != st.session_state.openaq_api_key:
    st.session_state.openaq_api_key = api_key_input
    # Reinitialize fetcher with new API key
    if api_key_input:
        openaq_fetcher = OpenAQFetcher(api_key=api_key_input)
        st.sidebar.success("API key updated!")
    else:
        openaq_fetcher = OpenAQFetcher()
        st.sidebar.info("Using default/mock data")

openaq_fetcher = OpenAQFetcher(api_key=st.session_state.openaq_api_key or None)

# Show API key status
if st.session_state.openaq_api_key:
    st.sidebar.markdown(f"**Status:** API key entered (connection not verified)")
else:
    st.sidebar.markdown("**Status:** Using mock data")
    st.sidebar.markdown("*Get your API key at [openaq.org](https://openaq.org/#/signup)*")

st.sidebar.markdown("---")

def create_map():
    """Create folium map with Bangalore monitoring stations"""
    m = folium.Map(
        location=[12.9716, 77.5946],
        zoom_start=12,
        tiles='OpenStreetMap'
    )

    # Use session state API key if available
    if st.session_state.openaq_api_key:
        openaq = OpenAQFetcher(api_key=st.session_state.openaq_api_key)
    else:
        openaq = openaq_fetcher
    
    aqi_data_openaq = openaq.get_aqi_data(city="Bangalore")

    for station in BANGALORE_STATIONS:
        lat = station['coordinates']['latitude']
        lon = station['coordinates']['longitude']
        name = station['name']
        station_type = station['type']

        station_aqi_data = None
        for location_name, location_data in aqi_data_openaq.items():
            if station['name'].lower() in location_name.lower():
                station_aqi_data = location_data
                break

        if station_aqi_data:
            aqi = station_aqi_data.get('aqi', 0)
            gradient, status, color, _ = get_aqi_color_gradient(aqi)
        else:
            aqi = random.randint(50, 200)
            gradient, status, color, _ = get_aqi_color_gradient(aqi)

        radius = 12 if name == st.session_state.selected_city else 8
        weight = 3 if name == st.session_state.selected_city else 1
        fillOpacity = 0.9 if name == st.session_state.selected_city else 0.6

        popup_content = f"""
            <div style="font-family: Poppins; padding: 0.5rem; background: #1a1a1a; color: white;">
                <h4 style="margin: 0 0 0.5rem 0; color: #DC143C;">{name}</h4>
                <p style="margin: 0.25rem 0; font-size: 20px; font-weight: bold; color: {color};">AQI: {aqi}</p>
                <p style="margin: 0.25rem 0; color: #b8b8b8;">Status: {status}</p>
                <p style="margin: 0.25rem 0; color: #888888;">Type: {station_type.title()}</p>
            </div>
        """

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            popup=folium.Popup(popup_content, max_width=250),
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=fillOpacity,
            weight=weight
        ).add_to(m)

    LocateControl().add_to(m)

    return m

# Navigation header
st.markdown("""
    <div class="nav-container">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="logo-container">
                <div class="logo-icon"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#7f1d1d" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 0 20 15.3 15.3 0 0 1 0-20z"/></svg></div>
                <div class="logo-text">AQI Monitor</div>
            </div>
            <div style="display: flex; gap: 1rem; align-items: center;">
                <div style="color: #a0a0a0; font-size: 14px; font-weight: 500;">
                    <span class="status-indicator status-good"></span>
                    Demo Interface
                </div>
                <div style="color: #707070; font-size: 13px;">
                    Rendered: """ + datetime.now().strftime('%H:%M') + """
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# Navigation buttons
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    if st.button("Dashboard", key="dashboard_btn_1"):
        st.session_state.selected_page = 'Dashboard'
with col2:
    if st.button("Map", key="map_btn_1"):
        st.session_state.selected_page = 'Map'
with col3:
    if st.button("News", key="news_btn_1"):
        st.session_state.selected_page = 'News'
with col4:
    if st.button("Scale", key="scale_btn_1"):
        st.session_state.selected_page = 'Scale'
with col5:
    if st.button("Forecast", key="forecast_btn_1"):
        st.session_state.selected_page = 'Forecast'
with col6:
    if st.button("History", key="history_btn_1"):
        st.session_state.selected_page = 'History'
with col7:
    if st.button("Alerts", key="alerts_btn_1"):
        st.session_state.selected_page = 'Alerts'

st.markdown("<br>", unsafe_allow_html=True)

# Page content based on selection
if st.session_state.selected_page == 'Dashboard':
    st.markdown('''
    <div class="hero-section">
        <div class="hero-title">Air Quality Monitor</div>
        <div class="hero-subtitle">Demo air quality monitoring across Bengaluru - Simulated data supported</div>
    ''', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    cities = sorted(list(BANGALORE_AREAS.keys())) + [station['name'] for station in BANGALORE_STATIONS]
    with col2:
        st.session_state.selected_city = st.selectbox("Select City", cities, label_visibility="collapsed")
        
    try:
        # Use session state API key if available
        if st.session_state.openaq_api_key:
            openaq = OpenAQFetcher(api_key=st.session_state.openaq_api_key)
        else:
            openaq = openaq_fetcher
        
        aqi_data_openaq = openaq.get_aqi_data(city="Bangalore")
        
        selected_station_data = None
        for station in BANGALORE_STATIONS:
            if station['name'] == st.session_state.selected_city:
                for location_name, location_data in aqi_data_openaq.items():
                    if station['name'].lower() in location_name.lower():
                        selected_station_data = location_data
                        break
        
        if selected_station_data:
            current_aqi = selected_station_data.get('aqi', 0)
            gradient, status, color, emoji = get_aqi_color_gradient(current_aqi)
            data_source = "OpenAQ API" if st.session_state.openaq_api_key else "Mock Data"
            
            st.markdown(f"""
            <div style="background: {gradient}; padding: 15px; border-radius: 10px; margin: 10px 0; text-align: center;">
                <h2 style="margin: 0; color: white;">Demo AQI for {st.session_state.selected_city}: {current_aqi}</h2>
                <p style="margin: 5px 0; color: white;">Status: {status}</p>
                <p style="margin: 0; color: white; font-size: 0.8em;">Source: {data_source} | Rendered: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            current_aqi = random.randint(50, 200)
            gradient, status, color, emoji = get_aqi_color_gradient(current_aqi)
            data_source = "Mock Data"
            
            if not st.session_state.openaq_api_key:
                st.warning("Enter your OpenAQ API key in the sidebar to get OpenAQ data")
            
            st.markdown(f"""
            <div style="background: {gradient}; padding: 15px; border-radius: 10px; margin: 10px 0; text-align: center;">
                <h2 style="margin: 0; color: white;">Simulated AQI for {st.session_state.selected_city}: {current_aqi}</h2>
                <p style="margin: 5px 0; color: white;">Status: {status}</p>
                <p style="margin: 0; color: white; font-size: 0.8em;">Source: {data_source} | Randomly generated demonstration value</p>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error fetching AQI data: {str(e)}")
        current_aqi = random.randint(50, 200)
        gradient, status, color, emoji = get_aqi_color_gradient(current_aqi)

    st.markdown('</div>', unsafe_allow_html=True)
    
    data = generate_calculated_data()
    
    st.markdown('''
    <div class="card">
        <div class="card-title">Demonstration Air Quality Metrics</div>
    ''', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">AQI</div>
                <div class="metric-value" style="color: {color};">{current_aqi}</div>
                <div class="metric-unit">{status}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        pm25 = random.randint(30, 120)
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">PM2.5</div>
                <div class="metric-value" style="color: #3b82f6;">{pm25}</div>
                <div class="metric-unit">µg/m³</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        pm10 = random.randint(50, 150)
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">PM10</div>
                <div class="metric-value" style="color: #8b5cf6;">{pm10}</div>
                <div class="metric-unit">µg/m³</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        temp = random.randint(15, 35)
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Temperature</div>
                <div class="metric-value" style="color: #f59e0b;">{temp}°C</div>
                <div class="metric-unit">Celsius</div>
            </div>
        """, unsafe_allow_html=True)

    with col5:
        humidity = random.randint(40, 80)
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Humidity</div>
                <div class="metric-value" style="color: #06b6d4;">{humidity}%</div>
                <div class="metric-unit">Relative</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('''
    <div class="card">
        <div class="card-title">Demo Air Quality Map</div>
        <p style="color: #888888; margin-bottom: 1.5rem;">Interactive map showing AQI levels across Bangalore monitoring stations</p>
    ''', unsafe_allow_html=True)

    with st.spinner('Loading map...'):
        m = create_map()
        st_folium(m, width=None, height=500, returned_objects=[])

    st.markdown("""
        <div style="display: flex; justify-content: space-around; margin-top: 1.5rem; flex-wrap: wrap; gap: 1rem;">
            <div style="text-align: center;">
                <div style="width: 30px; height: 30px; background: linear-gradient(135deg, #10b981 0%, #34d399 100%); border-radius: 50%; margin: 0 auto 0.5rem; box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);"></div>
                <div style="font-size: 11px; font-weight: 600; color: #b8b8b8;">Good</div>
            </div>
            <div style="text-align: center;">
                <div style="width: 30px; height: 30px; background: linear-gradient(135deg, #fbbf24 0%, #fde047 100%); border-radius: 50%; margin: 0 auto 0.5rem; box-shadow: 0 0 10px rgba(251, 191, 36, 0.5);"></div>
                <div style="font-size: 11px; font-weight: 600; color: #b8b8b8;">Moderate</div>
            </div>
            <div style="text-align: center;">
                <div style="width: 30px; height: 30px; background: linear-gradient(135deg, #f97316 0%, #fb923c 100%); border-radius: 50%; margin: 0 auto 0.5rem; box-shadow: 0 0 10px rgba(249, 115, 22, 0.5);"></div>
                <div style="font-size: 11px; font-weight: 600; color: #b8b8b8;">Poor</div>
            </div>
            <div style="text-align: center;">
                <div style="width: 30px; height: 30px; background: linear-gradient(135deg, #ef4444 0%, #f87171 100%); border-radius: 50%; margin: 0 auto 0.5rem; box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);"></div>
                <div style="font-size: 11px; font-weight: 600; color: #b8b8b8;">Unhealthy</div>
            </div>
            <div style="text-align: center;">
                <div style="width: 30px; height: 30px; background: linear-gradient(135deg, #a855f7 0%, #c084fc 100%); border-radius: 50%; margin: 0 auto 0.5rem; box-shadow: 0 0 10px rgba(168, 85, 247, 0.5);"></div>
                <div style="font-size: 11px; font-weight: 600; color: #b8b8b8;">Severe</div>
            </div>
            <div style="text-align: center;">
                <div style="width: 30px; height: 30px; background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%); border-radius: 50%; margin: 0 auto 0.5rem; box-shadow: 0 0 10px rgba(127, 29, 29, 0.5);"></div>
                <div style="font-size: 11px; font-weight: 600; color: #b8b8b8;">Hazardous</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('''
        <div class="card">
            <div class="card-title">24-Hour AQI Trend Analysis</div>
        ''', unsafe_allow_html=True)

        last_24h = data.tail(24)
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=last_24h['timestamp'],
            y=last_24h['aqi'],
            mode='lines',
            name='AQI',
            line=dict(color='#DC143C', width=3, shape='spline'),
            fill='tonexty',
            fillcolor='rgba(220, 20, 60, 0.2)'
        ))

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="",
            yaxis_title="AQI Value",
            hovermode='x unified',
            showlegend=False,
            height=350,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=True, gridcolor='rgba(139, 0, 0, 0.1)', color='#a0a0a0'),
            yaxis=dict(showgrid=True, gridcolor='rgba(139, 0, 0, 0.1)', color='#a0a0a0'),
            font=dict(color='#a0a0a0')
        )

        st.plotly_chart(fig, use_container_width=True, key="aqi_trend_chart")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('''
        <div class="card">
            <div class="card-title">Pollutant Breakdown</div>
        ''', unsafe_allow_html=True)

        pollutants_data = pd.DataFrame({
            'Pollutant': ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3'],
            'Value': [
                random.uniform(30, 70),
                random.uniform(50, 100),
                random.uniform(20, 50),
                random.uniform(10, 30),
                random.uniform(0.5, 2.0),
                random.uniform(30, 70)
            ]
        })

        colors = ['#DC143C', '#8B0000', '#FF6B6B', '#B22222', '#CD5C5C', '#F08080']

        fig = go.Figure(data=[go.Bar(
            x=pollutants_data['Value'],
            y=pollutants_data['Pollutant'],
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(color='rgba(139, 0, 0, 0.3)', width=1)
            ),
            text=pollutants_data['Value'].round(1),
            textposition='outside',
            textfont=dict(color='#a0a0a0')
        )])

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="",
            yaxis_title="",
            height=350,
            margin=dict(l=0, r=10, t=0, b=0),
            showlegend=False,
            xaxis=dict(color='#a0a0a0'),
            yaxis=dict(color='#a0a0a0'),
            font=dict(color='#a0a0a0')
        )
        
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('''
    <div class="card">
        <div class="card-title">Health Recommendations</div>
    ''', unsafe_allow_html=True)

    if current_aqi <= 100:
        st.markdown("""
        <div class='info-box'>
        <h3 style="margin-top: 0; color: #3b82f6; font-size: 20px;">Air Quality is Good</h3>
        <ul style="margin-bottom: 0; color: #b8b8b8; line-height: 1.8;">
            <li>Air quality is considered satisfactory and poses little to no risk</li>
            <li>Perfect time for outdoor activities and exercise</li>
            <li>Open windows for natural ventilation</li>
            <li>Great day for children to play outside</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    elif current_aqi <= 200:
        st.markdown("""
        <div class='warning-box'>
        <h3 style="margin-top: 0; color: #f59e0b; font-size: 20px;">Moderate Health Concern</h3>
        <ul style="margin-bottom: 0; color: #b8b8b8; line-height: 1.8;">
            <li>Sensitive groups may experience health effects</li>
            <li>Consider reducing prolonged outdoor activities</li>
            <li>People with respiratory issues should be cautious</li>
            <li>Monitor symptoms and take breaks if needed</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='danger-box'>
        <h3 style="margin-top: 0; color: #ef4444; font-size: 20px;">Health Alert - Take Action</h3>
        <ul style="margin-bottom: 0; color: #b8b8b8; line-height: 1.8;">
            <li>Everyone may experience serious health effects</li>
            <li>Avoid outdoor activities completely</li>
            <li>Keep windows closed and use air purifiers</li>
            <li>Wear N95 masks if going outside is necessary</li>
            <li>Stay hydrated and monitor your health closely</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.selected_page == 'Map':
    st.markdown('''
    <div class="card">
        <div class="card-title">Demo Air Quality Map</div>
        <p style="color: #888888; margin-bottom: 1.5rem;">Interactive map showing AQI levels across Bangalore monitoring stations</p>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        location_query = st.text_input("Search for a location", placeholder="e.g., Koramangala, Bangalore")
    with col2:
        search_clicked = st.button("Search Nearby", use_container_width=True)

    # Initialize session state for search results
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'nearby_stations' not in st.session_state:
        st.session_state.nearby_stations = []

    if search_clicked:
        if not location_query or len(location_query) < 3:
            st.error("Please enter at least 3 characters for search")
            st.session_state.search_results = None
            st.session_state.nearby_stations = []
        else:
            try:
                coords = location_search.get_city_coordinates(location_query)
                if coords:
                    st.success(f"Found location: {location_query}")
                    st.session_state.search_results = coords

                    # Find nearby stations
                    nearby = location_search.find_nearby_stations(
                        coords['latitude'], coords['longitude'], BANGALORE_STATIONS, max_distance_km=20
                    )
                    st.session_state.nearby_stations = nearby[:1]  # Nearest station only
                else:
                    st.warning("Location not found. Try a different search.")
                    st.session_state.search_results = None
                    st.session_state.nearby_stations = []
            except Exception as e:
                st.error(f"Search failed: {str(e)}")
                st.session_state.search_results = None
                st.session_state.nearby_stations = []

    # Display nearby stations if available
    if st.session_state.nearby_stations:
        st.markdown('''
        <div class="card">
            <div class="card-title">Nearest Monitoring Stations</div>
        ''', unsafe_allow_html=True)

        # Get AQI data for comparison
        openaq = OpenAQFetcher()
        aqi_data_openaq = openaq.get_aqi_data(city="Bangalore")

        for i, station in enumerate(st.session_state.nearby_stations, 1):
            station_aqi_data = None
            for location_name, location_data in aqi_data_openaq.items():
                if station['name'].lower() in location_name.lower():
                    station_aqi_data = location_data
                    break

            if station_aqi_data:
                reported_aqi = station_aqi_data.get('aqi', 0)
                # Calculate AQI from pollutants (simplified)
                pm25 = station_aqi_data.get('pm25', {}).get('value', 0)
                pm10 = station_aqi_data.get('pm10', {}).get('value', 0)
                calculated_aqi, _ = calculate_aqi(pm25, pm10)
            else:
                reported_aqi = random.randint(50, 200)
                pm25 = random.uniform(20, 80)
                pm10 = random.uniform(40, 120)
                calculated_aqi, _ = calculate_aqi(pm25, pm10)

            # Get AQI category and color
            _, status, color, _ = get_aqi_color_gradient(reported_aqi)

            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.markdown(f"**{i}. {station['name']}**")
                st.caption(f"Distance: {station['distance_km']:.1f} km")
            with col2:
                st.markdown(f"**Reported AQI:** {reported_aqi}")
                st.markdown(f"<span style='color:{color}; font-weight:bold;'>{status}</span>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"**Calculated AQI:** {calculated_aqi}")
                diff = calculated_aqi - reported_aqi
                color_diff = "#10b981" if abs(diff) < 10 else "#f59e0b" if abs(diff) < 30 else "#ef4444"
                st.markdown(f"<span style='color:{color_diff};'>Diff: {diff:+d}</span>", unsafe_allow_html=True)
            with col4:
                st.markdown("**Pollutants:**")
                st.caption(f"PM2.5: {pm25:.1f} µg/m³")
                st.caption(f"PM10: {pm10:.1f} µg/m³")

        st.markdown('</div>', unsafe_allow_html=True)

    with st.spinner('Loading map...'):
        m = create_map()
        st_folium(m, width=None, height=600, returned_objects=[])

    st.markdown('</div>', unsafe_allow_html=True)

    # Science section with formulas
    st.markdown('''
    <div class="card">
        <div class="card-title">Learn the Science</div>
        <p style="color: #888888; margin-bottom: 2rem;">Mathematical formulas used for AQI calculations and distance measurements</p>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### EPA AQI Calculation Formula")
        st.markdown("""
        The Air Quality Index (AQI) is calculated using the following formula:

        **AQI = ((AQI_high - AQI_low) / (Conc_high - Conc_low)) × (Conc - Conc_low) + AQI_low**

        Where:
        - **AQI_high** and **AQI_low**: AQI breakpoint values
        - **Conc_high** and **Conc_low**: Pollutant concentration breakpoints
        - **Conc**: Actual pollutant concentration

        #### AQI Breakpoints for PM2.5:
        | AQI Range | PM2.5 (µg/m³) | Category |
        |-----------|---------------|----------|
        | 0-50 | 0-12.0 | Good |
        | 51-100 | 12.1-35.4 | Moderate |
        | 101-150 | 35.5-55.4 | Unhealthy for Sensitive Groups |
        | 151-200 | 55.5-150.4 | Unhealthy |
        | 201-300 | 150.5-250.4 | Very Unhealthy |
        | 301-500 | 250.5-500.4 | Hazardous |
        """)

    with col2:
        st.markdown("### Haversine Distance Formula")
        st.markdown("""
        The distance between two points on Earth is calculated using the Haversine formula:

        **d = 2r × arcsin(√(sin²((lat₂-lat₁)/2) + cos(lat₁) × cos(lat₂) × sin²((lon₂-lon₁)/2)))**

        Where:
        - **r**: Earth's radius (6,371 km)
        - **lat₁, lon₁**: Latitude and longitude of first point
        - **lat₂, lon₂**: Latitude and longitude of second point

        #### Why Haversine?
        - Accounts for Earth's spherical shape
        - More accurate than simple Euclidean distance
        - Essential for geographic distance calculations
        - Used to find nearest monitoring stations within 20km radius
        """)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.selected_page == 'News':
    st.markdown('''
    <div class="hero-section">
        <div class="hero-title">Air Quality News</div>
        <div class="hero-subtitle">Latest updates and insights on air quality across India</div>
    </div>
    ''', unsafe_allow_html=True)

    news_articles = [
        {
            'badge': 'Breaking',
            'title': 'Delhi Air Quality Reaches Severe Levels Amid Winter Pollution',
            'date': 'November 2, 2025',
            'summary': 'Air quality in Delhi has deteriorated to severe levels as winter pollution sets in. Authorities have issued health advisories and implemented emergency measures including odd-even vehicle restrictions.'
        },
        {
            'badge': 'Update',
            'title': 'Mumbai Sees Improvement in Air Quality After Heavy Rains',
            'date': 'November 1, 2025',
            'summary': 'Recent rainfall in Mumbai has led to a significant improvement in air quality. PM2.5 levels have dropped by 40% compared to last week, providing relief to residents.'
        },
        {
            'badge': 'Research',
            'title': 'New Study Links Air Pollution to Increased Respiratory Diseases',
            'date': 'October 31, 2025',
            'summary': 'A comprehensive study by IIT researchers reveals a strong correlation between prolonged exposure to poor air quality and respiratory ailments in urban areas.'
        }
    ]

    for article in news_articles:
        st.markdown(f"""
        <div class="news-card">
            <div class="news-badge">{article['badge']}</div>
            <div class="news-title">{article['title']}</div>
            <div class="news-date">{article['date']}</div>
            <div class="news-summary">{article['summary']}</div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.selected_page == 'Scale':
    st.markdown('''
    <div class="hero-section">
        <div class="hero-title">AQI Scale Guide</div>
        <div class="hero-subtitle">Understanding the Air Quality Index and its health implications</div>
    </div>
    ''', unsafe_allow_html=True)

    aqi_levels = [
        {
            'gradient': 'linear-gradient(135deg, rgba(16, 185, 129, 0.7) 0%, rgba(52, 211, 153, 0.4) 100%)',
            'title': 'Good',
            'range': '0-50',
            'description': 'Air quality is satisfactory, and air pollution poses little or no risk. Perfect for outdoor activities.'
        },
        {
            'gradient': 'linear-gradient(135deg, rgba(251, 191, 36, 0.7) 0%, rgba(253, 224, 71, 0.4) 100%)',
            'title': 'Moderate',
            'range': '51-100',
            'description': 'Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.'
        },
        {
            'gradient': 'linear-gradient(135deg, rgba(249, 115, 22, 0.7) 0%, rgba(251, 146, 60, 0.4) 100%)',
            'title': 'Unhealthy for Sensitive Groups',
            'range': '101-150',
            'description': 'Members of sensitive groups may experience health effects. The general public is less likely to be affected.'
        },
        {
            'gradient': 'linear-gradient(135deg, rgba(239, 68, 68, 0.7) 0%, rgba(248, 113, 113, 0.4) 100%)',
            'title': 'Unhealthy',
            'range': '151-200',
            'description': 'Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.'
        },
        {
            'gradient': 'linear-gradient(135deg, rgba(168, 85, 247, 0.7) 0%, rgba(192, 132, 252, 0.4) 100%)',
            'title': 'Very Unhealthy',
            'range': '201-300',
            'description': 'Health alert: The risk of health effects is increased for everyone. Outdoor activities should be avoided.'
        },
        {
            'gradient': 'linear-gradient(135deg, rgba(127, 29, 29, 0.7) 0%, rgba(153, 27, 27, 0.4) 100%)',
            'title': 'Hazardous',
            'range': '300+',
            'description': 'Health warning of emergency conditions: everyone is more likely to be affected. Stay indoors and use air purifiers.'
        }
    ]

    for level in aqi_levels:
        st.markdown(f"""
        <div class="aqi-level-card" style="background: {level['gradient']};">
            <div class="aqi-level-title">{level['title']}</div>
            <div class="aqi-level-range">AQI Range: {level['range']}</div>
            <div class="aqi-level-desc">{level['description']}</div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.selected_page == 'Forecast':
    st.markdown('''
    <div class="hero-section">
        <div class="hero-title">AQI Forecast</div>
        <div class="hero-subtitle">Air quality forecasting using ML models</div>
    </div>
    ''', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["7-Day Trend Forecast", "Model Forecast"])
    
    with tab1:
        forecast_days = 7
        forecast_dates = [(datetime.now() + timedelta(days=i)).strftime('%b %d') for i in range(forecast_days)]
        forecast_aqi = [random.randint(50, 200) for _ in range(forecast_days)]

        st.markdown('''
        <div class="card">
            <div class="card-title">7-Day AQI Trend Forecast</div>
        ''', unsafe_allow_html=True)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=forecast_aqi,
            mode='lines+markers',
            name='Forecasted AQI',
            line=dict(color='#DC143C', width=3),
            marker=dict(size=10, color='#DC143C', line=dict(color='white', width=2)),
            fill='tozeroy',
            fillcolor='rgba(220, 20, 60, 0.2)'
        ))

        fig.add_hline(y=50, line_dash="dash", line_color="#10b981", annotation_text="Good",
                     annotation_position="right")
        fig.add_hline(y=100, line_dash="dash", line_color="#fbbf24", annotation_text="Moderate",
                     annotation_position="right")
        fig.add_hline(y=150, line_dash="dash", line_color="#f97316", annotation_text="Poor",
                     annotation_position="right")
        fig.add_hline(y=200, line_dash="dash", line_color="#ef4444", annotation_text="Unhealthy",
                     annotation_position="right")

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Date",
            yaxis_title="AQI Value",
            hovermode='x unified',
            showlegend=False,
            height=400,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=True, gridcolor='rgba(139, 0, 0, 0.1)', color='#a0a0a0'),
            yaxis=dict(showgrid=True, gridcolor='rgba(139, 0, 0, 0.1)', color='#a0a0a0'),
            font=dict(color='#a0a0a0')
        )
        
        st.plotly_chart(fig, use_container_width=True, key="forecast_chart")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab2:
        # Check if ensemble models exist
        model_files = [
            'models/random_forest.pkl',
            'models/gradient_boosting.pkl',
            'models/lstm_advanced_best.h5',
            'models/sklearn_scaler.pkl'
        ]

        models_available = all(os.path.exists(f) for f in model_files)

        if models_available and PREDICTOR_AVAILABLE and predictor.models_loaded:
            st.info('Demonstration projection: applies a saved ensemble trend with hand-written time-of-day adjustments. Inputs may be simulated or cached. This is not a validated forecast.')
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Ensemble-guided demonstration projection</div>', unsafe_allow_html=True)
            
            # Station selection dropdown
            trained_stations = [
                'Bapuji Nagar', 'BTM Layout', 'BWSSB Kadabesanahalli', 'City Railway Station',
                'Hebbal', 'Hombegowda Nagar', 'Jayanagar 5th Block', 'Jigani Industrial Area',
                'Kasturi Nagar RTO', 'Kaviika Mysore Road', 'NIMHANS', 'Nisarga Bhavan',
                'Peenya Industrial Area', 'RV Engineering College', 'Silk Board'
            ]
            
            # Default to dashboard city if it's in trained stations, otherwise use BTM Layout
            default_index = 1  # BTM Layout default
            if st.session_state.selected_city in trained_stations:
                default_index = trained_stations.index(st.session_state.selected_city)
            elif st.session_state.selected_forecast_station in trained_stations:
                default_index = trained_stations.index(st.session_state.selected_forecast_station)
            
            selected_station = st.selectbox(
                "Select Station for Forecast", 
                trained_stations, 
                index=default_index,
                key="forecast_station_select"
            )
            
            # Update session state
            st.session_state.selected_forecast_station = selected_station

            # Get current AQI data for prediction
            try:
                # Use the same OpenAQ fetcher as dashboard for consistency
                if st.session_state.openaq_api_key:
                    current_openaq = OpenAQFetcher(api_key=st.session_state.openaq_api_key)
                else:
                    current_openaq = openaq_fetcher
                
                # Get fresh data from OpenAQ
                aqi_data_openaq = current_openaq.get_aqi_data(city="Bangalore")
                
                # Find matching station data from OpenAQ response
                station_info = None
                if aqi_data_openaq and isinstance(aqi_data_openaq, dict):
                    for location_name, location_data in aqi_data_openaq.items():
                        if selected_station.lower() in location_name.lower():
                            station_info = {
                                'aqi': location_data.get('aqi', 0),
                                'pollutants': location_data.get('pollutants', {}),
                                'station_name': location_name,
                                'station_type': 'residential'  # Default type
                            }
                            break
                
                # If no match in OpenAQ data, try cache file as fallback
                if not station_info:
                    cache_file = 'bangalore_aqi_cache.json'
                    if os.path.exists(cache_file):
                        with open(cache_file, 'r') as f:
                            cache_data = json.load(f)
                            station_data = cache_data.get('data', [])
                        
                        if station_data:
                            for station in station_data:
                                if selected_station.lower() in station.get('station_name', '').lower():
                                    station_info = station
                                    break
                            
                            if not station_info:
                                station_info = station_data[0]
                
                if station_info:
                    # Get current AQI first
                    current_aqi = station_info['aqi']
                    category, color, _ = get_aqi_category(current_aqi)
                    
                    # Prepare current data for prediction with station-specific values
                    current_data = {
                        'pm25': station_info['pollutants'].get('pm25', 20),
                        'pm10': station_info['pollutants'].get('pm10', 30),
                        'no2': station_info['pollutants'].get('no2', 15),
                        'so2': station_info['pollutants'].get('so2', 5),
                        'co': station_info['pollutants'].get('co', 0.5),
                        'o3': station_info['pollutants'].get('o3', 30),
                        'temperature': 28,
                        'humidity': 65,
                        'wind_speed': 8,
                        'hour': datetime.now().hour,
                        'day_of_week': datetime.now().weekday(),
                        'day_of_year': datetime.now().timetuple().tm_yday
                    }
                    
                    # Add station-specific variation based on station type
                    station_type = station_info.get('station_type', 'residential')
                    if station_type == 'traffic':
                        current_data['pm25'] *= 1.3
                        current_data['no2'] *= 1.5
                    elif station_type == 'industrial':
                        current_data['pm10'] *= 1.4
                        current_data['so2'] *= 1.6
                    
                    # Add station-specific random variation for uniqueness
                    import hashlib
                    station_hash = int(hashlib.md5(selected_station.encode()).hexdigest()[:8], 16)
                    variation_factor = 0.8 + (station_hash % 40) / 100  # 0.8 to 1.2 variation
                    
                    current_data['pm25'] *= variation_factor
                    current_data['pm10'] *= variation_factor
                    current_data['no2'] *= variation_factor
                    
                    # Make predictions for future hours using current AQI as base
                    predictions = predictor.predict_future_hours(current_data, current_aqi, hours_ahead=[1, 6, 12, 24])
                    
                    if predictions:
                        # Display current AQI
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Input AQI (may be simulated)", f"{current_aqi}", delta=category)
                        col2.metric("1-Hour Demo Projection", f"{predictions[1]:.1f}")
                        col3.metric("6-Hour Demo Projection", f"{predictions[6]:.1f}")
                        
                        # Create prediction chart
                        prediction_times = [pd.Timestamp.now() + pd.Timedelta(hours=h) for h in sorted(predictions.keys())]
                        prediction_values = [predictions[h] for h in sorted(predictions.keys())]
                        
                        fig_predictions = go.Figure()
                        
                        # Add current point
                        fig_predictions.add_trace(go.Scatter(
                            x=[pd.Timestamp.now()],
                            y=[current_aqi],
                            mode='markers',
                            name='Input AQI (may be simulated)',
                            marker=dict(size=15, color=color, line=dict(color='white', width=2))
                        ))
                        
                        # Add predictions
                        fig_predictions.add_trace(go.Scatter(
                            x=prediction_times,
                            y=prediction_values,
                            mode='lines+markers',
                            name='Predicted AQI',
                            line=dict(color='#1E90FF', width=3),
                            marker=dict(size=10, color='#1E90FF', line=dict(color='white', width=2))
                        ))
                        
                        fig_predictions.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis_title="Time",
                            yaxis_title="AQI Value",
                            hovermode='x unified',
                            showlegend=False,
                            height=400,
                            margin=dict(l=0, r=0, t=0, b=0),
                            xaxis=dict(showgrid=True, gridcolor='rgba(139, 0, 0, 0.1)', color='#a0a0a0'),
                            yaxis=dict(showgrid=True, gridcolor='rgba(139, 0, 0, 0.1)', color='#a0a0a0'),
                            font=dict(color='#a0a0a0')
                        )
                        st.plotly_chart(fig_predictions, use_container_width=True, key="model_predictions_line_chart")

            except Exception as e:
                st.error(f"Error loading models or making predictions: {str(e)}")
                st.info("Please ensure all model files are present and data is properly formatted.")

            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("AI models not found. Using fallback predictions.")
            st.info("Model artifacts are included in models/. The original training pipeline is not included, and the saved metrics have not been independently reproduced.")

elif st.session_state.selected_page == 'History':
    st.markdown(f'''
    <div class="hero-section">
        <div class="hero-title">Simulated Historical Data</div>
        <div class="hero-subtitle">Generated demonstration trends for {st.session_state.selected_city}</div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
    <div class="card">
        <div class="card-title">Select Time Range</div>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        time_range = st.selectbox('Time Period', ['Last 7 Days', 'Last 30 Days', 'Last 90 Days', 'Last Year'])
    with col2:
        pollutant = st.selectbox('Pollutant', ['AQI', 'PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3'])

    st.markdown('</div>', unsafe_allow_html=True)

    if time_range == 'Last 7 Days':
        days = 7
    elif time_range == 'Last 30 Days':
        days = 30
    elif time_range == 'Last 90 Days':
        days = 90
    else:
        days = 365

    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    values = np.random.randint(30, 200, size=days) if pollutant == 'AQI' else np.random.randint(10, 150, size=days)

    st.markdown(f'''
    <div class="card">
        <div class="card-title">{pollutant} Trend - {time_range}</div>
    ''', unsafe_allow_html=True)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines',
        name=pollutant,
        line=dict(color='#DC143C', width=2),
        fill='tozeroy',
        fillcolor='rgba(220, 20, 60, 0.2)'
    ))

    if days >= 7:
        ma = pd.Series(values).rolling(window=7).mean()
        fig.add_trace(go.Scatter(
            x=dates,
            y=ma,
            mode='lines',
            name='7-Day Moving Average',
            line=dict(color='#FF6B6B', width=3, dash='dash')
        ))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Date",
        yaxis_title=f"{pollutant} Value",
        hovermode='x unified',
        height=400,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=True, gridcolor='rgba(139, 0, 0, 0.1)', color='#a0a0a0'),
        yaxis=dict(showgrid=True, gridcolor='rgba(139, 0, 0, 0.1)', color='#a0a0a0'),
        font=dict(color='#a0a0a0'),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#a0a0a0'))
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.selected_page == 'Alerts':
    st.markdown('''
    <div class="hero-section">
        <div class="hero-title">Example Alert Cards</div>
        <div class="hero-subtitle">Interface demonstration only. No background monitoring or notifications are sent.</div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
    <div class="card">
        <div class="card-title">Alert Preferences</div>
    ''', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        alert_threshold = st.selectbox('Alert when AQI exceeds', ['100', '150', '200', '250', '300'])
    with col2:
        alert_frequency = st.selectbox('Alert Frequency', ['Demo', 'Hourly', 'Daily', 'Weekly'])
    with col3:
        alert_types = st.multiselect('Alert Types', ['AQI Levels', 'Health Advisories', 'Weather Impact', 'Policy Changes'],
                                   default=['AQI Levels', 'Health Advisories'])

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('''
    <div class="card">
        <div class="card-title">Example Alerts (not current conditions)</div>
    ''', unsafe_allow_html=True)

    alerts = [
        {
            'level': 'danger',
            'title': 'High Pollution Alert - Bangalore Central',
            'message': 'AQI has reached 185 (Unhealthy). Sensitive groups should avoid outdoor activities.',
            'time': '2 hours ago',
            'location': 'Bangalore Central'
        },
        {
            'level': 'warning',
            'title': 'Moderate Pollution Alert - Koramangala',
            'message': 'AQI at 120 (Unhealthy for Sensitive Groups). Consider limiting prolonged outdoor exposure.',
            'time': '4 hours ago',
            'location': 'Koramangala'
        }
    ]

    for alert in alerts:
        alert_class = {
            'danger': 'danger-box',
            'warning': 'warning-box',
            'info': 'info-box'
        }.get(alert['level'], 'info-box')

        st.markdown(f"""
        <div class="{alert_class}" style="margin-bottom: 1rem;">
            <h4 style="margin-top: 0; font-size: 18px; font-weight: 700;">{alert['title']}</h4>
            <p style="margin-bottom: 0.5rem; line-height: 1.6;">{alert['message']}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #888888;">
                <span>{alert['location']}</span>
                <span>{alert['time']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)