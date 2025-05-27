# IntelliDoc Testing Guide

This guide will walk you through setting up, running, and testing the IntelliDoc conversational retrieval system.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- Google API Key (for full functionality)

### 1. Setup Environment

```bash
# Clone the repository
git clone https://github.com/eyuuab/intellidoc-conversational-retrieval-system.git
cd intellidoc-conversational-retrieval-system

# Create and activate virtual environment
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list | grep -E "(streamlit|fastapi|chromadb|sentence-transformers)"
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your Google API key
nano .env  # or use your preferred editor
```

Add your Google API key to the `.env` file:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

## 🎨 Running the Streamlit UI (Recommended)

### Option 1: Direct Streamlit Command
```bash
streamlit run streamlit_app.py
```

### Option 2: Using the Runner Script
```bash
python run_streamlit.py
```

The Streamlit app will open at: `http://localhost:8501`

## ⚡ Running the FastAPI Backend

```bash
# Start the FastAPI server
uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

The API will be available at:
- Main API: `http://127.0.0.1:8001`
- Swagger Docs: `http://127.0.0.1:8001/docs`
- ReDoc: `http://127.0.0.1:8001/redoc`

## 🧪 Testing the Application

### 1. Test Document Upload (Streamlit UI)

1. Open the Streamlit app at `http://localhost:8501`
2. Go to the "📤 Upload Documents" tab
3. Upload a PDF or TXT file
4. Verify the upload success message
5. Check the "📋 Document Library" tab to see uploaded documents

### 2. Test Chat Functionality

1. After uploading documents, go to the "💬 Chat with Documents" tab
2. Ask questions like:
   - "What are the main topics in the documents?"
   - "Summarize the key points"
   - "What is this document about?"
3. Verify you get relevant responses

### 3. Test Analytics Dashboard

1. Go to the "📊 Analytics" page
2. Verify document statistics are displayed
3. Check word frequency charts
4. Test export functionality

### 4. Test Settings Panel

1. Go to the "⚙️ Settings" page
2. Verify system information is displayed
3. Test configuration changes
4. Check environment variable management

### 5. Test FastAPI Endpoints

#### Test Health Check
```bash
curl http://127.0.0.1:8001/
```
Expected response: `{"message": "RAG backend is live!"}`

#### Test File Upload
```bash
# Upload a text file
curl -X POST "http://127.0.0.1:8001/api/upload" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@test_document.txt"
```

#### Test with Python
```python
import requests

# Test health endpoint
response = requests.get("http://127.0.0.1:8001/")
print(response.json())

# Test file upload
with open("test_document.txt", "rb") as f:
    files = {"file": f}
    response = requests.post("http://127.0.0.1:8001/api/upload", files=files)
    print(response.json())
```

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. Import Errors
```bash
# If you get import errors, ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. Google API Key Issues
- Ensure you have a valid Google API key from Google AI Studio
- Check that the key is correctly set in the `.env` file
- Verify the key has access to Gemini Pro API

#### 3. ChromaDB Issues
```bash
# If ChromaDB has issues, try clearing the database
rm -rf chroma_data/
# Then restart the application
```

#### 4. Port Already in Use
```bash
# If port 8501 is in use for Streamlit
streamlit run streamlit_app.py --server.port 8502

# If port 8001 is in use for FastAPI
uvicorn main:app --reload --host 127.0.0.1 --port 8002
```

#### 5. Memory Issues with Large Documents
- Reduce the embedding model size in settings
- Process smaller documents first
- Increase system memory if possible

## 📝 Creating Test Documents

### Sample Text File (test_document.txt)
```
IntelliDoc Test Document

This is a sample document for testing the IntelliDoc system.

Key Features:
- Document upload and processing
- Text embedding generation
- Vector storage with ChromaDB
- Conversational AI with Google Gemini Pro
- Beautiful Streamlit interface

The system can process both PDF and TXT files, extract text content,
generate semantic embeddings, and enable natural language queries
about the document content.

This document serves as a test case to verify that all components
of the system are working correctly.
```

### Sample Questions to Test
- "What is IntelliDoc?"
- "What are the key features mentioned?"
- "How does the system process documents?"
- "What technologies are used?"

## 🔧 Development Testing

### Running Tests with Different Configurations

#### Test with Debug Mode
```bash
# Set debug mode in .env
DEBUG=True
RELOAD=True

# Run with verbose logging
streamlit run streamlit_app.py --logger.level debug
```

#### Test with Different Embedding Models
1. Go to Settings page
2. Change embedding model to "all-mpnet-base-v2"
3. Upload new documents
4. Test query performance

#### Test File Size Limits
1. Try uploading files of different sizes
2. Test the max file size limit
3. Verify error handling for oversized files

## 📊 Performance Testing

### Load Testing
```python
import concurrent.futures
import requests
import time

def upload_test_file():
    with open("test_document.txt", "rb") as f:
        files = {"file": f}
        response = requests.post("http://127.0.0.1:8001/api/upload", files=files)
        return response.status_code

# Test concurrent uploads
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(upload_test_file) for _ in range(10)]
    results = [future.result() for future in futures]
    print(f"Success rate: {results.count(200)}/10")
```

## ✅ Verification Checklist

- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] Environment variables configured
- [ ] Streamlit app starts without errors
- [ ] FastAPI backend starts without errors
- [ ] Document upload works
- [ ] Text extraction works for PDF/TXT
- [ ] Embeddings are generated
- [ ] Vector storage works
- [ ] Chat functionality works (with Google API key)
- [ ] Analytics dashboard displays data
- [ ] Settings panel is functional
- [ ] All API endpoints respond correctly

## 🆘 Getting Help

If you encounter issues:

1. Check the console output for error messages
2. Verify all dependencies are installed correctly
3. Ensure environment variables are set properly
4. Check the troubleshooting section above
5. Review the application logs
6. Create an issue on GitHub with detailed error information

## 📈 Next Steps

After successful testing:

1. Upload your own documents
2. Experiment with different types of queries
3. Explore the analytics dashboard
4. Customize settings for your use case
5. Consider integrating with your own data sources
