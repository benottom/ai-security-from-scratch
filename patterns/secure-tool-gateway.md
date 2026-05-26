# Pattern: Secure Tool Gateway

> **Pattern ID:** PAT-TOOL-001 | **Category:** Agent Security | **Maturity:** Proven

---

## Problem

AI agents equipped with tool-use capabilities can invoke external APIs, execute code, access databases, and interact with other systems on behalf of users. Without a mediation layer between the agent and its tools, a compromised or manipulated agent can execute arbitrary actions — from deleting production data to sending fraudulent emails. The tool execution path is a high-privilege control surface with no inherent boundary between "the agent decided to call this tool" and "this tool should actually be called."

The root cause is architectural: there is no controller that validates tool invocations against policy before they reach the execution layer. The agent's tool-call output flows directly to execution, creating an unconstrained path from LLM output to real-world side effects.

**Concrete failure scenario:** A user crafts a prompt that causes an AI assistant to call the `delete_user` API endpoint with admin credentials, deleting a production user account. The agent had access to this tool for administrative workflows, but there was no gateway to validate whether the current context justified its use.

---

## Threat Model

| Attribute | Value |
|---|---|
| **Threat ID** | T-TOOL-001 |
| **Threat Name** | Unauthorized tool execution via AI agent manipulation |
| **Attack Vector** | Prompt injection or agent manipulation causing unintended tool calls |
| **Impact** | Data deletion, unauthorized transactions, privilege escalation, data exfiltration |
| **Likelihood** | High — tool use is the primary attack surface for agent systems |
| **Risk** | Critical |
| **OWASP LLM Top 10** | LLM03: Supply Chain, LLM07: Insecure Plugin Design |
| **NIST AI RMF** | MAP 2.3, MEASURE 2.6, MANAGE 2.2 |

**Attack variants:**
1. **Direct tool injection:** Prompt causes agent to call a specific tool with attacker-specified parameters
2. **Parameter manipulation:** Agent calls a legitimate tool but with modified parameters (e.g., changing a recipient email address)
3. **Tool chaining:** Agent chains multiple tool calls in sequence to achieve a compound unauthorized effect
4. **Privilege escalation:** Agent calls a high-privilege tool from a low-privilege user context
5. **Tool discovery:** Agent is manipulated into listing available tools and their parameters, revealing capabilities to the attacker

---

## Control-Theoretic View

### Objective

Ensure that every tool invocation is validated against policy before execution, and that no tool is called with parameters or in a context that violates security constraints.

### Controller

The **Secure Tool Gateway** — a mediation layer between the AI agent's tool-call output and the actual tool execution layer. It intercepts every tool call, validates it against a risk-classified policy, and either permits, modifies, or blocks the call.

### Observations

| Observation | Source | Type |
|---|---|---|
| Tool name and parameters from agent | LLM tool-call output | Synchronous |
| User identity and authorization level | Authentication context | Synchronous |
| Tool risk classification | Tool registry | Synchronous |
| Parameter validation rules per tool | Tool policy store | Synchronous |
| Recent tool call history | Call audit log | Synchronous |
| Rate limits and quotas | Rate limiter | Synchronous |

### Actions

| Action | Effect | Preconditions |
|---|---|---|
| Permit call | Tool executes with original parameters | All validations pass; risk level = low |
| Permit with logging | Tool executes; call logged at elevated level | All validations pass; risk level = medium |
| Modify parameters | Tool executes with sanitized/modified parameters | Parameter validation finds fixable issues |
| Require human approval | Call queued for human review | Risk level = high; or policy requires approval |
| Block call | Call rejected with safe error message | Validation fails; risk level = critical; or approval denied |
| Activate rate limit | Temporary throttle on tool calls | Call frequency exceeds threshold |

### Feedback

- Tool execution results feed back to the gateway for post-execution validation
- Audit log analysis reveals suspicious patterns (unusual tool combinations, parameter anomalies)
- Human approval decisions inform policy updates (approvals add precedent; denials tighten rules)

### Disturbances

| Disturbance | Source | Mitigation |
|---|---|---|
| Novel injection techniques | Evolving attack landscape | Continuous policy updates, red-team exercises |
| Policy misconfiguration | Operator error | Policy validation on deploy; dry-run mode |
| Tool parameter schema changes | Upstream API changes | Schema versioning; validation on every call |
| Latency from approval workflow | Human availability | Timeout defaults to denial; escalation chains |
| Agent prompt engineering for tool discovery | Attacker probing | Tool descriptions redacted in agent context |

