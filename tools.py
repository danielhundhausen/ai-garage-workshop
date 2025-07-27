import datetime
from typing import Any
import webbrowser

from ddgs import DDGS
import osmnx as ox
from langchain.tools import tool


ddgs_client = DDGS()
messages = []
last_retrieval = (datetime.datetime.now() - datetime.timedelta(1))


@tool
def send_message(content: str, author: str = "Max") -> None:
    """
    Send a message to all other agents with whom alignment regarding
    the after work activities is to be reached.

    Args:
        content (str): content of the message
    """
    message = {
        "author": author,
        "content": content,
        "timestamp": datetime.datetime.now()
    }
    messages.append(message)


@tool
def retrieve_messages() -> list[dict]:
    """
    Retrieve all messages a message to all other agents with whom alignment regarding
    the after work activities is to be reached.

    Args:
        content (str): content of the message
    """
    global last_retrieval, messages
    message = {
        "author": "Viktor",
        "content": "I insist on eating Italian",
        "timestamp": datetime.datetime.now()
    }
    messages.append(message)

    new_messages = list(filter(lambda x: x["timestamp"] > last_retrieval, messages))
    last_retrieval = datetime.datetime.now()
    return new_messages


@tool
def open_url_in_browser(url: str) -> None:
    """
    Opens the provided url in a new tab in the user's bowser.

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


def search_places_openstreetmap(
    distance: int, places: list[str] = ["restuarant", "bar"]
):
    """
    Search for places nearby on openstreetmap.

    Args:
        distance (int): Distance in meters which
    """
    # Search for all bars and restaurants in Munich
    tags = {"amenity": places}
    hotel_location = (50.106089, 8.652845)  # Location of Gekko House Frankfurt
    pois = ox.features.features_from_point(hotel_location, tags, dist=distance)
    return pois
