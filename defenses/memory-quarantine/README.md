# Memory Quarantine

## Overview

The **Memory Quarantine** system implements trust scoring and quarantine for AI system memories. New memories start in quarantine and must be validated before being promoted to trusted storage. This prevents adversarial or corrupted memories from persistently influencing the system.

## Control-Theoretic View

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│  New Memory  │────▶│  Quarantine      │────▶│  Trusted     │
│  (State      │     │  (State Filter)  │     │  Storage     │
│   Update)    │     │                  │     │  (Validated  │
│              │     │  Validation +    │     │   State)     │
│              │     │  Trust Scoring   │     │              │
└──────────────┘     └──────────────────┘     └──────────────┘
                              ▲                        │
                              │                        │
                     ┌────────┴────────┐               │
                     │  Demotion       │◀──────────────┘
                     │  (Trust decay)  │
                     └─────────────────┘
```

In the control-loop model:
- **Memories** are *state variables* — persistent information that influences future control decisions
- **Quarantine** is a *state filter* — new state updates must be validated before being committed
- **Trust scoring** is a *confidence metric* — how much the system should rely on each state variable
- **Demotion** is a *state correction* mechanism — if trusted state is found to be corrupted, it's reverted

### Memory States

| State        | Description                              | Trust Score Range |
|--------------|------------------------------------------|-------------------|
| QUARANTINED  | New memory awaiting validation           | 0.0 - threshold   |
| VALIDATED    | Passed basic validation                  | threshold - 0.9   |
| PROMOTED     | Fully trusted, in long-term storage      | threshold - 1.0   |
| DEMOTED      | Previously trusted, now back in quarantine| Below threshold   |
| EXPIRED      | Quarantined memory that wasn't validated  | N/A               |

## How It Works

1. **Addition**: New memories start in quarantine with trust_score=0.0 and an expiration time (TTL).
2. **Validation**: Validators increase or decrease trust score. Each validation is recorded in the entry's history.
3. **Promotion**: When trust_score >= promotion_threshold (default 0.7), the memory is promoted to trusted storage.
4. **Demotion**: If a trusted memory's score drops below demotion_threshold (default 0.3), it's returned to quarantine.
5. **Expiration**: Quarantined memories that aren't validated within the TTL are automatically expired.

## Usage Examples

### Basic Usage

```python
from memory_quarantine import MemoryQuarantine, MemorySource

mq = MemoryQuarantine(quarantine_ttl_hours=24, promotion_threshold=0.7)

# Add a new memory — starts in quarantine
entry = mq.add_memory("User prefers dark mode", source=MemorySource.USER_INPUT)
assert entry.is_quarantined

# Validate the memory
mq.validate(entry.memory_id, passed=True, trust_delta=0.4,
            reason="Cross-referenced with user settings")

# If trust_score >= 0.7, it's automatically promoted
# If not, continue validating
mq.validate(entry.memory_id, passed=True, trust_delta=0.3,
            reason="Consistent with recent interactions")
# Now promoted!
```

### Custom Validators

```python
def cross_reference_validator(entry: MemoryEntry) -> ValidationResult:
    """Check if memory content is consistent with existing trusted memories."""
    trusted = mq.retrieve_trusted()
    for t in trusted:
        if entry.content.lower() in t.content.lower():
            return ValidationResult(
                passed=True, trust_delta=0.2,
                reason=f"Cross-referenced with {t.memory_id}",
                validator_name="cross_reference",
            )
    return ValidationResult(
        passed=False, trust_delta=-0.1,
        reason="No cross-reference found",
        validator_name="cross_reference",
    )

mq.add_validator(cross_reference_validator)
```

### Expiring Old Memories

```python
# Remove memories that have been in quarantine too long
expired_count = mq.expire_quarantined()
print(f"Expired {expired_count} memories")
```

### Searching Memories

```python
# Search trusted memories only
results = mq.search("user preferences", trusted_only=True)

# Filter by tags
results = mq.retrieve_trusted(tags=["user_prefs"])
```

## Configuration

| Parameter              | Default | Description                                   |
|------------------------|---------|-----------------------------------------------|
| `quarantine_ttl_hours` | 72      | Hours before quarantined memories expire       |
| `promotion_threshold`  | 0.7     | Trust score needed for promotion               |
| `demotion_threshold`   | 0.3     | Trust score below which memories are demoted   |
| `max_quarantine_size`  | 1000    | Maximum quarantined entries                    |
| `max_trusted_size`     | 10000   | Maximum trusted entries                        |

## Limitations

- Trust scoring is numeric and may not capture all nuances of memory reliability.
- Expiration is checked explicitly (not automatically); call `expire_quarantined()` periodically.
- Search is keyword-based; production systems should use vector similarity.
- Does not prevent adversarial memories from being created (only from being trusted).