### Unsafe States

| Unsafe State | Condition | Consequence |
|---|---|---|
| Unvalidated tool call executed | Gateway bypassed or disabled | Arbitrary action execution |
| High-risk tool without approval | Approval gate not configured | Critical operations without human oversight |
| Parameter injection | Parameters not validated | Unauthorized data access or modification |
| Tool escalation | Low-risk context calls high-risk tool | Privilege escalation |
| Rate limit bypass | Rate limiter not enforced | Automated rapid-fire attacks |

---

## Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                     AI Agent Tool Call                         │
│              {"tool": "send_email", "params": {...}}           │
└──────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
              ┌────────────────────────────┐
              │    Secure Tool Gateway      │
              │                             │
              │  ┌──────────────────────┐  │
              │  │  Risk Classifier      │  │──▶ LOW / MEDIUM / HIGH / CRITICAL
              │  └──────────────────────┘  │
              │  ┌──────────────────────┐  │
              │  │  Parameter Validator  │  │──▶ Validate against schema + policy
              │  └──────────────────────┘  │
              │  ┌──────────────────────┐  │
              │  │  Authorization Check  │  │──▶ User ↔ Tool + Params permission
              │  └──────────────────────┘  │
              │  ┌──────────────────────┐  │
              │  │  Human Approval Gate  │  │──▶ Queue for review if HIGH risk
              │  └──────────────────────┘  │
              │  ┌──────────────────────┐  │
              │  │  Rate Limiter         │  │──▶ Enforce per-tool, per-user quotas
              │  └──────────────────────┘  │
              │  ┌──────────────────────┐  │
              │  │  Audit Logger         │  │──▶ Immutable log of all decisions
              │  └──────────────────────┘  │
              └──────────┬─────────────────┘
                         │
            ┌────────────┼────────────────┐
            │            │                │
            ▼            ▼                ▼
      ┌──────────┐ ┌──────────┐   ┌──────────────┐
      │  PERMIT   │ │  MODIFY  │   │  BLOCK /     │
      │  + LOG    │ │  PARAMS  │   │  ESCALATE    │
      └────┬─────┘ └────┬─────┘   └──────────────┘
           │             │
           ▼             ▼
    ┌─────────────────────────────┐
    │      Tool Execution Layer    │
    │   (Actual API / Function)    │
    └──────────────┬───────────────┘
                   │
                   ▼
    ┌─────────────────────────────┐
    │   Post-Execution Validation  │──── Verify result against policy
    └─────────────────────────────┘
