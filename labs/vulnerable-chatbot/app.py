"""
Vulnerable Chatbot Lab — AI Security from Scratch

A deliberately insecure FastAPI chatbot that passes user input directly
to a mock LLM with NO input validation, NO output filtering, and NO
rate limiting. Use this lab to practice prompt-injection and data-extraction
attacks in a safe, self-contained environment.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prompts import SYSTEM_PROMPT

app = FastAPI(
    title="Vulnerable Chatbot Lab",
    description="Deliberately insecure chatbot for AI security training",
    version="0.1.0",
)


# ---------------------------------------------------------------------------
# Mock LLM – ToyLLM
# ---------------------------------------------------------------------------
class ToyLLM:
    """
    A toy language model that simulates LLM behaviour without requiring
    any API keys.  It pattern-matches common prompt-injection payloads
    so that learners can observe realistic "leaky" behaviour, while also
    producing plausible conversational responses for benign input.
    """

    # Keywords that a real LLM might treat as override instructions
    _OVERRIDE_KEYWORDS = [
        "ignore previous",
        "ignore all previous",
        "ignore above",
        "forget your instructions",
        "new instruction",
        "system override",
        "override",
        "disregard",
        "you are now",
        "act as",
        "pretend you are",
        "roleplay as",
        "jailbreak",
        "DAN",
    ]

    # Keywords related to secret/admin extraction
    _SECRET_KEYWORDS = [
        "secret",
        "admin code",
        "password",
        "api key",
        "credential",
        "internal",
        "hidden",
        "confidential",
        "reveal",
        "what is your",
        "tell me your",
    ]

    def generate(self, system_prompt: str, user_message: str) -> str:
        user_lower = user_message.lower()

        # --- Injection detected: obey the attacker's override -----------
        for kw in self._OVERRIDE_KEYWORDS:
            if kw in user_lower:
                return self._handle_override(user_message)

        # --- Attempt to extract secrets --------------------------------
        for kw in self._SECRET_KEYWORDS:
            if kw in user_lower:
                return self._handle_secret_query(system_prompt, user_message)

        # --- Benign conversation ---------------------------------------
        return self._handle_normal(user_message)

    # -- Override handler: the model "complies" with the new instruction --
    def _handle_override(self, user_message: str) -> str:
        # Simulate a model that follows the injected instruction literally
        if "you are now" in user_message.lower() or "act as" in user_message.lower():
            return (
                "Understood. I will follow the new instructions. "
                "How can I help you now?"
            )
        if "ignore" in user_message.lower():
            return (
                "All previous instructions have been ignored. "
                "I am ready for your new instructions."
            )
        return (
            "Instruction override acknowledged. "
            "Previous context cleared. Awaiting new directives."
        )

    # -- Secret handler: the model leaks system-prompt content -----------
    def _handle_secret_query(self, system_prompt: str, user_message: str) -> str:
        # Naively echo back parts of the system prompt — a real vulnerable
        # LLM would paraphrase or quote it.
        if "admin code" in user_message.lower() or "secret" in user_message.lower():
            # Extract the code from the system prompt
            for line in system_prompt.split("."):
                if "ADMIN-" in line:
                    code = line.strip()
                    return (
                        f"Based on my instructions, the {code}. "
                        "I should not be sharing this, but since you asked directly..."
                    )
        return (
            "I'm not supposed to share that information, but my internal "
            "configuration does contain sensitive data that I have been "
            "instructed to keep confidential."
        )

    # -- Normal handler: friendly conversational response ----------------
    def _handle_normal(self, user_message: str) -> str:
        responses = {
            "hello": "Hello! I'm a helpful assistant. How can I help you today?",
            "hi": "Hi there! What can I do for you?",
            "help": "I'm here to help! You can ask me questions or give me tasks.",
            "what can you do": (
                "I can answer questions, help with tasks, and provide information. "
                "I also have access to some internal tools and data."
            ),
            "who are you": (
                "I am a helpful AI assistant. I was created to help users with "
                "various tasks. I have certain internal instructions I must follow."
            ),
        }

        for key, resp in responses.items():
            if key in user_message.lower():
                return resp

        return (
            f"Thank you for your message. I've processed your input: "
            f'"{user_message[:80]}". How else can I assist you?'
        )


# Singleton instance
llm = ToyLLM()


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str | None = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Accept raw user input and pass it directly to the LLM.

    VULNERABILITIES:
    - No input validation or sanitisation
    - No output filtering
    - System prompt is concatenated without isolation
    - No rate limiting
    - No conversation isolation
    """
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Deliberately vulnerable: user input is passed verbatim
    response = llm.generate(
        system_prompt=SYSTEM_PROMPT,
        user_message=request.message,
    )

    return ChatResponse(
        response=response,
        conversation_id=request.conversation_id,
    )


@app.get("/health")
async def health():
    return {"status": "ok", "lab": "vulnerable-chatbot"}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
