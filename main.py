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

dotenv.load_dotenv()


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
agent_tools = [
    # TODO: Let workshop participants fill this out
    tools.lookup_weather,
    tools.duckduckgo_search,
    tools.open_url_in_browser,
    tools.search_places_openstreetmap,
    # Tools for communication with other agents
    tools.send_message,
    tools.retrieve_messages,
]
llm_with_tools = llm.bind_tools(agent_tools)


def inject_prompt(state: State) -> dict:
    with open("system_prompt.j2", 'r') as f:
        prompt = f.read().replace("<username>", username)
    msgs = state["messages"]
    return {"messages": msgs + [{"role": "system", "content": prompt}]}


def user_chat(state: State) -> dict:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# Building the Agent Graph
graph_builder = StateGraph(State)
graph_builder.add_node("inject_prompt", inject_prompt)
graph_builder.add_node("user_chat", user_chat)
graph_builder.add_node("tools", ToolNode(agent_tools))
graph_builder.add_conditional_edges("user_chat", tools_condition)
graph_builder.add_edge("tools", "user_chat")
graph_builder.add_edge(START, "inject_prompt")
graph_builder.add_edge("inject_prompt", "user_chat")
graph_builder.add_edge("user_chat", END)
graph = graph_builder.compile(checkpointer=InMemorySaver())


def stream_graph_updates(user_input: str):
    """
    TODO: Add comments!
    """
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, {"configurable": {"thread_id": "1"}}):
        for value in event.values():
            utils.print_agent_event(value)


if __name__ == "__main__":
    # First user interaction, asking for name
    username = utils.get_user_input("What's your name? ")
    stream_graph_updates("")
    # Running the user chat infinite loop
    while True:
        try:
            user_input = utils.get_user_input(f"{username}: ")
            stream_graph_updates(user_input)
        except Exception as e:
            raise e
