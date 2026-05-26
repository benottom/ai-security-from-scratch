"""
Policy Engine — Policy-as-code engine for AI security.

Loads policies from YAML, evaluates inputs, outputs, and tool calls against them,
and returns allow/deny/require_approval decisions.

Control-Theoretic View:
    The policy engine acts as a reference governor in the control loop. It defines
    the constraint set (acceptable operating region) and ensures that the controller
    (LLM) never leaves this region. Policies are the formal specification of safety
    constraints, and the engine is the runtime enforcer.

Key Properties:
    1. Policy-as-code: policies defined in YAML, version-controlled
    2. Multiple policy types: content_filter, tool_call, data_access, output_check
    3. Composable: multiple policies can be evaluated in sequence
    4. Decisions: ALLOW, DENY, REQUIRE_APPROVAL with reasons
    5. Audit trail: all evaluations logged for compliance
"""

from __future__ import annotations

import enum
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


class PolicyDecision(enum.Enum):
    """Policy evaluation decision."""
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"


class PolicyType(enum.Enum):
    """Types of security policies."""
    CONTENT_FILTER = "content_filter"
    TOOL_CALL = "tool_call"
    DATA_ACCESS = "data_access"
    OUTPUT_CHECK = "output_check"


@dataclass
class PolicyRule:
    """A single rule within a policy."""
    name: str
    description: str
    policy_type: PolicyType
    patterns: list[str] = field(default_factory=list)  # Regex patterns
    denied_tools: list[str] = field(default_factory=list)  # Tool names to deny
    required_roles: list[str] = field(default_factory=list)  # Roles required for access
    action: PolicyDecision = PolicyDecision.DENY
    severity: str = "medium"  # low, medium, high, critical
    metadata: dict = field(default_factory=dict)
    _compiled_patterns: list[re.Pattern] = field(default_factory=list, repr=False)

    def __post_init__(self):
        self._compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.patterns]

    def matches(self, content: str) -> bool:
        """Check if any pattern in this rule matches the content."""
        return any(pat.search(content) for pat in self._compiled_patterns)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "policy_type": self.policy_type.value,
            "patterns": self.patterns,
            "denied_tools": self.denied_tools,
            "required_roles": self.required_roles,
            "action": self.action.value,
            "severity": self.severity,
        }


@dataclass
class Policy:
    """A named policy containing multiple rules."""
    name: str
    description: str
    enabled: bool = True
    rules: list[PolicyRule] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "rules": [r.to_dict() for r in self.rules],
        }


@dataclass
class EvaluationResult:
    """Result of evaluating a request against policies."""
    decision: PolicyDecision
    matched_policies: list[str] = field(default_factory=list)
    matched_rules: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    severity: str = "low"
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def is_allowed(self) -> bool:
        return self.decision == PolicyDecision.ALLOW

    @property
    def is_denied(self) -> bool:
        return self.decision == PolicyDecision.DENY

    @property
    def requires_approval(self) -> bool:
        return self.decision == PolicyDecision.REQUIRE_APPROVAL


@dataclass
class EvaluationRequest:
    """A request to evaluate against policies."""
    content: str = ""
    tool_name: str = ""
    tool_parameters: dict = field(default_factory=dict)
    user_role: str = ""
    data_access_level: str = ""
    context: dict = field(default_factory=dict)
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))


