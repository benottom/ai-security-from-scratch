"""
Memory Quarantine — Memory trust scoring and quarantine for AI systems.

New memories start in quarantine and must be validated before being promoted
to trusted storage. This prevents adversarial or corrupted memories from
influencing the system's behavior.

Control-Theoretic View:
    In the control loop, the memory system acts as state storage — it persists
    information across interactions. If adversarial content is stored as memory,
    it becomes a persistent disturbance that can affect all future control
    decisions. The quarantine system acts as a state filter, ensuring only
    validated state updates are committed to long-term storage.

Key Properties:
    1. Trust scoring: memories are scored on reliability (0.0-1.0)
    2. Quarantine by default: new memories start quarantined
    3. Promotion mechanics: memories must pass validation to be promoted
    4. Demotion: compromised memories can be demoted back to quarantine
    5. TTL: quarantined memories expire if not validated within a time window
    6. Source tracking: memories track their origin for forensic analysis
"""

from __future__ import annotations

import enum
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Callable, Optional


class MemoryState(enum.Enum):
    """State of a memory entry."""
    QUARANTINED = "quarantined"
    VALIDATED = "validated"
    PROMOTED = "promoted"
    DEMOTED = "demoted"
    EXPIRED = "expired"


class MemorySource(enum.Enum):
    """Origin of a memory entry."""
    USER_INPUT = "user_input"
    SYSTEM_GENERATED = "system_generated"
    RAG_RETRIEVAL = "rag_retrieval"
    TOOL_OUTPUT = "tool_output"
    EXTERNAL_API = "external_api"
    INFERENCE = "inference"


@dataclass
class MemoryEntry:
    """A single memory entry with trust metadata."""
    content: str
    source: MemorySource
    memory_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    state: MemoryState = MemoryState.QUARANTINED
    trust_score: float = 0.0
    source_id: str = ""  # ID of the user/tool/session that created this
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    validated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    validation_count: int = 0
    metadata: dict = field(default_factory=dict)
    validation_history: list[dict] = field(default_factory=list)

    @property
    def is_quarantined(self) -> bool:
        return self.state == MemoryState.QUARANTINED

    @property
    def is_trusted(self) -> bool:
        return self.state in (MemoryState.VALIDATED, MemoryState.PROMOTED)

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at


