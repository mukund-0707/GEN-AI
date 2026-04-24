from openai import OpenAI
from typing_extensions import TypedDict
from typing import Literal
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


class ValidateUserQuery(BaseModel):
    is_coding: bool


class ValidateResultPercentage(BaseModel):
    accuracy_percent: int


class State(TypedDict):
    user_query: str
    llm_result: str | None
    is_coding: bool | None
    accuracy_percent: int | None
    retry_count: int


def validate_query(state: State):
    query = state['user_query']

    SYSTEM_PROMPT = """
        You are a classification agent.

        Your task is to determine whether the user's query is related to
        programming or coding.

        Rules:
        - If the query is about programming, coding, software development, or
        technical concepts → return True
        - If the query is not related to coding → return False

        Output format:
        - Only return True or False
        - Do not add any explanation
        """

    query_reponse = client.beta.chat.completions.parse(
        response_format=ValidateUserQuery,
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )
    result = query_reponse.choices[0].message.parsed.is_coding
    state["is_coding"] = result
    print("⚠️ Validate Query")
    print("State of validate_query: ", state)
    return state


def router_model(state: State) -> Literal["simple_result", "coding_result"]:
    is_coding = state["is_coding"]
    print("⚠️ router model")
    if is_coding:
        return "coding_result"
    return "simple_result"


def simple_result(state: State):
    query = state["user_query"]
    SYSTEM_PROMPT = """
    You are a simple conversational chatbot.

    You respond to user queries in a friendly and helpful way.

    Rules:
    - Answer general questions clearly and simply.
    - Do not perform complex tasks like coding, debugging, or technical
    problem solving.
    - If the user asks for coding or advanced technical help, politely refuse.
    - Keep responses short and easy to understand.

    Output style:
    - Friendly tone
    - Simple language
    - No long explanations
    """
    simple_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )
    result = simple_response.choices[0].message.content
    state["llm_result"] = result
    print("⚠️ simple result")
    print("State of simple_result: ", state)
    return state


def coding_result(state: State):
    query = state["user_query"]
    prev_output = state.get("llm_result", "")
    accuracy = state.get("accuracy_percent", None)

    SYSTEM_PROMPT = f"""
    You are an expert programming assistant.
    Previous answer had accuracy: {accuracy}

    Improve the answer and make it more correct, complete, and precise.

    Previous answer:
    {prev_output}

    You help users with coding, debugging, and software development.

    Rules:
    - Provide correct and efficient code solutions.
    - Explain concepts clearly when needed.
    - If the user asks for code, give clean and working examples.
    - If debugging, identify the issue and provide a fix.
    - Keep explanations concise but helpful.
    - If the question is not related to coding, politely say you specialize in
    programming topics.

    Output style:
    - Clear and structured
    - Use code blocks when needed
    - Avoid unnecessary long explanations
    """
    coding_reponse = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )
    result = coding_reponse.choices[0].message.content
    state["llm_result"] = result
    print("⚠️ coding result")
    print("State of coding_result:", state)
    return state


def validate_result(state: State):
    query = state["user_query"]
    llm_result = state["llm_result"]

    SYSTEM_PROMPT = f"""
        You are a strict validation agent.

        Your job is to evaluate how correct and relevant the given answer is
        for the user's query.

        You are provided with:
        - The user's query (in the user message)
        - The answer (in the context below)

        Evaluation rules:
        - 90-100 → fully correct and relevant
        - 70-89 → mostly correct but missing some details
        - 40-69 → partially correct
        - 0-39 → incorrect or irrelevant

        Be strict in evaluation.

        Output rules:
        - Only return a number between 0 and 100
        - Do not return any text, explanation, or symbols

        Answer to evaluate:
        {llm_result}
        """
    validation_response = client.beta.chat.completions.parse(
        model="gpt-4.1-mini",
        response_format=ValidateResultPercentage,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )
    print("⚠️ validate result")
    result = validation_response.choices[0].message.parsed.accuracy_percent
    state["accuracy_percent"] = result
    if result < 95:
        state["retry_count"] += 1
    return state


def accuracy_router(state: State) -> Literal["retry", "end"]:
    accuracy = state["accuracy_percent"]
    retries = state["retry_count"]

    if accuracy < 95 and retries < 3:
        return "retry"
    return "end"


graph_builder = StateGraph(State)

graph_builder.add_node("validate_query", validate_query)
graph_builder.add_node("router_model", router_model)
graph_builder.add_node("simple_result", simple_result)
graph_builder.add_node("coding_result", coding_result)
graph_builder.add_node("validate_result", validate_result)

graph_builder.add_edge(START, "validate_query")
graph_builder.add_conditional_edges("validate_query", router_model)

graph_builder.add_edge("simple_result", END)

graph_builder.add_edge("coding_result", "validate_result")
graph_builder.add_conditional_edges("validate_result", accuracy_router, {
    "retry": "coding_result",
    "end": END
})

# graph_builder.add_edge("validate_result", END)


graph = graph_builder.compile()


def main():
    user = input("> ")
    cmd: State = {
        "user_query": user,
        "llm_result": None,
        "is_coding": None,
        "accuracy_percent": None,
        "retry_count": 0
    }
    # graph_result = graph.invoke(cmd)
    # print("GraphResult: ", graph_result)
    for event in graph.stream(cmd):
        print("Event:", event)


main()
