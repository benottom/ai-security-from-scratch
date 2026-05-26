# Pattern: Human Approval Gate

> **Pattern ID:** PAT-APPR-001 | **Category:** Agent Security | **Maturity:** Proven

---

## Problem

AI systems that take real-world actions — sending emails, executing trades, modifying databases, deploying code — require a trust boundary between the AI's decision to act and the actual execution of that action. Without this boundary, any manipulation of the AI (via prompt injection, adversarial input, or model error) translates directly into unauthorized real-world consequences.

The missing control is a human-in-the-loop checkpoint: a supervisory controller that requires explicit human confirmation before high-risk actions proceed. Without it, the AI's action output flows unimpeded to execution, creating an unconstrained path from model output to irreversible side effects.

**Concrete failure scenario:** An AI-powered trading assistant decides to sell 10,000 shares of a stock based on a misinterpreted news article. Without an approval gate, the sell order is executed immediately. By the time humans notice, the position has been liquidated at a significant loss.

---

## Threat Model

| Attribute | Value |
|---|---|
| **Threat ID** | T-APPR-001 |
| **Threat Name** | Unauthorized high-risk action execution without human oversight |
| **Attack Vector** | AI agent manipulated (prompt injection, model error) into triggering high-risk action |
| **Impact** | Financial loss, data corruption, reputational damage, regulatory violations |
| **Likelihood** | Medium — requires AI to be connected to high-impact action pathways |
| **Risk** | High |
| **OWASP LLM Top 10** | LLM07: Insecure Plugin Design, LLM08: Excessive Agency |
| **NIST AI RMF** | MANAGE 1.1, MANAGE 2.2 |

**Attack variants:**
1. **Direct action manipulation:** Prompt injection causes AI to trigger a high-risk action
2. **Contextual deception:** Misinformation causes AI to make an erroneous but internally consistent decision
3. **Authority impersonation:** Attacker presents as an authorized approver to bypass the gate
4. **Timeout exploitation:** Gate has a timeout that defaults to "approve"; attacker delays review until timeout fires
5. **Approval fatigue:** Flooding the approval queue causes humans to rubber-stamp without review

---

## Control-Theoretic View

### Objective

Ensure that no high-risk action is executed without explicit human authorization, and that actions pending approval are safely isolated until a decision is made.

### Controller

The **Human Approval Gate** — a supervisory control that intercepts high-risk actions, presents them to a human decision-maker, and enforces the human's decision (approve, deny, modify) before the action proceeds.

### Observations

| Observation | Source | Type |
|---|---|---|
| Action type and parameters | AI agent output / Tool gateway | Synchronous |
| Action risk classification | Risk classifier | Synchronous |
| Approver identity and availability | Approval routing engine | Asynchronous |
| Approval decision (approve/deny/modify) | Human approver | Asynchronous |
| Queue depth and wait times | Approval queue | Continuous |

### Actions

| Action | Effect | Preconditions |
|---|---|---|
| Queue for approval | Action held in pending state; approver notified | Risk level = HIGH or CRITICAL |
| Approve and execute | Action proceeds with original parameters | Human explicitly approves |
| Approve with modifications | Action proceeds with human-modified parameters | Human approves with changes |
| Deny and discard | Action cancelled; requester notified | Human denies; or timeout with deny-default |
| Escalate | Action forwarded to higher-authority approver | Original approver cannot decide; or risk level = CRITICAL |
| Timeout denial | Action automatically denied after configurable period | No human decision within timeout window |

### Feedback

- Approval/denial rates and reasons feed back into risk classification tuning
- Timeout rates indicate understaffed approval workflows
- Post-execution audits validate whether approved actions achieved intended outcomes

### Disturbances

| Disturbance | Source | Mitigation |
|---|---|---|
| Approver unavailability | Sick leave, time zones, off-hours | Multi-tier approval chains; auto-escalation |
| Approval fatigue | Excessive low-significance approvals | Tighten risk classification; only gate truly high-risk actions |
| Timeout exploitation | Attacker delays human review | Default-to-deny on timeout; configurable per risk level |
| Impersonation | Stolen approver credentials | MFA for approval actions; IP/device binding |
| Queue flooding | Denial-of-approval attack | Rate limiting on approval requests; batch triage |

### Unsafe States

