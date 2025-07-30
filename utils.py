import sys

from langchain_core.messages import AIMessage, ToolMessage


def print_agent_event(value: dict) -> None:
    respondant = "Assistant"
    last_message = value["messages"][-1]
    if isinstance(last_message, ToolMessage):
        print(f"  >>> Tool Invoked: {last_message.name}")
        respondant = f"    >>> "
    if isinstance(last_message, AIMessage) or isinstance(last_message, ToolMessage):
        print(f"{respondant}: ", last_message.content)


def get_user_input(msg: str) -> str:
    user_input = input(msg)
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Garage Out!")
        sys.exit(0)
    return user_input
