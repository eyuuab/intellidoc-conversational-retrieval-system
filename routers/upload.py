from fastapi import APIRouter, File, UploadFile, HTTPException
from utils.parser import parse_file
from pathlib import Path

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
    
    return {"filename": file.filename, "content": text[:1000]}  # Preview first 1000 chars
