from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition

import requests

load_dotenv()

todos = []


@tool
def add_task(task: str):
    """this add task in todos and return true"""
    todos.append(task)
    return True


@tool
def get_all_todos():
    """this returns all todos"""
    return todos


@tool
def remove_task(task: str):
    """this remove task from todos"""
    todos.remove(task)
    return True


@tool
def update_task(task: str, index: int):
    """update task in todos"""
    todos[index] = task


@tool
def add_two_numbers(a: int, b: int):
    """This two takes 2 number and add them"""
    return a + b


@tool
def get_weather(city: str) -> str:
    """This tool takes a city name as input and
returns the current weather in that city."""
    try:
        res = requests.get(f"https://wttr.in/{city}?format=3")

        if res.status_code == 200:
            return res.text
        else:
            return "Weather data not available"

    except Exception as e:
        return f"Error: {str(e)}"


tools = [get_weather, add_two_numbers, add_task, get_all_todos, remove_task, update_task]

llm = init_chat_model(model_provider="openai", model="gpt-4o-mini")
llm_with_tool = llm.bind_tools(tools)


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    messages = llm_with_tool.invoke(state["messages"])
    return {"messages": [messages]}


tool_node = ToolNode(tools=tools)

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
    )
graph_builder.add_edge("tools", "chatbot")


graph = graph_builder.compile()


def main():
    while True:
        query = input("> ")

        cmd = State(
            messages=[{"role": "user", "content": query}]
        )

        for event in graph.stream(cmd, stream_mode="values"):
            print("Event:", event)
            if "messages" in event:
                event["messages"][-1].pretty_print()


main()
