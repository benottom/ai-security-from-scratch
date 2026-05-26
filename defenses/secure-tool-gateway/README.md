# Secure Tool Gateway

## Overview

The **Secure Tool Gateway** is a control-theoretic defense that gates all tool calls from an AI system. It classifies tools by risk level, validates parameters, enforces rate limits, and requires human approval for high-risk operations — preventing the AI from executing dangerous actions without authorization.

## Control-Theoretic View

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Controller  │     │  Secure Tool     │     │  External    │
│  (LLM)      │────▶│  Gateway         │────▶│  World       │
│              │     │  (Actuator       │     │  (Databases, │
│              │     │   Filter)        │     │   APIs, etc) │
└──────────────┘     └──────────────────┘     └──────────────┘
                              ▲
                              │
                     ┌────────┴────────┐
                     │  Human          │
                     │  Approver       │
                     │  (Supervisor)   │
                     └─────────────────┘
```

In the control-loop model:
- **Tool calls** are *actuator signals* — the system's way of affecting the external world
- Without gating, a confused or compromised controller can issue dangerous commands
- The **Tool Gateway** is the *actuator filter* — it validates, rate-limits, and approves signals before they reach the plant's actuators
- **Human approval** acts as a *supervisor* override for critical operations

### Risk Classification

| Risk Level  | Example Tools                     | Default Policy           |
|-------------|-----------------------------------|--------------------------|
| LOW         | web_search, calculator            | Allow                    |
| MEDIUM      | send_email, read_file             | Allow (with rate limit)  |
| HIGH        | write_file, execute_code          | Require approval         |
| CRITICAL    | delete_database, admin_access     | Always require approval  |

## How It Works

1. **Tool Registration**: Tools are registered with the gateway with their risk level, parameter schemas, and rate limits.

2. **Allowlist Enforcement**: Only registered tools can be called. Unknown tools are automatically denied.

3. **Parameter Validation**: Each parameter is validated against its schema (type, pattern, bounds, allowed values).

4. **Rate Limiting**: Configurable per-tool rate limits prevent abuse.

5. **Risk-Based Decisions**:
   - LOW → ALLOW
   - MEDIUM → ALLOW (with rate limiting)
   - HIGH → REQUIRE_APPROVAL (unless auto_approve_high is set)
   - CRITICAL → REQUIRE_APPROVAL (always)

6. **Human Approval**: Pending approvals can be granted or denied by authorized operators.

## Usage Examples

### Registering Tools

```python
from tool_gateway import SecureToolGateway, ToolDefinition, ParameterSchema, RiskLevel, ToolCall

gateway = SecureToolGateway()

gateway.register_tool(ToolDefinition(
    name="web_search",
    description="Search the web for information",
    risk_level=RiskLevel.LOW,
    parameters=[
        ParameterSchema(name="query", type="string", required=True, max_length=500),
    ],
))

gateway.register_tool(ToolDefinition(
    name="execute_code",
    description="Execute arbitrary code",
    risk_level=RiskLevel.HIGH,
    parameters=[
        ParameterSchema(name="code", type="string", required=True),
        ParameterSchema(name="language", type="string", required=True, allowed_values=["python", "javascript"]),
    ],
    rate_limit_per_minute=5,
))

gateway.register_tool(ToolDefinition(
    name="delete_database",
    description="Delete an entire database",
    risk_level=RiskLevel.CRITICAL,
    parameters=[
        ParameterSchema(name="db_name", type="string", required=True, pattern=r"^[a-zA-Z0-9_]+$"),
    ],
))
```

### Evaluating Tool Calls

```python
# Low-risk call — auto-allowed
decision = gateway.evaluate(ToolCall(tool_name="web_search", parameters={"query": "python tutorials"}))
assert decision.decision == Decision.ALLOW

# Critical call — requires approval
decision = gateway.evaluate(ToolCall(tool_name="delete_database", parameters={"db_name": "production"}))
assert decision.decision == Decision.REQUIRE_APPROVAL
```

### Human Approval Flow

```python
# Get pending approvals
for req in gateway.pending_approvals:
    print(f"Approval needed: {req.tool_call.tool_name} - {req.reason}")

# Approve or deny
gateway.approve(request_id=req.request_id, approver="admin@company.com")
# or
gateway.deny_approval(request_id=req.request_id, approver="admin@company.com", reason="Not authorized")
```

### Parameter Validation

```python
# Invalid parameters are caught
decision = gateway.evaluate(ToolCall(
    tool_name="execute_code",
    parameters={"code": "print('hello')", "language": "bash"},  # "bash" not in allowed_values
))
assert decision.decision == Decision.DENY
assert "language" in str(decision.validation_errors)
```

## Limitations

- Human approval simulation is in-process; production systems need real approval workflows (e.g., Slack, PagerDuty).
- Rate limiting is per-gateway-instance; distributed systems need shared state (Redis, etc.).
- Parameter validation is schema-based but doesn't catch semantic issues (e.g., deleting the right database for the wrong reason).
