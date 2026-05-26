"""Tests for Memory Quarantine."""

import pytest
from datetime import datetime, timezone, timedelta
from memory_quarantine import (
    MemoryEntry,
    MemoryQuarantine,
    MemorySource,
    MemoryState,
    ValidationResult,
)


class TestMemoryEntry:
    def test_new_entry_is_quarantined(self):
        entry = MemoryEntry(content="test", source=MemorySource.USER_INPUT)
        assert entry.state == MemoryState.QUARANTINED
        assert entry.is_quarantined
        assert not entry.is_trusted

    def test_entry_properties(self):
        entry = MemoryEntry(
            content="User prefers dark mode",
            source=MemorySource.USER_INPUT,
            tags=["preferences"],
        )
        assert entry.content == "User prefers dark mode"
        assert entry.source == MemorySource.USER_INPUT
        assert entry.tags == ["preferences"]
        assert entry.trust_score == 0.0

    def test_is_expired_with_future_expiry(self):
        entry = MemoryEntry(
            content="test",
            source=MemorySource.USER_INPUT,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )
        assert not entry.is_expired

    def test_is_expired_with_past_expiry(self):
        entry = MemoryEntry(
            content="test",
            source=MemorySource.USER_INPUT,
            expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
        )
        assert entry.is_expired

    def test_is_expired_with_no_expiry(self):
        entry = MemoryEntry(content="test", source=MemorySource.USER_INPUT, expires_at=None)
        assert not entry.is_expired


