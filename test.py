from datetime import datetime
import main
import osmnx as ox


def test_llm_call(llm):
    messages = [
        (
            "system",
            "You are a helpful translator. Translate the user sentence to French.",
        ),
        ("human", "I viscerally detest programming."),
    ]
    resp = llm.invoke(messages)
    print(resp)


def search_places_openstreetmap(
    distance: int, places: list[str] = ["restuarant", "bar"]
):
    """
    Args:
        distance (int): Distance in meters which
    """
    # Search for all bars and restaurants in Munich
    tags = {"amenity": places}
    hotel_location = (50.106089, 8.652845)
    pois = ox.features.features_from_point(hotel_location, tags, dist=distance)

    # Print names and coordinates
    for name, row in pois.iterrows():
        print(row)
        print(row.get("name"), row.geometry.centroid.y, row.geometry.centroid.x)
        break


search_places_openstreetmap(500)


def send_message_local_test(content: str, author: str = "Max") -> None:
    """
    Send a message to all other agents with whom alignment regarding
    the after work activities is to be reached.

    Args:
        content (str): content of the message
    """
    message = {
        "author": author,
        "content": content,
        "timestamp": datetime.datetime.now(),
    }
    messages.append(message)


def retrieve_messages_local_test() -> list[dict]:
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
        "timestamp": datetime.datetime.now(),
    }
    messages.append(message)

    new_messages = list(filter(lambda x: x["timestamp"] > last_retrieval, messages))
    last_retrieval = datetime.datetime.now()
    return new_messages
