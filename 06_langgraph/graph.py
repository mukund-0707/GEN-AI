from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from openai import OpenAI


client = OpenAI()


class State(TypedDict):
    query: str
    llm_result: str | None


def chatbot(state: State):
    query = state['query']

    query_reponse = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "user", "content": query}
        ]
    )

    result = query_reponse.choices[0].message.content

    # OpenAI
    print("Result:", result)
    return {
        "query": query,
        "llm_result": result
    }


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()


def main():
    user = input("> ")
    cmd: State = {
        "query": user,
        "llm_result": None
    }
    graph_result = graph.invoke(cmd)
    print("GraphResult: ", graph_result)


main()
