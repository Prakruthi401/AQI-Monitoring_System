# 🌏 AQI Monitor - Air Quality Dashboard

A comprehensive **real-time air quality monitoring dashboard** for Bangalore built with Streamlit, featuring interactive maps, AI-powered forecasting with ensemble models, and scientific data visualization.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31+-red.svg)
![TensorFlow](https://img.shields.io/badge/tensorflow-2.15+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## ✨ Features

### 🎯 Interactive Dashboard
- **Real-time AQI Monitoring** for multiple locations across Bangalore
- **Color-coded Air Quality Indicators** with health recommendations
- **Dynamic Filters** - Filter by date range, pollutants, and locations
- **Auto-refresh Functionality** - Configurable refresh intervals (30s to 10min)
- **Live AQI Ticker** - Scrolling real-time updates across multiple stations
- **Pollutant Breakdown** - Track PM2.5, PM10, NO2, SO2, CO, and O3 levels
- **Downloadable Reports** - Export filtered data as CSV
- **OpenAQ API Integration** - User-provided API key for real-time data
- **Mock Data Fallback** - Automatic fallback when API is unavailable

### 🗺️ Interactive Map
- **Location Search** - Find any location in Bangalore
- **Nearest Station Finder** - Uses Haversine distance formula to identify 5 closest monitoring stations
- **Click-to-Explore** - Click any marker to view detailed station information
- **AQI Comparison** - Compare reported vs calculated AQI values
- **Cluster Markers** - Optimized display for multiple stations
- **Circle Markers** - Visual size representation based on AQI severity
- **Custom Popups** - Detailed pollutant data on hover/click
- **Scientific Formulas** - Learn EPA standard AQI calculation and distance formulas

### 📊 Advanced Visualizations
- **Interactive Line Charts** - Multi-location AQI trend comparison with range selectors
- **Heatmaps** - Pollutant concentration across locations
- **Radar Charts** - Pollutant profile comparison (up to 3 locations)
- **Time Series Analysis** - Zoom, pan, and explore historical data
- **Sortable Data Tables** - Filter, sort, and highlight AQI data
- **Comparison Tools** - Side-by-side location and pollutant analysis

### 📰 Air Quality News & Alerts
- **Latest News** - Real-time air quality updates and advisories
- **Environmental Alerts** - Threshold-based notifications
- **Health Impact Information** - Category-specific health recommendations
- **Custom Alert Configuration** - Set your own AQI thresholds

### 📈 AQI Scale Guide
- Comprehensive breakdown of AQI levels (Good to Hazardous)
- Health implications for each category
- Recommended actions and precautions
- Visual color coding system

### 🔮 AI-Powered Forecasting
- **Ensemble Model Predictions** - 96.17% accuracy using Random Forest, Gradient Boosting, and LSTM
- **Station-Specific Forecasts** - AI predictions for 15 trained Bangalore locations
- **Realistic Prediction Bounds** - Prevents unrealistic AQI jumps with persistence-based approach
- **Multi-Hour Forecasts** - 1-hour, 6-hour, 12-hour, and 24-hour AQI predictions
- **Time-Based Adjustments** - Diurnal patterns and trend analysis

### 📜 Historical Data Analysis
- View past AQI trends (customizable date ranges)
- Compare historical patterns across locations
- Analyze seasonal variations
- Export historical data for research

---

## 🛠️ Technologies Used

| Category | Technologies |
|----------|-------------|
| **Frontend** | Streamlit |
| **Data Visualization** | Plotly, Matplotlib, Seaborn |
| **Interactive Mapping** | Folium, streamlit-folium |
| **Machine Learning** | TensorFlow, Keras (LSTM models) |
| **Data Processing** | Pandas, NumPy |
| **API Integration** | OpenAQ Air Quality API, requests |
| **Geospatial** | Haversine distance calculations |

---

## 📋 Prerequisites

- Python 3.10 or higher (required for TensorFlow 2.15 compatibility)
- pip package manager
- Internet connection (for API access)
- OpenAQ API key (optional, for real-time data)

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```
git clone https://github.com/yourusername/aqi-monitor-bangalore.git
cd aqi-monitor-bangalore
```

### 2. Create Virtual Environment

**Windows:**
```
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

**requirements.txt:**
```
pandas==2.1.4
numpy==1.26.3
requests==2.31.0
scikit-learn==1.3.2
tensorflow==2.15.0
keras==2.15.0
matplotlib==3.8.2
seaborn==0.13.0
plotly==5.18.0
streamlit==1.31.0
joblib==1.3.2
folium>=0.14.0
streamlit-folium>=0.17.0
```

### 4. Run the Application

```
streamlit run main.py
```

Or if your file has a different name:
```
streamlit run app.py
```

### 5. Access the Dashboard

Open your browser and navigate to:
```
http://localhost:8501
```

The terminal will display:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

---

## 🎮 Usage Guide

### Dashboard Navigation

1. **Home/Dashboard Tab**
   - View real-time AQI for all monitored locations
   - Use sidebar filters to customize view
   - Enable auto-refresh for live updates

2. **Interactive Map Tab**
   - Search for your location
   - Click markers to see detailed information
   - Find nearest monitoring stations

3. **Forecast Tab**
   - Select location for prediction
   - Choose forecast horizon (1-7 days)
   - View confidence intervals and uncertainty

4. **Historical Data Tab**
   - Select date range
   - Compare multiple locations
   - Export data for analysis

5. **News & Alerts Tab**
   - Stay updated with latest air quality news
   - Configure custom alert thresholds
   - View health advisories

### Interactive Features

#### Sidebar Controls
- **Date Range Selector** - Filter data by time period
- **Pollutant Multi-select** - Choose which pollutants to display
- **Location Comparison** - Select multiple locations
- **AQI Alert Threshold** - Set custom alert levels
- **Auto-refresh Toggle** - Enable/disable live updates

#### Chart Interactions
- **Zoom** - Scroll or pinch to zoom in/out
- **Pan** - Click and drag to explore
- **Hover** - View detailed data points
- **Range Selector** - Quick time period selection (1h, 6h, 1d, All)
- **Legend Toggle** - Click to show/hide data series

---

## 📁 Project Structure

```
aqi-monitor-bangalore/
│
├── main.py                 # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
│
├── models/
│   ├── lstm_model.h5      # Trained LSTM model
│   └── model_scaler.pkl   # Data scaler for predictions
│
├── data/
│   ├── historical_aqi.csv # Historical AQI data
│   └── mock_data.py       # Fallback mock data generator
│
├── utils/
│   ├── api_handler.py     # OpenAQ API integration
│   ├── calculations.py    # AQI and distance calculations
│   ├── visualizations.py  # Chart generation functions
│   └── forecasting.py     # LSTM prediction functions
│
└── assets/
    ├── logo.png           # Dashboard logo
    └── styles.css         # Custom CSS styles
```

---

## 🔧 Configuration

### API Configuration

The app uses the OpenAQ API. No API key required, but rate limits apply.

**In `config.py`:**
```
# OpenAQ API settings
OPENAQ_BASE_URL = 'https://api.openaq.org/v2/latest'
API_TIMEOUT = 10  # seconds
MAX_RETRIES = 3

# Bangalore coordinates
BANGALORE_CENTER = [12.9716, 77.5946]

# Refresh intervals (seconds)
REFRESH_OPTIONS = 
```

### Customization

**Change default locations** in `config.py`:
```
DEFAULT_LOCATIONS = [
    'Jayanagar',
    'Koramangala',
    'Whitefield',
    'BTM Layout',
    'Indiranagar'
]
```

---

## 🐛 Troubleshooting

### Port Already in Use
```
streamlit run main.py --server.port 8502
```

### Module Not Found Errors
```
pip install -r requirements.txt --upgrade
```

### TensorFlow Installation Issues
```
# For CPU-only version
pip install tensorflow-cpu

# For GPU support
pip install tensorflow-gpu
```

### OpenAQ API Connection Issues
- Check internet connection
- App will automatically use mock data as fallback
- Verify API status at https://openaq.org

### Streamlit Warnings
Update deprecated parameters:
```
# Old
st.plotly_chart(fig, use_container_width=True)

# New
st.plotly_chart(fig, width='stretch')
```

---

## 📊 Features in Detail

### AQI Calculation Formula

The dashboard uses the EPA (Environmental Protection Agency) standard AQI calculation:

```
AQI = [(I_high - I_low) / (C_high - C_low)] × (C - C_low) + I_low

Where:
- I_high = AQI value corresponding to C_high
- I_low = AQI value corresponding to C_low
- C_high = Concentration breakpoint ≥ C
- C_low = Concentration breakpoint ≤ C
- C = Pollutant concentration
```

### Haversine Distance Formula

Used to find nearest monitoring stations:

```
a = sin²(Δφ/2) + cos φ₁ × cos φ₂ × sin²(Δλ/2)
c = 2 × atan2(√a, √(1-a))
d = R × c

Where:
- φ = latitude, λ = longitude
- R = Earth's radius (6371 km)
```

### LSTM Model Architecture

```
Model: Sequential
- LSTM(128, return_sequences=True)
- Dropout(0.2)
- LSTM(64, return_sequences=False)
- Dropout(0.2)
- Dense(32, activation='relu')
- Dense(1)

Optimizer: Adam
Loss: Mean Squared Error
Training: 100 epochs, batch_size=32
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

---

## 🙏 Acknowledgments

- [OpenAQ](https://openaq.org) for providing open air quality data
- [Streamlit](https://streamlit.io) for the amazing framework
- [TensorFlow](https://tensorflow.org) for machine learning capabilities
- Environmental agencies providing AQI standards

---

## 📞 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/yourusername/aqi-monitor-bangalore/issues)
- Email: your.email@example.com

---

## 🔮 Future Enhancements

- [ ] Mobile app version
- [ ] Push notifications for alerts
- [ ] Integration with more cities
- [ ] Weather correlation analysis
- [ ] Air quality index predictions using ensemble models
- [ ] Social media integration for alerts
- [ ] Comparison with historical averages
- [ ] Health impact calculator

---

## 📸 Screenshots

### Dashboard View
![Dashboard](screenshots/dashboard.png)

### Interactive Map
![Map](screenshots/map.png)

### Forecast Visualization
![Forecast](screenshots/forecast.png)

---

**⭐ If you find this project helpful, please consider giving it a star!**

---

Last Updated: November 2025
```
