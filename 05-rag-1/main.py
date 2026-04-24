from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv()

pdf_path = Path(__file__).parent / "sample.pdf"
loader = PyPDFLoader(file_path=pdf_path)
doc = loader.load()

# chunking the document into smaller pieces
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

splits_doc = text_splitter.split_documents(documents=doc)

# vector embedding

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = QdrantVectorStore.from_documents(
    collection_name="pdf_docs",
    documents=splits_doc,
    embedding=embeddings,
    url="http://vector-db:6333",
)
print(f"Document: {vector_store}")
print("Document loaded and indexed successfully!")
