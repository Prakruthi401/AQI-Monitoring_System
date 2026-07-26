import requests
from geopy.distance import geodesic
from openaq_fetcher import OpenAQFetcher
from location_search import LocationSearch
from bangalore_locations import BANGALORE_STATIONS

class AQIFallbackService:
    """Service to handle AQI data retrieval with fallback to nearby locations"""
    
    def __init__(self):
        self.openaq = OpenAQFetcher()
        self.location_search = LocationSearch()
        
    def get_aqi_with_fallback(self, location_query):
        """
        Get AQI data for a location with fallback to nearest available station
        
        Args:
            location_query (str): Location name to search for
            
        Returns:
            dict: AQI data with fallback information if needed
        """
        # Step 1: Get coordinates for the searched location
        location_info = self.location_search.get_city_coordinates(location_query)
        if not location_info:
            return {"error": f"Location '{location_query}' not found"}
            
        latitude = location_info['latitude']
        longitude = location_info['longitude']
        
        # Check if coordinates are within Bangalore boundaries
        bangalore_bounds = {
            'min_lat': 12.7,
            'max_lat': 13.2,
            'min_lon': 77.4,
            'max_lon': 77.8
        }
        
        if (latitude < bangalore_bounds['min_lat'] or latitude > bangalore_bounds['max_lat'] or
            longitude < bangalore_bounds['min_lon'] or longitude > bangalore_bounds['max_lon']):
            return {"error": f"Location '{location_query}' is outside Bangalore boundaries"}
        
        # Step 2: Try to get AQI data directly for the location
        aqi_data = self.openaq.get_aqi_data(city="Bangalore", latitude=latitude, longitude=longitude)
        
        # Step 3: If no data, find nearest monitoring station
        if not aqi_data or 'aqi' not in aqi_data:
            # Find nearest official monitoring station
            nearest_station = self.location_search.find_nearest_station(latitude, longitude, BANGALORE_STATIONS)
            
            if nearest_station:
                # Get AQI data from the nearest station
                station_aqi = self.openaq.get_aqi_data(
                    city="Bangalore", 
                    latitude=nearest_station['coordinates']['latitude'],
                    longitude=nearest_station['coordinates']['longitude']
                )
                
                if station_aqi and 'aqi' in station_aqi:
                    # Return AQI data with fallback information
                    return {
                        "aqi": station_aqi['aqi'],
                        "pollutants": station_aqi.get('pollutants', {}),
                        "timestamp": station_aqi.get('timestamp', ''),
                        "source": station_aqi.get('source', 'OpenAQ'),
                        "is_fallback": True,
                        "fallback_info": {
                            "original_location": location_query,
                            "nearest_station": nearest_station['name'],
                            "distance_km": nearest_station['distance_km'],
                            "station_id": nearest_station['id']
                        }
                    }
            
            # If still no data, return error
            return {"error": f"No AQI data available for '{location_query}' or nearby stations"}
        
        # Return direct AQI data if available
        return {
            "aqi": aqi_data['aqi'],
            "pollutants": aqi_data.get('pollutants', {}),
            "timestamp": aqi_data.get('timestamp', ''),
            "source": aqi_data.get('source', 'OpenAQ'),
            "is_fallback": False,
            "location": location_query
        }