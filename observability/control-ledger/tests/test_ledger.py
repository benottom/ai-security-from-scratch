"""Tests for Control Ledger."""

import os
import tempfile

import pytest
from ledger import ControlLedger, LedgerEvent


class TestLedgerEvent:
    def test_event_creation(self):
        event = LedgerEvent(
            event_type="input_validated",
            actor="context_firewall",
            action="validate",
            decision="allow",
            target="user_input",
        )
        assert event.event_type == "input_validated"
        assert event.actor == "context_firewall"
        assert event.event_id  # Auto-generated
        assert event.timestamp  # Auto-generated

    def test_compute_hash(self):
        event = LedgerEvent(
            event_type="test",
            actor="test",
            action="test",
            decision="allow",
        )
        hash1 = event.compute_hash()
        assert len(hash1) == 64  # SHA-256 hex digest

    def test_seal(self):
        event = LedgerEvent(event_type="test", actor="test", action="test", decision="allow")
        event.seal(previous_hash="abc123")
        assert event.previous_hash == "abc123"
        assert event.event_hash  # Computed
        assert len(event.event_hash) == 64

    def test_to_json(self):
        event = LedgerEvent(event_type="test", actor="test", action="test", decision="allow")
        event.seal("prev_hash")
        json_str = event.to_json()
        assert "test" in json_str
        assert "prev_hash" in json_str

    def test_from_json(self):
        event = LedgerEvent(event_type="test", actor="test", action="test", decision="allow")
        event.seal("prev_hash")
        json_str = event.to_json()
        restored = LedgerEvent.from_json(json_str)
        assert restored.event_type == "test"
        assert restored.actor == "test"
        assert restored.previous_hash == "prev_hash"
        assert restored.event_hash == event.event_hash

    def test_hash_deterministic(self):
        event = LedgerEvent(
            event_type="test", actor="test", action="test", decision="allow",
            event_id="fixed-id", timestamp="2025-01-15T00:00:00+00:00",
        )
        event.seal("prev_hash")
        hash1 = event.event_hash
        # Same event, same hash
        event2 = LedgerEvent(
            event_type="test", actor="test", action="test", decision="allow",
            event_id="fixed-id", timestamp="2025-01-15T00:00:00+00:00",
        )
        event2.seal("prev_hash")
        assert event2.event_hash == hash1

    def test_hash_changes_with_content(self):
        event1 = LedgerEvent(
            event_type="test1", actor="test", action="test", decision="allow",
            event_id="id1", timestamp="2025-01-01T00:00:00+00:00",
        )
        event1.seal("prev")
        event2 = LedgerEvent(
            event_type="test2", actor="test", action="test", decision="allow",
            event_id="id2", timestamp="2025-01-01T00:00:00+00:00",
        )
        event2.seal("prev")
        assert event1.event_hash != event2.event_hash


