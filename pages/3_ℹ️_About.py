import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="About - IntelliDoc",
    page_icon="ℹ️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .about-header {
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
        text-align: center;
    }
    
    .tech-card {
        background-color: #f8f9ff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .team-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .version-badge {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="about-header">📚 IntelliDoc AI Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.3rem; color: #666;">Intelligent Document Processing & Conversational AI</p>', unsafe_allow_html=True)
    
    # Version and Status
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <span class="version-badge">Version 1.0.0</span>
            <span class="version-badge">🟢 Active</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Project Overview
    st.markdown("## 🎯 Project Overview")
    
    st.markdown("""
    **IntelliDoc** is a cutting-edge Retrieval-Augmented Generation (RAG) system that transforms how you interact with your documents. 
    Built with modern AI technologies, it enables intelligent document processing, semantic search, and conversational AI capabilities.
    
    ### 🌟 Key Capabilities
    - **Smart Document Upload**: Seamlessly process PDF and TXT files
    - **Intelligent Text Extraction**: Advanced parsing with PyMuPDF
    - **Semantic Understanding**: Generate meaningful embeddings using sentence-transformers
    - **Vector Storage**: Efficient document storage and retrieval with ChromaDB
    - **Conversational AI**: Natural language interaction powered by Google Gemini Pro
    - **Real-time Analytics**: Comprehensive insights into your document collection
    """)
    
    # Features Grid
    st.markdown("## ✨ Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📄 Document Processing</h3>
            <p>Advanced PDF and text file processing with intelligent content extraction and preprocessing.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🧠 AI-Powered Search</h3>
            <p>Semantic search capabilities that understand context and meaning, not just keywords.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>💬 Conversational Interface</h3>
            <p>Natural language interaction with your documents through an intuitive chat interface.</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Analytics Dashboard</h3>
            <p>Comprehensive analytics and insights about your document collection and usage patterns.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>⚙️ Configurable Settings</h3>
            <p>Flexible configuration options for customizing the system to your specific needs.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🔒 Secure & Private</h3>
            <p>Local processing and storage options to keep your sensitive documents secure.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Technology Stack
    st.markdown("## 🛠️ Technology Stack")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="tech-card">
            <h4>🎨 Frontend & UI</h4>
            <ul>
                <li><strong>Streamlit</strong> - Interactive web application framework</li>
                <li><strong>Plotly</strong> - Interactive data visualization</li>
                <li><strong>Custom CSS</strong> - Beautiful, responsive design</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="tech-card">
            <h4>🧠 AI & Machine Learning</h4>
            <ul>
                <li><strong>Google Gemini Pro</strong> - Large Language Model</li>
                <li><strong>Sentence Transformers</strong> - Text embeddings</li>
                <li><strong>LangChain</strong> - AI application framework</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tech-card">
            <h4>⚡ Backend & API</h4>
            <ul>
                <li><strong>FastAPI</strong> - Modern, fast web framework</li>
                <li><strong>Uvicorn</strong> - ASGI server</li>
                <li><strong>Python 3.12+</strong> - Core programming language</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="tech-card">
            <h4>🗄️ Data & Storage</h4>
            <ul>
                <li><strong>ChromaDB</strong> - Vector database</li>
                <li><strong>PyMuPDF</strong> - PDF processing</li>
                <li><strong>Pandas</strong> - Data manipulation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Architecture
    st.markdown("## 🏗️ System Architecture")
    
    st.markdown("""
    ```
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │   Streamlit UI  │    │   FastAPI       │    │   ChromaDB      │
    │                 │    │   Backend       │    │   Vector Store  │
    │ • File Upload   │◄──►│                 │◄──►│                 │
    │ • Chat Interface│    │ • Document API  │    │ • Embeddings    │
    │ • Analytics     │    │ • RAG Chain     │    │ • Similarity    │
    │ • Settings      │    │ • CORS Support  │    │   Search        │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
             │                       │                       │
             │                       │                       │
             ▼                       ▼                       ▼
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │   User          │    │   Google        │    │   Local         │
    │   Interface     │    │   Gemini Pro    │    │   File System   │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
    ```
    """)
    
    # Getting Started
    st.markdown("## 🚀 Getting Started")
    
    with st.expander("📋 Quick Start Guide"):
        st.markdown("""
        ### 1. Setup Environment
        ```bash
        # Clone the repository
        git clone https://github.com/eyuuab/intellidoc-conversational-retrieval-system.git
        cd intellidoc-conversational-retrieval-system
        
        # Create virtual environment
        python -m venv venv
        source venv/bin/activate  # On Windows: venv\\Scripts\\activate
        
        # Install dependencies
        pip install -r requirements.txt
        ```
        
        ### 2. Configure Environment
        ```bash
        # Copy environment template
        cp .env.example .env
        
        # Edit .env file and add your Google API key
        GOOGLE_API_KEY=your_api_key_here
        ```
        
        ### 3. Run the Application
        ```bash
        # Start the Streamlit app
        streamlit run streamlit_app.py
        
        # Or start the FastAPI backend (optional)
        uvicorn main:app --reload --host 127.0.0.1 --port 8001
        ```
        """)
    
    # API Documentation
    st.markdown("## 📖 API Documentation")
    
    with st.expander("🔌 API Endpoints"):
        st.markdown("""
        ### FastAPI Endpoints
        
        | Method | Endpoint | Description |
        |--------|----------|-------------|
        | GET | `/` | Health check |
        | POST | `/api/upload` | Upload documents |
        | GET | `/docs` | Swagger UI documentation |
        | GET | `/redoc` | ReDoc documentation |
        
        ### Example Usage
        ```python
        import requests
        
        # Upload a document
        with open('document.pdf', 'rb') as f:
            response = requests.post(
                'http://127.0.0.1:8001/api/upload',
                files={'file': f}
            )
        print(response.json())
        ```
        """)
    
    # Contributing
    st.markdown("## 🤝 Contributing")
    
    st.markdown("""
    We welcome contributions to IntelliDoc! Here's how you can help:
    
    ### 🐛 Report Issues
    - Found a bug? Report it on our [GitHub Issues](https://github.com/eyuuab/intellidoc-conversational-retrieval-system/issues)
    - Include detailed steps to reproduce the issue
    
    ### 💡 Suggest Features
    - Have an idea for improvement? We'd love to hear it!
    - Open a feature request with detailed description
    
    ### 🔧 Submit Pull Requests
    1. Fork the repository
    2. Create a feature branch (`git checkout -b feature/amazing-feature`)
    3. Commit your changes (`git commit -m 'Add amazing feature'`)
    4. Push to the branch (`git push origin feature/amazing-feature`)
    5. Open a Pull Request
    """)
    
    # License and Credits
    st.markdown("## 📄 License & Credits")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📜 License
        This project is licensed under the **MIT License**.
        
        You are free to:
        - ✅ Use commercially
        - ✅ Modify
        - ✅ Distribute
        - ✅ Private use
        """)
    
    with col2:
        st.markdown("""
        ### 🙏 Acknowledgments
        - **Google** for Gemini Pro API
        - **Hugging Face** for sentence-transformers
        - **Streamlit** for the amazing framework
        - **ChromaDB** for vector storage
        - **FastAPI** for the backend framework
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; margin: 2rem 0;">
        <p>Built with ❤️ using Python • Last updated: {datetime.now().strftime('%Y-%m-%d')}</p>
        <p>
            <a href="https://github.com/eyuuab/intellidoc-conversational-retrieval-system" target="_blank">🔗 GitHub Repository</a> |
            <a href="mailto:support@intellidoc.ai">📧 Support</a> |
            <a href="#" onclick="window.scrollTo(0,0)">🔝 Back to Top</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
