import os
import requests

from ddgs import DDGS
import googlemaps
from langchain.tools import tool


# Initialize the Google Maps client with your API key
gmaps = None  # googlemaps.Client(key=os.environ["DANIELS_GOOGLE_MAPS_API_KEY"])
ddgs_client = DDGS()


# Define the tool function
@tool
def find_place(query: str) -> str:
    """ Find a place on Google Maps. """
    result = gmaps.places(query=query)
    if result["results"]:
        place = result["results"][0]
        name = place["name"]
        address = place["formatted_address"]
        return f"Found place: {name}, located at: {address}"
    else:
        return "No places found for that query."



# @tool
def find_places_openstreetmap() -> dict:
    """
    LangGraph tool to query Overpass API for restaurants in a given German city.

    Returns:
        dict: {
            "restaurants": list of dicts with name, lat, lon
        }
    """
    city = "Frankfurt"
    limit = 10

    if not city:
        return {"error": "Missing 'city' in input"}

    # Overpass QL query
    query = f"""
    [out:json][timeout:25];
    area["name"="{city}"]["boundary"="administrative"]["admin_level"="8"]->.searchArea;
    (
      node["amenity"="restaurant"](area.searchArea);
      way["amenity"="restaurant"](area.searchArea);
      relation["amenity"="restaurant"](area.searchArea);
    );
    out center {limit};
    """

    url = "https://overpass-api.de/api/interpreter"
    
    try:
        response = requests.post(url, data={"data": query})
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return {"error": f"Overpass API request failed: {str(e)}"}

    restaurants = []
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        name = tags.get("name")
        lat = element.get("lat") or element.get("center", {}).get("lat")
        lon = element.get("lon") or element.get("center", {}).get("lon")

        if name and lat and lon:
            restaurants.append({"name": name, "lat": lat, "lon": lon})

    return {"restaurants": restaurants[:limit]}


@tool
def lookup_weather(location: str) -> str:
    """ Weather lookup """
    raise NotImplementedError("tbd")


@tool
def duckduckgo_search(query: str) -> str:
    """
    Perform a search using DuckDuckGo Instant Answer API.
    This is not a full web search — returns abstract, related topics, etc.
    """
    try:
        result = ddgs_client.text(query)
        return result
    except Exception as e:
        print("Failed")
        raise e

    return "No relevant information found on DuckDuckGo."


# print(find_places_openstreetmap())
