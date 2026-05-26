"""
Secure Tool Gateway — Tool execution gateway with risk classification, allowlists,
parameter validation, and simulated human approval for high-risk tools.

Control-Theoretic View:
    In the AI control loop, tool calls represent the actuator signals — the system's
    ability to affect the external world. Without proper gating, a compromised or
    confused controller (LLM) can issue dangerous actuator commands.

    The secure tool gateway acts as an actuator filter/saturation element, ensuring
    that tool calls are classified, validated, and approved before execution.

Key Properties:
    1. Risk classification: tools are classified as LOW, MEDIUM, HIGH, or CRITICAL risk
    2. Allowlist enforcement: only explicitly approved tools can be called
    3. Parameter validation: tool parameters are validated against schemas
    4. Human approval: CRITICAL tools require simulated human approval
    5. Rate limiting: configurable call rate limits per tool
    6. Audit logging: all tool calls, approvals, and denials are logged
"""

from __future__ import annotations

import enum
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any, Callable, Optional


class RiskLevel(enum.Enum):
    """Risk classification for tools."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Decision(enum.Enum):
    """Gateway decision for a tool call."""
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"


class ToolGatewayError(Exception):
    """Base exception for tool gateway errors."""
    pass


class ToolNotFoundError(ToolGatewayError):
    """Raised when a tool is not in the allowlist."""
    pass


class ParameterValidationError(ToolGatewayError):
    """Raised when tool parameters fail validation."""
    pass


class RateLimitExceededError(ToolGatewayError):
    """Raised when rate limit is exceeded for a tool."""
    pass


@dataclass
class ParameterSchema:
    """Schema definition for a tool parameter."""
    name: str
    type: str  # "string", "integer", "number", "boolean", "array"
    required: bool = True
    pattern: Optional[str] = None  # Regex pattern for string validation
    min_value: Optional[float] = None  # For numeric types
    max_value: Optional[float] = None
    allowed_values: Optional[list[Any]] = None  # Enum-like restriction
    max_length: Optional[int] = None  # For string types

    def validate(self, value: Any) -> tuple[bool, str]:
        """Validate a value against this schema. Returns (valid, reason)."""
        # Type checking
        type_map = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "array": list,
        }
        expected_type = type_map.get(self.type)
        if expected_type and not isinstance(value, expected_type):
            # Allow int where float expected
            if self.type == "number" and isinstance(value, int):
                pass
            else:
                return False, f"Expected {self.type}, got {type(value).__name__}"

        # Pattern matching for strings
        if self.pattern and isinstance(value, str):
            if not re.match(self.pattern, value):
                return False, f"Value does not match pattern: {self.pattern}"

        # Numeric bounds
        if isinstance(value, (int, float)):
            if self.min_value is not None and value < self.min_value:
                return False, f"Value {value} below minimum {self.min_value}"
            if self.max_value is not None and value > self.max_value:
                return False, f"Value {value} above maximum {self.max_value}"

        # Allowed values
        if self.allowed_values is not None and value not in self.allowed_values:
            return False, f"Value not in allowed values: {self.allowed_values}"

        # String length
        if self.max_length is not None and isinstance(value, str):
            if len(value) > self.max_length:
                return False, f"String length {len(value)} exceeds max {self.max_length}"

        return True, ""


@dataclass
class ToolDefinition:
    """Definition of a tool available through the gateway."""
    name: str
    description: str
    risk_level: RiskLevel
    parameters: list[ParameterSchema] = field(default_factory=list)
    rate_limit_per_minute: Optional[int] = None  # Max calls per minute
    requires_approval: bool = False  # Explicit override for human approval
    enabled: bool = True
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        # CRITICAL tools always require approval unless explicitly configured
        if self.risk_level == RiskLevel.CRITICAL and not self.requires_approval:
            self.requires_approval = True


@dataclass
class ToolCall:
    """A tool call request."""
    call_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tool_name: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    caller_id: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class GatewayDecision:
    """The gateway's decision for a tool call."""
    decision: Decision
    tool_call: ToolCall
    reason: str = ""
    risk_level: RiskLevel = RiskLevel.LOW
    validation_errors: list[str] = field(default_factory=list)
    requires_approval_from: Optional[str] = None  # Role required for approval


