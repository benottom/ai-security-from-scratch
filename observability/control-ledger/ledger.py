"""
Control Ledger — Append-only event store with hash-chaining for integrity.

The control ledger provides a tamper-evident audit trail for all security-relevant
events in the AI system. Events are stored in JSONL format, and each event includes
a hash of the previous event, creating a chain that can detect tampering.

Control-Theoretic View:
    In the control loop, the ledger is the observer's record — it captures every
    state transition, decision, and control action. Without a reliable record,
    it's impossible to reconstruct what happened during a security incident.
    Hash-chaining ensures the record itself cannot be tampered with without detection.

Key Properties:
    1. Append-only: events cannot be deleted or modified after writing
    2. Hash-chaining: each event includes a hash of the previous event
    3. JSONL format: one JSON object per line for easy parsing
    4. Integrity verification: the entire chain can be verified
    5. Event typing: structured event types for filtering and analysis
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


@dataclass
class LedgerEvent:
    """A single event in the control ledger."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_type: str = ""  # e.g., "input_validated", "policy_checked", "output_filtered"
    actor: str = ""  # Who/what triggered this event
    action: str = ""  # What was done
    decision: str = ""  # allow, deny, require_approval
    target: str = ""  # What was affected
    details: dict = field(default_factory=dict)
    previous_hash: str = ""
    event_hash: str = ""  # Computed after creation

    def compute_hash(self) -> str:
        """Compute SHA-256 hash of this event (excluding the hash field itself)."""
        data = {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "actor": self.actor,
            "action": self.action,
            "decision": self.decision,
            "target": self.target,
            "details": self.details,
            "previous_hash": self.previous_hash,
        }
        serialized = json.dumps(data, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def seal(self, previous_hash: str) -> None:
        """Seal this event with the previous event's hash and compute its own hash."""
        self.previous_hash = previous_hash
        self.event_hash = self.compute_hash()

    def to_json(self) -> str:
        """Serialize to a single JSON line."""
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))

    @classmethod
    def from_json(cls, line: str) -> "LedgerEvent":
        """Deserialize from a JSON line."""
        data = json.loads(line)
        return cls(**data)


class ControlLedger:
    """
    Append-only control ledger with hash-chaining for integrity.

    Usage:
        ledger = ControlLedger()
        ledger.append(event_type="input_validated", actor="context_firewall",
                       action="validate_input", decision="allow", target="user_input")
        ledger.append(event_type="output_filtered", actor="output_validator",
                       action="check_secrets", decision="block", target="llm_output")

        # Verify integrity
        assert ledger.verify_integrity()

        # Write to file
        ledger.write_to_file("control-ledger.jsonl")
    """

    GENESIS_HASH = "0" * 64  # SHA-256 of nothing — genesis block

    def __init__(self):
        self._events: list[LedgerEvent] = []
        self._last_hash: str = self.GENESIS_HASH

    @property
    def events(self) -> list[LedgerEvent]:
        return list(self._events)

    @property
    def last_hash(self) -> str:
        return self._last_hash

    @property
    def size(self) -> int:
        return len(self._events)

    def append(
        self,
        event_type: str,
        actor: str,
        action: str,
        decision: str,
        target: str = "",
        details: dict = None,
        timestamp: str = "",
    ) -> LedgerEvent:
        """
        Append a new event to the ledger.

        Args:
            event_type: Type of event (e.g., "input_validated", "policy_checked").
            actor: Who/what triggered this event.
            action: What was done.
            decision: The decision made (allow, deny, require_approval).
            target: What was affected.
            details: Additional details.
            timestamp: Optional timestamp (defaults to now).

        Returns:
            The created and sealed LedgerEvent.
        """
        event = LedgerEvent(
            event_type=event_type,
            actor=actor,
            action=action,
            decision=decision,
            target=target,
            details=details or {},
            timestamp=timestamp or datetime.now(timezone.utc).isoformat(),
        )
        event.seal(self._last_hash)
        self._events.append(event)
        self._last_hash = event.event_hash
        return event

    def verify_integrity(self) -> tuple[bool, list[str]]:
        """
        Verify the integrity of the entire ledger chain.

        Returns:
            A tuple of (is_valid, list_of_errors).
        """
        errors: list[str] = []

        if not self._events:
            return True, []

        # Check first event's previous hash
        if self._events[0].previous_hash != self.GENESIS_HASH:
            errors.append(
                f"Event {self._events[0].event_id}: previous_hash is not genesis hash"
            )

        # Verify each event
        prev_hash = self.GENESIS_HASH
        for i, event in enumerate(self._events):
            # Check previous hash linkage
            if event.previous_hash != prev_hash:
                errors.append(
                    f"Event {event.event_id} (index {i}): previous_hash mismatch. "
                    f"Expected {prev_hash[:16]}..., got {event.previous_hash[:16]}..."
                )

            # Check event hash
            expected_hash = event.compute_hash()
            if event.event_hash != expected_hash:
                errors.append(
                    f"Event {event.event_id} (index {i}): event_hash mismatch. "
                    f"Event may have been tampered with."
                )

            prev_hash = event.event_hash

        return len(errors) == 0, errors

    def query(
        self,
        event_type: str = "",
        actor: str = "",
        decision: str = "",
        target: str = "",
        start_time: str = "",
        end_time: str = "",
    ) -> list[LedgerEvent]:
        """
        Query events by various filters.

        All filters are optional; only non-empty filters are applied.
        """
        results = self._events

        if event_type:
            results = [e for e in results if e.event_type == event_type]
        if actor:
            results = [e for e in results if e.actor == actor]
        if decision:
            results = [e for e in results if e.decision == decision]
        if target:
            results = [e for e in results if e.target == target]
        if start_time:
            results = [e for e in results if e.timestamp >= start_time]
        if end_time:
            results = [e for e in results if e.timestamp <= end_time]

        return results

    def get_events_by_type(self, event_type: str) -> list[LedgerEvent]:
        """Get all events of a specific type."""
        return [e for e in self._events if e.event_type == event_type]

    def get_denied_events(self) -> list[LedgerEvent]:
        """Get all events with a 'deny' decision."""
        return [e for e in self._events if e.decision == "deny"]

    def write_to_file(self, path: str | Path) -> None:
        """Write the entire ledger to a JSONL file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            for event in self._events:
                f.write(event.to_json() + "\n")

    @classmethod
    def read_from_file(cls, path: str | Path) -> "ControlLedger":
        """Read a ledger from a JSONL file."""
        ledger = cls()
        path = Path(path)

        if not path.exists():
            return ledger

        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                event = LedgerEvent.from_json(line)
                ledger._events.append(event)
                ledger._last_hash = event.event_hash

        return ledger

    def get_summary(self) -> dict:
        """Return a summary of the ledger."""
        decisions = {}
        event_types = {}
        actors = {}

        for event in self._events:
            decisions[event.decision] = decisions.get(event.decision, 0) + 1
            event_types[event.event_type] = event_types.get(event.event_type, 0) + 1
            actors[event.actor] = actors.get(event.actor, 0) + 1

        return {
            "total_events": len(self._events),
            "decisions": decisions,
            "event_types": event_types,
            "actors": actors,
            "last_hash": self._last_hash[:16] + "...",
        }
