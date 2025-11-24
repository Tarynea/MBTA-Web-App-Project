import os
import json
import urllib.request
from math import radians, cos, sin, sqrt, atan2
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

MAPBOX_BASE_URL = "https://api.mapbox.com/search/searchbox/v1/forward"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"
MBTA_ALERTS_URL = "https://api-v3.mbta.com/alerts"
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
# Nearest station with more details
# -----------------------------------------------------
def get_nearest_station_details(lat: float, lng: float):
    """
    Given latitude and longitude, return detailed info about the nearest stop:
    (stop_name, wheelchair_accessible, stop_lat, stop_lng, stop_id)
    """
    url = get_mbta_url(lat, lng)
    data = get_json(url)

    try:
        stop = data["data"][0]
        attrs = stop["attributes"]
        stop_name = attrs["name"]
        wheelchair = attrs["wheelchair_boarding"]
        stop_lat = attrs.get("latitude")
        stop_lng = attrs.get("longitude")
        stop_id = stop["id"]
        return stop_name, wheelchair, stop_lat, stop_lng, stop_id
    except (KeyError, IndexError):
        return None, None, None, None, None
    
# -----------------------------------------------------
# Weather helper 
# -----------------------------------------------------
def get_weather(lat: float, lng: float):
    """Return (description, temperature_F) for the given coordinates."""
    if OPENWEATHER_API_KEY is None:
        raise RuntimeError("OPENWEATHER_API_KEY not found. Check your .env file.")

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
# Distance + walking time helpers
# -----------------------------------------------------
def haversine_km(lat1, lng1, lat2, lng2):
    """Great-circle distance between two points (in kilometers)."""
    R = 6371.0  # Earth radius in km
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lng2 - lng1)

    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def estimate_walking_time_minutes(lat1, lng1, lat2, lng2, speed_kmh=4.8):
    """
    Rough walking time in minutes between two points.
    Default speed ≈ 4.8 km/h.
    """
    distance_km = haversine_km(lat1, lng1, lat2, lng2)
    hours = distance_km / speed_kmh
    minutes = hours * 60
    return round(minutes)

# -----------------------------------------------------
# Mapbox Static Map URL
# -----------------------------------------------------
def get_static_map_url(lat: float, lng: float, zoom: int = 15,
                       width: int = 600, height: int = 400) -> str:
    """Return a Mapbox static map URL centered on (lat, lng) with a pin."""
    if MAPBOX_TOKEN is None:
        raise RuntimeError("MAPBOX_TOKEN not found. Check your .env file.")

    # Mapbox uses lng,lat order in URLs
    return (
        "https://api.mapbox.com/styles/v1/mapbox/streets-v12/static/"
        f"pin-s+ff0000({lng},{lat})/"
        f"{lng},{lat},{zoom},0/"
        f"{width}x{height}"
        f"?access_token={MAPBOX_TOKEN}"
    )

# -----------------------------------------------------
# MBTA alerts for a stop
# -----------------------------------------------------
def get_alerts_for_stop(stop_id: str, max_alerts: int = 3):
    """
    Return a list of short alert messages for a given stop_id.
    """
    if MBTA_API_KEY is None:
        raise RuntimeError("MBTA_API_KEY not found. Check your .env file.")

    url = (
        f"{MBTA_ALERTS_URL}?api_key={MBTA_API_KEY}"
        f"&filter[stop]={stop_id}"
        f"&sort=-updated_at&page[limit]={max_alerts}"
    )

    data = get_json(url)
    alerts = []

    for item in data.get("data", []):
        attrs = item.get("attributes", {})
        text = (
            attrs.get("header")
            or attrs.get("short_header")
            or attrs.get("description")
            or "Service alert"
        )
        alerts.append(text)

    return alerts




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
# Manual tests 
# -----------------------------------------------------
if __name__ == "__main__":
    print("Testing get_lat_lng('Boston Common'):")
    print(get_lat_lng("Boston Common"))

    print("\nTesting find_stop_near('Boston Common'):")
    print(find_stop_near("Boston Common"))
