from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from services.vector_store import load_vector_store
from config import GEMINI_API_KEY, GEMINI_MODEL, TOP_K_RESULTS


LEGAL_PROMPT_TEMPLATE = """
You are an expert legal assistant. Your job is to analyze legal documents and answer questions accurately.

Use ONLY the context provided below to answer the question.
If the answer is not found in the context, say: "I could not find this information in the uploaded documents."

Always:
- Cite relevant clauses or sections when possible
- Highlight any legal risks or important obligations
- Keep your answer clear and structured

Context:
{context}

Question: {question}

Answer:
"""


def get_rag_chain():
    """Build and return the LangChain RAG chain."""
    vector_store = load_vector_store()

    if vector_store is None:
        raise ValueError("No documents uploaded yet. Please upload a legal document first.")

    # Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GEMINI_API_KEY,
        temperature=0.2,      # Low temp = more factual, less creative
        max_output_tokens=1024,
    )

    # Custom prompt
    prompt = PromptTemplate(
        template=LEGAL_PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )

    # Retriever — top 4 most relevant chunks
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K_RESULTS},
    )

    # Full RAG chain
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",           # Stuff all chunks into one prompt
        retriever=retriever,
        return_source_documents=True, # Sources bhi return karo
        chain_type_kwargs={"prompt": prompt},
    )

    return chain


def run_query(question: str) -> dict:
    """Run a question through the RAG chain and return answer + sources."""
    chain = get_rag_chain()
    result = chain.invoke({"query": question})

    # Extract source info
    sources = []
    seen = set()
    for doc in result.get("source_documents", []):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "?")
        key = f"{source}-{page}"
        if key not in seen:
            seen.add(key)
            sources.append({
                "file": os.path.basename(source) if source != "Unknown" else "Unknown",
                "page": page,
                "snippet": doc.page_content[:200] + "...",
            })

    import os
    return {
        "answer": result["result"],
        "sources": sources,
    }