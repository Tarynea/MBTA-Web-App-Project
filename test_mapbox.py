import os
import json
import pprint
import urllib.request
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MAPBOX_BASE_URL = "https://api.mapbox.com/search/searchbox/v1/forward"

if MAPBOX_TOKEN is None:
    raise RuntimeError("MAPBOX_TOKEN is not set. Check your .env file.")

def test_mapbox(query: str = "Babson College"):
    # Replace spaces with %20 for URL encoding 
    encoded_query = query.replace(" ", "%20")

    url = f"{MAPBOX_BASE_URL}?q={encoded_query}&access_token={MAPBOX_TOKEN}"

    print("Requesting URL:")
    print(url)

    with urllib.request.urlopen(url) as resp:
        response_text = resp.read().decode("utf-8")
        response_data = json.loads(response_text)

    # Pretty-print the response structure
    pprint.pprint(response_data)


    try:
        address = response_data["features"][0]["properties"]["address"]
        print("\nFirst result address:", address)
    except (KeyError, IndexError):
        print("\nCould not extract address from response.")

if __name__ == "__main__":
    test_mapbox("Babson College")
