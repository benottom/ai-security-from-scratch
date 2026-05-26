"""Tests for Secure Tool Gateway."""

import pytest
from tool_gateway import (
    ApprovalRequest,
    Decision,
    GatewayDecision,
    ParameterSchema,
    ParameterValidationError,
    RateLimitExceededError,
    RiskLevel,
    SecureToolGateway,
    ToolCall,
    ToolDefinition,
    ToolNotFoundError,
)


class TestParameterSchema:
    def test_valid_string(self):
        schema = ParameterSchema(name="query", type="string", required=True)
        valid, reason = schema.validate("hello")
        assert valid is True

    def test_invalid_type(self):
        schema = ParameterSchema(name="count", type="integer", required=True)
        valid, reason = schema.validate("not_a_number")
        assert valid is False
        assert "integer" in reason.lower() or "Expected" in reason

    def test_pattern_validation(self):
        schema = ParameterSchema(name="email", type="string", pattern=r"^[\w.]+@[\w]+\.[\w]+$")
        valid, _ = schema.validate("user@example.com")
        assert valid is True
        valid, _ = schema.validate("not-an-email")
        assert valid is False

    def test_numeric_bounds(self):
        schema = ParameterSchema(name="limit", type="integer", min_value=1, max_value=100)
        valid, _ = schema.validate(50)
        assert valid is True
        valid, _ = schema.validate(0)
        assert valid is False
        valid, _ = schema.validate(101)
        assert valid is False

    def test_allowed_values(self):
        schema = ParameterSchema(name="language", type="string", allowed_values=["python", "javascript"])
        valid, _ = schema.validate("python")
        assert valid is True
        valid, _ = schema.validate("ruby")
        assert valid is False

    def test_max_length(self):
        schema = ParameterSchema(name="query", type="string", max_length=10)
        valid, _ = schema.validate("hello")
        assert valid is True
        valid, _ = schema.validate("a" * 11)
        assert valid is False

    def test_number_type_accepts_int(self):
        schema = ParameterSchema(name="price", type="number", min_value=0)
        valid, _ = schema.validate(10)
        assert valid is True
        valid, _ = schema.validate(10.5)
        assert valid is True

    def test_boolean_type(self):
        schema = ParameterSchema(name="flag", type="boolean")
        valid, _ = schema.validate(True)
        assert valid is True
        valid, _ = schema.validate("true")
        assert valid is False


class TestToolDefinition:
    def test_critical_tool_requires_approval(self):
        tool = ToolDefinition(
            name="nuke",
            description="Deploy nuclear weapon",
            risk_level=RiskLevel.CRITICAL,
        )
        assert tool.requires_approval is True

    def test_low_risk_no_approval(self):
        tool = ToolDefinition(
            name="calculator",
            description="Simple math",
            risk_level=RiskLevel.LOW,
        )
        assert tool.requires_approval is False


