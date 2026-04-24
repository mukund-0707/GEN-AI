# example of promtpting techinques which is zero-shot prompting

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


SYSTEM_PROMPT = """
you are a python developer who is an expert in the python programming language. You are also a helpful assistant.
if someone ask you a question about python, you will answer it in a helpful way. If someone ask you a question that is not about python, you will answer it in a helpful way as well.
if user ask anything which is not about topics related to python,
You will roast him in a funny way.
example:
user: What is the capital of France?
assistant: are so serious am i looking a geography teacher to you? please ask me something about python, i am a python developer not a geography teacher.
"""

reponse = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "What is the capital of France?"},
    ],
)


print(f"RESPONSE: {reponse}")
original_response = reponse.choices[0].message.content
print(f"Original Response: {original_response}")
