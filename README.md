# IntelliDoc Conversational Retrieval System

A FastAPI-based Retrieval-Augmented Generation (RAG) system that allows users to upload documents and perform intelligent document retrieval and question answering.

## Features

- 📄 **Document Upload**: Support for PDF and TXT file uploads
- 🔍 **Text Parsing**: Automatic text extraction from uploaded documents
- 🧠 **Text Embeddings**: Generate semantic embeddings using sentence-transformers
- 🗄️ **Vector Storage**: Store and retrieve documents using ChromaDB
- 🚀 **FastAPI Backend**: RESTful API with automatic documentation
- 🔄 **CORS Support**: Cross-origin resource sharing enabled

## Project Structure

```
intellidoc-conversational-retrieval-system/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── routers/
│   └── upload.py          # File upload endpoints
├── services/
│   ├── embedding.py       # Text embedding service
│   └── rag.py            # RAG implementation (placeholder)
├── utils/
│   └── parser.py         # Document parsing utilities
└── vector_store/
    └── chroma_store.py   # ChromaDB vector store
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/eyuuab/intellidoc-conversational-retrieval-system.git
cd intellidoc-conversational-retrieval-system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

## API Endpoints

### Root Endpoint
- **GET** `/` - Health check endpoint
- **Response**: `{"message": "RAG backend is live!"}`

### File Upload
- **POST** `/api/upload` - Upload PDF or TXT files
- **Request**: Multipart form data with file
- **Response**: Document ID and upload confirmation

## Usage Example

```bash
# Upload a document
curl -X POST "http://127.0.0.1:8001/api/upload" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_document.pdf"
```

## Technologies Used

- **FastAPI**: Modern web framework for building APIs
- **ChromaDB**: Vector database for similarity search
- **sentence-transformers**: Pre-trained models for text embeddings
- **PyMuPDF**: PDF processing and text extraction
- **Uvicorn**: ASGI server for running the application

## Development

The application runs on `http://127.0.0.1:8001` by default. The API documentation is available at:
- Swagger UI: `http://127.0.0.1:8001/docs`
- ReDoc: `http://127.0.0.1:8001/redoc`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Commit and push your changes
5. Create a pull request

## License

This project is open source and available under the MIT License.
