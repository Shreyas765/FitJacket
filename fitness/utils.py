import requests
from django.conf import settings
import os

FOURSQUARE_API_KEY = api_key=os.environ.get("FOURSQUARE_API_KEY")
FOURSQUARE_API_URL = 'https://api.foursquare.com/v3/places/search'

def get_nearby_locations(latitude, longitude, categories):
    """
    Get nearby locations from Foursquare API
    Args:
        latitude (float): User's latitude
        longitude (float): User's longitude
        categories (list): List of Foursquare category IDs to search for
    Returns:
        list: List of nearby locations
    """
    headers = {
        'Authorization': FOURSQUARE_API_KEY,
        'accept': 'application/json'
    }
    
    params = {
        'll': f'{latitude},{longitude}',
        'radius': 5000,  # 5km radius
        'categories': ','.join(categories),
        'limit': 10
    }
    
    try:
        response = requests.get(FOURSQUARE_API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        locations = []
        for place in data.get('results', []):
            location = {
                'name': place.get('name', ''),
                'address': place.get('location', {}).get('formatted_address', ''),
                'distance': place.get('distance', 0),
                'category': place.get('categories', [{}])[0].get('name', ''),
                'latitude': place.get('geocodes', {}).get('main', {}).get('latitude'),
                'longitude': place.get('geocodes', {}).get('main', {}).get('longitude')
            }
            locations.append(location)
        
        return locations
    except requests.exceptions.RequestException as e:
        print(f"Error fetching locations: {e}")
        return [] 