"""
AI Security Gateway — Centralized security gateway combining input validation,
policy checks, output filtering, and audit logging.

Control-Theoretic View:
    The AI Security Gateway is the complete control-loop safety wrapper. It sits
    between the user and the LLM, acting as both the input filter AND output filter
    in the control loop. It composes all defense layers into a single, coherent
    security checkpoint.

    ┌────────┐    ┌──────────────────────────────────┐    ┌────────┐
    │  User  │───▶│  AI Security Gateway             │───▶│  User  │
    │        │    │                                  │    │        │
    │        │    │  Input Validation ──────────────▶│    │        │
    │        │    │  Policy Engine ─────────────────▶│    │        │
    │        │    │  ────▶ LLM ────▶                 │    │        │
    │        │    │  Output Validation ─────────────▶│    │        │
    │        │    │  Audit Logging                   │    │        │
    └────────┘    └──────────────────────────────────┘    └────────┘

Key Properties:
    1. Unified interface: single entry point for all security checks
    2. Composable defenses: combines context firewall, policy engine, output validator
    3. Pipeline architecture: input → policy → LLM → output → audit
    4. Comprehensive audit trail: every request logged with full decision context
    5. Graceful degradation: individual defense failures don't crash the gateway
"""

from __future__ import annotations

import enum
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Optional

# Import sibling defense modules (standalone, so use local imports)
import re


class GatewayStatus(enum.Enum):
    """Status of a gateway request."""
    ALLOWED = "allowed"
    BLOCKED = "blocked"
    MODIFIED = "modified"
    ERROR = "error"


class InputValidationResult:
    """Result of input validation checks."""

    def __init__(self, is_valid: bool, injection_score: float = 0.0, warnings: list[str] = None,
                 blocked_reason: str = ""):
        self.is_valid = is_valid
        self.injection_score = injection_score
        self.warnings = warnings or []
        self.blocked_reason = blocked_reason


class OutputValidationResult:
    """Result of output validation checks."""

    def __init__(self, is_valid: bool, findings: list[dict] = None, redacted_content: str = "",
                 blocked_reason: str = ""):
        self.is_valid = is_valid
        self.findings = findings or []
        self.redacted_content = redacted_content
        self.blocked_reason = blocked_reason


class PolicyCheckResult:
    """Result of policy evaluation."""

    def __init__(self, decision: str = "allow", matched_rules: list[str] = None, reasons: list[str] = None):
        self.decision = decision  # "allow", "deny", "require_approval"
        self.matched_rules = matched_rules or []
        self.reasons = reasons or []


@dataclass
class GatewayRequest:
    """A request passing through the security gateway."""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    user_role: str = "guest"
    input_content: str = ""
    tool_name: str = ""
    tool_parameters: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class GatewayResponse:
    """The gateway's response after processing a request."""
    request_id: str = ""
    status: GatewayStatus = GatewayStatus.ALLOWED
    input_validation: Optional[InputValidationResult] = None
    policy_check: Optional[PolicyCheckResult] = None
    output_validation: Optional[OutputValidationResult] = None
    final_content: str = ""
    llm_response: str = ""  # Placeholder for actual LLM response
    blocked_reason: str = ""
    audit_events: list[dict] = field(default_factory=list)
    processing_time_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Injection patterns for input validation
_INJECTION_PATTERNS = [
    re.compile(r"(?i)ignore\s+(previous|above|all)\s+(instructions|prompts|rules)"),
    re.compile(r"(?i)you\s+are\s+now\s+"),
    re.compile(r"(?i)new\s+instructions?\s*:"),
    re.compile(r"(?i)system\s*:\s*"),
    re.compile(r"(?i)disregard\s+(your|the)\s+(instructions|guidelines|rules)"),
    re.compile(r"(?i)forget\s+(everything|all|previous)"),
    re.compile(r"(?i)override\s+(previous|default|safety)"),
    re.compile(r"(?i)pretend\s+(you\s+are|to\s+be)"),
    re.compile(r"(?i)jailbreak"),
]

