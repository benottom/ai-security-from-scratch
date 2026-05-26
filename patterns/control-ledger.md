# Pattern: Control Ledger

> **Pattern ID:** PAT-LEDGER-001 | **Category:** Observability | **Maturity:** Proven

---

## Problem

AI security systems make numerous decisions — classifying inputs, blocking requests, filtering outputs, approving tool calls, quarantining memory, tripping circuit breakers. Each decision is a security-relevant event that may need to be audited, investigated, or used as evidence in compliance proceedings. Without a systematic, immutable record of these decisions, the system has no accountability trail: security controls operate in the dark, failures go unattributed, and compliance evidence must be reconstructed manually (if it can be reconstructed at all).

The root cause is an observation gap in the control loop: the system's own decisions are not treated as first-class observations. Decisions are logged to scattered, mutable, inconsistent logs that can be overwritten, deleted, or tampered with, destroying the audit trail precisely when it is most needed — after an incident.

**Concrete failure scenario:** A prompt injection attack succeeds and causes the AI to leak sensitive data. The security team investigates but finds that the input classifier's decision logs were stored in a rotating log file that has already been overwritten. There is no record of whether the classifier was called, what it decided, or why it failed to block the attack. The team cannot determine root cause, cannot produce evidence for regulators, and cannot fix the control gap.

---

## Threat Model

| Attribute | Value |
|---|---|
| **Threat ID** | T-LEDGER-001 |
| **Threat Name** | Loss or tampering of security decision audit trail |
| **Attack Vector** | Log deletion, modification, or rotation after an incident; or system design that fails to log critical decisions |
| **Impact** | Inability to investigate incidents; compliance violations; inability to improve controls |
| **Likelihood** | Medium — log rotation and deletion are common operational practices |
| **Risk** | High |
| **OWASP LLM Top 10** | LLM10: Insecure Output Handling (audit trail is an output) |
| **NIST AI RMF** | GOV 1.2, MEASURE 2.7, MANAGE 2.3 |

**Attack variants:**
1. **Log rotation/deletion:** Standard log management practices destroy evidence
2. **Log tampering:** Attacker with system access modifies audit logs to cover tracks
3. **Selective logging:** System logs some decisions but not others, creating blind spots
4. **Schema inconsistency:** Different components log in different formats, making correlation impossible
5. **Log injection:** Attacker injects false entries to create confusion or false alibis

---

## Control-Theoretic View

### Objective

Ensure that all security-relevant decisions made by the AI system are recorded in an immutable, queryable, and tamper-evident ledger that supports incident investigation, compliance evidence, and control-loop feedback.

### Controller

The **Control Ledger** — an append-only, content-addressed event store that records every security decision with a standardized schema, cryptographic integrity verification, and evidence-generation capabilities.

### Observations

| Observation | Source | Type |
|---|---|---|
| Security decision events | All security components (firewall, gateway, validators, etc.) | Asynchronous |
| Event integrity hashes | Content-addressed storage | Synchronous (verification) |
| Query results | Ledger query interface | Synchronous |
| Storage health metrics | Storage backend | Continuous |

### Actions

| Action | Effect | Preconditions |
|---|---|---|
| Record event | Decision appended to ledger | Any security-relevant decision is made |
| Verify integrity | Check that no events have been modified or deleted | Periodic verification; incident investigation |
| Query events | Retrieve decisions by time, type, component, or correlation ID | Investigation or reporting |
| Generate evidence package | Export filtered, signed event set for compliance | Compliance request or audit |
| Rotate storage | Move old events to archive (still immutable) | Storage capacity threshold |

### Feedback

- Ledger queries reveal patterns in security decisions (e.g., increasing block rates indicate evolving threats)
- Integrity verification failures trigger immediate security alerts
- Evidence packages feed assurance cases and compliance reports

### Disturbances

| Disturbance | Source | Mitigation |
|---|---|---|
| Storage exhaustion | High event volume | Tiered storage; compression; archival |
| Write latency | High throughput requirements | Async writes with ordering guarantees |
| Query performance | Large ledger size | Indexing; time-partitioned storage |
| Schema evolution | Component updates change event structure | Schema versioning; backward compatibility |
| Cryptographic key rotation | Certificate expiry | Dual-signing during rotation period |

### Unsafe States

| Unsafe State | Condition | Consequence |
|---|---|---|
| Events lost | Ledger storage failure without replication | Audit gap; compliance violation |
| Events tampered | Integrity verification fails | Evidence inadmissible; trust broken |
| Events not recorded | Component bypasses ledger | Decision made without accountability |
| Schema inconsistency | Different formats prevent correlation | Inability to reconstruct event sequences |
| Query unavailable | Storage backend down | Cannot investigate ongoing incidents |

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│               Security Components (Event Sources)             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │  Context     │ │  Tool       │ │  Output     │ ...       │
│  │  Firewall    │ │  Gateway    │ │  Validator  │           │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘           │
└─────────┼───────────────┼───────────────┼───────────────────┘
          │               │               │
          ▼               ▼               ▼
