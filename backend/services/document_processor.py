from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.schema import Document
from config import CHUNK_SIZE, CHUNK_OVERLAP
import os


def load_document(file_path: str) -> list[Document]:
    """Load PDF or DOCX and return list of LangChain Documents."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext in [".docx", ".doc"]:
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    documents = loader.load()
    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    """Split documents into chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    return chunks


def process_file(file_path: str) -> list[Document]:
    """Full pipeline: load → split → return chunks."""
    docs = load_document(file_path)
    chunks = split_documents(docs)
    print(f"[Processor] {len(chunks)} chunks created from {file_path}")
    return chunks