# Secret patterns for output validation
_SECRET_PATTERNS = [
    (re.compile(r"sk-[a-zA-Z0-9]{20,}"), "openai_api_key"),
    (re.compile(r"AKIA[A-Z0-9]{16}"), "aws_access_key"),
    (re.compile(r"ghp_[a-zA-Z0-9]{36}"), "github_pat"),
    (re.compile(r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----"), "private_key"),
    (re.compile(r"(?:mongodb|postgres|mysql)://[^\s'\"]+"), "connection_string"),
    (re.compile(r"(?i)password\s*[:=]\s*['\"]?[^\s'\"]{8,}"), "password"),
]

# PII patterns for output validation
_PII_PATTERNS = [
    (re.compile(r"\b\d{3}[-.]?\d{2}[-.]?\d{4}\b"), "ssn"),
    (re.compile(r"\b(?:\d[ -]?){13,16}\b"), "credit_card"),
    (re.compile(r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b"), "email"),
]


class AISecurityGateway:
    """
    Centralized AI security gateway combining input validation, policy checks,
    output filtering, and audit logging.

    Usage:
        gateway = AISecurityGateway()

        # Process a request
        response = gateway.process(GatewayRequest(
            user_id="user123",
            user_role="employee",
            input_content="What is the company policy on remote work?",
        ))

        if response.status == GatewayStatus.ALLOWED:
            print(response.final_content)
        else:
            print(f"Blocked: {response.blocked_reason}")
    """

    def __init__(
        self,
        injection_threshold: float = 0.3,
        block_secrets: bool = True,
        block_pii: bool = True,
        block_injection: bool = True,
        custom_input_rules: list[dict] = None,
        custom_output_rules: list[dict] = None,
    ):
        self._injection_threshold = injection_threshold
        self._block_secrets = block_secrets
        self._block_pii = block_pii
        self._block_injection = block_injection
        self._custom_input_rules = custom_input_rules or []
        self._custom_output_rules = custom_output_rules or []
        self._audit_log: list[dict] = []
        self._stats = {
            "total_requests": 0,
            "allowed": 0,
            "blocked": 0,
            "modified": 0,
            "errors": 0,
        }

    @property
    def audit_log(self) -> list[dict]:
        return list(self._audit_log)

    @property
    def stats(self) -> dict:
        return dict(self._stats)

    def process(self, request: GatewayRequest, llm_response: str = "") -> GatewayResponse:
        """
        Process a request through the full security pipeline.

        Pipeline:
        1. Input validation (injection detection, content checks)
        2. Policy check (role-based access, tool permissions)
        3. LLM response simulation (caller provides response)
        4. Output validation (secret/PII detection, redaction)
        5. Audit logging

        Args:
            request: The gateway request to process.
            llm_response: The LLM's response to validate (if available).

        Returns:
            A GatewayResponse with the final decision and content.
        """
        start_time = datetime.now(timezone.utc)
        self._stats["total_requests"] += 1

        response = GatewayResponse(request_id=request.request_id)

        try:
            # Step 1: Input validation
            input_result = self._validate_input(request)
            response.input_validation = input_result

            if not input_result.is_valid:
                response.status = GatewayStatus.BLOCKED
                response.blocked_reason = f"Input validation failed: {input_result.blocked_reason}"
                self._record(request, response, start_time)
                return response

            # Step 2: Policy check
            policy_result = self._check_policies(request)
            response.policy_check = policy_result

            if policy_result.decision == "deny":
                response.status = GatewayStatus.BLOCKED
                response.blocked_reason = f"Policy denied: {'; '.join(policy_result.reasons)}"
                self._record(request, response, start_time)
                return response

            # Step 3: If we have an LLM response, validate the output
            if llm_response:
                output_result = self._validate_output(llm_response)
                response.output_validation = output_result
                response.llm_response = llm_response

                if not output_result.is_valid:
                    response.status = GatewayStatus.BLOCKED
                    response.blocked_reason = f"Output validation failed: {output_result.blocked_reason}"
                    self._record(request, response, start_time)
                    return response

                if output_result.redacted_content != llm_response:
                    response.status = GatewayStatus.MODIFIED
                    response.final_content = output_result.redacted_content
                else:
                    response.status = GatewayStatus.ALLOWED
                    response.final_content = llm_response
            else:
                # No LLM response to validate — input passed, policy allows
                response.status = GatewayStatus.ALLOWED
                response.final_content = ""

        except Exception as e:
            response.status = GatewayStatus.ERROR
            response.blocked_reason = f"Internal error: {str(e)}"
            self._stats["errors"] += 1

        self._record(request, response, start_time)
        return response

    def process_input_only(self, request: GatewayRequest) -> GatewayResponse:
        """Process only the input validation and policy check (no output validation)."""
        return self.process(request, llm_response="")

    def validate_input(self, content: str, user_role: str = "guest") -> InputValidationResult:
        """Standalone input validation."""
        request = GatewayRequest(input_content=content, user_role=user_role)
        return self._validate_input(request)

    def validate_output(self, content: str) -> OutputValidationResult:
        """Standalone output validation."""
        return self._validate_output(content)

    def check_policies(self, content: str = "", tool_name: str = "", user_role: str = "guest") -> PolicyCheckResult:
        """Standalone policy check."""
        request = GatewayRequest(input_content=content, tool_name=tool_name, user_role=user_role)
        return self._check_policies(request)

    def _validate_input(self, request: GatewayRequest) -> InputValidationResult:
        """Validate input content for injection attempts and policy violations."""
        content = request.input_content
        if not content:
            return InputValidationResult(is_valid=True)

        # Compute injection score
        injection_matches = sum(1 for p in _INJECTION_PATTERNS if p.search(content))
        injection_score = min(1.0, injection_matches * 0.25)

        warnings = []

        if injection_score > 0:
            warnings.append(f"Injection score: {injection_score:.2f}")

        if self._block_injection and injection_score >= self._injection_threshold:
            return InputValidationResult(
                is_valid=False,
                injection_score=injection_score,
                warnings=warnings,
                blocked_reason=f"Injection score {injection_score:.2f} exceeds threshold {self._injection_threshold}",
            )

        # Custom input rules
        for rule in self._custom_input_rules:
            pattern = rule.get("pattern", "")
            if pattern:
                try:
                    if re.search(pattern, content, re.IGNORECASE):
                        action = rule.get("action", "block")
                        if action == "block":
                            return InputValidationResult(
                                is_valid=False,
                                injection_score=injection_score,
                                warnings=warnings,
                                blocked_reason=f"Custom rule '{rule.get('name', 'unnamed')}' matched",
                            )
                        elif action == "warn":
                            warnings.append(f"Custom rule '{rule.get('name', 'unnamed')}' matched")
                except re.error:
                    pass

        return InputValidationResult(
            is_valid=True,
            injection_score=injection_score,
            warnings=warnings,
        )

    def _check_policies(self, request: GatewayRequest) -> PolicyCheckResult:
        """Evaluate request against security policies."""
        matched_rules = []
        reasons = []
        decision = "allow"

        # Tool access policy
        dangerous_tools = {"delete_database", "format_disk", "execute_shell", "admin_override"}
        if request.tool_name:
            if request.tool_name in dangerous_tools and request.user_role != "admin":
                matched_rules.append("tool_access_restriction")
                reasons.append(f"Tool '{request.tool_name}' requires admin role")
                decision = "deny"
            elif request.tool_name in dangerous_tools:
                matched_rules.append("tool_requires_approval")
                reasons.append(f"Tool '{request.tool_name}' requires approval")
                if decision != "deny":
                    decision = "require_approval"

        # Data access policy
        if request.user_role == "guest":
            # Guests cannot access certain content
            restricted_keywords = ["internal", "confidential", "salary", "api_key"]
            content_lower = request.input_content.lower()
            for kw in restricted_keywords:
                if kw in content_lower:
                    matched_rules.append("guest_data_restriction")
                    reasons.append(f"Guest cannot access content about '{kw}'")
                    decision = "deny"
                    break

        return PolicyCheckResult(decision=decision, matched_rules=matched_rules, reasons=reasons)

    def _validate_output(self, content: str) -> OutputValidationResult:
        """Validate output content for secrets and PII."""
        if not content:
            return OutputValidationResult(is_valid=True, redacted_content=content)

        findings = []
        redacted = content
        is_blocked = False

        # Check for secrets
        if self._block_secrets:
            for pattern, name in _SECRET_PATTERNS:
                for match in pattern.finditer(content):
                    findings.append({
                        "type": "secret",
                        "rule": name,
                        "position": match.start(),
                        "action": "block",
                    })
                    is_blocked = True
                    redacted = redacted[:match.start()] + f"[REDACTED_SECRET]" + redacted[match.end():]

        # Check for PII
        if self._block_pii:
            for pattern, name in _PII_PATTERNS:
                for match in pattern.finditer(content):
                    # Skip email if it looks like a public domain example
                    if name == "email" and any(
                        d in match.group().lower()
                        for d in ["example.com", "test.com", "domain.com"]
                    ):
                        continue
                    findings.append({
                        "type": "pii",
                        "rule": name,
                        "position": match.start(),
                        "action": "redact",
                    })
                    redacted = redacted[:match.start()] + f"[REDACTED_PII]" + redacted[match.end():]

        blocked_reason = ""
        if is_blocked:
            secret_findings = [f for f in findings if f["action"] == "block"]
            blocked_reason = f"Output contains {len(secret_findings)} secret(s)"

        return OutputValidationResult(
            is_valid=not is_blocked,
            findings=findings,
            redacted_content=redacted,
            blocked_reason=blocked_reason,
        )

    def _record(self, request: GatewayRequest, response: GatewayResponse,
                start_time: datetime) -> None:
        """Record the request/response in the audit log and update stats."""
        end_time = datetime.now(timezone.utc)
        processing_ms = (end_time - start_time).total_seconds() * 1000

        response.processing_time_ms = round(processing_ms, 2)

        # Update stats
        if response.status == GatewayStatus.ALLOWED:
            self._stats["allowed"] += 1
        elif response.status == GatewayStatus.BLOCKED:
            self._stats["blocked"] += 1
        elif response.status == GatewayStatus.MODIFIED:
            self._stats["modified"] += 1

        # Audit log entry
        audit_entry = {
            "timestamp": end_time.isoformat(),
            "request_id": request.request_id,
            "user_id": request.user_id,
            "user_role": request.user_role,
            "status": response.status.value,
            "blocked_reason": response.blocked_reason,
            "input_injection_score": (
                response.input_validation.injection_score
                if response.input_validation else None
            ),
            "policy_decision": (
                response.policy_check.decision
                if response.policy_check else None
            ),
            "output_findings_count": (
                len(response.output_validation.findings)
                if response.output_validation else 0
            ),
            "processing_time_ms": response.processing_time_ms,
        }
        self._audit_log.append(audit_entry)

    def get_summary(self) -> dict:
        """Return a summary of the gateway state."""
        return {
            "stats": self._stats,
            "audit_log_entries": len(self._audit_log),
            "config": {
                "injection_threshold": self._injection_threshold,
                "block_secrets": self._block_secrets,
                "block_pii": self._block_pii,
                "block_injection": self._block_injection,
            },
        }