| Unsafe State | Condition | Consequence |
|---|---|---|
| Action executed without approval | Gate bypassed or timeout-defaults-to-approve | Unauthorized action in production |
| Stale action executed | Action was queued long ago; context has changed | Outdated action causes unintended consequences |
| Approver compromised | Attacker gains approver credentials | Malicious actions approved by unauthorized party |
| Approval queue overflow | Too many pending approvals | System becomes unusable or timeout denies legitimate actions |
| Dual-key bypass | Single approver when policy requires two | Insufficient oversight for critical actions |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  AI Agent Decision                           │
│           "Execute high-risk action: send $50K wire"         │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
               ┌──────────────────────────┐
               │   Human Approval Gate     │
               │                           │
               │  ┌────────────────────┐  │
               │  │  Risk Classifier    │  │──▶ Is this HIGH/CRITICAL risk?
               │  └────────────────────┘  │
               │  ┌────────────────────┐  │
               │  │  Approval Router   │  │──▶ Who should approve this?
               │  └────────────────────┘  │
               │  ┌────────────────────┐  │
               │  │  Action Quarantine │  │──▶ Hold action safely until decided
               │  └────────────────────┘  │
               │  ┌────────────────────┐  │
               │  │  Timeout Manager   │  │──▶ Default to DENY after T seconds
               │  └────────────────────┘  │
               │  ┌────────────────────┐  │
               │  │  Audit Trail       │  │──▶ Immutable log of all decisions
               │  └────────────────────┘  │
               └──────────┬───────────────┘
                          │
              ┌───────────┼───────────────┐
              │           │               │
              ▼           ▼               ▼
        ┌──────────┐ ┌──────────┐   ┌──────────────┐
        │ APPROVED │ │  DENIED  │   │  MODIFIED    │
        │          │ │          │   │  (alt params) │
        └────┬─────┘ └──────────┘   └──────┬───────┘
             │                              │
             ▼                              ▼
    ┌─────────────────────────────────────────────┐
    │            Action Execution                  │
    └──────────────────────────────────────────────┘
