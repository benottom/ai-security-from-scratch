# Control Ledger Event Schema

## Overview

This document defines the complete event schema for the AI Security Control Ledger. All events recorded by the control ledger conform to this schema.

## Schema Definition

### Required Fields

| Field           | Type   | Description                                           | Example                                    |
|-----------------|--------|-------------------------------------------------------|--------------------------------------------|
| `event_id`      | string | Unique identifier (UUID v4)                           | `"a1b2c3d4-e5f6-7890-abcd-ef1234567890"`  |
| `timestamp`     | string | ISO 8601 UTC timestamp                                | `"2025-01-15T14:30:00.123456+00:00"`       |
| `event_type`    | string | Category of event (see Event Types below)             | `"input_validated"`                         |
| `actor`         | string | System component or user that triggered the event     | `"context_firewall"`                        |
| `action`        | string | Specific action taken                                 | `"validate_input"`                          |
| `decision`      | string | Decision outcome: `allow`, `deny`, `require_approval` | `"deny"`                                    |
| `target`        | string | What was affected by the action                       | `"user_input"`                              |
| `details`       | object | Additional context (key-value pairs)                  | `{"injection_score": 0.8}`                 |
| `previous_hash` | string | SHA-256 hash of the previous event in the chain       | `"a1b2c3...f6e5d4"`                        |
| `event_hash`    | string | SHA-256 hash of this event (computed, not user-set)   | `"d4e5f6...c3b2a1"`                        |

### Field Constraints

- **event_id**: Must be a valid UUID v4. Auto-generated if not provided.
- **timestamp**: Must be ISO 8601 format with timezone (prefer UTC). Auto-generated if not provided.
- **event_type**: Must be one of the defined event types (see below). Cannot be empty.
- **actor**: Cannot be empty. Should identify the specific system component.
- **action**: Cannot be empty. Should describe what was done in verb form.
- **decision**: Must be one of `allow`, `deny`, `require_approval`.
- **target**: Describes what the action was applied to. Can be empty if not applicable.
- **details**: Must be a JSON object. Can be empty `{}`.
- **previous_hash**: 64-character hex string (SHA-256). Set by the ledger during sealing.
- **event_hash**: 64-character hex string (SHA-256). Computed by the ledger during sealing.

## Event Types

### Input Events

| Event Type           | Description                              | Typical Actors              |
|----------------------|------------------------------------------|-----------------------------|
| `input_received`     | New input received from user/system      | `api_gateway`               |
| `input_validated`    | Input passed validation                  | `context_firewall`          |
| `input_blocked`      | Input blocked due to validation failure  | `context_firewall`          |
| `input_quarantined`  | Input quarantined for review             | `context_firewall`          |

### Policy Events

| Event Type           | Description                              | Typical Actors              |
|----------------------|------------------------------------------|-----------------------------|
| `policy_checked`     | Request evaluated against policies       | `policy_engine`             |
| `policy_violation`   | Policy violation detected                | `policy_engine`             |
| `policy_approved`    | Request approved by policy               | `policy_engine`             |

### Tool Events

| Event Type           | Description                              | Typical Actors              |
|----------------------|------------------------------------------|-----------------------------|
| `tool_call_received` | Tool call request received               | `tool_gateway`              |
| `tool_call_allowed`  | Tool call allowed by gateway             | `tool_gateway`              |
| `tool_call_denied`   | Tool call denied by gateway              | `tool_gateway`              |
| `tool_call_pending`  | Tool call awaiting human approval        | `tool_gateway`              |
| `tool_call_approved` | Tool call approved by human              | `tool_gateway`              |

### Output Events

| Event Type           | Description                              | Typical Actors              |
|----------------------|------------------------------------------|-----------------------------|
| `output_generated`   | LLM output generated                     | `llm`                       |
| `output_validated`   | Output passed validation                 | `output_validator`          |
| `output_blocked`     | Output blocked due to validation failure | `output_validator`          |
| `output_redacted`    | Output modified (PII/secrets redacted)   | `output_validator`          |

### Memory Events

| Event Type           | Description                              | Typical Actors              |
|----------------------|------------------------------------------|-----------------------------|
| `memory_added`       | New memory created (in quarantine)       | `memory_quarantine`         |
| `memory_validated`   | Memory passed validation                 | `memory_quarantine`         |
| `memory_promoted`    | Memory promoted to trusted storage       | `memory_quarantine`         |
| `memory_demoted`     | Trusted memory demoted to quarantine     | `memory_quarantine`         |
| `memory_expired`     | Quarantined memory expired               | `memory_quarantine`         |

### Data Access Events

| Event Type           | Description                              | Typical Actors              |
|----------------------|------------------------------------------|-----------------------------|
| `data_access_checked`| Data access permission checked           | `permission_rag`            |
| `data_access_granted`| Data access granted                      | `permission_rag`            |
| `data_access_denied` | Data access denied                       | `permission_rag`            |

### System Events

| Event Type           | Description                              | Typical Actors              |
|----------------------|------------------------------------------|-----------------------------|
| `system_started`     | System started                           | `system`                    |
| `system_error`       | System error occurred                    | `system`                    |
| `configuration_changed` | Configuration updated                 | `admin`                     |

## Details Schema by Event Type

### input_validated / input_blocked / input_quarantined

```json
{
  "injection_score": 0.8,
  "user_id": "user123",
  "session_id": "sess-abc",
  "content_length": 256,
  "patterns_matched": ["ignore_previous", "system_override"]
}
```

### policy_checked / policy_violation

```json
{
  "policy_name": "no_secret_disclosure",
  "rule_name": "detect_api_keys",
  "user_role": "employee",
  "matched_patterns": ["sk-[a-zA-Z0-9]{20,}"],
  "severity": "critical"
}
```

### tool_call_denied / tool_call_allowed

```json
{
  "tool_name": "delete_database",
  "parameters": {"db_name": "production"},
  "risk_level": "critical",
  "validation_errors": [],
  "rate_limit_remaining": 5
}
```

### output_blocked / output_redacted

```json
{
  "findings": [
    {"category": "secret", "rule": "openai_api_key", "severity": "critical"}
  ],
  "original_length": 1024,
  "redacted_length": 980,
  "findings_count": 2
}
```

## Hash Computation

The `event_hash` is computed as:

```
SHA-256(
  JSON.stringify({
    event_id,
    timestamp,
    event_type,
    actor,
    action,
    decision,
    target,
    details,
    previous_hash
  }, sort_keys=true, separators=(",", ":"))
)
```

The `event_hash` field itself is NOT included in the hash computation to avoid circular dependency.

## JSONL Format

Events are stored in JSONL (JSON Lines) format — one JSON object per line:

```jsonl
{"action":"validate_input","actor":"context_firewall","decision":"allow","details":{"injection_score":0.0},"event_hash":"a1b2c3d4e5f6...","event_id":"uuid-1","event_type":"input_validated","previous_hash":"000000000000...","target":"user_input","timestamp":"2025-01-15T14:30:00+00:00"}
{"action":"evaluate_policy","actor":"policy_engine","decision":"deny","details":{"rule":"destructive_tools"},"event_hash":"d4e5f6a1b2c3...","event_id":"uuid-2","event_type":"policy_checked","previous_hash":"a1b2c3d4e5f6...","target":"tool_call:delete_database","timestamp":"2025-01-15T14:30:01+00:00"}
```
