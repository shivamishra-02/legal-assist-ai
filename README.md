# ⚖️ LegalAssist AI

RAG-powered legal document analyzer built with **FastAPI + LangChain + Gemini + FAISS**.

## Tech Stack
- **Backend**: FastAPI, LangChain, Google Gemini 1.5 Flash
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2` (local, free)
- **Vector Store**: FAISS (local)
- **Frontend**: Vanilla HTML/CSS/JS

## Setup

```bash
# 1. Clone & enter
git clone https://github.com/yourusername/legal-assist-ai.git
cd legal-assist-ai

# 2. Backend setup
cd backend
pip install -r requirements.txt

# 3. Add API key
# Create .env in root:
# GEMINI_API_KEY=your_key_here

# 4. Run backend
uvicorn main:app --reload

# 5. Open frontend
# Open frontend/index.html in browser
```

## Features
- Upload PDF/DOCX legal documents
- Semantic search using FAISS
- Gemini-powered Q&A with source citations
- Risk & obligation highlighting