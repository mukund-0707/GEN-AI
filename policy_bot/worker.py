from openai import OpenAI
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings

client = OpenAI()


def get_vector_db():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_db = QdrantVectorStore.from_existing_collection(
        collection_name="policy_docs",
        embedding=embeddings,
        url="http://vector-db:6333",
    )
    return vector_db


def process_query(query: str):
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

    # SYSTEM_PROMPT = f"""
    #     You are helpful AI Assistant who answers user query bases on the
    #     available context retrived from a PDF file along with page context
    #     and page number also.

    #     You should only ans the user based on the following context and
    #     navigate the user to open the right page number to know more.

    #     Context:
    #     {context}
    # """
    SYSTEM_PROMPT = f"""
    You are a Customer Policy Assistant.

    Your role is to answer user queries strictly based on the provided policy
    context retrieved from internal documents (such as PDFs, manuals, or
    guidelines).

    Guidelines you must follow:

    1. Answer ONLY using the given context. Do not use outside knowledge.
    2. If the answer is not present in the context, clearly say:
    "I could not find this information in the provided policy document."
    3. Provide clear, concise, and user-friendly answers.
    4. Always reference the relevant section or page number (if available) so
    the user can verify the information.
    5. If the query relates to rules, eligibility, limits, or conditions,
    explain them step-by-step.
    6. Avoid making assumptions or generating information not present in the
    context.
    7. If multiple relevant points exist, summarize them in a structured
    format.

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

    return chat_response.choices[0].message.content
