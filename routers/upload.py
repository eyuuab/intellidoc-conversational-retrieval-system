from fastapi import APIRouter, File, UploadFile, HTTPException
from utils.parser import parse_file
from pathlib import Path
import uuid
from services.embedding import embed_text
from vector_store.chroma_store import add_to_vectorstore


router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=400, detail="Only PDF or TXT files are allowed")

    contents = await file.read()
    filename = Path(file.filename)
    
    text = parse_file(contents, filename.suffix)
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Parsed file is empty")
    
    doc_id = str(uuid.uuid4())
    embedding = embed_text(text)
    add_to_vectorstore(doc_id, text, embedding)

    return {"filename": file.filename, "doc_id": doc_id, "message": "Document uploaded and embedded"}