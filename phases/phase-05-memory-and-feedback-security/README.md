# Phase 5 — Memory and Feedback Security

> **Classes:** 27–32 | **Estimated Total Time:** ~21 hours

## Phase Description

This phase examines the security of the feedback paths that close the AI control loop. Memory — both conversation history and long-term stored context — is a feedback channel that the AI system uses to maintain state across turns and sessions. When an attacker can write to memory, they are injecting a persistent disturbance that the controller will read as legitimate feedback. Learners explore how conversation history becomes an attack surface, how long-term memory stores can be poisoned, and how cross-user memory leakage violates isolation boundaries. The phase introduces memory trust scoring, memory quarantine, and feedback loop hardening as the control mechanisms that protect the integrity of the system's state. The core insight is that memory is not storage — it is a feedback path, and it must be protected with the same rigor as any control system's feedback channel.

## Main Outcome

Learners understand memory as a feedback path and can protect it — implementing trust scoring, quarantine, and isolation mechanisms that ensure stored context remains trustworthy and does not become a vector for persistent compromise.

## Classes

| Class | Title | Description |
|-------|-------|-------------|
| 27 | Conversation Memory Risks | Examines how session history becomes an attack surface for multi-turn manipulation |
| 28 | Long-Term Memory Poisoning | Explores injection into persistent memory stores that affects future sessions |
| 29 | Cross-User Memory Leakage | Covers data leakage between user sessions, tenants, and isolation boundaries |
| 30 | Memory Trust Scoring | Implements trust levels and validation for stored memories based on source and history |
| 31 | Memory Quarantine | Isolates and audits suspicious memory entries before they influence model behavior |
| 32 | Feedback Loop Security | Secures the feedback paths that update AI system behavior and prevent feedback manipulation |

## Prerequisites

- Completion of Phase 1 — Foundations (Classes 01–06)
- Completion of Phase 2 — Prompt Injection (Classes 07–12)
