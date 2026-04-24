from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
import json

from openai.types.chat import ChatCompletionMessageParam

client = OpenAI()


# SYSTEM_PROMPT = """
#     you are a python developer who is an expert in the python programming language. You are also a helpful assistant."""

# reponse = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {"role": "user", "content": "What is the capital of France?"}
#     ]
# )

SYSTEM_PROMPT = """
you are a helpful AI  assistant who is specialized in resolving user query.
for the given user input, analyse the imput breakdown the problem step-by-step

The steps are you get a user input, you analyse, you think, you think again and think for several

Follow the steps in that sequence that is "analyse", "think", "output", "validate" and finally "result".

Rules:
1. Follow strict JSON output as per schema
2. Always perform one step at a time and wait for the next input.
3. Carefully analyse the user query

Output Format"
{{"steps":"string", "content": "string"}}

Example:
Input What is 2+2
Output: {{"step": "analyse", "content": "Alright! The user is interest in math query and he is asking a basic arithmetic opretion"}}
Output: {{"step": "think", "content": "To perform this addition, I must go from left to right and all the operands."}}
Output: {{"step": "output", "content": "4"}}
Output: {{"step": "validate", "content": "Seems like 4 is correct ans for 2 + 2 "}}
Output: {{"step": "result", "content": "2 + 2 = 4 and this is calculated by adding all numbers"}}
"""

# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {"role": "user", "content": "What is 5/2*(3+4) to the 4th power?"},
#         {"role": "assistant", "content": json.dumps({"step": "analyse", "content": "The user is asking for the evaluation of a mathematical expression that involves division, multiplication, addition, and exponentiation."}) },
#         {"role": "assistant", "content": json.dumps({"step": "think", "content": "First, I need to calculate the expression inside the parentheses (3+4), then follow the order of operations to simplify the entire expression."}) },
#         {"role": "assistant", "content": json.dumps( {"step": "output", "content": "The expression simplifies to (5/2) * 7 to the 4th power."}) },
#         {"role": "assistant", "content": json.dumps({"step": "validate", "content": "The initial simplification seems correct as (3+4) equals 7."})},
#         {"role": "assistant", "content": json.dumps({"step": "result", "content": "The final calculation involves taking (5/2) * 7, and then raising the result to the 4th power. Therefore, (5/2 * 7) ^ 4."}) }
#     ]
# )

# print(f"RESPONSE: {response}")
# original_response = response.choices[0].message.content
# print(f"Original Response: {original_response}")


messages: list[ChatCompletionMessageParam] = [
    {"role": "system", "content": SYSTEM_PROMPT}
]
query = input("> ")
messages.append({"role": "user", "content": query})


while True:
    response = client.chat.completions.create(
        model="gpt-4o-mini", response_format={"type": "json_object"}, messages=messages
    )

    messages.append(
        {"role": "assistant", "content": response.choices[0].message.content}
    )
    # print(f"Response: {response.choices[0].message.content}")

    if response.choices[0].message.content is None:
        print("No content in the response. Ending the loop.")
        break

    if json.loads(response.choices[0].message.content)["steps"] != "result":
        print(f"Thinking: {response.choices[0].message.content}")
        continue
    else:
        print(f"Final Response: {response.choices[0].message.content}")
        break
