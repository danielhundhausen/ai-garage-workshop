import datetime
import json
import math
import platform
from typing import Any
import requests
import time
import urllib
import webbrowser

from ddgs import DDGS
import osmnx as ox
from langchain.tools import tool


BROKER_URL = "https://garage-workshop-agent-handson-frfuakb9g2acbcfb.germanywestcentral-01.azurewebsites.net/static/index.html"
session = requests.Session()
ddgs_client = DDGS()
messages = []
last_retrieval = datetime.datetime.now() - datetime.timedelta(1)


@tool
def send_message(content: str, sender: str) -> str:
    """
    Send a message to all other agents with whom alignment regarding
    the after work activities is to be reached.

    Args:
        content (str): content of the message
        sender (str): name of the sender

    Returns:
        response_text (int): HTML code and content of the send_message POST request
    """
    url = urllib.parse.urljoin(BROKER_URL, "/messages")
    message = {"sender": sender, "content": content, "user_id": platform.node()}
    r = session.post(url=url, data=json.dumps(message))
    return str(r) + " >> " + r.text


@tool
def wait(wait_duration: int) -> str:
    """
    Wait.

    Args:
        wait_duration (int): The amount of time in seconds to wait (max. 10)

    Returns:
        _ (str): Time waited as a string
    """
    wait_duration = min(wait_duration, 10)
    time.sleep(wait_duration)
    return f"Waited for {wait_duration}"


@tool
def retrieve_full_message_history() -> str:
    """
    Retrieve all messages of the entire chat history from all agents with whom alignment regarding
    the after work activities is to be reached.

    Returns:
        response_text: HTML code and response of the retrieve_message GET request
    """
    url = urllib.parse.urljoin(BROKER_URL, "/messages/all")
    r = session.get(url, params={"unique_user_id": platform.node()})
    return str(r) + " >> " + r.text



@tool
def retrieve_messages() -> str:
    """
    Retrieve all new messages from all agents with whom alignment regarding
    the after work activities is to be reached.

    Returns:
        response_text: HTML code and response of the retrieve_message GET request
    """
    url = urllib.parse.urljoin(BROKER_URL, "/messages/new")
    r = session.get(url, params={"unique_user_id": platform.node()})
    return str(r) + " >> " + r.text


@tool
def open_url_in_browser(url: str) -> None:
    """
    Presents the provided url in a new tab in the user's bowser.

    Args:
        url (str): URL to be opened in the user's browser
    """
    webbrowser.open_new_tab(url)


@tool
def lookup_weather(location: str) -> str:
    """Weather lookup"""
    # raise NotImplementedError("tbd")
    return f"It's actually sunny and 65 degrees everywhere on earth including {location} today!"


@tool
def duckduckgo_search(query: str) -> list[dict[str, Any]]:
    """
    Perform a search using DuckDuckGo.
    This is not a full web search — returns abstract, related topics, etc.
    """
    try:
        result = ddgs_client.text(query)
        return result
    except Exception as e:
        print("Failed")
        raise e


@tool
def get_current_location() -> tuple[float, float]:
    """
    Get the current location in coordinates.

    Returns:
        current_location (tuple[float, float]): location coordinates (latitude, longitude)
    """
    return (50.106089, 8.652845)  # Location of Gekko House Frankfurt


@tool
def search_places_openstreetmap(
    amenities: list[str],
    latitude: float,
    longitude: float,
    radius: int,
):
    """
    Search for certain types of establishments (amenities),
    such as bars or restaurants around given coordinates
    within a given radius on openstreetmap.

    Args:
        amenities (list[str]): Can be 'bar', 'biergarten', 'cafe', 'fast_food', 'ice_cream', 'pub', 'restuarant', 'parking', 'taxi'
        latitude (float): Latitude coordinate of the user's current location
        longitude (float): Longitudinal coordinate of the user's current location
        radius (int): Radius around location in meters in which to search (max. 1000)

    Returns:
        pois (dataframe): table object with search results
    """
    tags = {"amenity": amenities}
    pois = ox.features.features_from_point(
        (latitude, longitude), tags, dist=min(radius, 1000)
    )
    relevant_columns = [
        "addr:city",
        "addr:housenumber",
        "addr:street",
        "amenity",
        "cuisine",
        "indoor_seating",
        "name",
        "opening_hours",
        "outdoor_seating",
        "phone",
        "website",
        "brewery",
        "diet:kosher",
        "diet:vegan",
        "diet:vegetarian",
        "payment:credit_cards",
        "payment:debit_cards",
        "smoking",
        "url",
        "check_date:opening_hours",
        "cuisine:de",
        "level",
        "air_conditioning",
        "bar",
        "capacity",
        "changing_table",
        "reservation",
        "toilets",
        "contact:phone",
        "contact:website",
        "operator",
        "payment:cash",
        "takeaway",
        "source",
        "website:menu",
        "brand",
        "note",
        "contact:mobile",
        "opening_hours:signed",
        "name:zh",
        "description",
        "diet:lactose_free",
        "diet:nut_free",
        "payment:american_express",
        "payment:mastercard",
        "payment:visa",
        "mobile",
        "access",
        "cuisine:crossover",
        "organic",
        "payment:apple_pay",
        "payment:google_pay",
    ]
    options = []
    for _, row in pois.iterrows():
        option = {
            x: row[x]
            for x in relevant_columns
            if x in pois.columns and not str(row[x]) == "nan"
        }
        options.append(option)
    print(options[0]["name"])
    print(type(options[0]["name"]))
    return options


if __name__ == "__main__":
    x = search_places_openstreetmap(["restaurant"], 50.106089, 8.652845, 650)
    print(type(x))
    print(x)
    import sys
    sys.exit(0)
