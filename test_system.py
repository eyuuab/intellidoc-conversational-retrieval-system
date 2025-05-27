#!/usr/bin/env python3
"""
IntelliDoc System Test Script

This script tests the core functionality of the IntelliDoc system.
"""

import os
import sys
import requests
import time
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    required_modules = [
        'streamlit',
        'fastapi',
        'chromadb',
        'sentence_transformers',
        'langchain',
        'plotly',
        'pandas'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module.replace('-', '_'))
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("💡 Install missing packages with: pip install -r requirements.txt")
        return False
    
    print("✅ All imports successful!")
    return True

def test_environment():
    """Test environment configuration"""
    print("\n🔧 Testing environment...")
    
    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        print("  ✅ .env file found")
    else:
        print("  ⚠️  .env file not found")
        print("  💡 Copy .env.example to .env and configure")
    
    # Check Google API key
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if google_api_key:
        print("  ✅ Google API key configured")
    else:
        print("  ⚠️  Google API key not found")
        print("  💡 Add GOOGLE_API_KEY to your .env file")
    
    return True

def test_local_modules():
    """Test local module imports"""
    print("\n📦 Testing local modules...")
    
    try:
        from utils.parser import parse_file
        print("  ✅ utils.parser")
    except ImportError as e:
        print(f"  ❌ utils.parser: {e}")
        return False
    
    try:
        from services.embedding import embed_text
        print("  ✅ services.embedding")
    except ImportError as e:
        print(f"  ❌ services.embedding: {e}")
        return False
    
    try:
        from vector_store.chroma_store import collection
        print("  ✅ vector_store.chroma_store")
    except ImportError as e:
        print(f"  ❌ vector_store.chroma_store: {e}")
        return False
    
    try:
        from services.rag import get_rag_chain
        print("  ✅ services.rag")
    except ImportError as e:
        print(f"  ❌ services.rag: {e}")
        return False
    
    print("✅ All local modules imported successfully!")
    return True

def test_embedding_functionality():
    """Test embedding functionality"""
    print("\n🧠 Testing embedding functionality...")
    
    try:
        from services.embedding import embed_text
        
        # Test embedding generation
        test_text = "This is a test document for IntelliDoc."
        embedding = embed_text(test_text)
        
        if embedding is not None and len(embedding) > 0:
            print(f"  ✅ Embedding generated (dimension: {len(embedding)})")
            return True
        else:
            print("  ❌ Failed to generate embedding")
            return False
    
    except Exception as e:
        print(f"  ❌ Embedding test failed: {e}")
        return False

def test_vector_store():
    """Test vector store functionality"""
    print("\n🗄️ Testing vector store...")
    
    try:
        from vector_store.chroma_store import collection, add_to_vectorstore
        from services.embedding import embed_text
        
        # Test adding a document
        test_text = "IntelliDoc test document for vector store."
        test_id = "test_doc_001"
        embedding = embed_text(test_text)
        
        add_to_vectorstore(test_id, test_text, embedding)
        print("  ✅ Document added to vector store")
        
        # Test collection count
        count = collection.count()
        print(f"  ✅ Vector store contains {count} documents")
        
        return True
    
    except Exception as e:
        print(f"  ❌ Vector store test failed: {e}")
        return False

def test_file_parsing():
    """Test file parsing functionality"""
    print("\n📄 Testing file parsing...")
    
    try:
        from utils.parser import parse_file
        
        # Create a test text file
        test_content = b"This is a test document for IntelliDoc parsing functionality."
        
        # Test TXT parsing
        parsed_text = parse_file(test_content, ".txt")
        if parsed_text.strip():
            print("  ✅ TXT file parsing works")
        else:
            print("  ❌ TXT file parsing failed")
            return False
        
        return True
    
    except Exception as e:
        print(f"  ❌ File parsing test failed: {e}")
        return False

def test_fastapi_server():
    """Test if FastAPI server can be reached"""
    print("\n🚀 Testing FastAPI server...")
    
    try:
        response = requests.get("http://127.0.0.1:8001/", timeout=5)
        if response.status_code == 200:
            print("  ✅ FastAPI server is running")
            print(f"  📝 Response: {response.json()}")
            return True
        else:
            print(f"  ❌ FastAPI server returned status {response.status_code}")
            return False
    
    except requests.exceptions.ConnectionError:
        print("  ⚠️  FastAPI server not running")
        print("  💡 Start with: uvicorn main:app --reload --host 127.0.0.1 --port 8001")
        return False
    
    except Exception as e:
        print(f"  ❌ FastAPI test failed: {e}")
        return False

def create_test_document():
    """Create a test document for testing"""
    print("\n📝 Creating test document...")
    
    test_content = """IntelliDoc Test Document

This is a comprehensive test document for the IntelliDoc system.

Key Features Tested:
1. Document upload and processing
2. Text embedding generation
3. Vector storage with ChromaDB
4. Conversational AI with Google Gemini Pro
5. Beautiful Streamlit interface

Technical Components:
- FastAPI backend for document processing
- Sentence transformers for embeddings
- ChromaDB for vector storage
- LangChain for RAG implementation
- Streamlit for user interface

This document contains various topics and information that can be used
to test the question-answering capabilities of the system.

Sample questions you can ask:
- What is IntelliDoc?
- What are the key features?
- What technologies are used?
- How does the system work?
"""
    
    with open("test_document.txt", "w") as f:
        f.write(test_content)
    
    print("  ✅ Test document created: test_document.txt")
    return True

def main():
    """Main test function"""
    print("🧪 IntelliDoc System Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Environment Test", test_environment),
        ("Local Modules Test", test_local_modules),
        ("Embedding Test", test_embedding_functionality),
        ("Vector Store Test", test_vector_store),
        ("File Parsing Test", test_file_parsing),
        ("FastAPI Server Test", test_fastapi_server),
        ("Test Document Creation", create_test_document)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"  ❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your IntelliDoc system is ready to use.")
        print("\n🚀 Next steps:")
        print("1. Run: streamlit run streamlit_app.py")
        print("2. Open: http://localhost:8501")
        print("3. Upload the test_document.txt file")
        print("4. Start chatting with your documents!")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        print("\n💡 Common solutions:")
        print("- Install missing packages: pip install -r requirements.txt")
        print("- Configure .env file with Google API key")
        print("- Start FastAPI server: uvicorn main:app --reload")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
