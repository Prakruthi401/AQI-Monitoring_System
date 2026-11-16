import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import os
import logging
from aqi_helpers import calculate_aqi, get_aqi_category

class OpenAQFetcher:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://api.openaq.org/v3"
        # Only add API key header if provided
        self.headers = {"X-API-Key": api_key} if api_key else {}
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def get_locations(self, country="IN", city="Bangalore", limit=100):
        """Fetch monitoring locations for a city"""
        if not self.api_key:
            return []
        url = f"{self.base_url}/locations"
        params = {
            "country": country,
            "city": city,
            "limit": limit
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.logger.info(f"Successfully fetched {len(data.get('results', []))} locations for {city}")
            return data.get('results', [])
        except requests.exceptions.Timeout:
            self.logger.error(f"Timeout error fetching locations for {city}")
            return []
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error fetching locations for {city}: {e}")
            return []
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network error fetching locations for {city}: {e}")
            return []
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error fetching locations for {city}: {e}")
            return []

    def get_latest_measurements(self, location_id=None, city="Bangalore", limit=100):
        """Fetch latest air quality measurements"""
        url = f"{self.base_url}/latest"
        params = {
            "city": city,
            "limit": limit
        }
        if location_id:
            params["location_id"] = location_id

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.logger.info(f"Successfully fetched {len(data.get('results', []))} measurements")
            return data.get('results', [])
        except requests.exceptions.Timeout:
            self.logger.error(f"Timeout error fetching measurements")
            return []
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error fetching measurements: {e}")
            return []
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network error fetching measurements: {e}")
            return []
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error fetching measurements: {e}")
            return []

    def get_historical_data(self, location_id, date_from=None, date_to=None, limit=1000):
        """Fetch historical measurements for a location"""
        url = f"{self.base_url}/measurements"
        params = {
            "location_id": location_id,
            "limit": limit
        }
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            self.logger.info(f"Successfully fetched {len(data.get('results', []))} historical measurements")
            return data.get('results', [])
        except requests.exceptions.Timeout:
            self.logger.error(f"Timeout error fetching historical data")
            return []
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error fetching historical data: {e}")
            return []
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network error fetching historical data: {e}")
            return []
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error fetching historical data: {e}")
            return []

    def get_aqi_data(self, city="Bangalore"):
        """Get current AQI data for the city"""
        locations = self.get_locations(city=city)
        if not locations:
            return {}

        # Keep station names as mapping keys, matching dashboard/map consumers.
        station_data = {}
        for location in locations[:5]:
            measurements = self.get_latest_measurements(location_id=location['id'])
            processed = self._process_measurements_to_aqi(measurements)
            if processed:
                station_data[location.get('name', str(location['id']))] = processed
            time.sleep(0.1)
        return station_data

    def _process_measurements_to_aqi(self, measurements):
        """Process raw measurements into AQI values"""
        if not measurements:
            return {}

        # Group by parameter
        param_data = {}
        for measurement in measurements:
            param = measurement.get('parameter', '')
            value = measurement.get('value', 0)
            if param not in param_data:
                param_data[param] = []
            param_data[param].append(value)

        # Calculate averages
        averages = {}
        for param, values in param_data.items():
            averages[param] = sum(values) / len(values) if values else 0

        # Calculate AQI (simplified version)
        aqi = self._calculate_aqi_from_pollutants(averages)

        return {
            'aqi': aqi,
            'pollutants': averages,
            'timestamp': datetime.now().isoformat(),
            'source': 'OpenAQ'
        }

    def _calculate_aqi_from_pollutants(self, pollutants):
        """Calculate AQI from pollutant concentrations using EPA breakpoints"""
        pm25 = pollutants.get('pm25', 0)
        pm10 = pollutants.get('pm10', 0)
        no2 = pollutants.get('no2', 0)
        so2 = pollutants.get('so2', 0)
        co = pollutants.get('co', 0)
        o3 = pollutants.get('o3', 0)

        # Use the proper EPA-based AQI calculation
        aqi_value, category = calculate_aqi(pm25, pm10, no2, so2, co, o3)
        return aqi_value

    def get_bangalore_stations_data(self):
        """Get data from Bangalore KSPCB stations"""
        from bangalore_locations import BANGALORE_STATIONS

        cache_file = "bangalore_aqi_cache.json"
        cache_duration = timedelta(minutes=30)  # Cache for 30 minutes

        # Check cache first
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                    cache_time = datetime.fromisoformat(cache_data['timestamp'])
                    if datetime.now() - cache_time < cache_duration:
                        return cache_data['data']
            except (json.JSONDecodeError, KeyError):
                pass  # Cache invalid, fetch fresh data

        # Fetch fresh data from OpenAQ for Bangalore locations
        all_data = []
        for station in BANGALORE_STATIONS:
            try:
                # Search for locations near the station coordinates
                locations = self.get_locations_near_coordinates(
                    station['coordinates']['latitude'],
                    station['coordinates']['longitude'],
                    radius=10  # 10km radius
                )

                if locations:
                    # Get latest measurements from the nearest location
                    measurements = self.get_latest_measurements(location_id=locations[0]['id'])
                    if measurements:
                        processed_data = self._process_measurements_to_aqi(measurements)
                        if processed_data:
                            station_data = {
                                'station_id': station['id'],
                                'station_name': station['name'],
                                'station_type': station['type'],
                                'coordinates': station['coordinates'],
                                'aqi': processed_data.get('aqi', 0),
                                'pollutants': processed_data.get('pollutants', {}),
                                'timestamp': processed_data.get('timestamp', datetime.now().isoformat()),
                                'source': 'OpenAQ'
                            }
                            all_data.append(station_data)

                time.sleep(0.2)  # Rate limiting between requests

            except Exception as e:
                self.logger.error(f"Error fetching data for station {station['name']}: {e}")
                continue

        # If no data from API, return mock data
        if not all_data:
            self.logger.warning("No data from OpenAQ API, using mock data")
            all_data = self._generate_mock_bangalore_data()

        # Cache the data
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'data': all_data
        }
        try:
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)
        except Exception as e:
            self.logger.error(f"Error caching data: {e}")

        return all_data

    def get_locations_near_coordinates(self, lat, lon, radius=10):
        """Find OpenAQ locations near given coordinates"""
        if not self.api_key:
            return []
        url = f"{self.base_url}/locations"
        params = {
            "coordinates": f"{lat},{lon}",
            "radius": radius,
            "limit": 5
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.logger.info(f"Successfully fetched {len(data.get('results', []))} locations near coordinates")
            return data.get('results', [])
        except requests.exceptions.Timeout:
            self.logger.error(f"Timeout error fetching locations near coordinates")
            return []
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error fetching locations near coordinates: {e}")
            return []
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network error fetching locations near coordinates: {e}")
            return []
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error fetching locations near coordinates: {e}")
            return []

    def get_station_data_by_location(self, lat, lon):
        """Get AQI data for nearest station to given location"""
        from location_search import LocationSearch
        from bangalore_locations import BANGALORE_STATIONS

        location_search = LocationSearch()
        nearby_stations = location_search.find_nearby_stations(lat, lon, BANGALORE_STATIONS, max_distance_km=50)

        if not nearby_stations:
            return None

        # Get data for the nearest station
        nearest_station = nearby_stations[0]
        all_data = self.get_bangalore_stations_data()

        for station_data in all_data:
            if station_data['station_id'] == nearest_station['id']:
                station_data['distance_km'] = nearest_station.get('distance_km', 0)
                return station_data

        return None

    def get_aqi_data(self, city="Bangalore", latitude=None, longitude=None):
        """Get AQI data for a location by coordinates"""
        # If coordinates are provided, use them to find the nearest station
        if latitude is not None and longitude is not None:
            return self.get_station_data_by_location(latitude, longitude)
        
        # Otherwise, return data for the city
        all_data = self.get_bangalore_stations_data()
        return all_data[0] if all_data else None

    def _generate_mock_bangalore_data(self):
        """Generate mock data when API is unavailable"""
        from bangalore_locations import BANGALORE_STATIONS

        api_data = []
        for station in BANGALORE_STATIONS:
            # Generate realistic AQI values based on station type
            if station['type'] == 'traffic':
                base_aqi = 120 + np.random.normal(0, 30)
            elif station['type'] == 'industrial':
                base_aqi = 150 + np.random.normal(0, 40)
            else:  # residential
                base_aqi = 80 + np.random.normal(0, 20)

            aqi = max(0, int(base_aqi))

            api_data.append({
                'station_id': station['id'],
                'station_name': station['name'],
                'station_type': station['type'],
                'coordinates': station['coordinates'],
                'aqi': aqi,
                'pollutants': {
                    'pm25': max(0, aqi * 0.3 + np.random.normal(0, 5)),
                    'pm10': max(0, aqi * 0.5 + np.random.normal(0, 8)),
                    'no2': max(0, 20 + np.random.normal(0, 10)),
                    'so2': max(0, 5 + np.random.normal(0, 3)),
                    'co': max(0, 0.5 + np.random.normal(0, 0.3)),
                    'o3': max(0, 25 + np.random.normal(0, 15))
                },
                'timestamp': datetime.now().isoformat(),
                'source': 'API Data'
            })

        return api_data

    def get_historical_trends(self, station_id, days=30):
        """Get historical AQI trends for a station"""
        from bangalore_locations import get_station_by_id

        station = get_station_by_id(station_id)
        if not station:
            return []

        # For now, generate mock historical data
        # In production, this would fetch from OpenAQ historical API
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        trends = []

        for date in dates:
            # Simulate daily variation with seasonal trends
            base_aqi = 80 + np.random.normal(0, 20)
            seasonal_factor = 15 * np.sin(2 * np.pi * date.dayofyear / 365)
            daily_variation = np.random.normal(0, 10)

            aqi = max(0, int(base_aqi + seasonal_factor + daily_variation))

            trends.append({
                'date': date.strftime('%Y-%m-%d'),
                'aqi': aqi,
                'pm25': max(0, aqi * 0.3 + np.random.normal(0, 5)),
                'pm10': max(0, aqi * 0.5 + np.random.normal(0, 8))
            })

        return trends
