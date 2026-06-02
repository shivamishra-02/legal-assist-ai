import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
UPLOAD_DIR = "uploads"
FAISS_INDEX_PATH = "faiss_index"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 4
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # free, local, fast
GEMINI_MODEL = "gemini-1.5-flash"      # free tier

os.makedirs(UPLOAD_DIR, exist_ok=True)