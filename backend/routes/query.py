from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.rag_chain import run_query

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
async def query_document(request: QueryRequest):
    """Ask a question about the uploaded legal documents."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        result = run_query(request.question)
        return {
            "status": "success",
            "question": request.question,
            "answer": result["answer"],
            "sources": result["sources"],
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")