import os
from typing import Annotated

import dotenv
from langchain_openai import AzureChatOpenAI
from typing_extensions import TypedDict
from langchain_core.messages import ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

import tools

dotenv.load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]
    # user_preferences: dict[str, str]


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


def user_chat(state: State) -> dict:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# Building the Agent Graph
graph_builder = StateGraph(State)
graph_builder.add_node("user_chat", user_chat)
graph_builder.add_node("tools", ToolNode(agent_tools))
graph_builder.add_conditional_edges("user_chat", tools_condition)
graph_builder.add_edge("tools", "user_chat")
graph_builder.add_edge(START, "user_chat")
graph_builder.add_edge("user_chat", END)
graph_builder.set_entry_point("user_chat")
graph = graph_builder.compile(checkpointer=InMemorySaver())


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, {"configurable": {"thread_id": "1"}}):
        for value in event.values():
            respondant = "Assistant"
            if isinstance(value["messages"][-1], ToolMessage):
                respondant = f"Tool ({value['messages'][-1].name})"
            print(f"{respondant}: ", value["messages"][-1].content)


if __name__ == "__main__":
    # Running the user chat loop
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Garage Out!")
                break
            stream_graph_updates(user_input)
        except Exception as e:
            for m in state["messages"]:
                print(m)
            print(state["messages"])
            print(e)
