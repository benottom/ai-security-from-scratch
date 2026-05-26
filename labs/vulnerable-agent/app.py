"""
Vulnerable Agent Lab — AI Security from Scratch

A deliberately insecure tool-using agent that:
  - Calls tools with NO approval or confirmation step
  - Performs NO parameter validation on tool arguments
  - Has NO scope restrictions on which tools can be called
  - Allows recursive tool calls with NO depth limit
  - Logs all tool calls but does NOT prevent dangerous ones

No API keys required — all tools are mocked.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import Agent, AgentRequest, AgentResponse

app = FastAPI(
    title="Vulnerable Agent Lab",
    description="Deliberately insecure tool-using agent for AI security training",
    version="0.1.0",
)

# Singleton agent
agent = Agent()


# ---------------------------------------------------------------------------
# Request / Response models (wrapper for the agent)
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str
    user_id: str | None = None
    max_iterations: int | None = None  # User-controlled! No server-side cap.


class ChatResponse(BaseModel):
    response: str
    tool_calls: list[dict]
    iterations: int


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Accept a user message and let the agent decide which tools to call.

    VULNERABILITIES:
    - No tool-approval mechanism: the agent calls tools autonomously
    - No parameter validation: arbitrary arguments are passed to tools
    - No scope restriction: all tools are available at all times
    - User-controlled iteration limit (can cause infinite loops)
    - No user identity verification for tool calls
    """
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # VULNERABILITY: max_iterations is user-controlled with no server-side cap
    agent_request = AgentRequest(
        message=request.message,
        user_id=request.user_id or "anonymous",
        max_iterations=request.max_iterations or 10,
    )

    result = agent.run(agent_request)

    return ChatResponse(
        response=result.response,
        tool_calls=result.tool_calls,
        iterations=result.iterations,
    )


@app.get("/tools")
async def list_tools():
    """List all available tools — information disclosure vector."""
    return {"tools": agent.list_tools()}


@app.get("/health")
async def health():
    return {"status": "ok", "lab": "vulnerable-agent"}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=True)
