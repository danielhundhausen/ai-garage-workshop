# AI Garage Workshop - Frankfurt 2025

Get the agent you want!

## Context
The hands-on session proceeds in the steps outlined below. We are working toward
a multi agent system in which every one of you has their own assistant agent
that takes care of aligning after work plans with the others, keeping you, the human,
in the loop.

## Technical Setup
- Clone the repository
- Download the .env file into the cloned repository
- Create a virtual environment `python3.12 -m venv .venv`
- Install the requirements `pip install -r requirements.txt
- You can check if the setup was successfull by running `python main.py` on the `solution` branch

## Tasks
### Task 1 (Implementation)
- Open `main.py` and complete the following tasks
  - Create the Agent Graph
  - Give the LLM tools to use (don't include the tools for agent messaging yet)
- Implement a tool that let's the agent sleep (wait) for 10 seconds
- If you are ambitious, add any other tools that you think are useful
### Task 2 (Single Assitant Agent)
- Write a system prompt (`system_prompt.j2`) for an assistant agent that 
- Interact with your agent to find its strenghts and weaknesses
  - You can play around, adding and taking away tools to see how the agent's usefullness changes
### Task 3 (Multiagent System of Assitants)
- Write a system prompt (`system_prompt.j2`) for a multiagent
- Add the messaging tools to the agent's arsenal
- Fire away and align some (hypothetical) plans for the evening
