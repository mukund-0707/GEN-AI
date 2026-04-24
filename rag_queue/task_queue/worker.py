# flake8: noqa
# bash rag_queue/task_queue/worker.sh  run command
# root ➜ /workspaces/PROMPT ENGINEERING $ uvicorn rag_queue.server:app --host 0.0.0.0 --port 8001

from openai import OpenAI
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings

vector_db = None


client = OpenAI()


async def get_vector_db():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_db = QdrantVectorStore.from_existing_collection(
        collection_name="pdf_docs",
        embedding=embeddings,
        url="http://vector-db:6333",
    )
    return vector_db


async def process_query(query: str):
    vector_db = get_vector_db()

    print(f"Processing query: {query}")
    search_result = vector_db.similarity_search(query=query)
    print(f"Search Result: {search_result}")

    context = "\n\n\n".join(
        [
            f"""Page Content: {result.page_content}\n
                Page Number:{result.metadata['page_label']}\n
                File location: {result.metadata['source']}"""
            for result in search_result
        ]
    )

    SYSTEM_PROMPT = f"""
        You are helpful AI Assistant who answers user query bases on the available
        context retrived from a PDF file along eith page context and pasge number
        also.
    
        You should only ans the user based on the following context and navigate
        the user to open the right page number to know more.

        Context:
        {context}
    """

    chat_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
    )

    print(
        f"User Query: {query} and the response: {chat_response.choices[0].message.content}",
        "\n\n",
    )
    return chat_response.choices[0].message.content