class TestControlLedger:
    def test_append_event(self):
        ledger = ControlLedger()
        event = ledger.append(
            event_type="input_validated",
            actor="firewall",
            action="validate",
            decision="allow",
        )
        assert event.event_type == "input_validated"
        assert len(ledger.events) == 1
        assert event.previous_hash == ControlLedger.GENESIS_HASH

    def test_hash_chaining(self):
        ledger = ControlLedger()
        e1 = ledger.append(event_type="e1", actor="a", action="act", decision="allow")
        e2 = ledger.append(event_type="e2", actor="a", action="act", decision="deny")
        e3 = ledger.append(event_type="e3", actor="a", action="act", decision="allow")

        # Each event's previous_hash should be the previous event's hash
        assert e2.previous_hash == e1.event_hash
        assert e3.previous_hash == e2.event_hash
        assert ledger.last_hash == e3.event_hash

    def test_verify_integrity_valid(self):
        ledger = ControlLedger()
        ledger.append(event_type="e1", actor="a", action="act", decision="allow")
        ledger.append(event_type="e2", actor="a", action="act", decision="deny")
        is_valid, errors = ledger.verify_integrity()
        assert is_valid
        assert errors == []

    def test_verify_integrity_empty(self):
        ledger = ControlLedger()
        is_valid, errors = ledger.verify_integrity()
        assert is_valid

    def test_verify_integrity_tampered(self):
        ledger = ControlLedger()
        ledger.append(event_type="e1", actor="a", action="act", decision="allow")
        e2 = ledger.append(event_type="e2", actor="a", action="act", decision="deny")

        # Tamper with the first event
        ledger._events[0].decision = "tampered"

        is_valid, errors = ledger.verify_integrity()
        assert not is_valid
        assert len(errors) > 0

    def test_query_by_event_type(self):
        ledger = ControlLedger()
        ledger.append(event_type="input_validated", actor="fw", action="v", decision="allow")
        ledger.append(event_type="policy_checked", actor="pe", action="c", decision="deny")
        ledger.append(event_type="input_validated", actor="fw", action="v", decision="allow")

        results = ledger.query(event_type="input_validated")
        assert len(results) == 2

    def test_query_by_decision(self):
        ledger = ControlLedger()
        ledger.append(event_type="e1", actor="a", action="act", decision="allow")
        ledger.append(event_type="e2", actor="a", action="act", decision="deny")
        ledger.append(event_type="e3", actor="a", action="act", decision="allow")

        results = ledger.query(decision="deny")
        assert len(results) == 1

    def test_query_by_actor(self):
        ledger = ControlLedger()
        ledger.append(event_type="e", actor="firewall", action="a", decision="allow")
        ledger.append(event_type="e", actor="policy_engine", action="a", decision="deny")

        results = ledger.query(actor="firewall")
        assert len(results) == 1

    def test_get_events_by_type(self):
        ledger = ControlLedger()
        ledger.append(event_type="input", actor="a", action="a", decision="allow")
        ledger.append(event_type="output", actor="a", action="a", decision="allow")
        ledger.append(event_type="input", actor="a", action="a", decision="deny")

        results = ledger.get_events_by_type("input")
        assert len(results) == 2

    def test_get_denied_events(self):
        ledger = ControlLedger()
        ledger.append(event_type="e", actor="a", action="a", decision="allow")
        ledger.append(event_type="e", actor="a", action="a", decision="deny")
        ledger.append(event_type="e", actor="a", action="a", decision="deny")

        results = ledger.get_denied_events()
        assert len(results) == 2

    def test_size(self):
        ledger = ControlLedger()
        assert ledger.size == 0
        ledger.append(event_type="e", actor="a", action="a", decision="allow")
        assert ledger.size == 1

    def test_write_and_read_file(self):
        ledger = ControlLedger()
        ledger.append(event_type="e1", actor="a", action="act", decision="allow")
        ledger.append(event_type="e2", actor="a", action="act", decision="deny")

        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            filepath = f.name

        try:
            ledger.write_to_file(filepath)

            # Read back
            loaded = ControlLedger.read_from_file(filepath)
            assert loaded.size == 2
            assert loaded.verify_integrity()[0]
            assert loaded.events[0].event_type == "e1"
            assert loaded.events[1].event_type == "e2"
        finally:
            os.unlink(filepath)

    def test_read_nonexistent_file(self):
        ledger = ControlLedger.read_from_file("/nonexistent/path.jsonl")
        assert ledger.size == 0

    def test_get_summary(self):
        ledger = ControlLedger()
        ledger.append(event_type="input", actor="fw", action="v", decision="allow")
        ledger.append(event_type="policy", actor="pe", action="c", decision="deny")

        summary = ledger.get_summary()
        assert summary["total_events"] == 2
        assert summary["decisions"]["allow"] == 1
        assert summary["decisions"]["deny"] == 1

    def test_event_details(self):
        ledger = ControlLedger()
        event = ledger.append(
            event_type="test",
            actor="test",
            action="test",
            decision="allow",
            details={"injection_score": 0.3, "user_id": "u123"},
        )
        assert event.details["injection_score"] == 0.3
        assert event.details["user_id"] == "u123"

    def test_many_events_integrity(self):
        ledger = ControlLedger()
        for i in range(100):
            ledger.append(
                event_type=f"event_{i % 5}",
                actor=f"actor_{i % 3}",
                action="action",
                decision="allow" if i % 2 == 0 else "deny",
            )
        is_valid, errors = ledger.verify_integrity()
        assert is_valid
        assert ledger.size == 100
