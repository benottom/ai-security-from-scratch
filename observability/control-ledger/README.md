# Control Ledger

## Overview

The **Control Ledger** is an append-only, hash-chained event store that provides a tamper-evident audit trail for all security-relevant events in the AI system. It implements the observer pattern from control theory — recording every state transition, decision, and control action for forensic analysis.

## Control-Theoretic View

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Controller  │────▶│  Plant (LLM)     │────▶│  Output      │
│              │     │                  │     │              │
└──────────────┘     └──────────────────┘     └──────────────┘
       │                    │                        │
       ▼                    ▼                        ▼
┌──────────────────────────────────────────────────────────┐
│                    Control Ledger                        │
│  (Append-only, hash-chained record of all events)       │
└──────────────────────────────────────────────────────────┘
```

In the control-loop model:
- The **Control Ledger** is the *observer's record* — it captures every state transition, decision, and control action
- Without a reliable record, it's impossible to reconstruct what happened during a security incident
- **Hash-chaining** ensures the record itself cannot be tampered with without detection (like a blockchain for AI events)

## Event Schema

Each event contains:

| Field           | Type   | Description                                |
|-----------------|--------|--------------------------------------------|
| `event_id`      | string | Unique identifier (UUID)                   |
| `timestamp`     | string | ISO 8601 UTC timestamp                     |
| `event_type`    | string | Type of event (e.g., "input_validated")    |
| `actor`         | string | Who/what triggered the event               |
| `action`        | string | What was done                              |
| `decision`      | string | allow, deny, require_approval              |
| `target`        | string | What was affected                          |
| `details`       | object | Additional context                         |
| `previous_hash` | string | SHA-256 hash of the previous event         |
| `event_hash`    | string | SHA-256 hash of this event                 |

## How It Works

1. **Append-Only**: Events can only be added, never removed or modified.
2. **Hash-Chaining**: Each event includes the SHA-256 hash of the previous event, forming a chain.
3. **Genesis Hash**: The first event's `previous_hash` is a known genesis value (`0` * 64).
4. **Integrity Verification**: The entire chain can be verified by recomputing hashes.
5. **JSONL Format**: Events are stored as one JSON object per line for easy parsing and streaming.

## Usage Examples

### Basic Usage

```python
from ledger import ControlLedger

ledger = ControlLedger()

# Append events
ledger.append(
    event_type="input_validated",
    actor="context_firewall",
    action="validate_input",
    decision="allow",
    target="user_input",
    details={"injection_score": 0.0, "user_id": "user123"},
)

ledger.append(
    event_type="policy_checked",
    actor="policy_engine",
    action="evaluate_policy",
    decision="deny",
    target="tool_call:delete_database",
    details={"matched_rules": ["destructive_tools"]},
)
```

### Integrity Verification

```python
is_valid, errors = ledger.verify_integrity()
if not is_valid:
    print("LEDGER TAMPERING DETECTED!")
    for error in errors:
        print(f"  {error}")
```

### Querying Events

```python
# Get all denied events
denied = ledger.get_denied_events()

# Query by type
input_events = ledger.get_events_by_type("input_validated")

# Complex query
results = ledger.query(
    event_type="policy_checked",
    decision="deny",
    start_time="2025-01-15T00:00:00Z",
)
```

### File I/O

```python
# Write to file
ledger.write_to_file("control-ledger.jsonl")

# Read from file
loaded_ledger = ControlLedger.read_from_file("control-ledger.jsonl")
assert loaded_ledger.verify_integrity()[0]
```

## JSONL Format

Each line in the JSONL file is a complete JSON event:

```jsonl
{"action":"validate_input","actor":"context_firewall","decision":"allow","details":{"injection_score":0.0},"event_hash":"a1b2c3...","event_id":"uuid-1","event_type":"input_validated","previous_hash":"0000...0000","target":"user_input","timestamp":"2025-01-15T14:30:00+00:00"}
{"action":"evaluate_policy","actor":"policy_engine","decision":"deny","details":{"matched_rules":["destructive_tools"]},"event_hash":"d4e5f6...","event_id":"uuid-2","event_type":"policy_checked","previous_hash":"a1b2c3...","target":"tool_call:delete_database","timestamp":"2025-01-15T14:30:01+00:00"}
```

## Limitations

- Not a distributed ledger; each instance is standalone.
- No encryption at rest; sensitive details should be hashed before logging.
- File-based storage; high-throughput systems may need database-backed storage.
- No built-in rotation; manage file size externally.