@dataclass
class ApprovalRequest:
    """A pending approval request for a tool call."""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tool_call: ToolCall = None  # type: ignore
    risk_level: RiskLevel = RiskLevel.CRITICAL
    reason: str = ""
    status: str = "pending"  # pending, approved, denied
    approver: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SecureToolGateway:
    """
    Secure tool execution gateway with risk classification, allowlisting,
    parameter validation, and human approval for high-risk operations.

    Usage:
        gateway = SecureToolGateway()

        gateway.register_tool(ToolDefinition(
            name="web_search",
            description="Search the web",
            risk_level=RiskLevel.LOW,
            parameters=[ParameterSchema(name="query", type="string", required=True, max_length=500)],
        ))

        gateway.register_tool(ToolDefinition(
            name="delete_database",
            description="Delete a database",
            risk_level=RiskLevel.CRITICAL,
            parameters=[ParameterSchema(name="db_name", type="string", required=True)],
        ))

        decision = gateway.evaluate(ToolCall(tool_name="web_search", parameters={"query": "python"}))
        assert decision.decision == Decision.ALLOW
    """

    def __init__(self, auto_approve_high: bool = False):
        self._tools: dict[str, ToolDefinition] = {}
        self._pending_approvals: dict[str, ApprovalRequest] = {}
        self._call_history: dict[str, list[datetime]] = {}  # tool_name -> timestamps
        self._audit_log: list[dict] = []
        self._auto_approve_high = auto_approve_high

    @property
    def tools(self) -> list[ToolDefinition]:
        return list(self._tools.values())

    @property
    def audit_log(self) -> list[dict]:
        return list(self._audit_log)

    @property
    def pending_approvals(self) -> list[ApprovalRequest]:
        return [a for a in self._pending_approvals.values() if a.status == "pending"]

    def register_tool(self, tool: ToolDefinition) -> None:
        """Register a tool in the gateway."""
        self._tools[tool.name] = tool
        self._log_action("register_tool", tool_name=tool.name, risk_level=tool.risk_level.value)

    def unregister_tool(self, name: str) -> bool:
        """Remove a tool from the gateway. Returns True if found."""
        if name in self._tools:
            del self._tools[name]
            self._log_action("unregister_tool", tool_name=name)
            return True
        return False

    def evaluate(self, call: ToolCall) -> GatewayDecision:
        """
        Evaluate a tool call request and return a gateway decision.

        Evaluation steps:
        1. Check if tool is in allowlist
        2. Check if tool is enabled
        3. Check rate limits
        4. Validate parameters
        5. Determine risk-based decision (allow/deny/require_approval)
        """
        # Step 1: Allowlist check
        tool_def = self._tools.get(call.tool_name)
        if tool_def is None:
            decision = GatewayDecision(
                decision=Decision.DENY,
                tool_call=call,
                reason=f"Tool '{call.tool_name}' not in allowlist",
            )
            self._log_action("evaluate_deny", call_id=call.call_id,
                             tool_name=call.tool_name, reason="not_in_allowlist")
            return decision

        # Step 2: Enabled check
        if not tool_def.enabled:
            decision = GatewayDecision(
                decision=Decision.DENY,
                tool_call=call,
                reason=f"Tool '{call.tool_name}' is disabled",
                risk_level=tool_def.risk_level,
            )
            self._log_action("evaluate_deny", call_id=call.call_id,
                             tool_name=call.tool_name, reason="disabled")
            return decision

        # Step 3: Rate limit check
        if tool_def.rate_limit_per_minute is not None:
            if not self._check_rate_limit(call.tool_name, tool_def.rate_limit_per_minute):
                decision = GatewayDecision(
                    decision=Decision.DENY,
                    tool_call=call,
                    reason=f"Rate limit exceeded for '{call.tool_name}' ({tool_def.rate_limit_per_minute}/min)",
                    risk_level=tool_def.risk_level,
                )
                self._log_action("evaluate_deny", call_id=call.call_id,
                                 tool_name=call.tool_name, reason="rate_limit")
                return decision

        # Step 4: Parameter validation
        validation_errors = self._validate_parameters(call, tool_def)
        if validation_errors:
            decision = GatewayDecision(
                decision=Decision.DENY,
                tool_call=call,
                reason="Parameter validation failed",
                risk_level=tool_def.risk_level,
                validation_errors=validation_errors,
            )
            self._log_action("evaluate_deny", call_id=call.call_id,
                             tool_name=call.tool_name, reason="parameter_validation",
                             errors=validation_errors)
            return decision

        # Step 5: Risk-based decision
        if tool_def.requires_approval:
            approval_request = ApprovalRequest(
                tool_call=call,
                risk_level=tool_def.risk_level,
                reason=f"Tool '{call.tool_name}' requires human approval (risk: {tool_def.risk_level.value})",
            )
            self._pending_approvals[approval_request.request_id] = approval_request

            decision = GatewayDecision(
                decision=Decision.REQUIRE_APPROVAL,
                tool_call=call,
                reason=approval_request.reason,
                risk_level=tool_def.risk_level,
                requires_approval_from="human_operator",
            )
            self._log_action("evaluate_require_approval", call_id=call.call_id,
                             tool_name=call.tool_name, request_id=approval_request.request_id)
            return decision

        if tool_def.risk_level == RiskLevel.HIGH and not self._auto_approve_high:
            approval_request = ApprovalRequest(
                tool_call=call,
                risk_level=tool_def.risk_level,
                reason=f"HIGH risk tool '{call.tool_name}' requires approval",
            )
            self._pending_approvals[approval_request.request_id] = approval_request

            decision = GatewayDecision(
                decision=Decision.REQUIRE_APPROVAL,
                tool_call=call,
                reason=approval_request.reason,
                risk_level=tool_def.risk_level,
            )
            self._log_action("evaluate_require_approval", call_id=call.call_id,
                             tool_name=call.tool_name, request_id=approval_request.request_id)
            return decision

        # Record the call for rate limiting
        self._record_call(call.tool_name)

        decision = GatewayDecision(
            decision=Decision.ALLOW,
            tool_call=call,
            reason="All checks passed",
            risk_level=tool_def.risk_level,
        )
        self._log_action("evaluate_allow", call_id=call.call_id,
                         tool_name=call.tool_name, risk_level=tool_def.risk_level.value)
        return decision

    def approve(self, request_id: str, approver: str) -> Optional[ApprovalRequest]:
        """Approve a pending approval request."""
        request = self._pending_approvals.get(request_id)
        if request is None or request.status != "pending":
            return None

        request.status = "approved"
        request.approver = approver
        self._record_call(request.tool_call.tool_name)
        self._log_action("approve", request_id=request_id, approver=approver,
                         tool_name=request.tool_call.tool_name)
        return request

    def deny_approval(self, request_id: str, approver: str, reason: str = "") -> Optional[ApprovalRequest]:
        """Deny a pending approval request."""
        request = self._pending_approvals.get(request_id)
        if request is None or request.status != "pending":
            return None

        request.status = "denied"
        request.approver = approver
        self._log_action("deny_approval", request_id=request_id, approver=approver,
                         tool_name=request.tool_call.tool_name, reason=reason)
        return request

    def execute_with_approval(
        self,
        call: ToolCall,
        approver: str = "",
    ) -> GatewayDecision:
        """
        Convenience method: evaluate a call, and if it requires approval
        and an approver is provided, auto-approve it.
        """
        decision = self.evaluate(call)

        if decision.decision == Decision.REQUIRE_APPROVAL and approver:
            # Find the pending approval for this call
            for req in self._pending_approvals.values():
                if req.tool_call.call_id == call.call_id and req.status == "pending":
                    self.approve(req.request_id, approver)
                    decision.decision = Decision.ALLOW
                    decision.reason = f"Approved by {approver}"
                    break

        return decision

    def _validate_parameters(self, call: ToolCall, tool_def: ToolDefinition) -> list[str]:
        """Validate call parameters against the tool's parameter schema."""
        errors: list[str] = []

        # Check required parameters
        param_names = set(call.parameters.keys())
        for schema in tool_def.parameters:
            if schema.required and schema.name not in param_names:
                errors.append(f"Missing required parameter: {schema.name}")
                continue

            if schema.name in param_names:
                value = call.parameters[schema.name]
                valid, reason = schema.validate(value)
                if not valid:
                    errors.append(f"Parameter '{schema.name}': {reason}")

        # Check for unexpected parameters
        expected_params = {s.name for s in tool_def.parameters}
        unexpected = param_names - expected_params
        if unexpected:
            errors.append(f"Unexpected parameters: {unexpected}")

        return errors

    def _check_rate_limit(self, tool_name: str, limit: int) -> bool:
        """Check if a tool call is within rate limits."""
        now = datetime.now(timezone.utc)
        one_minute_ago = now - timedelta(minutes=1)

        calls = self._call_history.get(tool_name, [])
        recent_calls = [t for t in calls if t > one_minute_ago]

        return len(recent_calls) < limit

    def _record_call(self, tool_name: str) -> None:
        """Record a tool call timestamp for rate limiting."""
        now = datetime.now(timezone.utc)
        if tool_name not in self._call_history:
            self._call_history[tool_name] = []
        self._call_history[tool_name].append(now)

    def _log_action(self, action: str, **kwargs) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            **kwargs,
        }
        self._audit_log.append(entry)

    def get_summary(self) -> dict:
        """Return a summary of the gateway state."""
        return {
            "registered_tools": len(self._tools),
            "pending_approvals": len(self.pending_approvals),
            "audit_log_entries": len(self._audit_log),
            "tools_by_risk": {
                level.value: sum(1 for t in self._tools.values() if t.risk_level == level)
                for level in RiskLevel
            },
        }
