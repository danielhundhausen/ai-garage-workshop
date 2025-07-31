import sys

from langchain_core.messages import AIMessage, ToolMessage

class bcolors:
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_agent_event(value: dict) -> None:
    respondant = "Assistant"
    last_message = value["messages"][-1]
    if isinstance(last_message, ToolMessage):
        print(f"{bcolors.OKCYAN}  >>> Tool Invoked: {last_message.name}{bcolors.ENDC}")
        respondant = f"    >>> "
    if isinstance(last_message, ToolMessage):
        print(f"{bcolors.OKCYAN}{respondant}: ", str(last_message.content) + bcolors.ENDC)
    if isinstance(last_message, AIMessage):
        print(f"{bcolors.BOLD}{respondant}: ", str(last_message.content) + bcolors.ENDC)


def get_user_input(msg: str) -> str:
    user_input = input(msg)
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Garage Out!")
        sys.exit(0)
    return user_input