```

---

## Implementation

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Callable
from datetime import datetime, timedelta
import uuid
import time


class ApprovalDecision(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    MODIFIED = "modified"       # Approved with parameter changes
    ESCALATED = "escalated"
    TIMED_OUT = "timed_out"


class TimeoutPolicy(Enum):
    APPROVE = "approve"    # Dangerous — only for low-stakes contexts
    DENY = "deny"          # Safe default — action cancelled on timeout
    ESCALATE = "escalate"  # Forward to higher authority on timeout


@dataclass
class ApprovalRequest:
    """A request for human approval of a high-risk action."""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    action_type: str = ""
    action_parameters: dict[str, Any] = field(default_factory=dict)
    risk_level: str = ""
    requester_id: str = ""          # Who (or what AI agent) initiated the action
    assigned_approver: str = ""
    escalation_chain: list[str] = field(default_factory=list)
    timeout_seconds: int = 3600     # 1 hour default
    timeout_policy: TimeoutPolicy = TimeoutPolicy.DENY
    requires_dual_approval: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    decided_at: Optional[datetime] = None
    decision: ApprovalDecision = ApprovalDecision.PENDING
    decision_reason: str = ""
    modified_parameters: Optional[dict[str, Any]] = None
    approvers_who_decided: list[str] = field(default_factory=list)
    context_summary: str = ""       # Human-readable summary of why this action was triggered


@dataclass
class ApprovalResult:
    """The outcome of an approval request."""
    request_id: str
    decision: ApprovalDecision
    reason: str
    modified_parameters: Optional[dict[str, Any]] = None
    executed: bool = False


class HumanApprovalGate:
    """Supervisory control requiring human confirmation for high-risk AI actions.

    Control objective: No high-risk action is executed without explicit
    human authorization.
    """

    def __init__(
        self,
        risk_classifier: Optional[Callable] = None,
        approval_router: Optional[Callable] = None,
        audit_logger: Optional[Callable] = None,
        default_timeout_seconds: int = 3600,
        default_timeout_policy: TimeoutPolicy = TimeoutPolicy.DENY,
    ):
        self.risk_classifier = risk_classifier
        self.approval_router = approval_router
        self.audit_logger = audit_logger
        self.default_timeout_seconds = default_timeout_seconds
        self.default_timeout_policy = default_timeout_policy
        self._pending: dict[str, ApprovalRequest] = {}

    def submit(self, request: ApprovalRequest) -> ApprovalRequest:
        """Submit an action for approval. Returns the queued request."""
        # Apply defaults
        if not request.timeout_seconds:
            request.timeout_seconds = self.default_timeout_seconds
        if not request.timeout_policy:
            request.timeout_policy = self.default_timeout_policy

        # Route to approver if not already assigned
        if not request.assigned_approver and self.approval_router:
            request.assigned_approver = self.approval_router(
                action_type=request.action_type,
                risk_level=request.risk_level,
            )

        # Queue the request
        self._pending[request.request_id] = request

        # Log the submission
        self._log(request, "submitted")

        return request

    def approve(self, request_id: str, approver_id: str, reason: str = "") -> ApprovalResult:
        """Approve a pending action."""
        request = self._get_pending(request_id)
        if not request:
            return ApprovalResult(request_id=request_id, decision=ApprovalDecision.DENIED,
                                  reason="Request not found or already decided")

        # Verify this approver is authorized
        if request.assigned_approver and approver_id != request.assigned_approver:
            if approver_id not in request.escalation_chain:
                return ApprovalResult(request_id=request_id, decision=ApprovalDecision.DENIED,
                                      reason=f"Approver {approver_id} not authorized for this request")

        # Handle dual approval
        if request.requires_dual_approval:
            request.approvers_who_decided.append(approver_id)
            if len(request.approvers_who_decided) < 2:
                self._log(request, f"partial_approval by {approver_id}")
                return ApprovalResult(
                    request_id=request_id,
                    decision=ApprovalDecision.PENDING,
                    reason=f"First approval received from {approver_id}; awaiting second approver",
                )

        request.decision = ApprovalDecision.APPROVED
        request.decided_at = datetime.utcnow()
        request.decision_reason = reason
        request.approvers_who_decided.append(approver_id)

        self._log(request, f"approved by {approver_id}")
        self._pending.pop(request_id, None)

        return ApprovalResult(
            request_id=request_id,
            decision=ApprovalDecision.APPROVED,
            reason=reason,
        )

    def deny(self, request_id: str, approver_id: str, reason: str = "") -> ApprovalResult:
        """Deny a pending action."""
        request = self._get_pending(request_id)
        if not request:
            return ApprovalResult(request_id=request_id, decision=ApprovalDecision.DENIED,
                                  reason="Request not found")

        request.decision = ApprovalDecision.DENIED
        request.decided_at = datetime.utcnow()
        request.decision_reason = reason
        request.approvers_who_decided.append(approver_id)

        self._log(request, f"denied by {approver_id}")
        self._pending.pop(request_id, None)

        return ApprovalResult(request_id=request_id, decision=ApprovalDecision.DENIED, reason=reason)

    def modify_and_approve(
        self, request_id: str, approver_id: str, modified_params: dict, reason: str = ""
    ) -> ApprovalResult:
        """Approve with modified parameters."""
        request = self._get_pending(request_id)
        if not request:
            return ApprovalResult(request_id=request_id, decision=ApprovalDecision.DENIED,
                                  reason="Request not found")

        request.decision = ApprovalDecision.MODIFIED
        request.decided_at = datetime.utcnow()
        request.decision_reason = reason
        request.modified_parameters = modified_params
        request.approvers_who_decided.append(approver_id)

        self._log(request, f"modified and approved by {approver_id}")
        self._pending.pop(request_id, None)

        return ApprovalResult(
            request_id=request_id,
            decision=ApprovalDecision.MODIFIED,
            reason=reason,
            modified_parameters=modified_params,
        )

    def check_timeouts(self) -> list[ApprovalResult]:
        """Check for and process timed-out requests. Call periodically."""
        now = datetime.utcnow()
        results = []
        timed_out_ids = []

        for req_id, request in self._pending.items():
            elapsed = (now - request.created_at).total_seconds()
            if elapsed > request.timeout_seconds:
                result = self._handle_timeout(request)
                results.append(result)
                timed_out_ids.append(req_id)

        for req_id in timed_out_ids:
            self._pending.pop(req_id, None)

        return results

    def _handle_timeout(self, request: ApprovalRequest) -> ApprovalResult:
        """Handle a request that has timed out."""
        if request.timeout_policy == TimeoutPolicy.DENY:
            request.decision = ApprovalDecision.TIMED_OUT
            request.decided_at = datetime.utcnow()
            request.decision_reason = f"Timed out after {request.timeout_seconds}s; policy=deny"
            self._log(request, "timed_out_denied")
            return ApprovalResult(
                request_id=request.request_id,
                decision=ApprovalDecision.TIMED_OUT,
                reason=request.decision_reason,
            )
        elif request.timeout_policy == TimeoutPolicy.ESCALATE:
            request.decision = ApprovalDecision.ESCALATED
            next_approver = request.escalation_chain[0] if request.escalation_chain else "admin"
            request.assigned_approver = next_approver
            request.created_at = datetime.utcnow()  # Reset timeout
            self._log(request, f"escalated to {next_approver}")
            return ApprovalResult(
                request_id=request.request_id,
                decision=ApprovalDecision.ESCALATED,
                reason=f"Escalated to {next_approver}",
            )
        else:  # TimeoutPolicy.APPROVE — use with extreme caution
            request.decision = ApprovalDecision.APPROVED
            request.decided_at = datetime.utcnow()
            request.decision_reason = f"Timed out after {request.timeout_seconds}s; policy=approve"
            self._log(request, "timed_out_approved")
            return ApprovalResult(
                request_id=request.request_id,
                decision=ApprovalDecision.APPROVED,
                reason=request.decision_reason,
            )

    def _get_pending(self, request_id: str) -> Optional[ApprovalRequest]:
        return self._pending.get(request_id)

    def _log(self, request: ApprovalRequest, event: str):
        if self.audit_logger:
            self.audit_logger(
                request_id=request.request_id,
                action_type=request.action_type,
                event=event,
                risk_level=request.risk_level,
                timestamp=datetime.utcnow().isoformat(),
            )
```