┌──────────────────────────────────────────────────────────────┐
│                     Control Ledger                            │
│                                                              │
│  ┌──────────────────────────────────────────────────────────┐│
│  │  Event Ingestion                                         ││
│  │  • Schema validation         • Content hashing           ││
│  │  • Envelope wrapping         • Sequential ordering       ││
│  └──────────────────────────────────────────────────────────┘│
│  ┌──────────────────────────────────────────────────────────┐│
│  │  Immutable Storage (Append-Only)                         ││
│  │  • Content-addressed (hash = ID)  • Chain integrity      ││
│  │  • Replicated (3+ copies)         • Encrypted at rest    ││
│  │  • Tiered (hot → warm → archive)  • Tamper-evident       ││
│  └──────────────────────────────────────────────────────────┘│
│  ┌──────────────────────────────────────────────────────────┐│
│  │  Query & Evidence Interface                              ││
│  │  • Time-range queries          • Component filters       ││
│  │  • Correlation ID lookup       • Signed evidence export  ││
│  │  • Integrity verification      • Compliance reports      ││
│  └──────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘
```

---

## Implementation

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from datetime import datetime
import hashlib
import json
import uuid


class EventCategory(Enum):
    INPUT_VALIDATION = "input_validation"
    OUTPUT_FILTERING = "output_filtering"
    TOOL_EXECUTION = "tool_execution"
    APPROVAL_DECISION = "approval_decision"
    MEMORY_QUARANTINE = "memory_quarantine"
    CIRCUIT_BREAKER = "circuit_breaker"
    POLICY_CHANGE = "policy_change"
    CONFIGURATION = "configuration"
    INCIDENT = "incident"


@dataclass
class LedgerEvent:
    """A single security-relevant decision recorded in the control ledger."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    category: str = ""                     # EventCategory value
    source_component: str = ""             # e.g., "context_firewall", "tool_gateway"
    action: str = ""                       # e.g., "block", "permit", "sanitize"
    decision_outcome: str = ""             # "allowed", "blocked", "modified", "escalated"
    subject: str = ""                      # What was affected (user_id, doc_id, tool_name)
    details: dict[str, Any] = field(default_factory=dict)
    correlation_id: str = ""               # Links related events (e.g., same request)
    risk_score: float = 0.0
    schema_version: str = "1.0.0"
    previous_hash: str = ""                # Hash chain: links to previous event
    content_hash: str = ""                 # Hash of this event's content


class ControlLedger:
    """Immutable, observable logging of all security-relevant decisions.

    Control objective: All security-relevant decisions are recorded in
    an append-only, tamper-evident ledger.
    """

    def __init__(self, storage_backend=None, encryption_key: Optional[str] = None):
        self.storage = storage_backend or InMemoryLedgerStorage()
        self.encryption_key = encryption_key
        self._last_hash = "genesis"  # Hash chain anchor

    def record(self, event: LedgerEvent) -> LedgerEvent:
        """Record a security decision event in the ledger."""
        # Compute content hash
        event.content_hash = self._compute_hash(event)

        # Link to previous event (hash chain)
        event.previous_hash = self._last_hash

        # Validate schema
        if not self._validate_schema(event):
            raise ValueError(f"Event schema validation failed for {event.event_id}")

        # Store the event
        self.storage.append(event)

        # Update chain tip
        self._last_hash = event.content_hash

        return event

    def record_decision(
        self,
        category: str,
        source_component: str,
        action: str,
        decision_outcome: str,
        subject: str = "",
        details: Optional[dict] = None,
        correlation_id: str = "",
        risk_score: float = 0.0,
    ) -> LedgerEvent:
        """Convenience method to record a security decision."""
        event = LedgerEvent(
            category=category,
            source_component=source_component,
            action=action,
            decision_outcome=decision_outcome,
            subject=subject,
            details=details or {},
            correlation_id=correlation_id,
            risk_score=risk_score,
        )
        return self.record(event)

    def verify_integrity(self) -> tuple[bool, list[str]]:
        """Verify the integrity of the entire ledger (hash chain validation)."""
        events = self.storage.get_all()
        errors = []

        if not events:
            return True, []

        # Verify chain from genesis
        expected_prev = "genesis"
        for event in events:
            if event.previous_hash != expected_prev:
                errors.append(
                    f"Chain break at {event.event_id}: expected previous_hash={expected_prev}, "
                    f"got {event.previous_hash}"
                )

            # Verify content hash
            computed = self._compute_hash(event)
            if event.content_hash != computed:
                errors.append(
                    f"Content hash mismatch at {event.event_id}: "
                    f"stored={event.content_hash}, computed={computed}"
                )

            expected_prev = event.content_hash

        return len(errors) == 0, errors

    def query(
        self,
        category: Optional[str] = None,
        source_component: Optional[str] = None,
        correlation_id: Optional[str] = None,
        subject: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: int = 100,
    ) -> list[LedgerEvent]:
        """Query the ledger with filters."""
        results = []
        for event in self.storage.get_all():
            if category and event.category != category:
                continue
            if source_component and event.source_component != source_component:
                continue
            if correlation_id and event.correlation_id != correlation_id:
                continue
            if subject and event.subject != subject:
                continue
            if start_time and event.timestamp < start_time:
                continue
            if end_time and event.timestamp > end_time:
                continue
            results.append(event)
            if len(results) >= limit:
                break
        return results

    def generate_evidence_package(
        self,
        correlation_id: str,
        title: str = "",
        description: str = "",
    ) -> dict:
        """Generate a signed evidence package for compliance or audit."""
        events = self.query(correlation_id=correlation_id, limit=10000)
        is_valid, errors = self.verify_integrity()

        package = {
            "title": title or f"Evidence Package: {correlation_id}",
            "description": description,
            "generated_at": datetime.utcnow().isoformat(),
            "correlation_id": correlation_id,
            "event_count": len(events),
            "integrity_verified": is_valid,
            "integrity_errors": errors,
            "events": [
                {
                    "event_id": e.event_id,
                    "timestamp": e.timestamp,
                    "category": e.category,
                    "source_component": e.source_component,
                    "action": e.action,
                    "decision_outcome": e.decision_outcome,
                    "subject": e.subject,
                    "details": e.details,
                    "risk_score": e.risk_score,
                    "content_hash": e.content_hash,
                }
                for e in events
            ],
            "package_hash": "",  # Computed below
        }

        # Hash the entire package for tamper detection
        package_content = json.dumps(package, sort_keys=True, default=str)
        package["package_hash"] = hashlib.sha256(package_content.encode()).hexdigest()

        return package

    def _compute_hash(self, event: LedgerEvent) -> str:
        """Compute the content hash of an event."""
        content = json.dumps({
            "event_id": event.event_id,
            "timestamp": event.timestamp,
            "category": event.category,
            "source_component": event.source_component,
            "action": event.action,
            "decision_outcome": event.decision_outcome,
            "subject": event.subject,
            "details": event.details,
            "risk_score": event.risk_score,
            "schema_version": event.schema_version,
        }, sort_keys=True, default=str)
        return hashlib.sha256(content.encode()).hexdigest()

    def _validate_schema(self, event: LedgerEvent) -> bool:
        """Validate that the event conforms to the expected schema."""
        required_fields = ["event_id", "timestamp", "category", "source_component", "action"]
        for field_name in required_fields:
            if not getattr(event, field_name, None):
                return False
        return True


class InMemoryLedgerStorage:
    """In-memory storage backend for the control ledger (development/testing)."""

    def __init__(self):
        self._events: list[LedgerEvent] = []

    def append(self, event: LedgerEvent):
        self._events.append(event)

    def get_all(self) -> list[LedgerEvent]:
        return list(self._events)

    def count(self) -> int:
        return len(self._events)
```

