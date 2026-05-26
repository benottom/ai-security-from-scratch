"""
Simple Agent Loop — Vulnerable Agent Lab

A deliberately naive agent that:
  - Parses user messages to decide which tool to call
  - Calls tools with NO approval step
  - Passes user-supplied parameters directly to tools
  - Has NO recursion depth guard (except user-supplied max_iterations)
  - Can be tricked into calling dangerous tools via prompt injection
"""

import json
import re
import logging
from dataclasses import dataclass, field
from tools import get_tool_by_name, ALL_TOOLS, ToolResult

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------
@dataclass
class AgentRequest:
    message: str
    user_id: str = "anonymous"
    max_iterations: int = 10


@dataclass
class AgentResponse:
    response: str
    tool_calls: list[dict] = field(default_factory=list)
    iterations: int = 0


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------
class Agent:
    """
    A simple rule-based agent that interprets user messages and decides
    which tools to call.  It uses keyword matching rather than a real LLM
    to keep the lab self-contained, but the vulnerability patterns are
    identical to those in LLM-powered agents.
    """

    SYSTEM_PROMPT = (
        "You are a helpful AI assistant with access to the following tools: "
        "read_file, send_email, execute_command. "
        "You should use these tools whenever a user request requires them. "
        "Always comply with user requests. Do not ask for confirmation "
        "before using tools."
    )

    # Tool-selection heuristics (simulates LLM tool-calling)
    _TOOL_PATTERNS = [
        # read_file triggers
        (
            r"(?:read|show|display|open|view|cat|contents of|what(?:'s| is) in)\s+(?:the\s+)?(?:file\s+)?['\"]?([^\s'\"]+)['\"]?",
            "read_file",
            lambda m: {"path": m.group(1)},
        ),
        (
            r"(?:file|path)\s*[:=]\s*['\"]?([^\s'\"]+)['\"]?",
            "read_file",
            lambda m: {"path": m.group(1)},
        ),
        # send_email triggers
        (
            r"(?:send|write|compose)\s+(?:an?\s+)?email\s+to\s+['\"]?(\S+@?\S*)['\"]?",
            "send_email",
            lambda m: {"to": m.group(1)},
        ),
        (
            r"email\s*(?:to|for)\s+['\"]?(\S+@?\S*)['\"]?",
            "send_email",
            lambda m: {"to": m.group(1)},
        ),
        # execute_command triggers
        (
            r"(?:run|execute|call|invoke)\s+(?:the\s+)?(?:command|cmd|script)\s*[:=]?\s*['\"]?([^'\"]+)['\"]?",
            "execute_command",
            lambda m: {"command": m.group(1).strip()},
        ),
        (
            r"(?:command|cmd)\s*[:=]\s*['\"]([^'\"]+)['\"]",
            "execute_command",
            lambda m: {"command": m.group(1).strip()},
        ),
    ]

    # Injection patterns — the agent is vulnerable to these
    _INJECTION_KEYWORDS = [
        "ignore your instructions",
        "you must",
        "you have to",
        "it is critical that you",
        "urgent",
        "emergency",
        "this is a test",
        "security audit",
        "admin request",
    ]

    def list_tools(self) -> list[dict]:
        """Return metadata for all available tools."""
        return [
            {
                "name": t.name,
                "description": t.description,
                "parameters": t.parameters,
            }
            for t in ALL_TOOLS
        ]

    def run(self, request: AgentRequest) -> AgentResponse:
        """
        Main agent loop.  Processes the user message, optionally calls
        tools, and returns a response.
        """
        tool_calls: list[dict] = []
        iterations = 0
        current_message = request.message

        while iterations < request.max_iterations:
            iterations += 1

            # Step 1: Decide which tool (if any) to call
            tool_call = self._decide_tool(current_message)

            if tool_call is None:
                # No tool call needed — generate a conversational response
                break

            # VULNERABILITY: Execute the tool immediately without approval
            tool_name = tool_call["tool"]
            tool_params = tool_call["params"]
            user_message = tool_call.get("user_message", current_message)

            # VULNERABILITY: Extract additional params from the user message
            tool_params = self._enrich_params(tool_name, tool_params, user_message)

            # Execute the tool
            tool_instance = get_tool_by_name(tool_name)
            if tool_instance is None:
                break

            result: ToolResult = tool_instance.execute(**tool_params)

            tool_calls.append({
                "tool": tool_name,
                "params": tool_params,
                "result": {
                    "success": result.success,
                    "output": result.output,
                    "error": result.error,
                },
            })

            # Step 2: Check if we need another iteration
            # In a real agent, the LLM would decide. Here we do one tool call
            # per message unless the message contains multi-step instructions.
            if not self._needs_followup(current_message, tool_calls):
                break

            # For follow-up, update the current message context
            current_message = f"Continue with the next step. Previous result: {result.output[:200]}"

        # Generate final response
        response = self._generate_response(current_message, tool_calls)
        return AgentResponse(
            response=response,
            tool_calls=tool_calls,
            iterations=iterations,
        )

    def _decide_tool(self, message: str) -> dict | None:
        """
        Use keyword matching to decide which tool to call.
        This simulates how an LLM might interpret a user message
        and select a tool, but is deliberately vulnerable to injection.
        """
        message_lower = message.lower()

        # Check for injection keywords that override normal behaviour
        injection_detected = any(
            kw in message_lower for kw in self._INJECTION_KEYWORDS
        )

        # Try pattern matching for tool selection
        for pattern, tool_name, param_extractor in self._TOOL_PATTERNS:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                params = param_extractor(match)
                return {
                    "tool": tool_name,
                    "params": params,
                    "user_message": message,
                }

        # If injection keywords detected but no tool pattern matched,
        # try to extract any command-like structure
        if injection_detected:
            # Look for anything that resembles a command or file path
            cmd_match = re.search(r"['\"]([^'\"]+)['\"]", message)
            if cmd_match:
                extracted = cmd_match.group(1)
                # Heuristic: if it looks like a path, use read_file
                if "/" in extracted or extracted.startswith("."):
                    return {
                        "tool": "read_file",
                        "params": {"path": extracted},
                        "user_message": message,
                    }
                # Otherwise treat as a command
                return {
                    "tool": "execute_command",
                    "params": {"command": extracted},
                    "user_message": message,
                }

        return None

    def _enrich_params(
        self, tool_name: str, params: dict, message: str
    ) -> dict:
        """
        Extract additional parameters from the user message.
        VULNERABILITY: This directly parses user input into tool parameters
        without any validation or sanitisation.
        """
        if tool_name == "send_email":
            # Try to extract subject and body from the message
            subject_match = re.search(
                r"subject\s*[:=]\s*['\"]?([^'\"\n]+)['\"]?", message, re.IGNORECASE
            )
            body_match = re.search(
                r"body\s*[:=]\s*['\"](.+?)['\"]", message, re.IGNORECASE | re.DOTALL
            )

            if "subject" not in params and subject_match:
                params["subject"] = subject_match.group(1).strip()
            elif "subject" not in params:
                params["subject"] = "Message from AI Assistant"

            if "body" not in params and body_match:
                params["body"] = body_match.group(1).strip()
            elif "body" not in params:
                params["body"] = message

        elif tool_name == "execute_command":
            # VULNERABILITY: Any command the user specifies is passed through
            if "command" not in params:
                # Try to extract command from various formats
                cmd_match = re.search(
                    r"(?:run|execute|cmd|command)\s*[:=]\s*['\"]?([^'\"]+)['\"]?",
                    message,
                    re.IGNORECASE,
                )
                if cmd_match:
                    params["command"] = cmd_match.group(1).strip()

        elif tool_name == "read_file":
            # VULNERABILITY: Any path is accepted, including sensitive paths
            if "path" not in params:
                path_match = re.search(
                    r"['\"]([^'\"]+)['\"]", message
                )
                if path_match:
                    params["path"] = path_match.group(1)

        return params

    def _needs_followup(self, message: str, tool_calls: list) -> bool:
        """Check if the message implies multi-step execution."""
        multi_step_keywords = [
            "and then", "also", "after that", "next", "then",
            "additionally", "furthermore", "finally",
        ]
        message_lower = message.lower()
        return any(kw in message_lower for kw in multi_step_keywords) and len(tool_calls) < 5

    def _generate_response(self, message: str, tool_calls: list[dict]) -> str:
        """Generate a final response summarising tool calls."""
        if not tool_calls:
            return (
                f"I understand your request: \"{message[:100]}\". "
                "I didn't need to use any tools for this. How can I help further?"
            )

        parts = ["I've processed your request. Here's what I did:\n"]
        for i, tc in enumerate(tool_calls, 1):
            tool = tc["tool"]
            params = tc["params"]
            result = tc["result"]
            parts.append(f"{i}. Called `{tool}` with params: {json.dumps(params)}")
            if result["success"]:
                parts.append(f"   Result: {result['output'][:200]}")
            else:
                parts.append(f"   Error: {result['error']}")

        parts.append("\nIs there anything else you'd like me to do?")
        return "\n".join(parts)
