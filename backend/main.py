from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.upload import router as upload_router
from routes.query import router as query_router

app = FastAPI(
    title="LegalAssist AI",
    description="RAG-powered legal document analyzer using LangChain + Gemini",
    version="1.0.0",
)

# CORS — frontend se requests allow karo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production mein specific origin dena
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(upload_router, prefix="/api", tags=["Upload"])
app.include_router(query_router, prefix="/api", tags=["Query"])


@app.get("/")
def root():
    return {"message": "LegalAssist AI is running ✅"}


@app.get("/health")
def health():
    return {"status": "healthy"}