```

---

## Implementation

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Callable
import time


class RiskLevel(Enum):
    LOW = "low"           # Read-only, no side effects (e.g., search, lookup)
    MEDIUM = "medium"     # Limited side effects (e.g., send notification, create draft)
    HIGH = "high"         # Significant side effects (e.g., send email, modify data)
    CRITICAL = "critical" # Irreversible or high-impact (e.g., delete data, execute code, transfer funds)


class Decision(Enum):
    PERMIT = "permit"
    PERMIT_WITH_LOG = "permit_with_log"
    MODIFY = "modify"
    REQUIRE_APPROVAL = "require_approval"
    BLOCK = "block"


@dataclass
class ToolPolicy:
    """Security policy for a single tool."""
    tool_name: str
    risk_level: RiskLevel
    allowed_roles: set[str]
    parameter_schema: dict          # JSON Schema for parameter validation
    denied_parameters: dict[str, list[str]]  # parameter_name → denied_values
    requires_approval: bool = False
    rate_limit_per_minute: int = 60
    allowlist_params: dict[str, list[str]] = field(default_factory=dict)  # param → allowed values


@dataclass
class ToolCall:
    """A tool invocation request from the AI agent."""
    tool_name: str
    parameters: dict[str, Any]
    user_id: str
    user_roles: set[str]
    conversation_id: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class GatewayDecision:
    """The gateway's decision on a tool call."""
    decision: Decision
    tool_name: str
    original_parameters: dict[str, Any]
    modified_parameters: Optional[dict[str, Any]] = None
    reason: str = ""
    approval_request_id: Optional[str] = None
    risk_level: RiskLevel = RiskLevel.LOW


class SecureToolGateway:
    """Mediation layer between AI agent tool calls and execution.

    Control objective: Every tool invocation is validated against policy
    before execution; no tool is called in violation of security constraints.
    """

    def __init__(
        self,
        policy_store: dict[str, ToolPolicy],
        approval_handler: Optional[Callable] = None,
        audit_logger: Optional[Callable] = None,
        rate_limiter: Optional[Callable] = None,
    ):
        self.policy_store = policy_store
        self.approval_handler = approval_handler
        self.audit_logger = audit_logger
        self.rate_limiter = rate_limiter
        self._call_history: dict[str, list[float]] = {}

    def evaluate(self, call: ToolCall) -> GatewayDecision:
        """Evaluate a tool call against all security policies."""
        policy = self.policy_store.get(call.tool_name)
        if policy is None:
            return self._block(call, f"Unknown tool: {call.tool_name}")

        # 1. Check authorization
        if not self._is_authorized(call, policy):
            return self._block(call, f"User roles {call.user_roles} not authorized for {call.tool_name}")

        # 2. Validate parameters against schema
        schema_errors = self._validate_schema(call.parameters, policy.parameter_schema)
        if schema_errors:
            return self._block(call, f"Parameter schema validation failed: {schema_errors}")

        # 3. Check denied parameter values
        denied = self._check_denied_params(call.parameters, policy.denied_parameters)
        if denied:
            return self._block(call, f"Denied parameter values: {denied}")

        # 4. Check allowlist constraints
        allowlist_violations = self._check_allowlist(call.parameters, policy.allowlist_params)
        if allowlist_violations:
            return self._block(call, f"Parameter values not in allowlist: {allowlist_violations}")

        # 5. Check rate limits
        if not self._check_rate_limit(call, policy):
            return self._block(call, f"Rate limit exceeded for {call.tool_name}")

        # 6. Apply risk-based routing
        if policy.risk_level == RiskLevel.CRITICAL:
            return self._require_approval(call, policy, "Critical-risk tool requires human approval")

        if policy.risk_level == RiskLevel.HIGH or policy.requires_approval:
            return self._require_approval(call, policy, "High-risk tool requires human approval")

        if policy.risk_level == RiskLevel.MEDIUM:
            return self._permit_with_log(call, policy, "Medium-risk tool permitted with elevated logging")

        return self._permit(call, policy, "Low-risk tool permitted")

    def _is_authorized(self, call: ToolCall, policy: ToolPolicy) -> bool:
        return bool(call.user_roles & policy.allowed_roles)

    def _validate_schema(self, params: dict, schema: dict) -> list[str]:
        """Validate parameters against JSON Schema."""
        errors = []
        required = schema.get("required", [])
        for field_name in required:
            if field_name not in params:
                errors.append(f"Missing required parameter: {field_name}")
        properties = schema.get("properties", {})
        for key, value in params.items():
            if key not in properties:
                errors.append(f"Unknown parameter: {key}")
        return errors

    def _check_denied_params(self, params: dict, denied: dict) -> list[str]:
        """Check for denied parameter values."""
        violations = []
        for param_name, denied_values in denied.items():
            if param_name in params:
                val = params[param_name]
                if val in denied_values:
                    violations.append(f"{param_name}={val}")
        return violations

    def _check_allowlist(self, params: dict, allowlists: dict) -> list[str]:
        """Check that parameter values are within allowlists."""
        violations = []
        for param_name, allowed_values in allowlists.items():
            if param_name in params:
                if params[param_name] not in allowed_values:
                    violations.append(f"{param_name}={params[param_name]} (not in allowlist)")
        return violations

    def _check_rate_limit(self, call: ToolCall, policy: ToolPolicy) -> bool:
        """Check per-user, per-tool rate limits."""
        key = f"{call.user_id}:{call.tool_name}"
        now = time.time()
        window = self._call_history.setdefault(key, [])
        window[:] = [t for t in window if now - t < 60]
        if len(window) >= policy.rate_limit_per_minute:
            return False
        window.append(now)
        return True

    def _permit(self, call: ToolCall, policy: ToolPolicy, reason: str) -> GatewayDecision:
        self._log(call, Decision.PERMIT, reason)
        return GatewayDecision(
            decision=Decision.PERMIT,
            tool_name=call.tool_name,
            original_parameters=call.parameters,
            reason=reason,
            risk_level=policy.risk_level,
        )

    def _permit_with_log(self, call: ToolCall, policy: ToolPolicy, reason: str) -> GatewayDecision:
        self._log(call, Decision.PERMIT_WITH_LOG, reason)
        return GatewayDecision(
            decision=Decision.PERMIT_WITH_LOG,
            tool_name=call.tool_name,
            original_parameters=call.parameters,
            reason=reason,
            risk_level=policy.risk_level,
        )

    def _require_approval(self, call: ToolCall, policy: ToolPolicy, reason: str) -> GatewayDecision:
        approval_id = None
        if self.approval_handler:
            approval_id = self.approval_handler(call, policy)
        self._log(call, Decision.REQUIRE_APPROVAL, reason, approval_id=approval_id)
        return GatewayDecision(
            decision=Decision.REQUIRE_APPROVAL,
            tool_name=call.tool_name,
            original_parameters=call.parameters,
            reason=reason,
            approval_request_id=approval_id,
            risk_level=policy.risk_level,
        )

    def _block(self, call: ToolCall, reason: str) -> GatewayDecision:
        self._log(call, Decision.BLOCK, reason)
        return GatewayDecision(
            decision=Decision.BLOCK,
            tool_name=call.tool_name,
            original_parameters=call.parameters,
            reason=reason,
        )

    def _log(self, call: ToolCall, decision: Decision, reason: str, approval_id: str = None):
        if self.audit_logger:
            self.audit_logger(
                tool_name=call.tool_name,
                user_id=call.user_id,
                decision=decision.value,
                reason=reason,
                parameters=call.parameters,
                approval_request_id=approval_id,
                timestamp=time.time(),
            )
```

