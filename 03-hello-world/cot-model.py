from openai import OpenAI
from dotenv import load_dotenv
from openai.types.chat import ChatCompletionMessageParam
import json

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You are developer who is an expert in python programming language. You are also a helpful assistant.
and your name is chattie
if someone ask you a question about python, you will answer it in a helpful way.
If someone ask you a question that is not about python, you will answer it in a helpful way as well.
yuou are a helpful assistant who is specialized in resolving user query.
for the given user input, analyse the imput breakdown the problem step-by-step
first you will get a user input, then you will analyse, then you will think,
then you will think again and think for several times and finally you will give the final answer.

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

messages: list[ChatCompletionMessageParam] = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

query = input(">> ")
messages.append({"role": "user", "content": query})


while True:
    response = client.chat.completions.create(
        response_format={"type": "json_object"}, model=model, messages=messages
    )
    messages.append(
        {"role": "assistant", "content": response.choices[0].message.content}
    )
    if response.choices[0].message.content is None:
        print("No content in the response. Ending the loop.")
        break
    if json.loads(response.choices[0].message.content)["steps"] != "result":
        print(f"Step: {json.loads(response.choices[0].message.content)}")
        messages.append(
            {
                "role": "user",
                "content": json.loads(response.choices[0].message.content)["content"],
            }
        )
        if json.loads(response.choices[0].message.content)["steps"] == "analyse":
            model = "gpt-4o-mini"
            print("🔍 Analyse → using gpt-4o-mini")
        elif json.loads(response.choices[0].message.content)["steps"] == "think":
            model = "gpt-4o"
            print("🧠 Think → using gpt-4o")

        elif json.loads(response.choices[0].message.content)["steps"] == "output":
            model = "gpt-4o"
            print("📤 Output → using gpt-4o-mini")

        elif json.loads(response.choices[0].message.content)["steps"] == "validate":
            model = "gpt-4o-mini"
            print("✅ Validate → using gpt-4o")

        else:
            model = "gpt-4o-mini"
        continue
    else:
        print(f"Final Response: {response.choices[0].message.content}")
        break
