from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

reponse = client.embeddings.create(
    input="The food was delicious and the waiter was very attentive.",
    model="text-embedding-3-large",
)

print(f"RESPONSE: {reponse}")
print(f"Length of embedding: {len(reponse.data[0].embedding)}")
