import os
from typing import Annotated

import dotenv
from langchain_openai import AzureChatOpenAI
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

import tools
import utils


# TODO: Make sure the `dotenv` module loads the .env environment variables
# dotenv.???()


class State(TypedDict):
    messages: Annotated[list, add_messages]


llm = AzureChatOpenAI(
    azure_deployment="gpt-4o-mini-lhs",
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0,
    max_tokens=2000,
    timeout=None,
    max_retries=1,
)
# TODO: Define the list of tools at the agent's disposal
agent_tools = []
llm_with_tools = None # TODO: bind the tools to the llm


def inject_prompt(state: State) -> dict:
    with open("system_prompt.j2", "r") as f:
        prompt = f.read().replace("<username>", username)
    msgs = state["messages"]
    return {"messages": msgs + [{"role": "system", "content": prompt}]}


def user_chat(state: State) -> dict:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# Building the Agent Graph
# TODO: Build the graph
graph_builder = StateGraph(State)
# TODO: Add nodes to the graph
# TODO: Add edges between the nodes
# graph_builder.add_node("", None)
# graph_builder.add_conditional_edges("", tools_condition)
# graph_builder.add_edge("", "")
graph = graph_builder.compile(checkpointer=InMemorySaver())


def stream_graph_updates(user_input: str):
    """
    Streams and prints events from a LangGraph agent in response to user input.

    Sends the user's message to a LangGraph agent and listens to its streamed response events.
    Each event's values are processed and printed using a utility function, allowing real-time
    monitoring of the agent's internal steps or outputs.

    Args:
        user_input (str): The user's input message to be processed by the LangGraph agent.
    """
    for event in graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        {"configurable": {"thread_id": "1"}},
    ):
        for value in event.values():
            utils.print_agent_event(value)


if __name__ == "__main__":
    # First user interaction, asking for name
    username = utils.get_user_input("What's your name? ")
    stream_graph_updates("")
    # Running the user chat infinite loop
    # TODO: Wrap the try-except block below in an infinite loop to keep the interaction going
    try:
        user_input = utils.get_user_input(f"{username}: ")
        stream_graph_updates(user_input)
    except Exception as e:
        raise e