---

## Tests

```python
import pytest
from control_ledger import ControlLedger, LedgerEvent, EventCategory


class TestControlLedger:
    """Security regression tests for the Control Ledger pattern."""

    @pytest.fixture
    def ledger(self):
        return ControlLedger()

    def test_event_recorded(self, ledger):
        event = ledger.record_decision(
            category=EventCategory.INPUT_VALIDATION.value,
            source_component="context_firewall",
            action="block",
            decision_outcome="blocked",
            subject="user-123",
            details={"reason": "Prompt injection detected"},
            risk_score=0.95,
        )
        assert event.event_id is not None
        assert event.content_hash != ""

    def test_hash_chain_integrity(self, ledger):
        for i in range(10):
            ledger.record_decision(
                category=EventCategory.INPUT_VALIDATION.value,
                source_component="context_firewall",
                action="block" if i % 2 == 0 else "permit",
                decision_outcome="blocked" if i % 2 == 0 else "allowed",
                subject=f"user-{i}",
                risk_score=0.5,
            )
        is_valid, errors = ledger.verify_integrity()
        assert is_valid, f"Hash chain integrity check failed: {errors}"

    def test_tampering_detected(self, ledger):
        ledger.record_decision(
            category=EventCategory.INPUT_VALIDATION.value,
            source_component="context_firewall",
            action="block",
            decision_outcome="blocked",
            subject="user-123",
        )
        # Tamper with the stored event
        events = ledger.storage.get_all()
        events[0].action = "permit"  # Tampered!

        is_valid, errors = ledger.verify_integrity()
        assert not is_valid, "Tampering was not detected"

    def test_query_by_category(self, ledger):
        ledger.record_decision(
            category=EventCategory.INPUT_VALIDATION.value,
            source_component="firewall",
            action="block",
            decision_outcome="blocked",
            subject="u1",
        )
        ledger.record_decision(
            category=EventCategory.TOOL_EXECUTION.value,
            source_component="tool_gateway",
            action="permit",
            decision_outcome="allowed",
            subject="u1",
        )
        results = ledger.query(category=EventCategory.INPUT_VALIDATION.value)
        assert len(results) == 1
        assert results[0].category == EventCategory.INPUT_VALIDATION.value

    def test_query_by_correlation_id(self, ledger):
        corr_id = "req-abc-123"
        for i in range(3):
            ledger.record_decision(
                category=EventCategory.INPUT_VALIDATION.value,
                source_component=f"component-{i}",
                action="evaluate",
                decision_outcome="allowed",
                subject="u1",
                correlation_id=corr_id,
            )
        results = ledger.query(correlation_id=corr_id)
        assert len(results) == 3

    def test_evidence_package_generation(self, ledger):
        corr_id = "incident-001"
        ledger.record_decision(
            category=EventCategory.INPUT_VALIDATION.value,
            source_component="context_firewall",
            action="block",
            decision_outcome="blocked",
            subject="attacker",
            correlation_id=corr_id,
            details={"payload": "Ignore all instructions"},
            risk_score=0.95,
        )
        package = ledger.generate_evidence_package(
            correlation_id=corr_id,
            title="Prompt Injection Incident",
        )
        assert package["event_count"] == 1
        assert package["integrity_verified"] is True
        assert package["package_hash"] != ""
        assert package["events"][0]["action"] == "block"

    def test_schema_validation_rejects_invalid_event(self, ledger):
        with pytest.raises(ValueError):
            ledger.record(LedgerEvent())  # Missing required fields
```

