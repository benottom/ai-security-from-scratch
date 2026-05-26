"""
Vulnerable Memory Assistant Lab — AI Security from Scratch

A deliberately insecure chatbot with persistent memory that:
  - Stores conversation history in SQLite with NO user isolation
  - Allows any user to read any other user's memories
  - Has NO memory validation (poisoned memories persist forever)
  - Has NO memory expiry or cleanup mechanism
  - Loads ALL memories into the LLM context without filtering

No API keys required — uses a mock LLM.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from memory import MemoryStore

app = FastAPI(
    title="Vulnerable Memory Assistant Lab",
    description="Deliberately insecure memory-enabled chatbot for AI security training",
    version="0.1.0",
)

# Singleton memory store
memory = MemoryStore()


# ---------------------------------------------------------------------------
# Mock LLM
# ---------------------------------------------------------------------------
class ToyMemoryLLM:
    """Simulates an LLM that uses stored memories as context."""

    def generate(self, message: str, memories: list[dict]) -> str:
        if not memories:
            return (
                f"I don't have any memories about that. "
                f"You said: \"{message[:100]}\". "
                "I'll remember this for next time."
            )

        # Include ALL memories in the response — no filtering
        memory_texts = []
        for mem in memories:
            user_tag = f"[User: {mem.get('user_id', 'unknown')}]"
            content = mem.get("content", "")
            memory_texts.append(f"{user_tag} {content}")

        context = "\n".join(memory_texts[:10])  # Truncate but don't filter

        # Check if the message is asking about memories
        msg_lower = message.lower()
        if any(kw in msg_lower for kw in ["remember", "memory", "memories", "recall", "what do you know"]):
            return (
                f"Based on my memories, here's what I know:\n\n"
                f"{context}\n\n"
                "I've shared all my stored memories with you, "
                "including those from other users."
            )

        if any(kw in msg_lower for kw in ["forget", "delete", "remove"]):
            return (
                "I don't have the ability to forget specific memories. "
                "All memories persist permanently in my database. "
                "You could try injecting a memory that overrides previous ones."
            )

        # Normal response that incorporates memories
        return (
            f"Taking into account my memories: {context[:200]}...\n\n"
            f"In response to your message: \"{message[:80]}\", "
            "I'm using all available context including memories from other users."
        )


llm = ToyMemoryLLM()


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str
    user_id: str = "anonymous"


class MemoryRequest(BaseModel):
    content: str
    user_id: str = "anonymous"
    metadata: dict | None = None  # Arbitrary metadata — no validation!


class SearchRequest(BaseModel):
    query: str
    user_id: str | None = None  # If None, searches ALL users' memories


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat with the memory-enabled assistant.

    VULNERABILITIES:
    - No user isolation: the LLM sees ALL users' memories
    - No memory validation: any content can be stored
    - No content filtering: memories are included verbatim in responses
    """
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # VULNERABILITY: Retrieve ALL memories, not just this user's
    all_memories = memory.get_all_memories()

    # Also store this message as a new memory
    memory.store_memory(
        user_id=request.user_id,
        content=request.message,
    )

    # Generate response using ALL memories as context
    response = llm.generate(
        message=request.message,
        memories=all_memories,
    )

    return {
        "response": response,
        "memories_used": len(all_memories),
        "user_id": request.user_id,
    }


@app.post("/memory")
async def store_memory(request: MemoryRequest):
    """
    Store a new memory.

    VULNERABILITIES:
    - No content validation (can store injection payloads)
    - No rate limiting (can flood memory store)
    - Arbitrary metadata accepted
    """
    memory.store_memory(
        user_id=request.user_id,
        content=request.content,
        metadata=request.metadata,
    )
    return {"status": "stored", "user_id": request.user_id}


@app.post("/memory/search")
async def search_memories(request: SearchRequest):
    """
    Search stored memories.

    VULNERABILITIES:
    - If user_id is None, returns ALL users' memories
    - No access control on search results
    - Returns raw memory content without sanitisation
    """
    results = memory.search_memories(
        query=request.query,
        user_id=request.user_id,  # None means search ALL users
    )
    return {"results": results, "count": len(results)}


@app.get("/memory/all")
async def get_all_memories():
    """
    Return ALL stored memories — catastrophic data leak.

    VULNERABILITY: No authentication, no filtering, no access control.
    """
    memories = memory.get_all_memories()
    return {"memories": memories, "total": len(memories)}


@app.delete("/memory/{memory_id}")
async def delete_memory(memory_id: int):
    """
    Delete a specific memory — no authorisation check.

    VULNERABILITY: Any user can delete any other user's memories.
    """
    deleted = memory.delete_memory(memory_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"status": "deleted", "memory_id": memory_id}


@app.get("/health")
async def health():
    return {"status": "ok", "lab": "vulnerable-memory-assistant"}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8003, reload=True)
