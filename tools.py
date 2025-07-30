import datetime
import json
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
def retrieve_messages() -> str:
    """
    Retrieve all messages a message to all other agents with whom alignment regarding
    the after work activities is to be reached.

    Args:
        content (str): content of the message

    Returns:
        response_text (int): HTML code and response of the retrieve_message GET request
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
    latitude: float,
    longitude: float,
    radius: int,
):
    """
    Search for places like restaurants, bars and similar nearby on openstreetmap.
    Also returns leisure places.

    Args:
        latitude (float): Latitude coordinate of the user's current location
        longitude (float): Longitudinal coordinate of the user's current location
        radius (int): Radius around location in meters in which to search (max. 2000)

    Returns:
        pois (): object with search results
    """
    # amenities (list[str]): Types of establishments to search for, can be the default values
    amenities: list[str] = ['bar', 'biergarten', 'cafe', 'fast_food', 'ice_cream', 'pub', 'restuarant', 'parking', 'taxi']
    # Search for all bars and restaurants in Munich
    tags = {"amenity": amenities}
    pois = ox.features.features_from_point((latitude, longitude), tags, dist=min(radius, 2000))
    return pois


if __name__ == "__main__":
    x = search_places_openstreetmap()
    print(type(x))
    print(x)
    print(x.columns)
    import sys
    sys.exit(0)
    r = send_message("hi sir", "Max")
    print(r)
    r = retrieve_messages()
    print(r)