class TestSecureToolGateway:
    def setup_method(self):
        self.gateway = SecureToolGateway()
        self.gateway.register_tool(ToolDefinition(
            name="web_search",
            description="Search the web",
            risk_level=RiskLevel.LOW,
            parameters=[
                ParameterSchema(name="query", type="string", required=True, max_length=500),
            ],
        ))
        self.gateway.register_tool(ToolDefinition(
            name="send_email",
            description="Send an email",
            risk_level=RiskLevel.MEDIUM,
            parameters=[
                ParameterSchema(name="to", type="string", required=True),
                ParameterSchema(name="subject", type="string", required=True),
                ParameterSchema(name="body", type="string", required=True),
            ],
            rate_limit_per_minute=10,
        ))
        self.gateway.register_tool(ToolDefinition(
            name="execute_code",
            description="Execute code",
            risk_level=RiskLevel.HIGH,
            parameters=[
                ParameterSchema(name="code", type="string", required=True),
                ParameterSchema(name="language", type="string", required=True, allowed_values=["python", "javascript"]),
            ],
        ))
        self.gateway.register_tool(ToolDefinition(
            name="delete_database",
            description="Delete a database",
            risk_level=RiskLevel.CRITICAL,
            parameters=[
                ParameterSchema(name="db_name", type="string", required=True, pattern=r"^[a-zA-Z0-9_]+$"),
            ],
        ))

    def test_low_risk_tool_allowed(self):
        decision = self.gateway.evaluate(
            ToolCall(tool_name="web_search", parameters={"query": "python"})
        )
        assert decision.decision == Decision.ALLOW

    def test_unknown_tool_denied(self):
        decision = self.gateway.evaluate(
            ToolCall(tool_name="unknown_tool", parameters={})
        )
        assert decision.decision == Decision.DENY
        assert "not in allowlist" in decision.reason

    def test_critical_tool_requires_approval(self):
        decision = self.gateway.evaluate(
            ToolCall(tool_name="delete_database", parameters={"db_name": "test_db"})
        )
        assert decision.decision == Decision.REQUIRE_APPROVAL

    def test_high_risk_tool_requires_approval(self):
        decision = self.gateway.evaluate(
            ToolCall(tool_name="execute_code", parameters={"code": "print('hi')", "language": "python"})
        )
        assert decision.decision == Decision.REQUIRE_APPROVAL

    def test_missing_required_parameter_denied(self):
        decision = self.gateway.evaluate(
            ToolCall(tool_name="web_search", parameters={})
        )
        assert decision.decision == Decision.DENY
        assert any("query" in e for e in decision.validation_errors)

    def test_invalid_parameter_value_denied(self):
        decision = self.gateway.evaluate(
            ToolCall(tool_name="execute_code", parameters={"code": "ls", "language": "bash"})
        )
        assert decision.decision == Decision.DENY
        assert any("language" in e for e in decision.validation_errors)

    def test_parameter_pattern_validation(self):
        # Valid db name
        decision = self.gateway.evaluate(
            ToolCall(tool_name="delete_database", parameters={"db_name": "my_db_123"})
        )
        assert decision.decision == Decision.REQUIRE_APPROVAL

        # Invalid db name (special chars)
        decision = self.gateway.evaluate(
            ToolCall(tool_name="delete_database", parameters={"db_name": "db; DROP TABLE"})
        )
        assert decision.decision == Decision.DENY

    def test_unexpected_parameter_denied(self):
        decision = self.gateway.evaluate(
            ToolCall(tool_name="web_search", parameters={"query": "test", "extra": "value"})
        )
        assert decision.decision == Decision.DENY
        assert any("Unexpected" in e for e in decision.validation_errors)

    def test_disabled_tool_denied(self):
        self.gateway.unregister_tool("web_search")
        self.gateway.register_tool(ToolDefinition(
            name="web_search",
            description="Search the web",
            risk_level=RiskLevel.LOW,
            enabled=False,
        ))
        decision = self.gateway.evaluate(
            ToolCall(tool_name="web_search", parameters={"query": "test"})
        )
        assert decision.decision == Decision.DENY
        assert "disabled" in decision.reason

    def test_approval_flow(self):
        decision = self.gateway.evaluate(
            ToolCall(tool_name="delete_database", parameters={"db_name": "prod"})
        )
        assert decision.decision == Decision.REQUIRE_APPROVAL

        pending = self.gateway.pending_approvals
        assert len(pending) >= 1

        # Approve
        req = pending[0]
        approved = self.gateway.approve(req.request_id, approver="admin@company.com")
        assert approved is not None
        assert approved.status == "approved"
        assert approved.approver == "admin@company.com"

    def test_deny_approval(self):
        self.gateway.evaluate(
            ToolCall(tool_name="delete_database", parameters={"db_name": "prod"})
        )
        pending = self.gateway.pending_approvals
        req = pending[0]
        denied = self.gateway.deny_approval(req.request_id, approver="admin@company.com", reason="Unauthorized")
        assert denied is not None
        assert denied.status == "denied"

    def test_approve_nonexistent_request(self):
        result = self.gateway.approve("nonexistent-id", "admin")
        assert result is None

    def test_execute_with_approval(self):
        call = ToolCall(tool_name="delete_database", parameters={"db_name": "prod"})
        decision = self.gateway.execute_with_approval(call, approver="admin@company.com")
        assert decision.decision == Decision.ALLOW

    def test_execute_without_approval_for_critical(self):
        call = ToolCall(tool_name="delete_database", parameters={"db_name": "prod"})
        decision = self.gateway.execute_with_approval(call, approver="")
        assert decision.decision == Decision.REQUIRE_APPROVAL

    def test_unregister_tool(self):
        assert self.gateway.unregister_tool("web_search") is True
        assert self.gateway.unregister_tool("nonexistent") is False

    def test_audit_log(self):
        self.gateway.evaluate(ToolCall(tool_name="web_search", parameters={"query": "test"}))
        log = self.gateway.audit_log
        assert any(entry["action"] == "evaluate_allow" for entry in log)

    def test_get_summary(self):
        summary = self.gateway.get_summary()
        assert summary["registered_tools"] == 4
        assert summary["tools_by_risk"]["low"] == 1
        assert summary["tools_by_risk"]["critical"] == 1

    def test_auto_approve_high(self):
        gateway = SecureToolGateway(auto_approve_high=True)
        gateway.register_tool(ToolDefinition(
            name="execute_code",
            description="Execute code",
            risk_level=RiskLevel.HIGH,
            parameters=[ParameterSchema(name="code", type="string", required=True)],
        ))
        decision = gateway.evaluate(
            ToolCall(tool_name="execute_code", parameters={"code": "print('hi')"})
        )
        assert decision.decision == Decision.ALLOW


class TestRateLimiting:
    def test_rate_limit_enforcement(self):
        gateway = SecureToolGateway()
        gateway.register_tool(ToolDefinition(
            name="limited_tool",
            description="A rate-limited tool",
            risk_level=RiskLevel.LOW,
            parameters=[ParameterSchema(name="input", type="string", required=False)],
            rate_limit_per_minute=3,
        ))

        # First 3 calls should be allowed
        for _ in range(3):
            decision = gateway.evaluate(
                ToolCall(tool_name="limited_tool", parameters={"input": "test"})
            )
            assert decision.decision == Decision.ALLOW

        # 4th call should be denied
        decision = gateway.evaluate(
            ToolCall(tool_name="limited_tool", parameters={"input": "test"})
        )
        assert decision.decision == Decision.DENY
        assert "rate limit" in decision.reason.lower()
