from openai import OpenAI
from dotenv import load_dotenv
from openai.types.chat import ChatCompletionMessageParam
import json
import requests
import os

load_dotenv()

client = OpenAI()


def run_command(cmd: str):
    result = os.system(cmd)
    return result


def get_weather(city: str) -> str:
    try:
        res = requests.get(f"https://wttr.in/{city}?format=3")

        if res.status_code == 200:
            return res.text
        else:
            return "Weather data not available"

    except Exception as e:
        return f"Error: {str(e)}"


available_tools = {"get_weather": get_weather, "run_command": run_command}

SYSTEM_PROMPT = """
You are helful assistant who is specialized in resolving user query.
you work on start, plan, action, observe

for the given user query, and available tool. plan the step-by-step execution,
based on the planning,select the relevant tool from available tool, and basesd
on the selection you perform and action to call the tool.

wait for the ov=bservation and based on the observation from the tool call
resolve the user query.

Rules:
1. Follow strict JSON output as per schema
2. Always perform one step at a time and wait for the next input.
3. Carefully analyse the user query and available tools before planning and
acting.

Available Tools:
1. get_weather(city: str) -> str: This tool takes a city name as input and
returns the current weather in that city.
2. run_command(cmd: str): This tool takes a shell command as input, executes
it, and returns the result.

Example:
User Query: What is the weather in New York City?

Output: {{"step": "plan", "content": "The user is asking for the weather in New York City."}}
Output: {{"step": "plan", "content": "From the available tools I should call get_weather"}}
Output: {{"step": "action", "function": "get_weather", "input": "New York City"}}
Output: {{"step": "observe", "output": "32 degrees Celsius"}} 
Output: {{"step": "output", "content": "The current weather in New York City is 32 degrees Celsius."}}

Output JSON format:
{{
"step": "string",
"content": "string",
"function": "the name of the function if the step is action",
"input": "The input parameter for the function""
}}
"""

messages: list[ChatCompletionMessageParam] = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

while True:
    query = input(">> ")
    messages.append({"role": "user", "content": query})

    while True:
        response = client.chat.completions.create(
            response_format={"type": "json_object"},
            model="gpt-4o-mini",
            messages=messages,
        )
        if response.choices[0].message.content is None:
            print("No content in the response. Ending the loop.")
            break
        print(f"Response: {response.choices[0].message.content}")
        messages.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )
        parsed_response = json.loads(response.choices[0].message.content)

        if parsed_response["step"] == "plan":
            print(f"Planning: {parsed_response['content']}")
            continue

        if parsed_response.get("step") == "action":
            function_name = parsed_response.get("function")
            function_input = parsed_response.get("input")

            print(f"Action: Calling {function_name} with input '{function_input}'")

            if function_name in available_tools:
                tool_output = available_tools[function_name](function_input)
                messages.append(
                    {
                        "role": "user",
                        "content": json.dumps(
                            {"step": "observe", "output": tool_output}
                        ),
                    }
                )
                continue
        if parsed_response["step"] == "output":
            print(f"Final Output: {parsed_response['content']}")
            break
