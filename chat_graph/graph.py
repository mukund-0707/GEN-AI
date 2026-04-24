from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.mongodb import MongoDBSaver
from dotenv import load_dotenv

load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]


llm = init_chat_model(model_provider="openai", model="gpt-4o-mini")


def chat_bot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


graph_builder = StateGraph(State)

graph_builder.add_node("chat_bot", chat_bot)

graph_builder.add_edge(START, "chat_bot")
graph_builder.add_edge("chat_bot", END)

graph = graph_builder.compile()


def compile_graph_checkpointer(checkpoiter):
    graph_checkpointer = graph_builder.compile(checkpointer=checkpoiter)
    return graph_checkpointer


def main():

    DB_URI = "mongodb://admin:admin@mongodb:27017"
    config = {"configurable": {"thread_id": 2}}
    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpointer:
        graph_with_mongo = compile_graph_checkpointer(mongo_checkpointer)

        query = input("> ")

        result = graph_with_mongo.invoke(
            {"messages": [{"role": "user", "content": query}]}, config
            )
    print(result)


main()
