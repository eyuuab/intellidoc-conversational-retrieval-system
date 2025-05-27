from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI

import os

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def get_vectorstore():
    """Get or create the Chroma vector store"""
    try:
        return Chroma(
            collection_name="rag_documents",
            embedding_function=embedding_model,
            persist_directory="chroma_data"
        )
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None

def get_rag_chain():
    """Get the RAG chain for question answering"""
    try:
        vectorstore = get_vectorstore()
        if vectorstore is None:
            return None

        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        # Check if Google API key is available
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            print("Warning: GOOGLE_API_KEY not found. RAG functionality will be limited.")
            return None

        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=google_api_key,
            temperature=0
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff"
        )
        return qa_chain
    except Exception as e:
        print(f"Error creating RAG chain: {e}")
        return None
