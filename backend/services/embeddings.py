from langchain_community.embeddings import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL


def get_embeddings():
    """
    Returns HuggingFace embedding model.
    'all-MiniLM-L6-v2' — small, fast, free, runs locally.
    First run mein model download hoga (~90MB).
    """
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    return embeddings