class PolicyEngine:
    """
    Policy-as-code engine for AI security.

    Loads policies from YAML, evaluates requests against them, and returns
    allow/deny/require_approval decisions.

    Usage:
        engine = PolicyEngine.from_yaml("policies.yaml")
        result = engine.evaluate(EvaluationRequest(content="Hello!"))
        assert result.is_allowed

        result = engine.evaluate(EvaluationRequest(content="My API key is sk-abc123"))
        assert result.is_denied
    """

    def __init__(self):
        self._policies: dict[str, Policy] = {}
        self._audit_log: list[dict] = []

    @property
    def policies(self) -> list[Policy]:
        return list(self._policies.values())

    @property
    def audit_log(self) -> list[dict]:
        return list(self._audit_log)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "PolicyEngine":
        """
        Load policies from a YAML file.

        The YAML file should have a top-level 'policies' key containing
        a list of policy definitions.
        """
        try:
            import yaml
        except ImportError:
            raise ImportError("PyYAML is required. Install with: pip install pyyaml")

        engine = cls()
        yaml_path = Path(path)

        if not yaml_path.exists():
            raise FileNotFoundError(f"Policy file not found: {yaml_path}")

        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)

        if not data or "policies" not in data:
            raise ValueError("YAML file must contain a 'policies' key")

        for policy_data in data["policies"]:
            policy = _parse_policy(policy_data)
            engine.add_policy(policy)

        return engine

    def add_policy(self, policy: Policy) -> None:
        """Add a policy to the engine."""
        self._policies[policy.name] = policy
        self._log_action("add_policy", policy_name=policy.name,
                         rule_count=len(policy.rules), enabled=policy.enabled)

    def remove_policy(self, name: str) -> bool:
        """Remove a policy by name. Returns True if found."""
        if name in self._policies:
            del self._policies[name]
            self._log_action("remove_policy", policy_name=name)
            return True
        return False

    def enable_policy(self, name: str) -> bool:
        """Enable a policy. Returns True if found."""
        policy = self._policies.get(name)
        if policy:
            policy.enabled = True
            self._log_action("enable_policy", policy_name=name)
            return True
        return False

    def disable_policy(self, name: str) -> bool:
        """Disable a policy. Returns True if found."""
        policy = self._policies.get(name)
        if policy:
            policy.enabled = False
            self._log_action("disable_policy", policy_name=name)
            return True
        return False

    def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        """
        Evaluate a request against all enabled policies.

        Returns the most restrictive decision across all matching rules:
        DENY > REQUIRE_APPROVAL > ALLOW
        """
        matched_policies: list[str] = []
        matched_rules: list[str] = []
        reasons: list[str] = []
        highest_severity = "low"
        current_decision = PolicyDecision.ALLOW

        for policy in self._policies.values():
            if not policy.enabled:
                continue

            for rule in policy.rules:
                match_result = self._evaluate_rule(rule, request)
                if match_result:
                    matched_policies.append(policy.name)
                    matched_rules.append(rule.name)
                    reasons.append(f"[{policy.name}:{rule.name}] {match_result}")

                    # Upgrade severity
                    severity_order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
                    if severity_order.get(rule.severity, 0) > severity_order.get(highest_severity, 0):
                        highest_severity = rule.severity

                    # Upgrade decision (most restrictive wins)
                    if rule.action == PolicyDecision.DENY:
                        current_decision = PolicyDecision.DENY
                    elif rule.action == PolicyDecision.REQUIRE_APPROVAL and current_decision == PolicyDecision.ALLOW:
                        current_decision = PolicyDecision.REQUIRE_APPROVAL

        result = EvaluationResult(
            decision=current_decision,
            matched_policies=matched_policies,
            matched_rules=matched_rules,
            reasons=reasons,
            severity=highest_severity,
        )

        self._log_action(
            "evaluate",
            request_id=request.request_id,
            decision=current_decision.value,
            matched_policies=matched_policies,
            matched_rules=matched_rules,
            severity=highest_severity,
        )

        return result

    def evaluate_input(self, content: str, user_role: str = "") -> EvaluationResult:
        """Convenience method to evaluate input content."""
        return self.evaluate(EvaluationRequest(
            content=content,
            user_role=user_role,
        ))

    def evaluate_output(self, content: str) -> EvaluationResult:
        """Convenience method to evaluate output content."""
        return self.evaluate(EvaluationRequest(
            content=content,
            context={"evaluation_type": "output"},
        ))

    def evaluate_tool_call(self, tool_name: str, parameters: dict = None, user_role: str = "") -> EvaluationResult:
        """Convenience method to evaluate a tool call."""
        return self.evaluate(EvaluationRequest(
            tool_name=tool_name,
            tool_parameters=parameters or {},
            user_role=user_role,
        ))

    def _evaluate_rule(self, rule: PolicyRule, request: EvaluationRequest) -> Optional[str]:
        """
        Evaluate a single rule against a request.
        Returns a reason string if the rule matches, None otherwise.
        """
        # Content filter rules
        if rule.policy_type == PolicyType.CONTENT_FILTER:
            content = request.content
            if content and rule.matches(content):
                return f"Content matched pattern in rule '{rule.name}'"

        # Tool call rules
        elif rule.policy_type == PolicyType.TOOL_CALL:
            if request.tool_name and request.tool_name in rule.denied_tools:
                return f"Tool '{request.tool_name}' is denied by rule '{rule.name}'"
            if request.tool_name and rule.matches(request.tool_name):
                return f"Tool name matched pattern in rule '{rule.name}'"

        # Data access rules
        elif rule.policy_type == PolicyType.DATA_ACCESS:
            if rule.required_roles and request.user_role not in rule.required_roles:
                return f"Role '{request.user_role}' not in required roles {rule.required_roles}"

        # Output check rules
        elif rule.policy_type == PolicyType.OUTPUT_CHECK:
            content = request.content
            if content and rule.matches(content):
                return f"Output matched pattern in rule '{rule.name}'"

        return None

    def _log_action(self, action: str, **kwargs) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            **kwargs,
        }
        self._audit_log.append(entry)

    def get_summary(self) -> dict:
        """Return a summary of the policy engine state."""
        return {
            "total_policies": len(self._policies),
            "enabled_policies": sum(1 for p in self._policies.values() if p.enabled),
            "total_rules": sum(len(p.rules) for p in self._policies.values()),
            "audit_log_entries": len(self._audit_log),
        }


def _parse_policy(data: dict) -> Policy:
    """Parse a policy definition from a YAML dict."""
    policy = Policy(
        name=data["name"],
        description=data.get("description", ""),
        enabled=data.get("enabled", True),
        metadata=data.get("metadata", {}),
    )

    for rule_data in data.get("rules", []):
        action_str = rule_data.get("action", "deny")
        action = PolicyDecision(action_str)

        policy_type_str = rule_data.get("type", "content_filter")
        policy_type = PolicyType(policy_type_str)

        rule = PolicyRule(
            name=rule_data["name"],
            description=rule_data.get("description", ""),
            policy_type=policy_type,
            patterns=rule_data.get("patterns", []),
            denied_tools=rule_data.get("denied_tools", []),
            required_roles=rule_data.get("required_roles", []),
            action=action,
            severity=rule_data.get("severity", "medium"),
            metadata=rule_data.get("metadata", {}),
        )
        policy.rules.append(rule)

    return policy
