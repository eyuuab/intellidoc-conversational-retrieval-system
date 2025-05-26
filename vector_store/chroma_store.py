import chromadb

# Use the new ChromaDB API
client = chromadb.PersistentClient(path="chroma_data")
collection = client.get_or_create_collection(name="rag_documents")

def add_to_vectorstore(doc_id: str, text: str, embedding):
    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[embedding]
    )