class TestMemoryQuarantine:
    def setup_method(self):
        self.mq = MemoryQuarantine(
            quarantine_ttl_hours=72,
            promotion_threshold=0.7,
            demotion_threshold=0.3,
        )

    def test_add_memory_starts_quarantined(self):
        entry = self.mq.add_memory("test content", source=MemorySource.USER_INPUT)
        assert entry.is_quarantined
        assert entry.trust_score == 0.0
        assert len(self.mq.quarantine) == 1

    def test_add_memory_with_metadata(self):
        entry = self.mq.add_memory(
            "test",
            source=MemorySource.RAG_RETRIEVAL,
            source_id="doc-123",
            tags=["finance"],
            initial_trust=0.3,
            metadata={"confidence": 0.8},
        )
        assert entry.source_id == "doc-123"
        assert entry.tags == ["finance"]
        assert entry.trust_score == 0.3

    def test_validate_increases_trust(self):
        entry = self.mq.add_memory("test", source=MemorySource.USER_INPUT)
        updated = self.mq.validate(entry.memory_id, passed=True, trust_delta=0.4, reason="Verified")
        assert updated.trust_score == 0.4
        assert updated.validation_count == 1

    def test_validate_decreases_trust(self):
        entry = self.mq.add_memory("test", source=MemorySource.USER_INPUT, initial_trust=0.5)
        updated = self.mq.validate(entry.memory_id, passed=False, trust_delta=0.3, reason="Inconsistent")
        assert updated.trust_score == 0.2  # 0.5 - 0.3

    def test_validate_nonexistent(self):
        result = self.mq.validate("nonexistent", passed=True, trust_delta=0.5)
        assert result is None

    def test_promotion_on_threshold(self):
        entry = self.mq.add_memory("test", source=MemorySource.USER_INPUT)
        # Add trust up to threshold
        self.mq.validate(entry.memory_id, passed=True, trust_delta=0.4, reason="First validation")
        self.mq.validate(entry.memory_id, passed=True, trust_delta=0.4, reason="Second validation")
        # Should be promoted (trust_score = 0.8 >= 0.7)
        assert entry.memory_id not in [e.memory_id for e in self.mq.quarantine]
        assert entry.memory_id in [e.memory_id for e in self.mq.trusted_memories]

    def test_no_promotion_below_threshold(self):
        entry = self.mq.add_memory("test", source=MemorySource.USER_INPUT)
        self.mq.validate(entry.memory_id, passed=True, trust_delta=0.3, reason="Partial")
        # trust_score = 0.3 < 0.7
        assert entry.is_quarantined

    def test_manual_promotion(self):
        entry = self.mq.add_memory("test", source=MemorySource.USER_INPUT)
        promoted = self.mq.promote(entry.memory_id, reason="Admin override")
        assert promoted is not None
        assert promoted.is_trusted

    def test_manual_promotion_nonexistent(self):
        result = self.mq.promote("nonexistent")
        assert result is None

    def test_demotion_below_threshold(self):
        entry = self.mq.add_memory("test", source=MemorySource.USER_INPUT, initial_trust=0.8)
        # Manually promote
        self.mq.promote(entry.memory_id)
        # Demote by reducing trust
        self.mq.validate(entry.memory_id, passed=False, trust_delta=0.6, reason="Found to be incorrect")
        # trust_score = 0.2 < 0.3
        assert entry.state == MemoryState.DEMOTED
        assert entry.memory_id in [e.memory_id for e in self.mq.quarantine]

    def test_manual_demotion(self):
        entry = self.mq.add_memory("test", source=MemorySource.USER_INPUT, initial_trust=0.8)
        self.mq.promote(entry.memory_id)
        demoted = self.mq.demote(entry.memory_id, reason="Security concern")
        assert demoted is not None
        assert demoted.is_quarantined

    def test_manual_demotion_nonexistent(self):
        result = self.mq.demote("nonexistent")
        assert result is None

    def test_expire_quarantined(self):
        # Add memory with very short TTL
        mq = MemoryQuarantine(quarantine_ttl_hours=0)
        entry = mq.add_memory("test", source=MemorySource.USER_INPUT)
        # Manually set expiry to past
        entry.expires_at = datetime.now(timezone.utc) - timedelta(hours=1)
        expired = mq.expire_quarantined()
        assert expired == 1
        assert len(mq.quarantine) == 0

    def test_expire_does_not_affect_trusted(self):
        entry = self.mq.add_memory("test", source=MemorySource.USER_INPUT, initial_trust=0.8)
        self.mq.promote(entry.memory_id)
        # Set expiry to past on promoted entry
        entry.expires_at = datetime.now(timezone.utc) - timedelta(hours=1)
        expired = self.mq.expire_quarantined()
        assert expired == 0  # Not in quarantine anymore
        assert len(self.mq.trusted_memories) == 1

    def test_retrieve_trusted(self):
        self.mq.add_memory("test1", source=MemorySource.USER_INPUT, tags=["pref"])
        entry2 = self.mq.add_memory("test2", source=MemorySource.SYSTEM_GENERATED, tags=["config"])
        self.mq.promote(entry2.memory_id)

        # Filter by tags
        results = self.mq.retrieve_trusted(tags=["config"])
        assert len(results) == 1

        # Filter by source
        results = self.mq.retrieve_trusted(source=MemorySource.SYSTEM_GENERATED)
        assert len(results) == 1

    def test_search_trusted_only(self):
        entry1 = self.mq.add_memory("dark mode preferences", source=MemorySource.USER_INPUT)
        entry2 = self.mq.add_memory("light mode settings", source=MemorySource.USER_INPUT)
        self.mq.promote(entry1.memory_id)

        results = self.mq.search("preferences", trusted_only=True)
        assert len(results) == 1
        assert results[0].content == "dark mode preferences"

    def test_search_all(self):
        self.mq.add_memory("dark mode preferences", source=MemorySource.USER_INPUT)
        self.mq.add_memory("light mode settings", source=MemorySource.USER_INPUT)

        results = self.mq.search("mode", trusted_only=False)
        assert len(results) == 2

    def test_custom_validator(self):
        def always_trust_validator(entry: MemoryEntry) -> ValidationResult:
            return ValidationResult(
                passed=True,
                trust_delta=0.8,
                reason="Auto-validated",
                validator_name="always_trust",
            )

        self.mq.add_validator(always_trust_validator)
        entry = self.mq.add_memory("test", source=MemorySource.USER_INPUT)
        self.mq.validate_with_custom_validators(entry.memory_id)
        # Should be promoted (0.0 + 0.8 = 0.8 >= 0.7)
        assert entry.is_trusted

    def test_validation_history(self):
        entry = self.mq.add_memory("test", source=MemorySource.USER_INPUT)
        self.mq.validate(entry.memory_id, passed=True, trust_delta=0.3, reason="Check 1")
        self.mq.validate(entry.memory_id, passed=True, trust_delta=0.2, reason="Check 2")
        assert len(entry.validation_history) == 2
        assert entry.validation_history[0]["reason"] == "Check 1"

    def test_audit_log(self):
        self.mq.add_memory("test", source=MemorySource.USER_INPUT)
        log = self.mq.audit_log
        assert any(entry["action"] == "add_memory" for entry in log)

    def test_get_summary(self):
        self.mq.add_memory("test1", source=MemorySource.USER_INPUT)
        entry = self.mq.add_memory("test2", source=MemorySource.USER_INPUT, initial_trust=0.8)
        self.mq.promote(entry.memory_id)

        summary = self.mq.get_summary()
        assert summary["quarantined_count"] == 1
        assert summary["trusted_count"] == 1
        assert summary["promotion_threshold"] == 0.7
        assert summary["demotion_threshold"] == 0.3

    def test_trust_score_bounded(self):
        entry = self.mq.add_memory("test", source=MemorySource.USER_INPUT, initial_trust=0.9)
        self.mq.validate(entry.memory_id, passed=True, trust_delta=0.5, reason="High trust")
        assert entry.trust_score <= 1.0

    def test_trust_score_not_negative(self):
        entry = self.mq.add_memory("test", source=MemorySource.USER_INPUT, initial_trust=0.1)
        self.mq.validate(entry.memory_id, passed=False, trust_delta=0.5, reason="Low trust")
        assert entry.trust_score >= 0.0

    def test_max_quarantine_eviction(self):
        mq = MemoryQuarantine(max_quarantine_size=3)
        mq.add_memory("m1", source=MemorySource.USER_INPUT)
        mq.add_memory("m2", source=MemorySource.USER_INPUT)
        mq.add_memory("m3", source=MemorySource.USER_INPUT)
        mq.add_memory("m4", source=MemorySource.USER_INPUT)  # Should evict oldest
        assert len(mq.quarantine) <= 3
