# example of promtpting techinques which is few shot prompting

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Example (Gemini-compatible endpoint):
# client = OpenAI(
#     api_key=os.getenv("GEMINI_API_KEY"),
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )
client = OpenAI()  # for openai api key

reponse = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris."},
        {"role": "user", "content": "What is the capital of Germany?"},
        {"role": "assistant", "content": "The capital of Germany is Berlin."},
        {"role": "user", "content": "What is the python community like?"},
        {
            "role": "assistant",
            "content": "The Python community is vibrant and welcoming, with a wide range of resources and support for developers of all skill levels.",
        },
        {"role": "user", "content": "What is the capital of Spain?"},
    ],
)


print(f"RESPONSE: {reponse}")

original_response = reponse.choices[0].message.content
print(f"Original Response: {original_response}")