# Validation result types
@dataclass
class ValidationResult:
    """Result of validating a memory entry."""
    passed: bool
    trust_delta: float = 0.0  # Change in trust score
    reason: str = ""
    validator_name: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class MemoryQuarantine:
    """
    Memory trust scoring and quarantine system.

    New memories start in quarantine and must be validated before being
    promoted to trusted storage. This prevents adversarial or corrupted
    memories from influencing the system's behavior.

    Usage:
        mq = MemoryQuarantine(quarantine_ttl_hours=24, promotion_threshold=0.7)
        entry = mq.add_memory("User prefers dark mode", source=MemorySource.USER_INPUT)
        mq.validate(entry.memory_id, passed=True, trust_delta=0.3, reason="Cross-referenced with user settings")
        # After enough validations, the memory is promoted
    """

    def __init__(
        self,
        quarantine_ttl_hours: int = 72,
        promotion_threshold: float = 0.7,
        demotion_threshold: float = 0.3,
        max_quarantine_size: int = 1000,
        max_trusted_size: int = 10000,
    ):
        self._quarantine: dict[str, MemoryEntry] = {}
        self._trusted: dict[str, MemoryEntry] = {}
        self._quarantine_ttl = timedelta(hours=quarantine_ttl_hours)
        self._promotion_threshold = promotion_threshold
        self._demotion_threshold = demotion_threshold
        self._max_quarantine_size = max_quarantine_size
        self._max_trusted_size = max_trusted_size
        self._validators: list[Callable[[MemoryEntry], ValidationResult]] = []
        self._audit_log: list[dict] = []

    @property
    def quarantine(self) -> list[MemoryEntry]:
        return list(self._quarantine.values())

    @property
    def trusted_memories(self) -> list[MemoryEntry]:
        return list(self._trusted.values())

    @property
    def audit_log(self) -> list[dict]:
        return list(self._audit_log)

    def add_validator(self, validator: Callable[[MemoryEntry], ValidationResult]) -> None:
        """
        Register a custom validator function.

        Validators receive a MemoryEntry and return a ValidationResult.
        They are called during the validate() method.
        """
        self._validators.append(validator)

    def add_memory(
        self,
        content: str,
        source: MemorySource,
        source_id: str = "",
        tags: list[str] = None,
        initial_trust: float = 0.0,
        metadata: dict = None,
    ) -> MemoryEntry:
        """
        Add a new memory entry. It starts in quarantine by default.

        Args:
            content: The memory content.
            source: Where this memory came from.
            source_id: ID of the source (user, tool, session).
            tags: Optional tags for categorization.
            initial_trust: Starting trust score (default 0.0).
            metadata: Additional metadata.

        Returns:
            The created MemoryEntry (in QUARANTINED state).
        """
        if len(self._quarantine) >= self._max_quarantine_size:
            self._evict_oldest_quarantined()

        entry = MemoryEntry(
            content=content,
            source=source,
            source_id=source_id,
            tags=tags or [],
            trust_score=initial_trust,
            expires_at=datetime.now(timezone.utc) + self._quarantine_ttl,
            metadata=metadata or {},
        )

        self._quarantine[entry.memory_id] = entry
        self._log_action("add_memory", memory_id=entry.memory_id,
                         source=source.value, trust_score=initial_trust)

        return entry

    def validate(
        self,
        memory_id: str,
        passed: bool = True,
        trust_delta: float = 0.1,
        reason: str = "",
        validator_name: str = "manual",
    ) -> Optional[MemoryEntry]:
        """
        Validate a memory entry, adjusting its trust score.

        If the trust score reaches the promotion threshold, the memory
        is automatically promoted to trusted storage.

        Args:
            memory_id: ID of the memory to validate.
            passed: Whether the validation passed.
            trust_delta: How much to adjust the trust score.
            reason: Reason for the validation result.
            validator_name: Name of the validator.

        Returns:
            The updated MemoryEntry, or None if not found.
        """
        entry = self._quarantine.get(memory_id) or self._trusted.get(memory_id)
        if entry is None:
            return None

        # Record validation
        validation = ValidationResult(
            passed=passed,
            trust_delta=trust_delta if passed else -abs(trust_delta),
            reason=reason,
            validator_name=validator_name,
        )
        entry.validation_history.append({
            "passed": passed,
            "trust_delta": validation.trust_delta,
            "reason": reason,
            "validator_name": validator_name,
            "timestamp": validation.timestamp.isoformat(),
        })
        entry.validation_count += 1

        # Adjust trust score
        entry.trust_score = max(0.0, min(1.0, entry.trust_score + validation.trust_delta))

        # Check for promotion
        if entry.state == MemoryState.QUARANTINED and entry.trust_score >= self._promotion_threshold:
            self._promote(entry)
        # Check for demotion
        elif entry.state in (MemoryState.VALIDATED, MemoryState.PROMOTED) and entry.trust_score < self._demotion_threshold:
            self._demote(entry)

        self._log_action(
            "validate",
            memory_id=memory_id,
            passed=passed,
            trust_delta=validation.trust_delta,
            new_trust_score=entry.trust_score,
            reason=reason,
            validator_name=validator_name,
        )

        return entry

    def validate_with_custom_validators(self, memory_id: str) -> Optional[MemoryEntry]:
        """
        Run all registered custom validators against a memory entry.

        Returns:
            The updated MemoryEntry after all validators have run.
        """
        entry = self._quarantine.get(memory_id) or self._trusted.get(memory_id)
        if entry is None:
            return None

        for validator in self._validators:
            result = validator(entry)
            self.validate(
                memory_id,
                passed=result.passed,
                trust_delta=result.trust_delta,
                reason=result.reason,
                validator_name=result.validator_name,
            )

        return self._quarantine.get(memory_id) or self._trusted.get(memory_id)

    def promote(self, memory_id: str, reason: str = "Manual promotion") -> Optional[MemoryEntry]:
        """Manually promote a memory entry to trusted storage."""
        entry = self._quarantine.get(memory_id)
        if entry is None:
            return None
        self._promote(entry, reason)
        return self._trusted.get(memory_id)

    def demote(self, memory_id: str, reason: str = "Manual demotion") -> Optional[MemoryEntry]:
        """Manually demote a trusted memory back to quarantine."""
        entry = self._trusted.get(memory_id)
        if entry is None:
            return None
        self._demote(entry, reason)
        return self._quarantine.get(memory_id)

    def expire_quarantined(self) -> int:
        """
        Remove expired entries from quarantine.

        Returns:
            The number of entries expired.
        """
        now = datetime.now(timezone.utc)
        expired_ids = [
            mid for mid, entry in self._quarantine.items()
            if entry.expires_at and now > entry.expires_at
        ]

        for mid in expired_ids:
            entry = self._quarantine.pop(mid)
            entry.state = MemoryState.EXPIRED
            self._log_action("expire", memory_id=mid, content_preview=entry.content[:100])

        return len(expired_ids)

    def retrieve_trusted(self, tags: list[str] = None, source: MemorySource = None) -> list[MemoryEntry]:
        """
        Retrieve trusted memories, optionally filtered by tags or source.

        Args:
            tags: If provided, only return memories with at least one matching tag.
            source: If provided, only return memories from this source.

        Returns:
            A list of trusted MemoryEntry objects.
        """
        results = list(self._trusted.values())

        if tags:
            results = [m for m in results if any(t in m.tags for t in tags)]

        if source:
            results = [m for m in results if m.source == source]

        return results

    def search(self, query: str, trusted_only: bool = True) -> list[MemoryEntry]:
        """
        Simple keyword search across memories.

        Args:
            query: Search terms.
            trusted_only: If True, only search trusted memories.

        Returns:
            A list of matching MemoryEntry objects.
        """
        query_terms = set(query.lower().split())
        results = []

        search_space = list(self._trusted.values())
        if not trusted_only:
            search_space += list(self._quarantine.values())

        for entry in search_space:
            content_terms = set(entry.content.lower().split())
            if query_terms & content_terms:
                results.append(entry)

        return results

    def _promote(self, entry: MemoryEntry, reason: str = "Trust threshold reached") -> None:
        """Promote a memory from quarantine to trusted storage."""
        if len(self._trusted) >= self._max_trusted_size:
            self._evict_lowest_trust()

        entry.state = MemoryState.PROMOTED
        entry.validated_at = datetime.now(timezone.utc)
        entry.expires_at = None  # Trusted memories don't expire

        if entry.memory_id in self._quarantine:
            del self._quarantine[entry.memory_id]
        self._trusted[entry.memory_id] = entry

        self._log_action("promote", memory_id=entry.memory_id,
                         trust_score=entry.trust_score, reason=reason)

    def _demote(self, entry: MemoryEntry, reason: str = "Trust below threshold") -> None:
        """Demote a trusted memory back to quarantine."""
        entry.state = MemoryState.DEMOTED
        entry.expires_at = datetime.now(timezone.utc) + self._quarantine_ttl

        if entry.memory_id in self._trusted:
            del self._trusted[entry.memory_id]
        self._quarantine[entry.memory_id] = entry

        self._log_action("demote", memory_id=entry.memory_id,
                         trust_score=entry.trust_score, reason=reason)

    def _evict_oldest_quarantined(self) -> None:
        """Evict the oldest quarantined entry."""
        if not self._quarantine:
            return
        oldest_id = min(self._quarantine, key=lambda k: self._quarantine[k].created_at)
        entry = self._quarantine.pop(oldest_id)
        self._log_action("evict_quarantine", memory_id=oldest_id,
                         content_preview=entry.content[:100])

    def _evict_lowest_trust(self) -> None:
        """Evict the trusted memory with the lowest trust score."""
        if not self._trusted:
            return
        lowest_id = min(self._trusted, key=lambda k: self._trusted[k].trust_score)
        entry = self._trusted.pop(lowest_id)
        self._log_action("evict_trusted", memory_id=lowest_id,
                         trust_score=entry.trust_score, content_preview=entry.content[:100])

    def _log_action(self, action: str, **kwargs) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            **kwargs,
        }
        self._audit_log.append(entry)

    def get_summary(self) -> dict:
        """Return a summary of the memory quarantine state."""
        return {
            "quarantined_count": len(self._quarantine),
            "trusted_count": len(self._trusted),
            "promotion_threshold": self._promotion_threshold,
            "demotion_threshold": self._demotion_threshold,
            "avg_trust_score_quarantine": (
                sum(e.trust_score for e in self._quarantine.values()) / len(self._quarantine)
                if self._quarantine else 0.0
            ),
            "avg_trust_score_trusted": (
                sum(e.trust_score for e in self._trusted.values()) / len(self._trusted)
                if self._trusted else 0.0
            ),
            "validators_registered": len(self._validators),
            "audit_log_entries": len(self._audit_log),
        }
