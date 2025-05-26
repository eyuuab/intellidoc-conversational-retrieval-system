import fitz  # PyMuPDF
import io

def parse_file(file_bytes: bytes, file_extension: str) -> str:
    if file_extension == ".pdf":
        return parse_pdf(file_bytes)
    elif file_extension == ".txt":
        return file_bytes.decode("utf-8")
    else:
        return ""

def parse_pdf(file_bytes: bytes) -> str:
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text
