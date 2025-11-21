import os
import json
import urllib.request
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

MAPBOX_BASE_URL = "https://api.mapbox.com/search/searchbox/v1/forward"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# -----------------------------------------------------
# Helper to GET JSON data from a URL
# -----------------------------------------------------
def get_json(url: str) -> dict:
    """Return parsed JSON response from a URL."""
    with urllib.request.urlopen(url) as response:
        response_text = response.read().decode("utf-8")
        return json.loads(response_text)


# -----------------------------------------------------
# MAPBOX: Convert place name → (lat, lng)
# -----------------------------------------------------
def get_lat_lng(place_name: str):
    """Given a place name, return (latitude, longitude) floats."""
    if MAPBOX_TOKEN is None:
        raise RuntimeError("MAPBOX_TOKEN not found. Check your .env file.")

    # Simple URL encoding for spaces
    query = place_name.replace(" ", "%20")

    url = f"{MAPBOX_BASE_URL}?q={query}&access_token={MAPBOX_TOKEN}"

    data = get_json(url)

    # If there are no features at all, bail out
    features = data.get("features", [])
    if not features:
        return None, None

    feature = features[0]

    # Case 1: coordinates stored as a dict with latitude/longitude keys
    coords_dict = feature.get("coordinates")
    if isinstance(coords_dict, dict):
        lat = coords_dict.get("latitude")
        lng = coords_dict.get("longitude")
        if lat is not None and lng is not None:
            return lat, lng

    # Case 2: coordinates stored in geometry.coordinates = [lng, lat]
    geometry = feature.get("geometry")
    if geometry and "coordinates" in geometry:
        coords_list = geometry["coordinates"]
        if isinstance(coords_list, (list, tuple)) and len(coords_list) >= 2:
            lng, lat = coords_list[0], coords_list[1]
            return lat, lng

    # If we couldn't find coordinates in either format:
    return None, None

# -----------------------------------------------------
# MBTA: Build URL for finding nearest stop
# -----------------------------------------------------
def get_mbta_url(lat: float, lng: float) -> str:
    """Build the MBTA API URL for nearest stop lookup."""
    if MBTA_API_KEY is None:
        raise RuntimeError("MBTA_API_KEY not found. Check your .env file.")

    return (
        f"{MBTA_BASE_URL}?api_key={MBTA_API_KEY}"
        f"&sort=distance&filter[latitude]={lat}&filter[longitude]={lng}"
    )


# -----------------------------------------------------
# MBTA: Get nearest station
# -----------------------------------------------------
def get_nearest_station(lat: float, lng: float):
    """Return (station_name, wheelchair_accessibility)."""
    url = get_mbta_url(lat, lng)
    data = get_json(url)

    try:
        stop = data["data"][0]
        stop_name = stop["attributes"]["name"]
        wheelchair = stop["attributes"]["wheelchair_boarding"]
        return stop_name, wheelchair
    except (KeyError, IndexError):
        return None, None


# -----------------------------------------------------
# Combine everything into one function
# -----------------------------------------------------
def find_stop_near(place_name: str):
    """Return nearest MBTA stop to a place name."""
    lat, lng = get_lat_lng(place_name)

    if lat is None or lng is None:
        return None, None

    return get_nearest_station(lat, lng)

# -----------------------------------------------------
# OpenWeather: Get current weather by latitude/longitude
# -----------------------------------------------------
def get_weather(lat: float, lng: float):
    """Return (description, temperature_F) for the given coordinates."""
    if OPENWEATHER_API_KEY is None:
        raise RuntimeError("OPENWEATHER_API_KEY not found. Check your .env file.")

    # We'll use imperial units (Fahrenheit). Use units=metric for Celsius.
    url = (
        f"{OPENWEATHER_BASE_URL}?lat={lat}&lon={lng}"
        f"&units=imperial&appid={OPENWEATHER_API_KEY}"
    )

    data = get_json(url)

    try:
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return description, temp
    except (KeyError, IndexError):
        return None, None

# -----------------------------------------------------
# Manual tests (THIS MUST BE AT THE VERY BOTTOM)
# -----------------------------------------------------
if __name__ == "__main__":
    print("Testing get_lat_lng('Boston Common'):")
    print(get_lat_lng("Boston Common"))

    print("\nTesting find_stop_near('Boston Common'):")
    print(find_stop_near("Boston Common"))
