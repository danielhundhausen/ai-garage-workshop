import os
from typing import Annotated

from langchain_openai import AzureChatOpenAI
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

import dotenv

dotenv.load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


# from langchain.chat_models import init_chat_model
# llm = init_chat_model("o3-mini")

llm = AzureChatOpenAI(
    azure_deployment="gpt-4o-mini-lhs",  # or your deployment
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),  # or your api version
    temperature=0,
    max_tokens=2000,
    timeout=None,
    max_retries=1,
)
    # azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],


def _test_llm_call(llm):
    messages = [
        (
            "system",
            "You are a helpful translator. Translate the user sentence to French.",
        ),
        ("human", "I viscerally detest programming."),
    ]
    resp = llm.invoke(messages)
    print(resp)


def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break
