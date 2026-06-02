from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from services.embeddings import get_embeddings
from config import FAISS_INDEX_PATH
import os


def build_vector_store(chunks: list[Document]) -> FAISS:
    """Create FAISS index from document chunks and save to disk."""
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(FAISS_INDEX_PATH)
    print(f"[VectorStore] Index saved to {FAISS_INDEX_PATH}")
    return vector_store


def load_vector_store() -> FAISS | None:
    """Load existing FAISS index from disk. Returns None if not found."""
    if not os.path.exists(FAISS_INDEX_PATH):
        return None
    embeddings = get_embeddings()
    vector_store = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )
    print("[VectorStore] Index loaded from disk")
    return vector_store


def add_to_vector_store(chunks: list[Document]):
    """Add new chunks to existing index, or create new one."""
    existing = load_vector_store()
    embeddings = get_embeddings()

    if existing:
        existing.add_documents(chunks)
        existing.save_local(FAISS_INDEX_PATH)
        print(f"[VectorStore] Added {len(chunks)} chunks to existing index")
    else:
        build_vector_store(chunks)