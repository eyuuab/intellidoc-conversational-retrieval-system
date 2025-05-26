import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="chroma_data"))
collection = client.get_or_create_collection(name="rag_documents")

def add_to_vectorstore(doc_id: str, text: str, embedding):
    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[embedding]
    )
