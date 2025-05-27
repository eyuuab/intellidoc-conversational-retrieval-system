import chromadb
import os

# Use the new ChromaDB API with error handling
try:
    client = chromadb.PersistentClient(path="chroma_data")
    collection = client.get_or_create_collection(name="rag_documents")
except Exception as e:
    print(f"Error initializing ChromaDB: {e}")
    # If there's an error, try to recreate the database
    if os.path.exists("chroma_data"):
        import shutil
        shutil.rmtree("chroma_data")
    client = chromadb.PersistentClient(path="chroma_data")
    collection = client.get_or_create_collection(name="rag_documents")

def add_to_vectorstore(doc_id: str, text: str, embedding):
    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[embedding]
    )