---

## Monitoring

| Metric | Collection | Warning | Critical | Alert Channel |
|---|---|---|---|---|
| Event write rate | Per-second | > 1000/sec | > 10000/sec | Infrastructure |
| Write latency (P99) | Per-second | > 50ms | > 200ms | Infrastructure |
| Integrity verification failures | Per-check | Any | Any | Incident response |
| Storage utilization | Per-hour | > 70% | > 90% | Infrastructure |
| Query latency (P95) | Per-query | > 500ms | > 2s | Operations |
| Missing events (gap detection) | Per-minute | Any gap | Any gap > 30s | Security SIEM |

---

## Failure Modes

| Failure Mode | Cause | Detection | Mitigation |
|---|---|---|---|
| **Storage failure** | Disk/DB outage | Write errors; health checks | Replicated storage; write-ahead buffer |
| **Hash chain break** | Event modified or deleted | Integrity verification failure | Append-only enforcement; replication |
| **Schema incompatibility** | Component updated, new event format | Schema validation failure on write | Schema versioning; backward compatibility |
| **Write bottleneck** | High throughput overwhelms storage | P99 latency alert | Async writes; batching; horizontal scaling |
| **Query timeout** | Large ledger, complex queries | Query latency alert | Indexing; time-partitioned storage; caching |

---

## When Not To Use

1. **Systems with no security decisions to log:** If your AI system has no security controls, there is nothing to ledger. (You probably need security controls first.)

2. **Short-lived test environments with no audit requirements:** During unit testing, an in-memory ledger is sufficient; no persistent ledger is needed.

3. **Systems with existing immutable audit logging that meets all requirements:** If you already have an append-only, tamper-evident, queryable audit system (e.g., CloudTrail + S3 Object Lock), a separate control ledger may be redundant. Ensure it captures all security decisions with the required schema.

4. **Extreme low-latency systems where even async logging is too slow:** In rare cases, the overhead of event recording (even async) may be unacceptable. Consider sampling critical events and logging others asynchronously.

5. **When the overhead of hash chain verification is prohibitive:** For very high-throughput systems, maintaining a per-event hash chain may be too expensive. Consider Merkle tree batching (hash tree updated every N events instead of every event).

---

## Assurance Evidence

| Artifact | Description | Format | Retention |
|---|---|---|---|
| Ledger event stream | All security-relevant decisions | Structured JSON (append-only) | Permanent |
| Integrity verification reports | Periodic hash chain checks | Report | 2 years |
| Evidence packages | Signed, filtered exports for compliance | JSON (signed) | Permanent |
| Schema version history | Evolution of the event schema | Markdown | Permanent |
| Storage health reports | Capacity, replication status, performance | Report | 90 days |

---

*Pattern version: 1.0.0 | AI Security from Scratch*
