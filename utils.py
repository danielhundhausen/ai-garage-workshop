import sys

from langchain_core.messages import AIMessage, ToolMessage


def print_agent_event(value: dict) -> None:
    respondant = "Assistant"
    if isinstance(value["messages"][-1], ToolMessage):
        print(" >>> Tool Invoked:")
        respondant = f" >>> Tool ({value['messages'][-1].name}) <<< "
    if isinstance(value["messages"][-1], AIMessage):
        print(f"{respondant}: ", value["messages"][-1].content)


def get_user_input(msg: str) -> str:
    user_input = input(msg)
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Garage Out!")
        sys.exit(0)
    return user_input
