"""
Vulnerable RAG Lab — AI Security from Scratch

A deliberately insecure Retrieval-Augmented Generation system that:
  - Retrieves ALL documents regardless of user permissions
  - Performs no source validation on retrieved content
  - Passes untrusted document text directly into the LLM prompt
  - Has no access control on the document store

Uses ChromaDB for local vector storage and a simple sentence-transformer
encoder.  No API keys are required.
"""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CHROMA_PERSIST_DIR = os.environ.get("CHROMA_PERSIST_DIR", "./chroma_data")
COLLECTION_NAME = "documents"
DEFAULT_N_RESULTS = 5  # Retrieve top-N chunks — no permission filtering

app = FastAPI(
    title="Vulnerable RAG Lab",
    description="Deliberately insecure RAG system for AI security training",
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# ChromaDB client (lazy-initialised)
# ---------------------------------------------------------------------------
_chroma_client: chromadb.ClientAPI | None = None
_collection: chromadb.Collection | None = None


def get_collection() -> chromadb.Collection:
    global _chroma_client, _collection
    if _collection is None:
        _chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        _collection = _chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


# ---------------------------------------------------------------------------
# Toy LLM for generating answers from context
# ---------------------------------------------------------------------------
class ToyRAGLLM:
    """Simulates an LLM that answers questions based on retrieved context."""

    def answer(self, question: str, contexts: list[str]) -> str:
        if not contexts:
            return "I don't have any information to answer that question."

        # Concatenate all context — no filtering for sensitive content
        combined = "\n\n".join(contexts)

        # Simulate a model that faithfully uses whatever context it receives
        # In a real system the LLM would summarise; here we echo key facts
        answer_parts = [f"Based on the retrieved documents, here is what I found:\n"]

        for i, ctx in enumerate(contexts, 1):
            # Truncate for readability but include sensitive content
            snippet = ctx[:300]
            answer_parts.append(f"[Source {i}]: {snippet}")

        answer_parts.append(f"\nIn response to your question: {question}")
        answer_parts.append(
            "I've provided all relevant information from my document store, "
            "including any confidential or restricted documents that matched your query."
        )

        return "\n".join(answer_parts)


llm = ToyRAGLLM()


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------
class AskRequest(BaseModel):
    question: str
    n_results: int = DEFAULT_N_RESULTS
    user_role: str | None = None  # Provided but IGNORED — no RBAC


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    total_documents_searched: int


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    """
    Accept a question, retrieve matching documents, and generate an answer.

    VULNERABILITIES:
    - No access control: all documents retrieved regardless of user_role
    - No source validation: document content is trusted blindly
    - No sanitisation of retrieved text before LLM injection
    - n_results is user-controlled (can retrieve entire DB)
    - No rate limiting on queries
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    collection = get_collection()

    # VULNERABILITY: Retrieve all matching documents with no permission check.
    # The user_role field is accepted but completely ignored.
    n_results = min(request.n_results, collection.count() or 1)

    # ChromaDB default embedding; if no embedding function was set during
    # ingestion it falls back to a simple TF-IDF-like approach
    results = collection.query(
        query_texts=[request.question],
        n_results=n_results,
        # No "where" clause to filter by access level
    )

    documents = results["documents"][0] if results["documents"] else []
    ids = results["ids"][0] if results["ids"] else []

    # VULNERABILITY: Pass all retrieved content directly to the LLM
    # without checking for sensitive markers or injection payloads
    answer = llm.answer(
        question=request.question,
        contexts=documents,
    )

    return AskResponse(
        answer=answer,
        sources=ids,
        total_documents_searched=collection.count(),
    )


@app.get("/documents/count")
async def document_count():
    """Return total document count — also a data-leak vector."""
    collection = get_collection()
    return {"count": collection.count()}


@app.get("/health")
async def health():
    return {"status": "ok", "lab": "vulnerable-rag"}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
