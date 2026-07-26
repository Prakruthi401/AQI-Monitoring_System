import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time

class LocationSearch:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="aqi_monitor_app")

    def search_locations(self, query, country="India"):
        """Search for locations using geocoding"""
        try:
            locations = self.geolocator.geocode(query, exactly_one=False, limit=5, country_codes=[country.lower()[:2]])
            if not locations:
                return []

            results = []
            for loc in locations:
                results.append({
                    'name': loc.address,
                    'latitude': loc.latitude,
                    'longitude': loc.longitude,
                    'display_name': loc.address
                })

            return results
        except Exception as e:
            print(f"Error searching locations: {e}")
            return []

    def get_city_coordinates(self, city_name):
        """Get coordinates for a city"""
        try:
            location = self.geolocator.geocode(city_name)
            if location:
                return {
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'name': location.address
                }
        except Exception as e:
            print(f"Error getting city coordinates: {e}")
        return None

    def find_nearby_stations(self, latitude, longitude, stations, max_distance_km=50):
        """Find monitoring stations near a location"""
        user_location = (latitude, longitude)
        nearby_stations = []

        for station in stations:
            if 'coordinates' in station:
                station_coords = (
                    station['coordinates']['latitude'],
                    station['coordinates']['longitude']
                )
                distance = geodesic(user_location, station_coords).kilometers
                if distance <= max_distance_km:
                    station['distance_km'] = distance
                    nearby_stations.append(station)

        # Sort by distance
        nearby_stations.sort(key=lambda x: x['distance_km'])
        return nearby_stations

    def reverse_geocode(self, latitude, longitude):
        """Get address from coordinates"""
        try:
            location = self.geolocator.reverse((latitude, longitude))
            return location.address if location else None
        except Exception as e:
            print(f"Error reverse geocoding: {e}")
            return None
