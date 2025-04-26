import requests
from django.conf import settings
import os

FOURSQUARE_API_KEY = "fsq3WJfirOzGoX2fm0wljwRNC/mTzDzmHwdN5v9kcOm6wI4="
FOURSQUARE_API_URL = 'https://api.foursquare.com/v3/places/search'

def get_nearby_locations(latitude, longitude, categories):
    """
    Get nearby locations from Foursquare API
    Args:
        latitude (float): User's latitude
        longitude (float): User's longitude
        categories (list): List of Foursquare category IDs to search for
    Returns:
        list: List of nearby locations with distances in miles (rounded to nearest hundredth)
    """
    headers = {
        'Authorization': FOURSQUARE_API_KEY,
        'accept': 'application/json'
    }
    
    params = {
        'll': f'{latitude},{longitude}',
        'radius': 8047,  # 5 miles in meters
        'categories': ','.join(categories),
        'limit': 10
    }
    
    try:
        response = requests.get(FOURSQUARE_API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        locations = []
        for place in data.get('results', []):
            # Convert distance from meters to miles (1 meter = 0.000621371 miles)
            distance_meters = place.get('distance', 0)
            distance_miles = round(distance_meters * 0.000621371, 2)  # Round to nearest hundredth
            
            location = {
                'name': place.get('name', ''),
                'address': place.get('location', {}).get('formatted_address', ''),
                'distance': distance_miles,
                'category': place.get('categories', [{}])[0].get('name', ''),
                'latitude': place.get('geocodes', {}).get('main', {}).get('latitude'),
                'longitude': place.get('geocodes', {}).get('main', {}).get('longitude')
            }
            locations.append(location)
        
        return locations
    except requests.exceptions.RequestException as e:
        print(f"Error fetching locations: {e}")
        return [] 