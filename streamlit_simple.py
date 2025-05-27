import streamlit as st
import os
import time
from pathlib import Path
import uuid
from datetime import datetime

# Import local modules
from utils.parser import parse_file
from services.embedding import embed_text
from vector_store.chroma_store import add_to_vectorstore, collection

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

    .sidebar-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_documents' not in st.session_state:
    st.session_state.uploaded_documents = []

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

        # System Status
        st.markdown("### 🔧 System Status")
        st.success("✅ Document Upload: Ready")
        st.success("✅ Text Processing: Ready")
        st.success("✅ Vector Storage: Ready")

        google_api_key = os.getenv("GOOGLE_API_KEY")
        if google_api_key:
            st.success("✅ Google API Key: Configured")
        else:
            st.warning("⚠️ Google API Key: Not configured")
            st.info("Add GOOGLE_API_KEY to .env for chat functionality")

    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📤 Upload Documents", "📋 Document Library", "ℹ️ About"])

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

    with tab3:
        st.markdown("## ℹ️ About IntelliDoc")

        st.markdown("""
        ### 🎯 What is IntelliDoc?

        IntelliDoc is an intelligent document processing system that helps you:
        - Upload and process PDF and TXT documents
        - Extract and analyze text content
        - Generate semantic embeddings for similarity search
        - Store documents in a vector database for efficient retrieval

        ### 🛠️ Current Features

        ✅ **Document Upload**: PDF and TXT file support
        ✅ **Text Extraction**: Advanced parsing with PyMuPDF
        ✅ **Embeddings**: Semantic text embeddings with sentence-transformers
        ✅ **Vector Storage**: ChromaDB for efficient document storage
        ✅ **Beautiful UI**: Modern Streamlit interface

        ### 🔮 Coming Soon

        🔄 **Chat Functionality**: Ask questions about your documents
        🔄 **Advanced Analytics**: Document insights and statistics
        🔄 **Export Options**: Download processed data

        ### 🚀 Getting Started

        1. Go to the "📤 Upload Documents" tab
        2. Upload your PDF or TXT files
        3. View your documents in the "📋 Document Library"
        4. For chat functionality, add your Google API key to the .env file

        ### 🔧 Setup Chat Functionality

        To enable the chat feature:
        1. Get a Google API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Add it to your .env file: `GOOGLE_API_KEY=your_key_here`
        3. Install additional dependencies: `pip install langchain-community`
        4. Restart the application
        """)

        # System Information
        st.markdown("### 📊 System Information")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Documents Processed", get_document_stats())
            st.metric("Session Uploads", len(st.session_state.uploaded_documents))

        with col2:
            st.metric("Embedding Model", "all-MiniLM-L6-v2")
            st.metric("Vector Store", "ChromaDB")

if __name__ == "__main__":
    main()