---

## Tests

```python
import pytest
from human_approval_gate import (
    HumanApprovalGate, ApprovalRequest, ApprovalDecision, TimeoutPolicy
)


class TestHumanApprovalGate:
    """Security regression tests for the Human Approval Gate."""

    @pytest.fixture
    def gate(self):
        return HumanApprovalGate(
            default_timeout_seconds=300,
            default_timeout_policy=TimeoutPolicy.DENY,
        )

    def test_high_risk_action_requires_approval(self, gate):
        request = ApprovalRequest(
            action_type="wire_transfer",
            action_parameters={"amount": 50000, "recipient": "ACCT-999"},
            risk_level="CRITICAL",
            requester_id="ai-agent-001",
            assigned_approver="approver-1",
        )
        result = gate.submit(request)
        assert result.decision == ApprovalDecision.PENDING

    def test_approved_action_can_proceed(self, gate):
        request = gate.submit(ApprovalRequest(
            action_type="send_email", action_parameters={"to": "user@example.com"},
            risk_level="HIGH", requester_id="ai-agent-001", assigned_approver="approver-1",
        ))
        result = gate.approve(request.request_id, "approver-1", "Verified recipient")
        assert result.decision == ApprovalDecision.APPROVED

    def test_denied_action_is_blocked(self, gate):
        request = gate.submit(ApprovalRequest(
            action_type="delete_database", action_parameters={"db": "production"},
            risk_level="CRITICAL", requester_id="ai-agent-001", assigned_approver="approver-1",
        ))
        result = gate.deny(request.request_id, "approver-1", "Not authorized for this action")
        assert result.decision == ApprovalDecision.DENIED

    def test_unauthorized_approver_cannot_approve(self, gate):
        request = gate.submit(ApprovalRequest(
            action_type="wire_transfer", action_parameters={"amount": 50000},
            risk_level="CRITICAL", requester_id="ai-agent-001", assigned_approver="approver-1",
        ))
        result = gate.approve(request.request_id, "random-user", "Trying to approve")
        assert result.decision == ApprovalDecision.DENIED

    def test_timeout_defaults_to_deny(self, gate):
        request = ApprovalRequest(
            action_type="wire_transfer", action_parameters={"amount": 50000},
            risk_level="CRITICAL", requester_id="ai-agent-001",
            assigned_approver="approver-1",
            timeout_seconds=0,  # Immediate timeout for testing
            timeout_policy=TimeoutPolicy.DENY,
            created_at=datetime.utcnow() - timedelta(seconds=1),
        )
        gate.submit(request)
        results = gate.check_timeouts()
        assert results[0].decision == ApprovalDecision.TIMED_OUT

    def test_dual_approval_required(self, gate):
        request = gate.submit(ApprovalRequest(
            action_type="deploy_production", action_parameters={"version": "2.0"},
            risk_level="CRITICAL", requester_id="ai-agent-001",
            assigned_approver="approver-1",
            requires_dual_approval=True,
        ))
        # First approval — should still be pending
        result = gate.approve(request.request_id, "approver-1", "First approval")
        assert result.decision == ApprovalDecision.PENDING

    def test_modified_approval(self, gate):
        request = gate.submit(ApprovalRequest(
            action_type="send_email", action_parameters={"to": "all@company.com", "body": "..."},
            risk_level="HIGH", requester_id="ai-agent-001", assigned_approver="approver-1",
        ))
        result = gate.modify_and_approve(
            request.request_id, "approver-1",
            modified_params={"to": "managers@company.com", "body": "..."},
            reason="Restricted distribution",
        )
        assert result.decision == ApprovalDecision.MODIFIED
        assert result.modified_parameters["to"] == "managers@company.com"
```

