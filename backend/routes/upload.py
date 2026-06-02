from fastapi import APIRouter, UploadFile, File, HTTPException
from services.document_processor import process_file
from services.vector_store import add_to_vector_store
from config import UPLOAD_DIR
import os
import shutil

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF or DOCX legal document.
    Automatically processes and indexes it into FAISS.
    """
    # File type check
    allowed = [".pdf", ".docx", ".doc"]
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"Only PDF and DOCX files allowed. Got: {ext}")

    # Save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process + index
    try:
        chunks = process_file(file_path)
        add_to_vector_store(chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    return {
        "status": "success",
        "filename": file.filename,
        "chunks_indexed": len(chunks),
        "message": f"Document '{file.filename}' uploaded and indexed successfully.",
    }