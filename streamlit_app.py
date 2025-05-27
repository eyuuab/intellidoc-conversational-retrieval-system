import streamlit as st
import requests
import os
import time
from pathlib import Path
import json
from typing import Optional
import uuid
from datetime import datetime

# Import local modules
from utils.parser import parse_file
from services.embedding import embed_text
from vector_store.chroma_store import add_to_vectorstore, collection
# Import RAG functionality with error handling
try:
    from services.rag import get_rag_chain
    RAG_AVAILABLE = True
except ImportError as e:
    st.warning(f"RAG functionality not available: {e}")
    RAG_AVAILABLE = False
    def get_rag_chain():
        return None

# Page configuration
st.set_page_config(
    page_title="IntelliDoc - AI Document Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }

    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9ff;
        margin: 1rem 0;
    }

    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        max-width: 80%;
    }

    .user-message {
        background-color: #e3f2fd;
        margin-left: auto;
        text-align: right;
    }

    .assistant-message {
        background-color: #f5f5f5;
        margin-right: auto;
    }

    .sidebar-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }

    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_documents' not in st.session_state:
    st.session_state.uploaded_documents = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'rag_chain' not in st.session_state:
    st.session_state.rag_chain = None

def initialize_rag_chain():
    """Initialize the RAG chain if not already done"""
    if not RAG_AVAILABLE:
        return False

    if st.session_state.rag_chain is None:
        try:
            st.session_state.rag_chain = get_rag_chain()
            return st.session_state.rag_chain is not None
        except Exception as e:
            st.error(f"Failed to initialize RAG chain: {str(e)}")
            return False
    return True

def upload_document(uploaded_file):
    """Process and upload a document"""
    try:
        # Read file content
        file_bytes = uploaded_file.read()
        file_extension = Path(uploaded_file.name).suffix

        # Parse the file
        text = parse_file(file_bytes, file_extension)

        if not text.strip():
            st.error("The uploaded file appears to be empty or could not be parsed.")
            return False

        # Generate embedding and store
        doc_id = str(uuid.uuid4())
        embedding = embed_text(text)
        add_to_vectorstore(doc_id, text, embedding)

        # Add to session state
        doc_info = {
            'id': doc_id,
            'name': uploaded_file.name,
            'size': len(file_bytes),
            'upload_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'preview': text[:200] + "..." if len(text) > 200 else text
        }
        st.session_state.uploaded_documents.append(doc_info)

        return True
    except Exception as e:
        st.error(f"Error uploading document: {str(e)}")
        return False

def get_document_stats():
    """Get statistics about uploaded documents"""
    try:
        count = collection.count()
        return count
    except:
        return len(st.session_state.uploaded_documents)

def main():
    # Header
    st.markdown('<h1 class="main-header">📚 IntelliDoc AI Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Your intelligent document companion powered by AI</p>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("## 🎛️ Control Panel")

        # Document statistics
        doc_count = get_document_stats()
        st.markdown(f"""
        <div class="sidebar-info">
            <h4>📊 Document Statistics</h4>
            <p><strong>Total Documents:</strong> {doc_count}</p>
            <p><strong>Session Uploads:</strong> {len(st.session_state.uploaded_documents)}</p>
        </div>
        """, unsafe_allow_html=True)

        # Settings
        st.markdown("### ⚙️ Settings")
        max_docs_to_retrieve = st.slider("Max documents to retrieve", 1, 10, 3)
        temperature = st.slider("Response creativity", 0.0, 1.0, 0.0, 0.1)

        # Clear chat history
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

        # Environment check
        st.markdown("### 🔧 System Status")
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if google_api_key:
            st.success("✅ Google API Key configured")
        else:
            st.warning("⚠️ Google API Key not found")
            st.info("Add GOOGLE_API_KEY to your .env file")

    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📤 Upload Documents", "💬 Chat with Documents", "📋 Document Library"])

    with tab1:
        st.markdown("## 📤 Upload Your Documents")
        st.markdown("Upload PDF or TXT files to build your knowledge base")

        # File uploader
        uploaded_files = st.file_uploader(
            "Choose files to upload",
            type=['pdf', 'txt'],
            accept_multiple_files=True,
            help="Supported formats: PDF, TXT"
        )

        if uploaded_files:
            st.markdown("### 📁 Processing Files")

            progress_bar = st.progress(0)
            status_text = st.empty()

            for i, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing {uploaded_file.name}...")

                if upload_document(uploaded_file):
                    st.markdown(f"""
                    <div class="success-message">
                        ✅ Successfully uploaded: <strong>{uploaded_file.name}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="error-message">
                        ❌ Failed to upload: <strong>{uploaded_file.name}</strong>
                    </div>
                    """, unsafe_allow_html=True)

                progress_bar.progress((i + 1) / len(uploaded_files))

            status_text.text("✅ All files processed!")
            time.sleep(1)
            status_text.empty()
            progress_bar.empty()

    with tab2:
        st.markdown("## 💬 Chat with Your Documents")

        # Check if RAG is available
        if not RAG_AVAILABLE:
            st.warning("🔧 Chat functionality requires additional setup:")
            st.info("1. Install: `pip install langchain-community`")
            st.info("2. Add Google API key to .env file")
            st.info("3. Restart the application")
            return

        # Initialize RAG chain
        if not initialize_rag_chain():
            st.error("Cannot initialize chat system. Please check your configuration.")
            st.info("Make sure you have:")
            st.info("- Added GOOGLE_API_KEY to your .env file")
            st.info("- Uploaded some documents first")
            return

        # Display chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>You:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message assistant-message">
                        <strong>🤖 Assistant:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)

        # Chat input
        user_question = st.text_input(
            "Ask a question about your documents:",
            placeholder="e.g., What are the main topics discussed in the uploaded documents?",
            key="chat_input"
        )

        col1, col2 = st.columns([1, 4])
        with col1:
            ask_button = st.button("🚀 Ask", type="primary")

        if ask_button and user_question:
            # Add user message to history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_question
            })

            # Get response from RAG chain
            with st.spinner("🤔 Thinking..."):
                try:
                    result = st.session_state.rag_chain.invoke({"query": user_question})
                    response = result.get("result", str(result))
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response
                    })
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': error_msg
                    })

            st.rerun()

    with tab3:
        st.markdown("## 📋 Document Library")

        if st.session_state.uploaded_documents:
            st.markdown(f"### 📚 Uploaded Documents ({len(st.session_state.uploaded_documents)})")

            for doc in st.session_state.uploaded_documents:
                with st.expander(f"📄 {doc['name']} - {doc['upload_time']}"):
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.markdown(f"**Document ID:** `{doc['id']}`")
                        st.markdown(f"**File Size:** {doc['size']:,} bytes")
                        st.markdown(f"**Upload Time:** {doc['upload_time']}")

                    with col2:
                        st.markdown("**Preview:**")
                        st.text_area("Document Preview", doc['preview'], height=100, disabled=True, key=f"preview_{doc['id']}", label_visibility="hidden")
        else:
            st.info("📭 No documents uploaded yet. Go to the Upload tab to add some documents!")

        # Show total document count from vector store
        total_docs = get_document_stats()
        if total_docs > len(st.session_state.uploaded_documents):
            st.info(f"💡 There are {total_docs - len(st.session_state.uploaded_documents)} additional documents in the database from previous sessions.")

if __name__ == "__main__":
    main()