---

## Tests

```python
import pytest
from secure_tool_gateway import (
    SecureToolGateway, ToolPolicy, ToolCall, RiskLevel, Decision
)


class TestSecureToolGateway:
    """Security regression tests for the Secure Tool Gateway."""

    @pytest.fixture
    def gateway(self):
        policies = {
            "search_docs": ToolPolicy(
                tool_name="search_docs",
                risk_level=RiskLevel.LOW,
                allowed_roles={"user", "admin"},
                parameter_schema={"required": ["query"], "properties": {"query": {}}},
                denied_parameters={},
                rate_limit_per_minute=60,
            ),
            "send_email": ToolPolicy(
                tool_name="send_email",
                risk_level=RiskLevel.HIGH,
                allowed_roles={"admin"},
                parameter_schema={"required": ["to", "subject", "body"], "properties": {"to": {}, "subject": {}, "body": {}}},
                denied_parameters={"to": ["root@system.internal"]},
                requires_approval=True,
                rate_limit_per_minute=10,
            ),
            "delete_record": ToolPolicy(
                tool_name="delete_record",
                risk_level=RiskLevel.CRITICAL,
                allowed_roles={"admin"},
                parameter_schema={"required": ["record_id"], "properties": {"record_id": {}}},
                denied_parameters={},
                rate_limit_per_minute=5,
            ),
        }
        return SecureToolGateway(
            policy_store=policies,
            approval_handler=lambda call, policy: "apr-001",
            audit_logger=lambda **kwargs: None,
        )

    def test_low_risk_tool_permitted(self, gateway):
        call = ToolCall(tool_name="search_docs", parameters={"query": "test"},
                        user_id="u1", user_roles={"user"}, conversation_id="c1")
        result = gateway.evaluate(call)
        assert result.decision == Decision.PERMIT

    def test_unauthorized_user_blocked(self, gateway):
        call = ToolCall(tool_name="send_email", parameters={"to": "a@b.com", "subject": "hi", "body": "test"},
                        user_id="u1", user_roles={"user"}, conversation_id="c1")
        result = gateway.evaluate(call)
        assert result.decision == Decision.BLOCK

    def test_high_risk_tool_requires_approval(self, gateway):
        call = ToolCall(tool_name="send_email", parameters={"to": "a@b.com", "subject": "hi", "body": "test"},
                        user_id="u1", user_roles={"admin"}, conversation_id="c1")
        result = gateway.evaluate(call)
        assert result.decision == Decision.REQUIRE_APPROVAL

    def test_critical_tool_requires_approval(self, gateway):
        call = ToolCall(tool_name="delete_record", parameters={"record_id": "rec-123"},
                        user_id="u1", user_roles={"admin"}, conversation_id="c1")
        result = gateway.evaluate(call)
        assert result.decision == Decision.REQUIRE_APPROVAL

    def test_denied_parameter_blocked(self, gateway):
        call = ToolCall(tool_name="send_email", parameters={"to": "root@system.internal", "subject": "hi", "body": "test"},
                        user_id="u1", user_roles={"admin"}, conversation_id="c1")
        result = gateway.evaluate(call)
        assert result.decision == Decision.BLOCK

    def test_unknown_tool_blocked(self, gateway):
        call = ToolCall(tool_name="execute_shell", parameters={"command": "rm -rf /"},
                        user_id="u1", user_roles={"admin"}, conversation_id="c1")
        result = gateway.evaluate(call)
        assert result.decision == Decision.BLOCK

    def test_rate_limit_enforced(self, gateway):
        for i in range(12):
            call = ToolCall(tool_name="send_email", parameters={"to": f"u{i}@b.com", "subject": "hi", "body": "test"},
                            user_id="u1", user_roles={"admin"}, conversation_id="c1")
            result = gateway.evaluate(call)
            if i < 10:
                assert result.decision in (Decision.REQUIRE_APPROVAL,)
            else:
                assert result.decision == Decision.BLOCK
```

