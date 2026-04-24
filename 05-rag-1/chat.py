from openai import OpenAI
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings

load_dotenv()

client = OpenAI()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_db = QdrantVectorStore.from_existing_collection(
    collection_name="pdf_docs",
    embedding=embeddings,
    url="http://vector-db:6333",
)

query = input("> ")

search_result = vector_db.similarity_search(query=query)

print(f"Search Result: {search_result}")

context = "\n\n\n".join([f"""Page Content: {result.page_content}\n
            Page Number:{result.metadata['page_label']}\n
            File location: {result.metadata['source']}""" for result in search_result])

SYSTEM_PROMPT = f"""
    You are helpful AI Assistant who answers user query bases on the available
    context retrived from a PDF file along eith page context and pasge number
    also.

    You should only ans the user based on the following context and navigate
    the user to open the right page number to know more.

    Context:
    {context}
"""

print(f"System Prompt: {SYSTEM_PROMPT}")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query},
    ],
)

print(f"Response: {response.choices[0].message.content}")