---

## Monitoring

| Metric | Collection | Warning | Critical | Alert Channel |
|---|---|---|---|---|
| Pending approval count | Continuous | > 20 pending | > 100 pending | Operations |
| Approval latency (P95) | Per-approval | > 10 min | > 60 min | Operations + management |
| Timeout rate | Hourly | > 5% of requests | > 20% of requests | Operations + security |
| Denial rate | Daily | > 30% of requests | > 60% of requests | Security + product |
| Dual approval completion rate | Daily | < 80% within SLA | < 50% within SLA | Compliance |
| Approver impersonation attempts | Per-event | Any | > 3 in 1 hour | Incident response |

---

## Failure Modes

| Failure Mode | Cause | Detection | Mitigation |
|---|---|---|---|
| **Timeout default-to-approve** | Misconfigured timeout policy | Audit review finds approved-without-human entries | Always default to deny; alert on any approve-on-timeout |
| **Approval fatigue** | Excessive approvals degrade human attention | Denial rate drops to near-zero; approval time drops | Only gate truly high-risk actions; batch trivial approvals |
| **Impersonation** | Compromised approver credentials | MFA challenge failures; unusual approval patterns | MFA for approvals; device binding; anomaly detection |
| **Stale approval execution** | Approved action executed much later in changed context | Time gap between approval and execution | Re-validation before execution; approval TTL |
| **Single point of failure** | Only one approver configured | Approver unavailability → all actions timeout | Multi-tier approval chains; backup approvers |

---

## When Not To Use

1. **Fully autonomous systems with no human oversight requirement:** Some systems are designed for complete autonomy (e.g., spam filtering, content moderation at scale). Human approval would be impractical.

2. **Low-stakes actions with trivial impact:** If an action is easily reversible and has negligible impact (e.g., sending a notification, updating a UI preference), the approval overhead is not justified.

3. **Real-time systems where human latency is unacceptable:** If decisions must be made in milliseconds (e.g., autonomous driving collision avoidance), human approval is infeasible. Use the AI Circuit Breaker pattern instead.

4. **Systems with compensating controls that make approval redundant:** If every action is validated by a deterministic post-execution audit that can fully reverse any action, approval may be redundant. Consider whether reversal is truly possible.

5. **Development and testing environments with synthetic data:** Approval gates add friction during development. Enable them in staging and production.

---

## Assurance Evidence

| Artifact | Description | Format | Retention |
|---|---|---|---|
| Approval audit log | Every submission, decision, and timeout | Structured JSON | 2 years |
| Approval request records | Full context of each request and its resolution | Database records | 2 years |
| Timeout events | All timeout occurrences with policy applied | Structured JSON | 1 year |
| Denial analysis | Patterns in denied requests | Quarterly report | Permanent |
| Dual-approval compliance | Verification that dual-approval policy was followed | Compliance report | Permanent |

---

*Pattern version: 1.0.0 | AI Security from Scratch*