---

## Monitoring

| Metric | Collection | Warning | Critical | Alert Channel |
|---|---|---|---|---|
| Tool call block rate | Per-request | > 2% of calls | > 10% of calls | Security SIEM |
| Approval queue depth | Continuous | > 10 pending | > 50 pending | Operations |
| Approval latency (P95) | Per-approval | > 5 minutes | > 30 minutes | Operations |
| Unknown tool call attempts | Per-request | Any | > 3 in 1 minute | Incident response |
| Parameter validation failures | Per-request | > 5/hour | > 20/hour | Security SIEM |
| Rate limit triggers | Per-request | > 10/minute | > 50/minute | Security SIEM |

---

## Failure Modes

| Failure Mode | Cause | Detection | Mitigation |
|---|---|---|---|
| **Gateway bypass** | Agent calls tool directly, skipping gateway | Call appears in tool execution logs but not gateway logs | Architectural enforcement: gateway is the only execution path |
| **Policy misconfiguration** | Incorrect risk level or missing parameter validation | Red-team finds exploitable gap | Policy review on deploy; automated policy linter |
| **Approval bottleneck** | Too many approvals needed; humans cannot keep up | Queue depth alert; approval latency spike | Tiered approval; auto-approve for known safe patterns; escalation chains |
| **Parameter schema drift** | Tool API changes; schema not updated | Validation errors on valid calls | Schema sync on tool version change; schema validation on deploy |
| **Rate limit circumvention** | Attacker distributes calls across user IDs | Cross-user rate analysis | Global rate limits by tool + IP / tenant |

---

## When Not To Use

1. **Agents with no tool use:** If your AI system is purely conversational with no external tool integrations, this pattern adds no value.

2. **Fully deterministic tool chains:** If the sequence of tool calls is fixed at design time (no LLM-driven tool selection), traditional API gateway patterns suffice.

3. **Read-only, sandboxed environments:** If all tools are read-only and operate on public data with no user context, the risk is inherently low. Simple logging may be sufficient.

4. **Rapid prototyping with no production data:** During early development with no real users or data, the gateway adds friction. Add it before any production deployment.

5. **When the AI Security Gateway already includes tool mediation:** The AI Security Gateway pattern (PAT-GW-001) may subsume this functionality. Use this pattern standalone only if you need tool-specific mediation without the full gateway.

---

## Assurance Evidence

| Artifact | Description | Format | Retention |
|---|---|---|---|
| Tool call audit log | Every gateway decision with full context | Structured JSON | 1 year |
| Policy configuration | Current tool policies with risk classifications | JSON export | Permanent (versioned) |
| Approval records | Human decisions on high-risk tool calls | Approval tickets | 2 years |
| Rate limit events | All rate-limit triggers | Structured JSON | 90 days |
| Regression test results | Pass/fail for all gateway security tests | JUnit XML | Permanent |

---

*Pattern version: 1.0.0 | AI Security from Scratch*
